# Chapter 06 Starter Resources

Chapter 06 실습에 사용하는 실행 리소스입니다.

## 환경

- Python 3
- 외부 패키지 없음

## 초기 테스트

```powershell
python -m unittest discover -s tests -v
```

아직 구현되지 않은 `filter` 관련 테스트는 초기 상태에서 실패합니다.

## 포함 리소스

```text
CLAUDE.md
app.py
tests/
docs/SPEC.md
.claude/agents/worker.md
.claude/agents/reviewer.md
```

Claude Code를 이 디렉터리에서 실행한 뒤 입력창에서 `@`를 누르고 `worker (agent)`, `reviewer (agent)`를 선택해 Custom Sub-agent가 인식되는지 확인합니다. 수동 입력은 `@agent-worker`, `@agent-reviewer` 형식을 사용할 수 있습니다.

> 최신 Claude Code에서는 `/agents`가 예전의 생성·관리 Wizard를 열지 않습니다. Custom Sub-agent는 `.claude/agents/` 파일로 관리합니다.

이 저장소처럼 `.claude/agents/` 디렉터리가 이미 존재한 상태에서 세션을 시작했다면 Agent 파일 수정은 일반적으로 몇 초 안에 감지됩니다. 세션 시작 후 처음으로 `agents` 디렉터리 자체를 만든 경우에는 재시작이 필요할 수 있습니다.
