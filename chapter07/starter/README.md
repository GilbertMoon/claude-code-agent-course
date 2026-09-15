# Chapter 07 Starter

Multi-Agent Workflow 실습용 Task Manager 리소스입니다.

## 실행

```bash
python app.py list
python -m unittest discover -s tests -v
```

`search` 기능은 `docs/SPEC.md`에 정의되어 있으며 Starter에서는 아직 완성되지 않았습니다.

Claude Code를 이 폴더에서 실행한 뒤 입력창에서 `@worker`, `@reviewer`를 입력해 mention 후보로 인식되는지 확인하거나, Claude에게 해당 Agent를 사용하도록 요청합니다.

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
