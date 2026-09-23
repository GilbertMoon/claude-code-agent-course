# PROJECT SPEC — AX 채용정보 Agent Pipeline

## 1. 프로젝트 목적

잡코리아 등 채용정보 소스에서 AX / AI / 데이터 분석 관련 공고를 정기적으로 수집하고, Python과 pandas로 정제·분석한 뒤 Gemini API로 주요 내용을 요약합니다. 최종 결과는 Markdown 보고서로 만들고 Slack과 Gmail로 전송하며, 로컬 검증이 끝난 뒤 GitHub Actions로 주 1회 자동 실행합니다.

이 프로젝트의 학습 목표는 특정 사이트 크롤링 기술 자체가 아니라 다음 전체 흐름을 직접 이해하는 것입니다.

```text
수집 → 정제 → 분석 → AI 해석 → 검증 → 보고 → 전송 → 자동화
```

---

## 2. 학습자 기준

이 프로젝트는 **Python 데이터 분석 초보자**를 기준으로 진행합니다.

따라서 다음 원칙을 지킵니다.

- 어려운 코드를 한 번에 작성하지 않는다.
- Jupyter Notebook에서 작은 셀 단위로 실행한다.
- 실행 결과를 눈으로 확인한다.
- 각 STEP의 목적과 성공 조건을 이해한 뒤 다음으로 넘어간다.
- 오류가 발생하면 다음 STEP으로 넘어가지 않는다.

---

## 3. 개발 환경

- OS: Windows
- Editor: VS Code
- Python: 3.12.x 기준
- 가상환경: `.venv`
- 주 개발 방식: Jupyter Notebook
- Git 저장소: `GilbertMoon/claude-code-agent-course`
- 작업 브랜치: `ax-job-agent`
- 프로젝트 루트: `chapter11/ax-job-agent`

### 기본 Python 패키지

```text
pandas
requests
beautifulsoup4
jupyter
python-dotenv
```

Gemini / Slack / Gmail 관련 패키지는 실제 해당 STEP에 도달했을 때만 추가합니다.

---

## 4. AI 도구 역할 분리

### GPT Web — Orchestrator

역할:

- 전체 목표 이해
- 작업을 작은 STEP으로 분해
- 현재 STEP의 완료 조건 정의
- 로컬 Coding Agent에 전달할 프롬프트 작성
- 실행 결과를 바탕으로 다음 STEP 결정

GPT Web은 로컬 파일을 직접 수정하는 Coding Agent가 아니라 **전체 진행을 조정하는 역할**입니다.

### Claude Code / Codex / Copilot — Local Coding Agent

세 도구는 토큰 사용량과 상황에 따라 번갈아 사용합니다.

역할:

- 실제 프로젝트 파일 읽기
- 코드 작성 및 수정
- Notebook 생성 또는 수정
- 명령 실행
- 오류 원인 확인과 수정

중요한 규칙:

> 어떤 Agent를 사용하든 한 번에 현재 STEP 하나만 맡깁니다.

### Human — 최종 검증자

학습자는 다음을 직접 확인합니다.

- Notebook 출력
- DataFrame 내용
- 계산 결과
- Gemini 요약과 원문 비교
- Slack / Gmail 실제 도착 여부
- Git 변경 사항

### Gemini API — 운영 Pipeline의 AI

Gemini는 다음과 같은 **텍스트 해석 작업**을 담당합니다.

- 공고 핵심 내용 요약
- 요구 기술 추출
- 직무 유형 분류
- AX 관련성 설명
- 추천 이유 작성

다음과 같은 값은 Gemini가 아니라 pandas가 계산합니다.

- 신규 공고 수
- 회사별 공고 수
- 지역별 공고 수
- 중복 수
- 검색어별 건수

---

## 5. 개발 단계 구조

```text
GPT Web / Gemini Web / Claude Web
        ↓
     Orchestrator
        ↓
Claude Code / Codex / Copilot
        ↓
VS Code + Jupyter Notebook
        ↓
셀 단위 실행
        ↓
Human Verification
        ↓
다음 STEP 결정
        ↓
main.py 통합
```

