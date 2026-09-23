"""전처리와 신규 공고 판별 (Notebook STEP 06~07).

find_new_jobs는 판별만 하고 파일을 쓰지 않는다. history 저장은 save_history로만 한다.
"""
import os

import pandas as pd

DEFAULT_HISTORY_PATH = "data/processed/jobs_history.csv"

WEEKDAY_NAMES = "월화수목금토일"
DATE_PATTERN = r"^(\d{2})/(\d{2})\(([월화수목금토일])\) (?:등록|마감)$"
JOB_URL_PATTERN = r"https://www\.jobkorea\.co\.kr/Recruit/GI_Read/\d+"


def whitespace_counts(df):
    """컬럼별로 앞뒤 공백이 있는 값의 수 (STEP 06: 확인만 하고 값은 바꾸지 않는다)."""
    return {column: int((df[column] != df[column].str.strip()).sum()) for column in df.columns}


def normalize_job_url(urls):
    """job_url에서 ? 이후의 query parameter를 제거한다. -> https://www.jobkorea.co.kr/Recruit/GI_Read/<ID>"""
    return urls.str.split("?").str[0]


def collection_year(df):
    """collected_at의 연도. 여러 연도가 섞여 있으면 오류."""
    years = pd.to_datetime(df["collected_at"]).dt.year.unique()
    if len(years) != 1:
        raise ValueError(f"collected_at 연도가 하나가 아닙니다: {years.tolist()}")
    return int(years[0])


def convert_dates(original, year):
    """'09/21(월) 등록' -> 2026-09-21. 원본 요일과 달력 요일 비교표도 돌려준다. (STEP 06)

    형식이 다른 값(예: 상시채용, 내일마감)은 NaT가 된다. 이 처리는 STEP 06과 같다.
    """
    parts = original.str.extract(DATE_PATTERN)  # 0: 월, 1: 일, 2: 요일
    converted = pd.to_datetime(str(year) + "-" + parts[0] + "-" + parts[1], format="%Y-%m-%d")
    calendar_weekday = converted.dt.weekday.map(lambda i: WEEKDAY_NAMES[i] if pd.notna(i) else None)
    table = pd.DataFrame({
        "원본": original,
        "변환": converted.dt.strftime("%Y-%m-%d"),
        "원본 요일": parts[2],
        f"{year}년 달력 요일": calendar_weekday,
        "요일 일치": calendar_weekday == parts[2],
    })
    return converted, table


def clean_jobs(df):
    """STEP 06 전처리. 입력 df는 바꾸지 않고 정리한 복사본을 돌려준다.

    1. job_url 정규화 (query parameter 제거)
    2. 정규화된 job_url 기준 중복 제거
    3. posted_date, closing_date를 collected_at 연도로 날짜형 변환
    """
    clean_df = df.copy()
    clean_df["job_url"] = normalize_job_url(clean_df["job_url"])
    clean_df = clean_df.drop_duplicates(subset=["job_url"]).reset_index(drop=True)

    year = collection_year(clean_df)
    for column in ["posted_date", "closing_date"]:
        clean_df[column], _ = convert_dates(clean_df[column], year)
    return clean_df


def check_jobs(raw_df, clean_df):
    """STEP 06에서 확인한 항목을 숫자로 돌려준다. (파일을 쓰지 않는다)"""
    normalized = normalize_job_url(raw_df["job_url"])
    year = collection_year(raw_df)
    date_tables = {column: convert_dates(raw_df[column], year)[1] for column in ["posted_date", "closing_date"]}
    return {
        "missing": {k: int(v) for k, v in raw_df.isna().sum().items()},
        "whitespace": whitespace_counts(raw_df),
        "search_keywords": raw_df["search_keyword"].unique().tolist(),
        "job_url_format_ok": bool(normalized.str.fullmatch(JOB_URL_PATTERN).all()),
        "total": len(raw_df),
        "duplicates": int(normalized.duplicated().sum()),
        "after_dedup": len(clean_df),
        "year": year,
        "date_format_mismatch": {c: int(t["원본 요일"].isna().sum()) for c, t in date_tables.items()},
        "weekday_match": {c: bool(t["요일 일치"].all()) for c, t in date_tables.items()},
        "date_tables": date_tables,
    }


def load_history(path=DEFAULT_HISTORY_PATH):
    """history 파일을 읽는다. 없으면 빈 history(첫 실행)를 돌려준다. (STEP 07)"""
    if os.path.exists(path):
        return pd.read_csv(path, dtype=str)
    return pd.DataFrame(columns=["job_url"])


def find_new_jobs(df, history_df):
    """history에 없는 job_url만 신규로 판별한다. 파일을 쓰지 않는다. (STEP 07)"""
    is_existing = df["job_url"].isin(history_df["job_url"])
    return df[~is_existing].reset_index(drop=True)


def update_history(df, history_df):
    """기존 history + 이번 실행 job_url, job_url 중복 제거. 파일을 쓰지 않는다. (STEP 07)"""
    return (
        pd.concat([history_df, df[["job_url"]]], ignore_index=True)
        .drop_duplicates(subset=["job_url"])
        .reset_index(drop=True)
    )


def save_history(df, history_df, path=DEFAULT_HISTORY_PATH):
    """update_history 결과를 history 파일로 저장한다. 이 함수만 history 파일을 쓴다. (STEP 07)"""
    updated = update_history(df, history_df)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    updated.to_csv(path, index=False, encoding="utf-8")
    return updated
