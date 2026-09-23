"""주간 리포트 작성 (Notebook STEP 11).

create_report는 Markdown 문자열만 돌려준다. 파일 저장은 save_report로만 한다.
리포트 구조는 실제로 실행·검증한 STEP 11 결과(data/processed/weekly_report.md)를 따른다.
"""
import os

import pandas as pd

DEFAULT_REPORT_PATH = "data/processed/weekly_report.md"
SKILL_KIND_ORDER = ["직무 표현", "업무 설명", "업무 분야(도메인)"]


def _table(header, rows):
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(str(v) for v in row) + " |" for row in rows]
    return "\n".join(lines)


def _skills_text(skills):
    return ", ".join(skills) if skills else "`[]`"


def _non_skill_terms(term_df):
    """STEP 10에서 기술이 아니라 직무·업무·도메인 표현으로 분류된 required_skills (분류 순서, 처음 나온 순서)."""
    skills = term_df[(term_df["필드"] == "required_skills") & term_df["분류"].isin(SKILL_KIND_ORDER)]
    ordered = []
    for kind in SKILL_KIND_ORDER:
        for term in skills.loc[skills["분류"] == kind, "표현"]:
            if term not in ordered:
                ordered.append(term)
    return ordered


def create_report(analysis, summaries, verification=None, source=None, history_count=None, model="gemini-3.5-flash"):
    """주간 리포트 Markdown 문자열을 만든다. 새 통계를 계산하지 않고 인자로 받은 결과만 쓴다.

    - analysis: analyze_jobs 결과
    - summaries: Gemini 결과 DataFrame (load_gemini_results 또는 summarize_with_gemini 결과)
    - verification: verify_gemini_results 결과 (basic_df, term_df). 없으면 9장을 뺀다.
    - source: crawler.read_source_info 결과 (html_path, card_count, search_url)
    - history_count: STEP 07 history의 URL 수 (첫 실행 신규 판별 참고 문구에 사용)
    """
    jobs = analysis["jobs"]
    collected_at = analysis["collected_at"]
    new_jobs = analysis["this_week_jobs"]
    week_start, week_end = analysis["week_start"], analysis["week_end"]
    keyword_counts = analysis["keyword_counts"]
    keyword_table = keyword_counts[keyword_counts > 0].sort_values(ascending=False, kind="stable")
    total = len(jobs)
    source = source or {}

    lines = [
        "# AX 채용공고 주간 리포트",
        "",
        f"> 이 리포트는 현재 확보한 **{total}건의 표본**에 대한 결과이며, 전체 JobKorea 채용시장이나 전체 AX 채용시장을 대표하지 않는다.",
        "",
        "## 1. 수집 개요",
        "",
        f"- 수집 기준일: {collected_at[:10]} (저장된 HTML 파일의 수정 시각 `{collected_at}` 기준)",
        f"- 검색 키워드: `{jobs['search_keyword'].iloc[0]}`",
        f"- 이번 주 범위: {week_start:%Y-%m-%d} ~ {week_end:%Y-%m-%d}",
        f"- 분석 대상 공고 수: {total}건",
        f"- 신규 공고 수: {len(new_jobs)}건 (등록일 `posted_date`가 이번 주 범위에 포함된 공고)",
    ]
    if history_count is not None:
        lines.append(
            f"  - 참고: STEP 07의 history 기준 판별(첫 실행)에서는 이전 기록이 없어 {history_count}건 모두 신규로 판별되었다. 두 기준은 정의가 다르다."
        )
    lines += [
        f"- 데이터 출처: JobKorea 채용공고 검색 결과 목록 화면 (`{source.get('search_url')}`)",
        "- 데이터 수집 방식: `requests`로 직접 요청하면 보안정책 안내 페이지가 반환되어, **브라우저에서 저장한 검색 결과 HTML**"
        f"(`{source.get('html_path')}`, 1페이지 {source.get('card_count')}건)에서 앞의 {total}건을 추출했다.",
        f"- 데이터 한계: {total}건의 소량 표본이며, 상세 공고 본문은 확보하지 못했다. (10장 참고)",
        "",
        "## 2. 이번 주 신규 공고",
        "",
        _table(["회사명", "공고명", "경력", "근무지역", "등록일", "공고 URL"],
               [[r.company_name, r.job_title, r.career, r.location, f"{r.posted_date:%Y-%m-%d}", r.job_url]
                for r in new_jobs.itertuples()]),
        "",
        "## 3. 전체 분석 대상 공고",
        "",
        _table(["공고", "회사명", "공고명", "경력", "근무지역", "AX 관련성 (Gemini)"],
               [[f"공고 {r.Index + 1}", r.company_name, r.job_title, r.career, r.location, r.ax_relevance]
                for r in summaries.itertuples()]),
        "",
        "AX 관련성은 STEP 09의 Gemini 응답(`ax_relevance`)을 수정 없이 옮긴 것이다. (9장 검증 결과 참고)",
        "",
        "## 4. 회사별 분포",
        "",
        _table(["회사명", "공고 수"], analysis["company_counts"].items()),
        "",
        "## 5. 경력 분포",
        "",
        _table(["경력", "공고 수"], analysis["career_counts"].items()),
        "",
        "## 6. 근무지역 분포",
        "",
        _table(["근무지역", "공고 수"], analysis["location_counts"].items()),
        "",
        "`서울 강남구 외 1`은 근무지가 여러 곳인 공고이며, 원본 문자열 그대로 집계했다.",
        "",
        "## 7. 주요 직무/키워드",
        "",
        _table(["키워드", "포함 공고 수"], keyword_table.items()),
        "",
        "미리 정의한 키워드 목록이 공고 제목에 포함된 공고 수를 센 **정의된 키워드 목록의 빈도 분석**이다. (자동 추출한 키워드가 아님)",
        "",
        "## 8. Gemini 분석 요약",
        "",
        f"`{model}`가 회사명·공고 제목·경력·근무지역 4개 정보만으로 분석한 결과다. (값 수정 없음)",
        "",
        _table(["공고", "회사명", "직무 유형", "추출된 required_skills", "AX 관련성"],
               [[f"공고 {r.Index + 1}", r.company_name, r.job_type, _skills_text(r.required_skills), r.ax_relevance]
                for r in summaries.itertuples()]),
        "",
    ]

    empty_skills = int(summaries["required_skills"].map(len).eq(0).sum())
    if verification is not None:
        basic_df, term_df = verification
        judge_counts = term_df["판정"].value_counts()
        over = term_df[term_df["판정"].str.startswith("과도한 해석")]
        inferred = term_df[term_df["판정"].str.startswith("입력 외 추론")]
        non_skills = ", ".join(f"`{t}`" for t in _non_skill_terms(term_df))
        lines += [
            f"- 주의: STEP 10 검증 결과, `required_skills` 중 일부({non_skills})는 기술 스킬이라기보다 **직무·업무·도메인 표현**에 가깝다.",
            f"- 공고 제목에 기술(도구·언어 등)이 명시된 공고는 없었으며, {empty_skills}건은 `[]`(빈 리스트)로 반환되었다.",
            "",
            "## 9. Gemini 결과 검증 요약",
            "",
            f"- 기본 정보(회사명·공고 제목·경력·근무지역): {int(basic_df[['company_name', 'job_title', 'career', 'location']].all(axis=1).sum())}건 모두 원본과 일치",
            f"- summary: {total}건 모두 입력 정보 범위에서 작성됨",
            f"- 확인한 표현 {len(term_df)}건 중:",
            f"  - 입력 근거 있음: {judge_counts.get('입력 근거 있음', 0)}건",
            f"  - 입력 외 추론: {judge_counts.get('입력 외 추론 (원본 카드에는 있음)', 0)}건",
            f"  - 과도한 해석: {judge_counts.get('과도한 해석 (원본에 없음)', 0)}건",
            "",
            _table(["판정", "공고", "회사명", "필드", "표현"],
                   [[r.판정.split(" (")[0], r.공고, r.회사명, r.필드, r.표현] for r in pd.concat([over, inferred]).itertuples()]),
            "",
            "- `과도한 해석`은 해당 정보가 반드시 거짓이라는 뜻이 아니라, **현재 확보한 원본 자료에서 직접 확인되지 않는 표현**이라는 뜻이다.",
            "- `입력 외 추론`은 Gemini에게 주지 않은 정보인데, 원본 목록 화면 카드(업종·직무 칩)에는 있는 표현이다.",
            "- `required_skills` 중 일부는 기술 스킬보다 직무·업무·도메인 표현에 가깝다.",
            "- 상세 공고 본문이 없어 기술요건·자격요건·우대사항은 검증할 수 없다.",
            "",
        ]

    lines += [
        "## 10. 데이터 품질 및 한계",
        "",
        f"1. 분석 대상은 {total}건의 소량 표본이다.",
        "2. JobKorea에 직접 HTTP 요청을 보냈을 때 보안정책 안내 페이지가 반환되었다.",
        "3. 실제 분석에는 브라우저에서 저장한 검색 결과 HTML을 사용했다.",
        "4. 상세 공고 본문은 확보하지 못했다.",
        "5. 따라서 기술요건, 자격요건, 우대사항은 검증할 수 없다.",
        f"6. 원본 날짜에는 연도가 없어, 수집 기준일의 연도({collected_at[:4]})를 적용했다. (요일 일치로 확인)",
        f"7. `상시채용`, `내일마감` 같은 특수 마감 표현은 이번 표본({total}건)에는 없었다.",
        f"8. 회사·지역·경력 등의 분포는 현재 {total}건 표본의 결과일 뿐 전체 채용시장을 의미하지 않는다.",
        "9. Gemini API 호출 성공과 분석 결과의 정확성은 별개의 문제이며, STEP 10에서 별도로 검증했다.",
        "",
    ]
    return "\n".join(lines)


def save_report(report_text, path=DEFAULT_REPORT_PATH, overwrite=False):
    """리포트를 저장한다. 파일이 이미 있으면 덮어쓰지 않는다. (STEP 11과 같은 보호 장치)

    - 없으면 새로 만든다. -> "created"
    - 같은 내용이면 그대로 둔다. -> "unchanged"
    - 다른 내용이면 overwrite=True일 때만 덮어쓰고, 아니면 RuntimeError로 중단한다.
    """
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            if f.read() == report_text:
                return "unchanged"
        if not overwrite:
            raise RuntimeError(f"{path}가 이미 있고 내용이 다릅니다. 덮어쓰지 않았습니다.")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(report_text)
    return "created"
