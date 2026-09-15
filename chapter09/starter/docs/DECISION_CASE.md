# JSON Persistence Decision Case

## 배경

현재 Task Manager의 데이터는 프로그램을 다시 실행하면 초기 상태로 돌아갑니다.

다음 단계에서는 JSON 파일에 Task를 저장하고 다시 불러오는 Persistence 기능을 고려합니다.

이번 실습에서는 구현하지 않습니다. Agent Team이 아래 쟁점을 검토하고 구현 전에 설계 결정을 제안해야 합니다.

## 현재 Task 데이터

```python
{
    "id": 1,
    "title": "Claude Code 학습하기",
    "done": False,
    "due": None,
    "priority": "medium",
}
```

## 결정해야 할 쟁점

### 1. 저장 파일이 없을 때

- 빈 Task 목록으로 시작
- 샘플 Task로 시작
- 오류를 출력하고 종료

### 2. JSON 파일이 손상되었을 때

- 오류를 출력하고 종료
- 자동으로 빈 데이터로 초기화
- 기존 파일을 백업한 뒤 초기화

데이터 손실을 조용히 숨기지 않아야 합니다.

### 3. 저장 시점

- 변경 직후 자동 저장
- 사용자가 `save` 명령을 실행할 때만 저장
- 프로그램 종료 시 저장

### 4. 저장 경로

- 프로젝트의 `data/tasks.json` 고정
- CLI argument로 경로 지정
- 환경 변수 사용

### 5. 테스트 격리

테스트는 사용자의 실제 `data/tasks.json`을 변경하면 안 됩니다.

## 프로젝트 제약

- Python 표준 라이브러리만 사용
- 기존 CLI 명령의 의미를 바꾸지 않음
- 불필요한 Framework 도입 금지
- 구현 전 Human Approval 필요

## Team 목표

UX, Architecture, QA 관점에서 독립 검토한 뒤 서로의 제안을 반박·보완하고 최종 권고안을 만듭니다.

최종 결과 형식:

```text
Decision
Rationale
Risk
Test implication
Unresolved question
```
