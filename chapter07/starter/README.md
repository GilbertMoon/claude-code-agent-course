# Chapter 07 Starter

Multi-Agent Workflow 실습용 Task Manager 리소스입니다.

## 실행

```bash
python app.py list
python -m unittest discover -s tests -v
```

`search` 기능은 `docs/SPEC.md`에 정의되어 있으며 Starter에서는 아직 완성되지 않았습니다.

이 폴더에서 Claude Code 새 세션을 시작하고 `/agents`에서 `worker`, `reviewer`가 로드되는지 확인합니다.

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
