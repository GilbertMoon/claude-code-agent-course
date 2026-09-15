# Chapter 08 Starter Resource

이 폴더는 Parallel Agent + Git Worktree 실습용 Starter입니다.

## 기준 확인

```powershell
python -m unittest tests.test_app -v
```

기존 기능 테스트가 먼저 통과해야 합니다.

## 병렬 Workstream

```text
Stats  → docs/STATS_SPEC.md
Export → docs/EXPORT_SPEC.md
```

각 Workstream은 별도 Worktree에서 진행합니다.

```powershell
claude --worktree stats
claude --worktree export
```

각 Worker는 자신의 Workstream 테스트만 실행합니다.

```powershell
python -m unittest workstreams.stats.test_stats -v
python -m unittest workstreams.export.test_export -v
```

두 Branch를 통합한 뒤 `docs/INTEGRATION_SPEC.md`를 기준으로 `app.py`를 연결하고 다음을 실행합니다.

```powershell
python -m unittest integration.test_integration -v
python -m unittest tests.test_app -v
```

이 폴더를 별도 실습 디렉터리에 복사해 하나의 Git 저장소로 초기화한 뒤 사용하는 것을 권장합니다.
