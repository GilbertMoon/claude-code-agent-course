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

Claude Code를 이 디렉터리에서 실행한 후 `/agents`에서 `worker`, `reviewer`가 보이는지 확인할 수 있습니다.

직접 Agent 파일을 추가한 직후라면 새 Claude Code 세션을 시작해야 반영될 수 있습니다.
