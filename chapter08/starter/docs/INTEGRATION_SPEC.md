# Integration SPEC

전제: `task_stats.py`, `task_export.py`가 Main Branch에 통합되어 있고 각 Workstream Test가 PASS해야 합니다.

## 목표
```powershell
python app.py stats
python app.py export
```

## Stats 출력
```text
total: 3
completed: 1
pending: 2
high_priority: 1
```

## Export 출력
첫 줄은 다음 Header입니다.
```text
id,title,done,due,priority
```

## 규칙
- `calculate_stats()`와 `tasks_to_csv()`를 재사용합니다.
- 두 모듈의 구현을 `app.py`에 복사하지 않습니다.
- 기존 명령은 변경하지 않습니다.
- 외부 dependency를 추가하지 않습니다.

## 검증
```powershell
python -m unittest integration.test_integration -v
python -m unittest tests.test_app -v
python -m unittest workstreams.stats.test_stats -v
python -m unittest workstreams.export.test_export -v
```
