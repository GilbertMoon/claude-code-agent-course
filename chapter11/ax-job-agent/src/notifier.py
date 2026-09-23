"""Slack / Gmail 발송 (Notebook STEP 12~13).

- 인증정보(SLACK_WEBHOOK_URL, GMAIL_USER, GMAIL_APP_PASSWORD)는 .env에서 읽고, 출력하거나 저장하지 않는다.
- 발송 기록 파일(slack_sent.json, gmail_sent.json)에 같은 메시지 해시가 있으면 다시 보내지 않는다.
  일부러 다시 보낼 때만 force=True를 쓴다.
- 메시지 생성(build_*)은 네트워크를 쓰지 않는다.
"""
import hashlib
import html
import json
import os
import re
import smtplib
from datetime import datetime
from email.message import EmailMessage

import requests

DEFAULT_SLACK_LOG_PATH = "data/processed/slack_sent.json"
DEFAULT_GMAIL_LOG_PATH = "data/processed/gmail_sent.json"


def _read_log(path):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return None


def _write_log(path, result):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({k: v for k, v in result.items() if k != "sent"}, f, ensure_ascii=False, indent=2)


def _load_env():
    from dotenv import load_dotenv

    load_dotenv()


# ---- Slack (STEP 12) ----

def _section(report, number):
    match = re.search(rf"^## {number}\. .*?$(.*?)(?=^## |\Z)", report, flags=re.M | re.S)
    return match.group(1) if match else ""


def _table_rows(text):
    rows = [line.strip().strip("|").split("|") for line in text.splitlines() if line.startswith("|")]
    return [[cell.strip() for cell in row] for row in rows[2:]]


def _bullet_value(text, label):
    match = re.search(rf"^- {label}: (.+)$", text, flags=re.M)
    return match.group(1).strip() if match else None


