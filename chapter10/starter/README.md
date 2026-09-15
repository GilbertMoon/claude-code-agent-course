# Chapter 10 Starter Resource

이 폴더는 Agent Architecture Optimization Lab용 공통 Starter입니다.

## Baseline 확인

```powershell
python -m unittest tests.test_app -v
python -m unittest evaluation.test_persistence -v
```

기존 기능 테스트는 PASS해야 하고, Persistence Evaluation은 Starter 상태에서 실패가 포함되어야 정상입니다.

## 공통 성공 조건

`docs/PERSISTENCE_SPEC.md`를 사용합니다.

모든 Architecture 실험은 동일한 Starter, SPEC, Evaluation을 사용합니다.

## 실험 Prompt

```text
prompts/A_DIRECT.md
prompts/B_PLAN.md
prompts/C_WORKER_REVIEWER.md
prompts/D_TEAM_OPTIONAL.md
```

## 측정

실험마다 `../templates/OPTIMIZATION_RUN_RECORD.md`를 복사해 결과를 기록합니다.

완료 후:

```powershell
python -m unittest evaluation.test_persistence -v
python -m unittest tests.test_app -v
git diff --stat
git diff
```
