# Experiment C — Worker → Reviewer Prompt

`docs/PERSISTENCE_SPEC.md`를 기준으로 Main Claude가 다음 순서로 조율하세요.

1. 입력창의 `@` picker에서 `worker (agent)`를 선택하거나 `@agent-worker`를 사용해 구현을 맡깁니다.
2. Worker가 Evaluation과 Regression Test를 실행합니다.
3. `reviewer (agent)`를 picker에서 선택하거나 `@agent-reviewer`를 사용해 SPEC, diff, 테스트 결과를 독립 검토합니다.
4. `FIX_REQUIRED`면 지적사항만 Worker에게 다시 전달합니다.
5. 최대 2회 수정 후에도 PASS하지 못하면 사람에게 Escalate 합니다.
6. PASS 후 Main이 전체 테스트와 `git diff`를 다시 확인합니다.

규칙:

- Main은 직접 구현하지 않습니다.
- Reviewer는 파일을 수정하지 않습니다.
- 테스트 파일은 수정하지 않습니다.
- 외부 dependency를 추가하지 않습니다.

최종 보고에는 Worker Round 수, Reviewer 판정, 전체 테스트, 변경 파일을 포함합니다.