---

## 6. 최종 운영 구조

```text
GitHub Actions
      ↓
main.py
      ↓
Crawler
      ↓
pandas
├─ 정제
├─ 중복 제거
├─ 신규 공고 판별
├─ 관련 공고 필터링
└─ 기본 통계
      ↓
Gemini API
├─ 요약
├─ 기술 추출
├─ 직무 분류
└─ 추천 이유
      ↓
Markdown Report
      ↓
Slack / Gmail
```

---

## 7. 최종 프로젝트 구조

최종적으로 아래 형태를 목표로 합니다.

```text
chapter11/
└── ax-job-agent/
    ├── docs/
    │   ├── README.md
    │   ├── PROJECT_SPEC.md
    │   └── PROGRESS.md
    ├── notebooks/
    │   └── ax_job_pipeline.ipynb
    ├── src/
    │   ├── crawler.py
    │   ├── preprocess.py
    │   ├── analyzer.py
    │   ├── gemini_client.py
    │   ├── reporter.py
    │   └── notifier.py
    ├── data/
    │   ├── raw/
    │   └── processed/
    ├── reports/
    ├── .env.example
    ├── .gitignore
    ├── main.py
    ├── requirements.txt
    └── README.md
```

처음부터 모든 파일을 만들지 않습니다. 필요한 STEP에 도달할 때 하나씩 생성합니다.

---

## 8. 데이터 명세

DataFrame의 **한 행은 채용공고 한 건**을 의미합니다.

초기 컬럼:

| 컬럼 | 의미 |
|---|---|
| `company_name` | 회사명 |
| `job_title` | 공고 제목 |
| `career` | 경력 조건 |
| `location` | 근무 지역 |
| `posted_date` | 등록일 |
| `closing_date` | 마감일 |
| `job_url` | 공고 URL |
| `search_keyword` | 어떤 검색어로 발견했는지 |
| `collected_at` | 수집 시각 |

처음부터 상세 페이지의 모든 내용을 저장하지 않습니다. 검색 결과에서 안정적으로 얻을 수 있는 항목부터 시작합니다.

---

## 9. 검색 주제 예시

- AX
- AI
- 인공지능
- 데이터 분석
- 생성형 AI
- LLM
- Machine Learning
- Data Scientist
- AI Engineer

초기 개발에서는 여러 키워드를 동시에 사용하지 않습니다.

```text
1개 검색어 → 1개 페이지 → 1개 공고 → 5~10개 공고 → DataFrame → 확장
```

---

## 10. pandas 분석 원칙

Gemini에 데이터를 보내기 전에 pandas에서 사실을 먼저 만듭니다.

확인 항목:

- DataFrame shape
- head
- 결측치
- 중복 URL
- 날짜 변환
- 검색어 통합
- 기존 / 신규 공고 구분
- AX 관련성 기본 필터
- 기본 통계

핵심 원칙:

> Python이 계산할 수 있는 사실은 Python으로 계산하고, Gemini는 요약과 해석에 사용합니다.

---

## 11. 신규 공고 판별

기본 기준은 `job_url`입니다.

```text
지난 실행에서 저장한 URL
        +
이번 실행에서 수집한 URL
        ↓
새로 나타난 URL = 신규 공고
```

필요 시 보조 키:

```text
회사명 + 공고 제목 + 마감일
```

초기에는 데이터베이스를 추가하지 않고 CSV 또는 JSON으로 충분히 검증합니다.

예:

```text
data/processed/jobs_history.csv
```

---

## 12. Gemini 사용 규칙

API Key는 코드에 직접 작성하지 않습니다.

로컬:

```text
.env
```

예:

```env
GEMINI_API_KEY=your-key-here
SLACK_WEBHOOK_URL=
GMAIL_USER=
GMAIL_APP_PASSWORD=
```

저장소에는 실제 키가 없는 `.env.example`만 올립니다.

