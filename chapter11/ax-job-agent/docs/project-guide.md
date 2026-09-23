# Chapter 11 AX Job Agent 프로젝트 사양 및 진행 가이드

## 0. 문서 목적

이 문서는 `chapter11/ax-job-agent` 프로젝트를 진행할 때 매번 작업 시작 전에 현재 상태와 다음 작업을 확인하기 위한 **프로젝트 기준 문서**다.

이 프로젝트는 데이터 분석 초보자가 다음 구조를 직접 경험하는 것을 목표로 한다.

> 수집 → 정제 → 분석 → AI 해석 → 검증 → 보고 → 전송 → 자동화

### 개발 역할

- **GPT Web**: Orchestrator. 전체 목표와 단계, 완료 조건, Claude Code용 작업 프롬프트를 관리한다.
- **Claude Code**: Coding Agent. 로컬 파일을 읽고 만들고 수정하고 실행한다.
- **VS Code + Jupyter Notebook**: 코드 실행과 결과 확인의 주 개발 환경.
- **Human**: 실제 실행 결과와 데이터/해석을 검증하고 다음 단계 진행 여부를 결정한다.
- **Gemini API**: 운영 파이프라인 안에서 채용공고를 요약·해석한다.
- **GitHub Actions**: 마지막에 검증된 `main.py`를 주 1회 실행한다.

> 원본 강의안에서는 `chapter11/ax-job-agent`라는 폴더명을 사용한다.  
> 현재 프로젝트에서는 사용자가 지정한 `chapter11/ax-job-agent`를 작업 폴더명으로 사용한다.  
> 폴더명 외의 프로젝트 사양은 강의안 기준을 따른다.

---

# 1. 최종 목표

잡코리아의 AX / AI / 데이터 분석 관련 채용공고를 주기적으로 수집하고,

1. 필요한 데이터만 정리하고
2. 중복 및 신규 공고를 구분하고
3. 기본 통계를 pandas로 계산하고
4. 관련성이 높은 공고를 필터링하고
5. Gemini API로 주요 내용을 요약·해석하고
6. 주간 Markdown 보고서를 만들고
7. Slack과 Gmail로 보내고
8. GitHub Actions가 주 1회 자동 실행하도록 만든다.

특정 크롤링 기술 자체가 핵심이 아니라 **전체 Agent Pipeline을 작은 단계로 나누어 검증하면서 연결하는 것**이 핵심이다.

---

# 2. 반드시 지키는 개발 원칙

## 원칙 1. 한 번에 전체 프로그램을 만들지 않는다

현재 STEP 하나만 구현한다.

## 원칙 2. 모든 STEP은 다음 순서로 진행한다

```text
작업 계획
    ↓
Claude Code 작업 지시
    ↓
코드/파일 작성
    ↓
Jupyter 또는 Terminal 실행
    ↓
실제 결과 확인
    ↓
결과 해석
    ↓
완료 조건 확인
    ↓
다음 STEP 승인
```

## 원칙 3. Notebook에서 먼저 검증한다

운영 코드부터 만들지 않는다.

Notebook에서 작은 데이터와 작은 코드로 먼저 확인한 뒤 검증된 코드를 `src/`로 옮긴다.

## 원칙 4. 계산 가능한 사실은 Python/pandas로 계산한다

예:

- 신규 공고 수
- 회사별 공고 수
- 지역별 공고 수
- 경력 조건 분포
- 검색어별 건수
- 중복 건수

Gemini에게 이런 계산을 맡기지 않는다.

## 원칙 5. Gemini는 요약과 해석에 사용한다

예:

- 공고 핵심 내용 요약
- 요구 기술 추출
- 직무 유형 분류
- AX 관련성 설명
- 추천 이유

## 원칙 6. 실제 결과를 사람이 확인한다

코드가 실행되었다고 성공한 것이 아니다.

특히 다음을 직접 확인한다.

- 수집 데이터
- DataFrame
- 중복 제거 결과
- 신규 공고 결과
- 통계 결과
- Gemini 응답
- Markdown 보고서
- Slack/Gmail 발송 결과

## 원칙 7. GitHub Actions는 마지막에 추가한다

`python main.py`가 로컬에서 끝까지 성공한 후에만 Actions를 만든다.

---

# 3. 최종 프로젝트 구조

처음부터 모든 파일을 만들지 않는다.

