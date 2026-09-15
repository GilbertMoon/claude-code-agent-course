# Chapter 09 Starter Resource

이 폴더는 Agent Teams와 Cross-session Messaging 비교 실습용 리소스입니다.

## 환경 확인

```powershell
claude --version
```

Native Windows에서 Cross-session Messaging까지 실습하려면 v2.1.234 이상을 권장합니다.

## 기준 코드 확인

```powershell
python app.py list
python app.py stats
python app.py export
python -m unittest tests.test_app -v
```

## 실습 리소스

```text
config/settings.agent-teams.example.json
docs/DECISION_CASE.md
docs/DECISION_RUBRIC.md
.claude/agents/
prompts/TEAM_START_PROMPT.md
prompts/CROSS_SESSION_PROMPTS.md
```

Agent Team은 JSON Persistence를 구현하지 않고 설계만 검토합니다.

결과는 상위 `templates/TEAM_RUN_RECORD.md`를 복사해 기록합니다.
