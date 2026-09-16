# Chapter 09 Starter Resource

이 폴더는 Agent Teams와 Cross-session Messaging 비교 실습용 리소스입니다.

## 환경 확인

```powershell
claude --version
```

Agent Teams가 기본 실습입니다.

Cross-session Messaging 선택 실습은 **Claude Code v2.1.224 이상 + macOS/Linux/WSL2**에서만 진행합니다. Native Windows에서는 지원되지 않습니다.

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

Windows 환경에서 WSL2를 사용하지 않는 경우 Cross-session Messaging은 실행하지 않고 강사 데모 또는 구조 비교로 대체합니다.

결과는 상위 `templates/TEAM_RUN_RECORD.md`를 복사해 기록합니다.