최종적으로는 다음 구조를 목표로 한다.

```text
chapter11/
└── ax-job-agent/
    ├── notebooks/
    │   └── ax_job_pipeline.ipynb
    │
    ├── src/
    │   ├── crawler.py
    │   ├── preprocess.py
    │   ├── analyzer.py
    │   ├── gemini_client.py
    │   ├── reporter.py
    │   └── notifier.py
    │
    ├── data/
    │   ├── raw/
    │   └── processed/
    │
    ├── reports/
    │
    ├── docs/
    │   └── project-guide.md
    │
    ├── .env.example
    ├── .gitignore
    ├── main.py
    ├── requirements.txt
    └── README.md
```

필요해지는 시점에 하나씩 만든다.

---

# 4. 현재 진행 상태

## 프로젝트 상태표

| STEP | 내용 | 상태 |
|---|---|---|
| 00 | 프로젝트 사양 확인 | 완료 |
| 01 | GitHub Fork | 완료 |
| 02 | 로컬 Clone | 완료 |
| 03 | 실습 브랜치 `ax-job-agent` 생성 | 완료 |
| 04 | `chapter11/ax-job-agent` 폴더 생성 | 완료 |
| 05 | Python `.venv` 생성 및 활성화 | 완료 |
| 06 | 기본 패키지 설치 | 진행 예정 |
| 07 | Notebook 환경 확인 | 예정 |
| 08 | 데이터 명세 정의 | 예정 |
| 09 | 채용공고 페이지 접근 테스트 | 예정 |
| 10 | 소량 데이터 수집 | 예정 |
| 11 | DataFrame 생성 | 예정 |
| 12 | 전처리 / 중복 제거 | 예정 |
| 13 | 신규 공고 판별 | 예정 |
| 14 | 기본 분석 / 관련 공고 필터링 | 예정 |
| 15 | Gemini API 연동 | 예정 |
| 16 | Gemini 결과 검증 | 예정 |
| 17 | Markdown 보고서 | 예정 |
| 18 | Slack 발송 | 예정 |
| 19 | Gmail 발송 | 예정 |
| 20 | 함수화 / `src/` 분리 | 예정 |
| 21 | `main.py` 통합 | 예정 |
| 22 | 로컬 전체 파이프라인 검증 | 예정 |
| 23 | Git 커밋 / Push | 예정 |
| 24 | GitHub Actions 수동 실행 | 예정 |
| 25 | GitHub Secrets 설정 | 예정 |
| 26 | GitHub Actions 주간 실행 | 예정 |
| 27 | 최종 점검 | 예정 |

### 현재 정확한 위치

**STEP 06 — 기본 패키지 설치 직전**

현재 터미널은 다음 상태여야 한다.

```text
(.venv) PS C:\dev\claude-code-agent-course\chapter11\ax-job-agent>
```

다음 작업은 이것이다.

```powershell
python -m pip install --upgrade pip
python -m pip install pandas requests beautifulsoup4 jupyter python-dotenv
```

Gemini/Slack 관련 패키지는 아직 설치하지 않는다.

---

# 5. 상세 진행 순서

## STEP 01. 개발환경 확인

### 목표

Python과 VS Code/Jupyter 환경이 정상인지 확인한다.

### 해야 할 일

- `.venv` 활성화
- Python 버전 확인
- VS Code Python 인터프리터를 `.venv`로 선택
- 필요한 패키지 설치
- Jupyter 실행 가능 여부 확인

### 완료 조건

- `python --version` 정상
- `where.exe python` 결과가 프로젝트 `.venv`를 가리킴
- pandas import 성공
- requests import 성공
- BeautifulSoup import 성공
- Jupyter Notebook 실행 가능

---

## STEP 02. 수집 데이터 명세

### 목표

크롤링 전에 **DataFrame의 한 행이 무엇인지** 결정한다.

### 한 행의 의미

> 채용공고 한 건

### 초기 컬럼

```text
company_name
job_title
career
location
posted_date
closing_date
job_url
search_keyword
collected_at
```

### 완료 조건

각 컬럼의 의미와 필요한 이유를 설명할 수 있다.

---

## STEP 03. 채용공고 페이지 접근 테스트

### 목표

대량 수집 전에 HTTP 요청이 가능한지만 확인한다.

### 확인 항목

- 상태 코드
- Content-Type
- 응답 길이
- HTML 구조
- 필요한 채용정보 존재 여부

