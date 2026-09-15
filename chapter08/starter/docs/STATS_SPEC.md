# Stats Workstream SPEC

## 목표
Task 목록 요약 통계를 계산하는 `task_stats.py`를 구현합니다. `app.py`는 수정하지 않습니다.

## 필수 함수
```python
calculate_stats(items)
```

## 반환 키
```text
total
completed
pending
high_priority
```

## 규칙
- 전체/완료/미완료/high priority 수를 계산합니다.
- 입력 리스트를 수정하지 않습니다.
- 빈 리스트를 처리합니다.
- 외부 패키지를 추가하지 않습니다.

## 검증
```powershell
python -m unittest workstreams.stats.test_stats -v
```
