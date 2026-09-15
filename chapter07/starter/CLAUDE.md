# Project Rules

## Goal

Task Manager 기능을 SPEC과 테스트에 맞게 구현하고, 변경 결과를 검증 가능한 상태로 유지합니다.

## Workflow

```text
SPEC 확인
→ Worker 구현
→ Reviewer 검토
→ PASS / FIX_REQUIRED
→ 필요 시 Worker 수정
→ Reviewer 재검토
→ Main 최종 테스트
→ Human Review
```

## Main Claude

- 먼저 `docs/SPEC.md`를 확인합니다.
- 구현은 기본적으로 Worker에게 위임합니다.
- Reviewer 결과에 따라 다음 행동을 결정합니다.
- `FIX_REQUIRED`는 실행 가능한 수정 목록으로 정리해 Worker에게 전달합니다.
- 2회 연속 `FIX_REQUIRED`, 요구사항 충돌, 큰 구조 변경은 Human Checkpoint로 올립니다.
- `PASS` 이후 전체 테스트와 `git diff`를 최종 확인합니다.

## Implementation Rules

- 필요한 파일만 수정합니다.
- 요청하지 않은 기능과 리팩터링을 추가하지 않습니다.
- 외부 dependency를 추가하지 않습니다.
- 테스트를 삭제하거나 약화하지 않습니다.
- Python 표준 라이브러리만 사용합니다.

## Review Rules

- Reviewer는 구현을 직접 수정하지 않습니다.
- SPEC, 전체 테스트, 회귀, 불필요한 변경을 검토합니다.
- 판정은 `PASS` 또는 `FIX_REQUIRED`로 시작합니다.

## Human Checkpoint

- SPEC 충돌
- 2회 연속 FIX_REQUIRED
- 데이터 삭제
- 새로운 dependency 필요
- 테스트 자체를 바꿔야 할 가능성
- 요청 범위를 넘는 구조 변경