`.gitignore` 필수 항목:

```text
.env
.venv/
__pycache__/
```

Gemini 응답은 최소 몇 개 공고를 원문과 비교해 검증합니다.

> API 호출 성공 = 분석 성공이 아닙니다.

---

## 13. 보고서 기본 구조

```markdown
# 주간 AX 채용 동향

## 1. 이번 주 요약
- 신규 공고 수
- AX 관련성이 높은 공고 수
- 주요 키워드

## 2. 주요 동향

## 3. 추천 공고
### 회사명 / 공고 제목
- 주요 업무
- 요구 기술
- 추천 이유
- 공고 링크

## 4. 데이터 기준
- 검색어
- 수집 시각
- 분석 대상 건수

## 5. 주의사항
- 실제 지원 전 원문 공고 재확인
```

보고서에서 pandas가 계산한 사실과 Gemini가 작성한 설명을 코드 구조상 구분합니다.

---

## 14. 알림 구현 순서

한 번에 Slack과 Gmail을 모두 구현하지 않습니다.

```text
Markdown Report
      ↓
Slack 성공
      ↓
Gmail 추가
```

Slack에서 확인:

- HTTP 상태
- 실제 메시지 도착
- 한글 깨짐
- 링크 표시
- 메시지 길이

Gmail 인증정보 역시 `.env` 및 GitHub Secrets에서 관리합니다.

---

## 15. Notebook → 함수 → main.py

Notebook에서 모든 단계가 검증된 후 재사용 가능한 함수로 이동합니다.

예:

```python
def collect_jobs():
    ...

def clean_jobs(df):
    ...

def find_new_jobs(df, history_df):
    ...

def analyze_jobs(df):
    ...

def summarize_with_gemini(df):
    ...

def create_report(analysis, summaries):
    ...

def send_slack(report):
    ...

def send_email(report):
    ...
```

Notebook은 삭제하지 않습니다.

- Notebook = 실험 및 검증 기록
- `src/` = 재사용 가능한 운영 코드
- `main.py` = 전체 실행 순서

최종 `main.py` 개념:

```python
def main():
    jobs = collect_jobs()
    clean = clean_jobs(jobs)
    new_jobs = find_new_jobs(clean)
    analysis = analyze_jobs(new_jobs)
    summaries = summarize_with_gemini(new_jobs)
    report = create_report(analysis, summaries)
    send_slack(report)
    send_email(report)

if __name__ == "__main__":
    main()
```

---

## 16. GitHub Actions 원칙

다음 명령이 로컬에서 끝까지 성공하기 전에는 GitHub Actions를 추가하지 않습니다.

```powershell
python main.py
```

진행 순서:

```text
로컬 전체 성공
      ↓
GitHub Actions workflow_dispatch 수동 실행
      ↓
GitHub Secrets 등록
      ↓
수동 실행 성공
      ↓
주 1회 schedule 추가
```

주간 실행 예:

```yaml
schedule:
  - cron: "0 0 * * 1"
```

UTC 월요일 00:00 = 한국시간 월요일 오전 9시입니다.

---

## 17. 전체 STEP

### STEP 01 — 개발환경 확인
Python, 가상환경, VS Code, Notebook 실행 환경을 검증합니다.

### STEP 02 — 수집 데이터 명세
DataFrame 한 행과 컬럼의 의미를 확정합니다.

### STEP 03 — 채용공고 페이지 접근 테스트
HTTP 요청이 가능한지 최소 요청으로 검증합니다.

### STEP 04 — 소량 데이터 수집
1개 검색어, 1개 페이지, 소량 공고만 가져옵니다.

### STEP 05 — DataFrame 생성
수집 결과를 pandas DataFrame으로 변환합니다.

### STEP 06 — 전처리 / 중복 제거
결측, 중복, 날짜 형식 등을 확인합니다.

### STEP 07 — 신규 공고 판별
이전 실행 데이터와 비교해 신규 공고를 구분합니다.