### 주의

사이트 이용약관, `robots.txt`, 요청 빈도, 페이지 구조를 확인한다.

자동 수집이 제한되거나 실습하기 어렵다면 저장된 샘플 HTML/CSV를 사용한다.

### 완료 조건

실제 페이지 또는 샘플 데이터에서 이후 단계에 사용할 수 있는 구조를 확인한다.

---

## STEP 04. 소량 데이터 수집

### 수집 확장 순서

```text
1개 검색어
 ↓
1개 페이지
 ↓
1개 공고
 ↓
5~10개 공고
 ↓
DataFrame
 ↓
더 많은 공고
 ↓
필요한 경우 여러 검색어
```

처음부터 여러 검색어와 여러 페이지를 동시에 처리하지 않는다.

### 완료 조건

5~10개 정도의 실제 또는 샘플 공고를 구조화할 수 있다.

---

## STEP 05. DataFrame 생성

### 목표

수집 결과를 pandas DataFrame으로 만든다.

### 기본 확인

```python
print(df.shape)
display(df.head())
display(df.isna().sum())
```

### 완료 조건

- 행 = 채용공고
- 컬럼 = 정의한 항목
- 데이터가 실제로 들어 있음
- 결측 상태를 확인함

---

## STEP 06. 전처리 / 중복 제거

### 목표

분석 가능한 형태로 정리한다.

### 작업

- 결측 확인
- 중복 확인
- 날짜 변환
- 검색어 통합
- URL 중복 제거
- 필요한 문자열 정리

### 핵심 확인

```python
df.duplicated(subset=["job_url"]).sum()
```

### 완료 조건

중복과 날짜 변환 상태를 사람이 확인한다.

---

## STEP 07. 신규 공고 판별

### 목표

매주 같은 공고를 다시 신규로 처리하지 않도록 한다.

### 기본 기준

`job_url`

```text
지난 실행 URL
+
이번 실행 URL
↓
이번에 처음 나타난 URL
↓
신규 공고
```

### 저장 방식

처음에는 데이터베이스를 사용하지 않는다.

예:

```text
data/processed/jobs_history.csv
```

필요하면 CSV 또는 JSON으로 관리한다.

---

## STEP 08. 기본 분석 / 관련 공고 필터링

### pandas로 계산

- 이번 주 신규 공고 수
- 회사별 공고 수
- 지역별 공고 수
- 경력 조건 분포
- 검색어별 발견 건수
- 주요 직무 키워드

### 관련성 필터

AX/AI/데이터 관련성을 기본 조건으로 필터링한다.

### 원칙

계산 결과는 코드가 만든 사실로 유지한다.

---

## STEP 09. Gemini API 연동

### Gemini 역할

- 핵심 내용 요약
- 요구 기술 추출
- 직무 유형 분류
- AX 관련성 설명
- 추천 이유

### 하지 않는 것

- 신규 공고 수 계산
- 회사별 건수 계산
- 지역별 건수 계산

이런 값은 pandas가 계산한다.

### 보안

실제 API Key는 코드에 직접 쓰지 않는다.

```text
.env
GEMINI_API_KEY=실제키
```

`.gitignore`:

```text
.env
.venv/
__pycache__/
```

`.env.example`에는 실제 값을 넣지 않는다.

---

## STEP 10. Gemini 결과 검증

### 목표

API 성공과 분석 성공을 구분한다.

### 검증 방법

일부 공고를 원문과 Gemini 결과로 비교한다.

확인:

- 기술 누락
- 잘못된 기술 추출
- 과도한 해석
- 원문과 다른 내용
- 사용할 수 있는 결과인지

### 완료 조건

검증 기록을 Notebook Markdown에 남긴다.

---

## STEP 11. Markdown 보고서

### 기본 구조

```text
# 주간 AX 채용 동향

실행일

## 1. 이번 주 요약

## 2. 주요 동향

## 3. 추천 공고

## 4. 데이터 기준

## 5. 주의사항
```

### 중요

보고서에서 다음을 구분한다.

- pandas가 계산한 사실
- Gemini가 작성한 설명

---

## STEP 12. Slack 발송

먼저 Slack만 구현한다.

### 확인

- HTTP 상태
- 실제 메시지 도착
- 한글 깨짐
- 링크
- 메시지 길이

Slack이 성공한 뒤 Gmail로 넘어간다.

