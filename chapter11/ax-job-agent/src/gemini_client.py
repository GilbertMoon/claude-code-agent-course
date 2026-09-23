"""Gemini 분석과 결과 검증 (Notebook STEP 09~10).

- summarize_with_gemini는 API만 호출하고 파일을 쓰지 않는다. 저장은 save_gemini_results로만 한다.
- API Key는 .env의 GEMINI_API_KEY에서 읽고, 출력하거나 오류 메시지에 남기지 않는다.
- 주의 (STEP 10): 프롬프트로 금지해도 모델은 입력에 없는 내용(예: 기업 특성, AX 풀이)을 추론할 수 있다.
  결과는 verify_gemini_results로 원본과 대조한 뒤 사용한다.
"""
import json
import os
import re
import time

import pandas as pd
from bs4 import BeautifulSoup
from pydantic import BaseModel

DEFAULT_MODEL = "gemini-3.5-flash"  # STEP 09: gemini-3.8-flash / 3.7-flash는 503 반복으로 사용하지 못함
DEFAULT_RESULTS_PATH = "data/processed/gemini_results.json"
RESULT_COLUMNS = [
    "company_name",
    "job_title",
    "career",
    "location",
    "summary",
    "required_skills",
    "job_type",
    "ax_relevance",
    "recommendation_reason",
]


class JobAnalysis(BaseModel):
    """Gemini가 돌려줄 JSON 구조."""
    summary: str
    required_skills: list[str]
    job_type: str
    ax_relevance: str
    recommendation_reason: str


PROMPT_TEMPLATE = """다음은 채용 사이트 검색 결과 목록 화면에서 가져온 채용공고 정보다.
상세 공고 본문(업무 내용, 자격요건, 우대사항)은 확보하지 못했다.

- 회사명: {company_name}
- 공고 제목: {job_title}
- 경력 조건: {career}
- 근무 지역: {location}

아래 원칙을 반드시 지켜라.
1. 위에 입력된 회사명, 공고 제목, 경력 조건, 근무 지역만 근거로 판단한다.
2. 입력에 없는 업무 내용, 기술 스택, 자격요건을 추측하거나 사실처럼 쓰지 않는다.
3. 공고 수나 건수 같은 통계는 계산하지 않는다.
4. JSON 외의 설명은 반환하지 않는다.

각 항목 작성 기준:
- summary: 입력 정보로 확인 가능한 공고의 핵심 내용 요약 (1~2문장)
- required_skills: 상세 공고 본문이 없으므로, 회사명이나 직무명만 보고 기술 스택이나 자격요건을 추측하지 않는다.
  공고 제목에 명시적으로 적힌 기술/역량만 넣고, 확인할 수 없으면 빈 리스트 []로 반환한다.
- job_type: 공고 제목의 직무명을 기준으로 한 직무 유형 분류 (과도한 추측 금지)
- ax_relevance: 제공된 공고 제목/회사명 정보만으로 AX 관련성을 설명하고, 상세 업무 내용은 확인하지 못했다는 한계를 함께 밝힌다.
- recommendation_reason: 입력된 경력 조건, 근무 지역, 공고 제목 등 확인된 정보만 근거로 추천 이유를 쓴다.

모든 값은 한국어로 작성한다.
"""


def build_prompt(job):
    """공고 1건의 프롬프트. 입력은 company_name, job_title, career, location 4개만 쓴다."""
    return PROMPT_TEMPLATE.format(
        company_name=job["company_name"],
        job_title=job["job_title"],
        career=job["career"],
        location=job["location"],
    )


def make_client():
    """.env의 GEMINI_API_KEY로 Gemini 클라이언트를 만든다. (http_options 없음 = SDK 자동 재시도 없음)"""
    from dotenv import load_dotenv
    from google import genai

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(".env에 GEMINI_API_KEY가 없습니다.")
    return genai.Client(api_key=api_key)


def _safe_error(error):
    api_key = os.getenv("GEMINI_API_KEY")
    text = f"{type(error).__name__}: {error}"
    return text.replace(api_key, "***") if api_key else text


def summarize_with_gemini(df, model=DEFAULT_MODEL, client=None, max_attempts=3, base_wait_seconds=5, sleep=time.sleep):
    """공고 1건당 generate_content 1회. 503 UNAVAILABLE일 때만 최대 max_attempts회까지 재시도한다. (STEP 09)

    - 503 이외 오류 또는 max_attempts회 모두 503이면 RuntimeError로 중단하고, 결과를 만들지 않는다.
    - 모든 호출이 성공한 경우에만 JSON을 파싱한다.
    - 반환: (결과 DataFrame, 호출 기록 dict). 파일을 쓰지 않는다.
    """
    from google.genai import errors, types

    client = client or make_client()
    config = types.GenerateContentConfig(response_mime_type="application/json", response_schema=JobAnalysis)

    raw_responses, attempt_log = [], []
    http_request_count = 0
    for _, job in df.iterrows():
        prompt = build_prompt(job)
        results, response = [], None
        for attempt in range(1, max_attempts + 1):
            http_request_count += 1
            try:
                response = client.models.generate_content(model=model, contents=prompt, config=config)
                results.append("성공")
                break
            except errors.APIError as error:
                if error.code == 503 and attempt < max_attempts:
                    results.append("503")
                    sleep(base_wait_seconds * 2 ** (attempt - 1))
                    continue
                results.append(str(error.code))
                stop_error = _safe_error(error)
                break
            except Exception as error:
                results.append("기타 오류")
                stop_error = _safe_error(error)
                break

        attempt_log.append({
            "company_name": job["company_name"],
            "first_result": results[0],
            "attempts": len(results),
            "retries": len(results) - 1,
            "final": "성공" if response is not None else "실패",
        })
        if response is None:
            raise RuntimeError(f"Gemini 생성 호출 최종 실패 ({job['company_name']}): {stop_error}")
        raw_responses.append((job, response.text))

    rows = []
    for n, (job, raw_text) in enumerate(raw_responses, start=1):
        try:
            result = json.loads(raw_text)
        except json.JSONDecodeError as error:
            raise RuntimeError(f"응답 {n} JSON 파싱 실패: {error}") from None
        rows.append({
            **{k: job[k] for k in ["company_name", "job_title", "career", "location"]},
            **{k: result[k] for k in ["summary", "required_skills", "job_type", "ax_relevance", "recommendation_reason"]},
        })

    log = {
        "model": model,
        "job_call_count": len(attempt_log),
        "http_request_count": http_request_count,
        "attempts": attempt_log,
        "raw_responses": [text for _, text in raw_responses],
    }
    return pd.DataFrame(rows, columns=RESULT_COLUMNS), log


