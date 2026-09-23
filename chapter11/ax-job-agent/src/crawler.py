"""채용공고 수집 (Notebook STEP 04~05).

JobKorea에 직접 요청하면 보안정책 페이지가 반환되므로(STEP 03),
브라우저에서 저장한 검색 결과 HTML을 파싱한다. 이 모듈은 네트워크 요청을 보내지 않는다.
"""
import json
import os
import re
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup

DEFAULT_HTML_PATH = "data/raw/jobkorea_search_ax.html"

# STEP 02에서 정의한 컬럼 (한 행 = 채용공고 1건)
COLUMNS = [
    "company_name",
    "job_title",
    "career",
    "location",
    "posted_date",
    "closing_date",
    "job_url",
    "search_keyword",
    "collected_at",
]


def extract_job(card):
    """공고 카드(CardJob) 1개에서 7개 필드를 화면 문자열 그대로 꺼낸다. 없으면 None. (STEP 04)"""
    job = {
        "company_name": None,
        "job_title": None,
        "career": None,
        "location": None,
        "posted_date": None,
        "closing_date": None,
        "job_url": None,
    }

    title_link = card.find(attrs={"data-sentry-component": "Title"})
    if title_link:
        job["job_title"] = title_link.get_text(strip=True)
        job["job_url"] = title_link.get("href")

        # 회사명: 제목 블록 바로 다음 span 안의 회사 링크, 그 안의 첫 번째 span
        company_block = title_link.parent.find_next_sibling("span")
        if company_block and company_block.find("span"):
            job["company_name"] = company_block.find("span").get_text(strip=True)

    # 근무지역: 장소(place) 아이콘이 들어 있는 GrayChip
    for chip in card.find_all(attrs={"data-sentry-component": "GrayChip"}):
        if chip.find("span", class_=re.compile("place")):
            job["location"] = chip.get_text(strip=True)
            break

    # 등록일: "등록"으로 끝나는 span
    posted = card.find("span", string=re.compile("등록$"))
    if posted:
        job["posted_date"] = posted.get_text(strip=True)

        # 마감일: 등록일 옆 span 중 구분점(•)이 아닌 첫 번째 값
        for span in posted.find_next_siblings("span"):
            text = span.get_text(strip=True)
            if text != "•":
                job["closing_date"] = text
                break

        # 경력: 등록일이 있는 정보 줄의 왼쪽 묶음에서 첫 번째 span
        info_row = posted.parent.parent
        left_group = info_row.find("div")
        if left_group and left_group.find("span"):
            job["career"] = left_group.find("span").get_text(strip=True)

    return job


def read_cards(html_path=DEFAULT_HTML_PATH):
    """저장된 HTML에서 공고 카드(CardJob) 목록을 읽는다."""
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    return soup.find_all(attrs={"data-sentry-component": "CardJob"})


def read_source_info(html_path=DEFAULT_HTML_PATH):
    """보고서에 적을 원본 정보: 파일 경로, 카드 수, 브라우저가 기록한 저장 원본 URL."""
    with open(html_path, encoding="utf-8") as f:
        head = f.read(2000)
    match = re.search(r"saved from url=\(\d+\)(\S+)", head)
    return {
        "html_path": html_path,
        "card_count": len(read_cards(html_path)),
        "search_url": match.group(1).rstrip(" -") if match else None,
    }


def html_collected_at(html_path=DEFAULT_HTML_PATH):
    """HTML을 저장한 시각 문자열.

    같은 이름의 메타 파일(예: jobkorea_search_ax.meta.json)이 있으면 그 안의 collected_at을 쓰고,
    없으면 HTML 파일의 수정 시각을 쓴다. git checkout은 파일 수정 시각을 보존하지 않으므로
    다른 환경(GitHub Actions 등)에서도 같은 값을 쓰려면 메타 파일이 필요하다.
    """
    meta_path = os.path.splitext(html_path)[0] + ".meta.json"
    if os.path.exists(meta_path):
        with open(meta_path, encoding="utf-8") as f:
            return json.load(f)["collected_at"]
    return datetime.fromtimestamp(os.path.getmtime(html_path)).strftime("%Y-%m-%d %H:%M:%S")


def collect_jobs(html_path=DEFAULT_HTML_PATH, limit=5, search_keyword="ax"):
    """저장된 HTML에서 앞의 limit건을 추출해 STEP 02 컬럼의 DataFrame으로 만든다. (STEP 04~05)

    - 값은 HTML 화면 문자열 그대로다. (날짜 변환, URL 정규화는 clean_jobs에서 한다)
    - collected_at은 HTML을 저장한 시각이다. (메타 파일 값, 없으면 HTML 파일 수정 시각. 정확한 공고 수집 시각이 아님)
    """
    jobs = [extract_job(card) for card in read_cards(html_path)[:limit]]
    collected_at = html_collected_at(html_path)

    rows = []
    for job in jobs:
        row = dict(job)
        row["search_keyword"] = search_keyword
        row["collected_at"] = collected_at
        rows.append(row)

    return pd.DataFrame(rows, columns=COLUMNS)