### STEP 08 — 기본 분석 / 관련 공고 필터링
회사, 지역, 경력, 검색어, 직무 키워드 등의 통계를 계산합니다.

### STEP 09 — Gemini API 연동
검증된 일부 신규 공고만 Gemini에 전달합니다.

### STEP 10 — Gemini 결과 검증
원문과 응답을 직접 비교합니다.

### STEP 11 — Markdown 보고서 생성
pandas 사실 + Gemini 해석을 보고서로 결합합니다.

### STEP 12 — Slack 발송
Webhook을 이용해 보고서를 Slack에 전송합니다.

### STEP 13 — Gmail 발송
Slack 성공 이후 Gmail을 추가합니다.

### STEP 14 — 함수화
Notebook에서 검증된 코드를 `src/` 함수로 이동합니다.

### STEP 15 — main.py 통합
전체 작업 흐름을 하나의 실행 진입점으로 연결합니다.

### STEP 16 — 로컬 전체 실행 검증
`python main.py`가 처음부터 끝까지 성공하는지 확인합니다.

### STEP 17 — GitHub Actions 수동 실행
`workflow_dispatch`로 먼저 검증합니다.

### STEP 18 — GitHub Actions 주간 실행
수동 실행 성공 후 schedule을 추가합니다.

---

## 18. 각 STEP 공통 Notebook 패턴

모든 STEP은 가능하면 아래 형태를 유지합니다.

### Markdown Cell — 작업 계획

```markdown
# STEP NN. 제목

## 작업 계획
- 이번 단계에서 무엇을 확인하는가
- 아직 무엇은 하지 않는가
- 완료 조건은 무엇인가
```

### Code Cell — 실행

현재 STEP에 필요한 최소 코드만 작성합니다.

### Code Cell — 확인

`shape`, `head`, 상태 코드, 중복 수처럼 사람이 검증할 수 있는 결과를 출력합니다.

### Markdown Cell — 결과 해석

```markdown
## 실행 결과 해석
- 성공 여부:
- 확인한 데이터:
- 예상과 다른 부분:
- 다음 단계 진행 가능 여부:
- 추가 확인 사항:
```

---

## 19. 작업 시작 시 필수 점검

매번 작업을 시작할 때 다음 순서로 확인합니다.

```powershell
cd C:\dev\claude-code-agent-course\chapter11\ax-job-agent

.\.venv\Scripts\Activate.ps1

git branch --show-current
git status
python --version
where.exe python
```

확인 기준:

- 브랜치: `ax-job-agent`
- 프롬프트 앞: `(.venv)`
- 첫 Python 경로: 프로젝트 `.venv\Scripts\python.exe`
- `PROGRESS.md`의 현재 STEP과 실제 파일 상태가 일치

---

## 20. 완료 기준

프로젝트 완료 시 다음 질문에 직접 답할 수 있어야 합니다.

- 웹 LLM Orchestrator와 로컬 Coding Agent의 차이는 무엇인가?
- Notebook에서 왜 셀 단위 검증을 하는가?
- DataFrame 한 행은 무엇을 의미하는가?
- pandas와 Gemini의 역할은 어떻게 다른가?
- 신규 공고를 어떤 기준으로 판별하는가?
- Gemini 결과를 어떻게 검증하는가?
- `main.py`는 무엇을 담당하는가?
- GitHub Actions는 왜 마지막에 추가하는가?
- Secrets는 왜 필요한가?
- 전체 Agent Pipeline을 자신의 말로 설명할 수 있는가?

---

## 21. 가장 중요한 운영 원칙

```text
PLAN
 ↓
현재 STEP 하나만 Agent에게 전달
 ↓
BUILD
 ↓
Notebook / Terminal 실행
 ↓
OBSERVE
 ↓
Human Verification
 ↓
PROGRESS.md 갱신
 ↓
다음 STEP
```

> **목표는 AI에게 모든 것을 맡기는 것이 아니라, 사람이 목표와 검증 기준을 유지하면서 AI Agent를 단계적으로 사용하는 것입니다.**
