# Agent Team Start Prompt

```text
이번 작업은 Subagent가 아니라 Agent Team으로 진행해 주세요.

목표는 코드를 구현하는 것이 아니라 Task Manager의 JSON Persistence 설계를 검토하는 것입니다.

먼저 다음 파일을 읽으세요.
- docs/DECISION_CASE.md
- docs/DECISION_RUBRIC.md

세 명의 Teammate를 구성해 주세요.
- ux-reviewer: 사용자 경험과 예측 가능성 관점
- architecture-reviewer: 구조, 책임 분리, 복구 가능성 관점
- qa-reviewer: 테스트 가능성, 실패 조건, 데이터 격리 관점

가능하면 .claude/agents/의 동일한 역할 정의를 사용하세요.

운영 규칙:
1. 각 Teammate는 먼저 독립적으로 검토합니다.
2. Shared Task List를 사용해 각 검토 작업과 최종 종합 작업의 상태를 관리합니다.
3. 각 Teammate는 다른 Teammate에게 최소 한 번 이상 중요한 질문, 반론 또는 발견을 직접 전달해야 합니다.
4. 서로의 의견을 받은 뒤 필요하면 자신의 제안을 수정합니다.
5. 어느 Teammate도 파일을 수정하지 않습니다.
6. 합의되지 않은 내용은 NEEDS_HUMAN_DECISION으로 남깁니다.
7. 세 Teammate의 검토와 상호 메시지가 끝난 뒤에만 Lead가 결과를 종합합니다.

최종 결과는 다음 네 주제별로 정리하세요.
- Missing file
- Corrupt JSON
- Save timing
- Storage path / Test isolation

각 주제마다 아래 형식을 사용하세요.
- Decision
- Rationale
- Risk
- Test implication
- Unresolved question

마지막에 Human Approval이 필요한 항목을 따로 정리하세요.
```
