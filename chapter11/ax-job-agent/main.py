"""AX Job Agent 실행 진입점. 전체 실행 순서만 담당한다. (실제 처리 로직은 src/에 있다)

collect -> clean -> find new -> analyze -> Gemini -> report -> Slack -> Gmail

프로젝트 루트에서 실행한다:  python main.py
"""
from src.analyzer import analyze_jobs
from src.crawler import collect_jobs, read_source_info
from src.gemini_client import (
    STEP10_REVIEW_TERMS,
    STEP10_SKILL_KIND,
    load_gemini_results,
    verify_gemini_results,
)
from src.notifier import send_email, send_slack
from src.preprocess import clean_jobs, find_new_jobs, load_history, save_history
from src.reporter import create_report, save_report

HTML_PATH = "data/raw/jobkorea_search_ax.html"  # 브라우저에서 저장한 검색 결과 (JobKorea에 직접 요청하지 않음)


def main():
    # 1. collect
    raw_jobs = collect_jobs(html_path=HTML_PATH)
    print(f"[collect] 저장된 HTML에서 {len(raw_jobs)}건 추출")

    # 2. clean
    jobs = clean_jobs(raw_jobs)
    print(f"[clean] 전처리 후 {len(jobs)}건")

    # 3. find new (새 공고가 있을 때만 history 저장)
    history = load_history()
    new_jobs = find_new_jobs(jobs, history)
    if len(new_jobs) > 0:
        save_history(jobs, history)
    print(f"[find new] history {len(history)}건 기준 신규 {len(new_jobs)}건"
          f" -> history {'저장' if len(new_jobs) > 0 else '변경 없음'}")

    # 4. analyze
    analysis = analyze_jobs(jobs)
    print(f"[analyze] 이번 주 등록 {len(analysis['this_week_jobs'])}건, 관련 공고 {analysis['relevant_count']}건")

    # 5. Gemini (저장된 STEP 09 결과를 재사용하고 원본과 대조한다. API는 호출하지 않는다)
    summaries = load_gemini_results()
    verification = verify_gemini_results(summaries, html_path=HTML_PATH,
                                         review_terms=STEP10_REVIEW_TERMS, skill_kind=STEP10_SKILL_KIND)
    print(f"[Gemini] 저장된 결과 {len(summaries)}건 사용 (API 호출 없음), 검증 표현 {len(verification[1])}건")

    # 6. report
    report = create_report(analysis, summaries, verification=verification,
                           source=read_source_info(HTML_PATH), history_count=len(history))
    print(f"[report] {len(report)}글자 -> {save_report(report)}")

    # 7. Slack
    slack = send_slack(report)
    print(f"[Slack] {'발송' if slack['sent'] else '건너뜀: ' + slack.get('reason', '')}")

    # 8. Gmail
    email = send_email(report)
    print(f"[Gmail] {'발송' if email['sent'] else '건너뜀: ' + email.get('reason', '')}")

    print("완료")


if __name__ == "__main__":
    main()
