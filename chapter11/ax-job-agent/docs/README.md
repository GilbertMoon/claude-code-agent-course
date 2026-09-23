# AX Job Agent 프로젝트 문서 안내

이 `docs/` 폴더는 `chapter11/ax-job-agent` 프로젝트를 진행할 때 **항상 가장 먼저 확인하는 기준 문서 모음**입니다.

## 문서 구성

1. [`PROJECT_SPEC.md`](./PROJECT_SPEC.md)
   - 프로젝트 전체 목표
   - 도구별 역할
   - 데이터 구조
   - 전체 파이프라인
   - 구현 원칙
   - 최종 완료 조건

2. [`PROGRESS.md`](./PROGRESS.md)
   - 현재 어디까지 진행했는지
   - 다음에 무엇을 해야 하는지
   - 각 STEP의 완료 여부
   - 작업 재개 시 확인할 명령

## 작업을 시작할 때 항상 하는 순서

```text
1. docs/PROGRESS.md를 연다
2. 현재 완료 STEP을 확인한다
3. '다음 작업'을 확인한다
4. 현재 브랜치와 Git 상태를 확인한다
5. .venv가 활성화되어 있는지 확인한다
6. 현재 STEP 하나만 진행한다
7. 실행 결과를 직접 확인한다
8. 정상일 때만 PROGRESS.md를 갱신한다
9. 다음 STEP으로 이동한다
```

## 초보자용 핵심 원칙

이 프로젝트는 Python 데이터 분석 초보자가 진행하는 것을 기준으로 합니다.

- 한 번에 전체 프로그램을 만들지 않습니다.
- Jupyter Notebook에서 셀 단위로 먼저 실행합니다.
- 각 셀의 결과를 사람이 직접 확인합니다.
- Python으로 계산할 수 있는 사실은 pandas가 계산합니다.
- Gemini는 요약과 설명에 사용합니다.
- Claude Code / Codex / Copilot은 현재 STEP에 필요한 작업만 수행합니다.
- GPT Web은 전체 흐름을 관리하는 Orchestrator 역할을 합니다.
- 로컬에서 전체 파이프라인이 검증된 뒤에만 GitHub Actions를 추가합니다.

> **현재 프로젝트 폴더 이름은 `ai-job-agent`가 아니라 `ax-job-agent`입니다.**
