# Chapter 07 Starter

Multi-Agent Workflow 실습용 Task Manager 리소스입니다.

## 실행

```bash
python app.py list
python -m unittest discover -s tests -v
```

`search` 기능은 `docs/SPEC.md`에 정의되어 있으며 Starter에서는 아직 완성되지 않았습니다.

Claude Code를 이 폴더에서 실행한 뒤 입력창에서 `@`를 누르고 `worker (agent)`, `reviewer (agent)`를 선택해 Agent가 인식되는지 확인합니다. 수동 입력은 `@agent-worker`, `@agent-reviewer` 형식을 사용할 수 있습니다.

> 최신 Claude Code에서는 `/agents`가 과거의 생성·관리 Wizard를 열지 않습니다. 프로젝트 Custom Sub-agent는 `.claude/agents/` 파일로 관리합니다.

```text
CLAUDE.md
app.py
docs/SPEC.md
tests/test_app.py
.claude/agents/worker.md
.claude/agents/reviewer.md
review_case/
```

`review_case/`는 FIX_REQUIRED → 수정 → 재검토 흐름을 재현하기 위한 별도 검증 리소스입니다.
