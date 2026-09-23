"""기본 분석과 관련 공고 필터링 (Notebook STEP 08). 파일을 쓰지 않는다."""
import re

import pandas as pd

# STEP 08에서 정한 직무 키워드 목록 (자동 추출이 아니라 정의된 목록의 빈도 분석)
JOB_KEYWORDS = ["컨설턴트", "기획", "담당", "전략", "최적화", "HRD", "물류", "광고"]

# AX, AI는 앞뒤에 영문자가 붙으면 제외 (예: MAIL, TAX). 한글·숫자·기호가 붙은 경우는 포함 (예: AX전략, [AX])
# \b를 쓰지 않는 이유: 파이썬에서는 한글도 단어 글자라서 'AX전략'의 AX를 찾지 못한다.
RELEVANCE_PATTERN = r"(?<![A-Za-z])(?:AX|AI)(?![A-Za-z])|데이터"


def this_week_range(df):
    """collected_at이 속한 주의 월요일 ~ 일요일."""
    collected_date = pd.to_datetime(df["collected_at"]).dt.normalize().unique()
    if len(collected_date) != 1:
        raise ValueError(f"collected_at 날짜가 하나가 아닙니다: {collected_date}")
    collected_date = collected_date[0]
    week_start = collected_date - pd.Timedelta(days=collected_date.weekday())
    return collected_date, week_start, week_start + pd.Timedelta(days=6)


def filter_relevant(df, pattern=RELEVANCE_PATTERN):
    """job_title에 AX / AI / 데이터가 있는 공고 (대소문자 구분 없음)."""
    is_relevant = df["job_title"].str.contains(pattern, flags=re.IGNORECASE, regex=True)
    return df[is_relevant].reset_index(drop=True)


def analyze_jobs(df, job_keywords=JOB_KEYWORDS):
    """STEP 08 분석 결과를 dict로 돌려준다. df는 clean_jobs 결과(posted_date가 날짜형)."""
    collected_date, week_start, week_end = this_week_range(df)
    this_week = df["posted_date"].between(week_start, week_end)
    keyword_counts = pd.Series(
        {kw: int(df["job_title"].str.contains(kw, case=False, regex=False).sum()) for kw in job_keywords}
    )
    relevant_jobs_df = filter_relevant(df)

    return {
        "jobs": df,
        "total": len(df),
        "collected_at": df["collected_at"].iloc[0],
        "collected_date": collected_date,
        "week_start": week_start,
        "week_end": week_end,
        "this_week_jobs": df[this_week],
        "company_counts": df["company_name"].value_counts(),
        "location_counts": df["location"].value_counts(),
        "career_counts": df["career"].value_counts(),
        "search_keyword_counts": df["search_keyword"].value_counts(),
        "keyword_counts": keyword_counts,
        "relevant_jobs_df": relevant_jobs_df,
        "relevant_count": len(relevant_jobs_df),
        "relevant_ratio": len(relevant_jobs_df) / len(df) if len(df) else 0.0,
    }
