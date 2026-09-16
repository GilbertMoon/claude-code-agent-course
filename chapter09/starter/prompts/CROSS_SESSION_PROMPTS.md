# Cross-session Messaging Prompt Samples

> Claude Code v2.1.224 이상 + macOS/Linux/WSL2에서 사용하는 선택 실습입니다. Native Windows에서는 지원되지 않습니다.

## Session 시작 예

터미널 A:

```bash
claude --name architecture
```

터미널 B:

```bash
claude --name qa
```

## 도달 가능한 Session 확인

```text
/list-agents
```

또는:

```text
/peers
```

## Architecture → QA

```text
qa 세션에 JSON Persistence 설계에서 Architecture 관점으로 가장 위험하다고 본 가정 2개를 전달하고,
QA 관점의 반론을 요청해 주세요.
```

## QA → Architecture

```text
architecture 세션에 실제 사용자 파일을 건드리지 않는 테스트 격리 조건을 전달하고,
그 조건을 만족하는 가장 단순한 저장 경로 설계를 요청해 주세요.
```

사용자가 `ListAgents`나 `SendMessage`를 직접 호출하지 않습니다. Claude가 도달 가능한 Session을 찾고 plain-text 메시지를 전달합니다.

## 비교 포인트

Cross-session Messaging에는 Agent Team의 Shared Task List나 Team Lead가 없습니다.

- 메시지를 사람이 요청해야 했는가?
- 어떤 정보만 메시지로 전달되었는가?
- 상대 Session의 Context 전체가 아니라 plain text만 전달되는가?
- 진행 상태를 한 곳에서 관리할 수 있는가?
- 이 문제에 Agent Team이 실제로 더 편리했는가?