---

## STEP 13. Gmail 발송

교육용 계정에서 허용되는 인증 방식을 사용한다.

인증정보는:

```text
.env
```

에 보관한다.

GitHub Actions에서는 Secrets를 사용한다.

---

## STEP 14. 함수화 / `src/` 분리

Notebook에서 검증된 코드를 함수로 옮긴다.

예:

```python
collect_jobs()
clean_jobs(df)
find_new_jobs(df, history_df)
analyze_jobs(df)
summarize_with_gemini(df)
create_report(analysis, summaries)
send_slack(report)
send_email(report)
```

### 역할

- Notebook = 검증 기록
- `src/` = 재사용 가능한 운영 코드

Notebook은 삭제하지 않는다.

---

## STEP 15. `main.py` 통합

`main.py`는 전체 실행 순서만 담당한다.

```text
collect
 ↓
clean
 ↓
find new
 ↓
analyze
 ↓
Gemini
 ↓
report
 ↓
Slack
 ↓
Gmail
```

### 완료 조건

다음 명령이 로컬에서 끝까지 성공한다.

```powershell
python main.py
```

---

## STEP 16. 로컬 전체 파이프라인 검증

다음 체크리스트를 모두 확인한다.

```text
[ ] 수집 건수가 0이 아닌가?
[ ] 필수 컬럼이 존재하는가?
[ ] URL 중복이 예상 범위인가?
[ ] 날짜 변환이 정상인가?
[ ] 신규 공고 판별이 정상인가?
[ ] Gemini 응답이 원문과 크게 다르지 않은가?
[ ] Markdown 보고서가 생성되는가?
[ ] Slack에 도착하는가?
[ ] Gmail에 도착하는가?
[ ] 오류가 발생했는데 성공처럼 보이지 않는가?
```

실행 로그:

```text
실행 시각
수집 건수
신규 공고 수
Gemini 처리 건수
Slack 성공 여부
Email 성공 여부
오류 메시지
```

---

## STEP 17. Git 저장

민감정보를 확인한다.

절대로 커밋하지 않는다.

```text
.env
실제 API Key
Gmail 비밀번호
Slack Webhook URL
민감한 Notebook 출력
```

그 후:

```powershell
git status
git add .
git commit -m "Add AX job agent pipeline"
git push -u origin ax-job-agent
```

---

## STEP 18. GitHub Actions 수동 실행

로컬 `python main.py`가 성공한 뒤에만 진행한다.

처음에는:

```yaml
on:
  workflow_dispatch:
```

수동 실행으로 검증한다.

---

## STEP 19. GitHub Secrets

다음 값을 Repository Secrets로 등록한다.

```text
GEMINI_API_KEY
SLACK_WEBHOOK_URL
GMAIL_USER
GMAIL_APP_PASSWORD
```

로컬 `.env`의 실제 값은 GitHub에 커밋하지 않는다.

---

## STEP 20. GitHub Actions 주간 실행

수동 실행 성공 후 주간 스케줄을 추가한다.

강의안 예시:

```yaml
on:
  workflow_dispatch:

  schedule:
    - cron: "0 0 * * 1"
```

이는 UTC 월요일 00:00, 한국시간 월요일 오전 9시 기준이다.

---

# 6. 매번 작업을 시작할 때 사용하는 진행 확인 절차

앞으로 이 프로젝트 작업을 시작할 때마다 다음 순서로 확인한다.

## ① 현재 위치 확인

```powershell
pwd
```

## ② Git 상태 확인

```powershell
git status
```

## ③ 현재 브랜치 확인

```powershell
git branch
```

## ④ Python 환경 확인

```powershell
python --version
where.exe python
```

## ⑤ 이 문서의 "현재 정확한 위치" 확인

이 문서의 **4. 현재 진행 상태**를 읽는다.

## ⑥ 마지막으로 완료된 STEP 확인

예:

```text
마지막 완료: STEP 05
```

## ⑦ 다음 STEP 확인

예:

```text
다음 작업: STEP 06
```

## ⑧ 이번 작업의 완료 조건 확인

완료 조건을 먼저 읽고 작업한다.

## ⑨ Claude Code에는 현재 STEP만 전달

전체 프로젝트를 한 번에 구현하도록 요청하지 않는다.

## ⑩ 실행 결과 확인 후 다음 STEP으로 이동