def save_gemini_results(results_df, path=DEFAULT_RESULTS_PATH):
    """Gemini 결과를 JSON으로 저장한다. 이 함수만 결과 파일을 쓴다."""
    records = results_df[RESULT_COLUMNS].to_dict(orient="records")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def load_gemini_results(path=DEFAULT_RESULTS_PATH):
    """저장된 Gemini 결과를 읽는다."""
    with open(path, encoding="utf-8") as f:
        return pd.DataFrame(json.load(f), columns=RESULT_COLUMNS)


# ---- STEP 10 검증 ----

# 2026-09-23 실행 결과를 사람이 읽고 고른 확인 대상 표현과 skill 분류.
# 다른 실행의 Gemini 결과에는 그대로 맞지 않으므로 다시 검토해서 넘겨야 한다.
STEP10_REVIEW_TERMS = [
    ("GS리테일", "통합공고", "ax_relevance", "AI/Digital Transformation"),
    ("GS리테일", "통합공고", "recommendation_reason", "유통"),
    ("에스코어", "컨설턴트", "ax_relevance", "AI 전환"),
    ("㈜NAVER", "최적화", "ax_relevance", "AI 전환"),
    ("㈜NAVER", "최적화", "recommendation_reason", "국내 대표 IT 기업"),
]
STEP10_SKILL_KIND = {
    "광고 프로덕트 기획": "직무 표현",
    "AX 광고 예산/과금 구조 설계": "업무 설명",
    "AX 광고 최적화 전략": "업무 설명",
    "HRD": "업무 분야(도메인)",
    "AX": "업무 분야(도메인)",
}


def _squash(text):
    """공백을 없앤 비교용 문자열 (예: 'IT 컨설팅'과 'IT컨설팅'을 같게 본다)."""
    return re.sub(r"\s+", "", text).lower()


def _judge(term, input_text, card_text):
    if _squash(term) in _squash(input_text):
        return "입력 근거 있음"
    if _squash(term) in _squash(card_text):
        return "입력 외 추론 (원본 카드에는 있음)"
    return "과도한 해석 (원본에 없음)"


def verify_gemini_results(results_df, html_path="data/raw/jobkorea_search_ax.html", review_terms=(), skill_kind=None):
    """Gemini 결과를 원본 목록 화면 카드와 대조한다. (STEP 10) 결과는 수정하지 않는다.

    반환: (basic_df: 기본 정보 일치표, term_df: 표현별 근거 판정표)
    """
    skill_kind = skill_kind or {}
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    card_by_title = {}
    for card in soup.find_all(attrs={"data-sentry-component": "CardJob"}):
        title = card.find(attrs={"data-sentry-component": "Title"})
        if title:
            card_by_title[title.get_text(strip=True)] = card

    basic_rows, term_rows = [], []
    for n, g in results_df.iterrows():
        card = card_by_title.get(g["job_title"])
        card_strings = list(card.stripped_strings) if card else []
        card_text = " ".join(card_strings)
        input_text = " ".join([g["company_name"], g["job_title"], g["career"], g["location"]])
        label = f"공고 {n + 1}"

        basic_rows.append({
            "공고": label,
            "회사명": g["company_name"],
            "원본 카드 찾음": card is not None,
            "company_name": g["company_name"] in card_strings,
            "job_title": g["job_title"] in card_strings,
            "career": g["career"] in card_strings,
            "location": g["location"] in card_strings,
            "제목에 AX": "AX" in g["job_title"],
            "ax_relevance에 본문 한계 언급": "본문" in g["ax_relevance"],
        })

        for skill in g["required_skills"]:
            term_rows.append({
                "공고": label, "회사명": g["company_name"], "필드": "required_skills", "표현": skill,
                "판정": _judge(skill, g["job_title"], card_text), "분류": skill_kind.get(skill, "미분류"),
            })

        for part in re.split(r"[,/]", g["job_type"]):
            part = part.strip()
            if part:
                term_rows.append({
                    "공고": label, "회사명": g["company_name"], "필드": "job_type", "표현": part,
                    "판정": _judge(part, input_text, card_text), "분류": "",
                })

        for company, title_word, field, term in review_terms:
            if company != g["company_name"] or title_word not in g["job_title"]:
                continue
            term_rows.append({
                "공고": label, "회사명": g["company_name"], "필드": field, "표현": term,
                "Gemini 결과에 있음": term in g[field],
                "판정": _judge(term, input_text, card_text), "분류": "",
            })

    return pd.DataFrame(basic_rows), pd.DataFrame(term_rows)