def _slack_escape(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_slack_message(report):
    """weekly_report.md 내용에서 Slack mrkdwn 요약 메시지를 만든다. (표 없이 텍스트와 bullet)"""
    overview = _section(report, 1)
    collected = _bullet_value(overview, "수집 기준일").split(" ")[0]
    keyword = _bullet_value(overview, "검색 키워드").strip("`")
    week_range = _bullet_value(overview, "이번 주 범위")
    total = _bullet_value(overview, "분석 대상 공고 수")
    new_count = _bullet_value(overview, "신규 공고 수").split(" ")[0]
    new_jobs = _table_rows(_section(report, 2))
    check = _section(report, 9)
    judge = {name: re.search(rf"- {name}: (\d+)건", check).group(1) for name in ["입력 근거 있음", "입력 외 추론", "과도한 해석"]}
    term_total = re.search(r"확인한 표현 (\d+)건", check).group(1)

    def counts_line(rows):
        return ", ".join(f"{_slack_escape(name)} {count}건" for name, count in rows)

    lines = [
        "*AX 채용공고 주간 리포트*",
        "",
        f"• 기준일: {collected} (이번 주: {week_range})",
        f"• 검색 키워드: `{keyword}`",
        f"• 분석 대상 공고: {total}",
        f"• 이번 주 신규 공고 (등록일 기준): {new_count}",
        "",
        "*이번 주 신규 공고*",
    ]
    for company, title, career, location, posted, url in new_jobs:
        lines += [
            f"• {_slack_escape(company)} | {_slack_escape(title)}",
            f"   등록일 {posted} · {_slack_escape(career)} · {_slack_escape(location)}",
            f"   <{url}>",
        ]
    lines += [
        "",
        f"*회사별*: {counts_line(_table_rows(_section(report, 4)))}",
        f"*경력별*: {counts_line(_table_rows(_section(report, 5)))}",
        f"*지역별*: {counts_line(_table_rows(_section(report, 6)))}",
        f"*주요 키워드* (정의된 목록 빈도): {counts_line(_table_rows(_section(report, 7)))}",
        "",
        "*Gemini 분석 주의사항*",
        f"• Gemini 결과 표현 {term_total}건 검증: 입력 근거 있음 {judge['입력 근거 있음']}건 / "
        f"입력 외 추론 {judge['입력 외 추론']}건 / 과도한 해석 {judge['과도한 해석']}건",
        "• 과도한 해석은 거짓이라는 뜻이 아니라, 확보한 원본 자료에서 직접 확인되지 않는 표현이라는 뜻입니다.",
        "• required_skills 일부는 기술 스킬보다 직무·업무·도메인 표현에 가깝습니다.",
        "",
        "*데이터 한계*",
        f"• {total} 소량 표본 결과이며 전체 채용시장을 대표하지 않습니다.",
        "• 브라우저에서 저장한 검색 결과 HTML 기준이며, 상세 공고 본문은 확보하지 못했습니다.",
        "_자세한 내용: data/processed/weekly_report.md_",
    ]
    return "\n".join(lines)


def slack_message_hash(message):
    return hashlib.sha256(message.encode("utf-8")).hexdigest()


def send_slack(report, webhook_url=None, sent_log_path=DEFAULT_SLACK_LOG_PATH, force=False, post=requests.post):
    """리포트 요약을 Slack Incoming Webhook으로 보낸다. 같은 메시지를 이미 보냈으면 건너뛴다.

    반환: 결과 dict (sent, status_code, response_text, 길이 등). Webhook URL은 결과와 오류에 넣지 않는다.
    """
    if webhook_url is None:
        _load_env()
        webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        raise RuntimeError(".env에 SLACK_WEBHOOK_URL이 없습니다.")

    def hide_secret(text):
        text = str(text).replace(webhook_url, "***")
        return re.sub(r"/services/[A-Za-z0-9/_-]+", "/services/***", text)

    message = build_slack_message(report)
    message_hash = slack_message_hash(message)
    sent_log = _read_log(sent_log_path)
    if sent_log and sent_log.get("message_sha256") == message_hash and not force:
        return {"sent": False, "reason": "이미 같은 메시지를 발송함", **sent_log}

    try:
        response = post(webhook_url, json={"text": message}, timeout=10)
    except requests.RequestException as error:
        raise RuntimeError("Slack 요청 실패 - " + hide_secret(f"{type(error).__name__}: {error}")) from None

    result = {
        "sent": response.status_code == 200 and response.text == "ok",
        "sent_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status_code": response.status_code,
        "response_text": hide_secret(response.text[:200]),
        "message_length_chars": len(message),
        "message_length_bytes": len(message.encode("utf-8")),
        "message_sha256": message_hash,
    }
    if not result["sent"]:
        raise RuntimeError(f"Slack 발송 실패 - HTTP {result['status_code']}: {result['response_text']}")
    _write_log(sent_log_path, result)
    return result


# ---- Gmail (STEP 13) ----

def _inline_html(text):
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return re.sub(r"(https?://[^\s<|)]+)", r'<a href="\1">\1</a>', text)


def report_to_html(markdown_text):
    """리포트에서 쓰는 Markdown 요소(제목, 목록, 번호 목록, 인용, 표)만 HTML로 바꾼다."""
    out, table, in_list = [], [], None

    def close_list():
        nonlocal in_list
        if in_list:
            out.append(f"</{in_list}>")
            in_list = None

    def flush_table():
        if not table:
            return
        rows = [[c.strip() for c in line.strip().strip("|").split("|")] for line in table]
        head, body = rows[0], rows[2:]
        cell = 'style="border:1px solid #ccc;padding:4px 8px;text-align:left"'
        out.append('<table style="border-collapse:collapse">')
        out.append("<tr>" + "".join(f"<th {cell}>{_inline_html(c)}</th>" for c in head) + "</tr>")
        for row in body:
            out.append("<tr>" + "".join(f"<td {cell}>{_inline_html(c)}</td>" for c in row) + "</tr>")
        out.append("</table>")
        table.clear()

    for line in markdown_text.splitlines():
        if line.startswith("|"):
            close_list()
            table.append(line)
            continue
        flush_table()
        if line.startswith("# "):
            close_list(); out.append(f"<h1>{_inline_html(line[2:])}</h1>")
        elif line.startswith("## "):
            close_list(); out.append(f"<h2>{_inline_html(line[3:])}</h2>")
        elif line.startswith("> "):
            close_list(); out.append(f"<blockquote>{_inline_html(line[2:])}</blockquote>")
        elif line.startswith("  - "):
            out.append(f"<ul><li>{_inline_html(line[4:])}</li></ul>")
        elif line.startswith("- "):
            if in_list != "ul":
                close_list(); out.append("<ul>"); in_list = "ul"
            out.append(f"<li>{_inline_html(line[2:])}</li>")
        elif re.match(r"^\d+\. ", line):
            if in_list != "ol":
                close_list(); out.append("<ol>"); in_list = "ol"
            out.append(f"<li>{_inline_html(line.split('. ', 1)[1])}</li>")
        elif line.strip():
            close_list(); out.append(f"<p>{_inline_html(line)}</p>")
    flush_table()
    close_list()
    return "\n".join(out)


def build_email_content(report):
    """메일 제목, 텍스트 본문(리포트 원문), HTML 본문을 만든다. 주소·인증정보는 쓰지 않는다."""
    collected = re.search(r"^- 수집 기준일: (\d{4}-\d{2}-\d{2})", report, flags=re.M).group(1)
    subject = f"AX 채용공고 주간 리포트 - {collected}"
    footer = "\n\n---\n상세 리포트 파일: data/processed/weekly_report.md\n이 메일은 AX Job Agent 실습 과정에서 자동 생성되었습니다."
    text_body = report + footer
    html_body = (
        '<html><body style="font-family:sans-serif">'
        + report_to_html(report)
        + "<hr><p>상세 리포트 파일: <code>data/processed/weekly_report.md</code><br>"
        + "이 메일은 AX Job Agent 실습 과정에서 자동 생성되었습니다.</p></body></html>"
    )
    message_hash = hashlib.sha256((subject + text_body + html_body).encode("utf-8")).hexdigest()
    return {"subject": subject, "text_body": text_body, "html_body": html_body, "message_sha256": message_hash}


def _mask_email(address):
    name, _, domain = address.partition("@")
    return f"{name[:1]}***@{domain}"


def send_email(report, user=None, app_password=None, recipient=None,
               sent_log_path=DEFAULT_GMAIL_LOG_PATH, force=False, smtp_factory=smtplib.SMTP_SSL):
    """리포트를 Gmail SMTP(smtp.gmail.com:465, SSL, 앱 비밀번호)로 보낸다. 같은 메일을 이미 보냈으면 건너뛴다.

    recipient를 주지 않으면 본인(GMAIL_USER)에게 보낸다. (STEP 13 테스트와 같음)
    반환: 결과 dict. 주소와 인증정보는 결과·오류에 넣지 않는다.
    """
    if user is None or app_password is None:
        _load_env()
        user = user or os.getenv("GMAIL_USER")
        app_password = app_password or os.getenv("GMAIL_APP_PASSWORD")
    if not user or not app_password:
        raise RuntimeError(".env에 GMAIL_USER 또는 GMAIL_APP_PASSWORD가 없습니다.")
    recipient = recipient or user

    def hide_secret(text):
        text = str(text)
        for secret in {app_password, app_password.replace(" ", "")}:
            if secret:
                text = text.replace(secret, "***")
        return text.replace(user, _mask_email(user))

    content = build_email_content(report)
    sent_log = _read_log(sent_log_path)
    if sent_log and sent_log.get("message_sha256") == content["message_sha256"] and not force:
        return {"sent": False, "reason": "이미 같은 메일을 발송함", **sent_log}

    email = EmailMessage()
    email["Subject"] = content["subject"]
    email["From"] = user
    email["To"] = recipient
    email.set_content(content["text_body"])
    email.add_alternative(content["html_body"], subtype="html")

    try:
        with smtp_factory("smtp.gmail.com", 465, timeout=30) as server:
            server.login(user, app_password)
            refused = server.send_message(email)
    except (smtplib.SMTPException, OSError) as error:
        raise RuntimeError("Gmail 발송 실패 - " + hide_secret(f"{type(error).__name__}: {error}")) from None

    result = {
        "sent": refused == {},
        "sent_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "smtp_refused_recipients": len(refused),
        "subject": content["subject"],
        "text_body_length_chars": len(content["text_body"]),
        "html_body_length_chars": len(content["html_body"]),
        "message_sha256": content["message_sha256"],
    }
    if not result["sent"]:
        raise RuntimeError("Gmail 서버가 일부 수신자를 거부했습니다.")
    _write_log(sent_log_path, result)
    return result
