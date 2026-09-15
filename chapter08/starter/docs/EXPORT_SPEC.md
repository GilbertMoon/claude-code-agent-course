# CSV Export Workstream SPEC

## 목표
Task 목록을 CSV 문자열로 변환하는 `task_export.py`를 구현합니다. `app.py`는 수정하지 않습니다.

## 필수 함수
```python
tasks_to_csv(items)
```

## 컬럼 순서
```text
id,title,done,due,priority
```

## 규칙
- 첫 줄은 Header입니다.
- `done`은 `true` 또는 `false`로 출력합니다.
- `due=None`은 빈 문자열입니다.
- 쉼표가 포함된 제목도 올바른 CSV여야 합니다.
- 표준 라이브러리만 사용합니다.
- 빈 리스트는 Header만 반환합니다.
- 줄바꿈은 `\n`을 사용합니다.

## 검증
```powershell
python -m unittest workstreams.export.test_export -v
```