성공하지 않았다면 다음 STEP으로 넘어가지 않는다.

---

# 7. 작업 기록 규칙

각 STEP은 Notebook에 다음 구조로 남긴다.

```text
Markdown Cell
# STEP XX. 제목

## 작업 계획

이번 단계에서 무엇을 확인하는가?

## 완료 조건

무엇이 확인되면 성공인가?

Code Cell
실행 코드

Code Cell
결과 확인

Markdown Cell
## 실행 결과 해석

- 실제 결과:
- 예상과 일치:
- 문제:
- 추가 확인:
- 다음 단계 진행 여부:
```

이렇게 하면 Notebook이 단순한 코드 파일이 아니라 **실습 과정의 검증 기록**이 된다.

---

# 8. Claude Code 작업 요청 원칙

Claude Code에는 항상 다음 정보를 포함한다.

```text
현재 프로젝트:
chapter11/ax-job-agent

현재 STEP:
STEP XX

목표:
...

이번 단계에서 할 일:
1.
2.
3.

이번 단계에서 하지 않을 일:
1.
2.
3.

완료 조건:
1.
2.
3.

실행 후 결과를 보여 달라.
```

특히 다음과 같은 요청은 하지 않는다.

```text
전체 프로젝트를 한 번에 만들어줘.
```

---

# 9. 문제 발생 시 규칙

문제가 생기면 임의로 다음 STEP으로 넘어가지 않는다.

다음 정보를 먼저 확인한다.

```text
1. 실행한 명령
2. 전체 오류 메시지
3. 현재 파일 구조
4. 현재 Python 환경
5. 문제가 발생한 STEP
6. 문제가 발생한 Code Cell
7. 실행 결과
```

그리고 문제를 해결한 후 같은 STEP의 완료 조건을 다시 확인한다.

---

# 10. 최종 완성 구조

```text
주 1회
  ↓
GitHub Actions
  ↓
main.py
  ↓
Crawler
  ↓
pandas
  ├─ 정제
  ├─ 중복 제거
  ├─ 신규 공고
  ├─ 관련 공고 필터
  └─ 기본 통계
  ↓
Gemini API
  ├─ 요약
  ├─ 기술 추출
  ├─ 직무 분류
  └─ 추천 이유
  ↓
Report
  ↓
Slack + Gmail
```

개발 과정에서는:

```text
GPT Web
  ↓
계획 / 프롬프트
  ↓
Claude Code
  ↓
로컬 파일 / 코드
  ↓
Jupyter 실행
  ↓
사람의 검증
  ↓
수정
  ↓
다음 STEP
```

---

# 11. 최종 자기점검

프로젝트가 끝났을 때 다음 질문에 답할 수 있어야 한다.

```text
[ ] Fork와 Clone의 차이를 설명할 수 있는가?
[ ] origin과 upstream의 차이를 설명할 수 있는가?
[ ] Orchestrator와 Claude Code Agent의 역할 차이를 설명할 수 있는가?
[ ] Notebook에서 셀 단위 검증을 한 이유를 설명할 수 있는가?
[ ] DataFrame에서 한 행이 무엇을 의미하는지 설명할 수 있는가?
[ ] 중복 공고와 신규 공고의 판단 방법을 설명할 수 있는가?
[ ] pandas와 Gemini의 역할 차이를 설명할 수 있는가?
[ ] Gemini 결과를 어떻게 검증했는지 설명할 수 있는가?
[ ] main.py의 역할을 설명할 수 있는가?
[ ] GitHub Actions가 왜 마지막 단계인지 설명할 수 있는가?
[ ] GitHub Secrets가 왜 필요한지 설명할 수 있는가?
[ ] 전체 Agent Pipeline을 자신의 말로 설명할 수 있는가?
```

---

# 12. 현재 작업 재개 지점

**현재 완료 상태**

```text
Fork                  ✓
Clone                 ✓
브랜치 생성           ✓
프로젝트 폴더 생성    ✓
.venv 생성            ✓
.venv 활성화          ✓
```

**다음 작업**

```text
STEP 06
기본 패키지 설치
```

명령:

```powershell
python -m pip install --upgrade pip
python -m pip install pandas requests beautifulsoup4 jupyter python-dotenv
```

설치 후에는 **STEP 07 Notebook 환경 확인**으로 진행한다.

이 문서의 상태표를 프로젝트 진행에 따라 계속 갱신한다.
