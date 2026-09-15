# JSON Persistence SPEC

## 목표

Task Manager의 변경 내용을 프로세스 종료 후에도 유지합니다.

## 데이터 파일

기본값은 `tasks.json`입니다.
환경변수 `TASKS_FILE`이 설정되어 있으면 해당 경로를 사용합니다.

## 필수 모듈

```text
storage.py
```

필수 함수:

```python
load_tasks(path)
save_tasks(path, items)
```

## load_tasks(path)

- `path`는 `str` 또는 `Path`를 허용합니다.
- 파일이 없으면 `[]`를 반환합니다.
- UTF-8 JSON을 읽습니다.
- 정상 JSON이면 Task 리스트를 반환합니다.
- JSON이 손상되었으면 `ValueError`를 발생시킵니다.
- 손상된 파일을 자동으로 덮어쓰거나 초기화하지 않습니다.

## save_tasks(path, items)

- UTF-8 JSON으로 저장합니다.
- 한글을 사람이 읽을 수 있게 유지합니다(`ensure_ascii=False`).
- 최종 파일을 직접 덮어쓰기보다 같은 디렉터리에 임시 파일을 먼저 작성한 뒤 교체합니다.
- 저장 성공 후 임시 파일이 남지 않아야 합니다.
- 외부 패키지를 사용하지 않습니다.

## app.py 연결

프로그램 시작 시 `TASKS_FILE` 또는 기본 `tasks.json`에서 Task를 읽습니다.

성공한 변경 명령은 저장합니다.

```text
add
complete
due
priority
```

읽기 전용 명령은 데이터를 변경하지 않습니다.

```text
list
filter
search
stats
export
```

## 오류 처리

프로그램 시작 시 JSON이 손상된 경우:

```text
오류: Task 데이터 파일을 읽을 수 없습니다.
```

를 출력하고 명령을 수행하지 않습니다.

손상된 원본 파일은 그대로 유지합니다.

## 기존 기능 유지

기존 `list`, `add`, `complete`, `due`, `priority`, `filter`, `search`, `stats`, `export` 동작을 유지합니다.

## 검증

```powershell
python -m unittest evaluation.test_persistence -v
python -m unittest tests.test_app -v
```

## 제외 범위

- Database
- File Lock
- Multi-user 동시성
- Cloud Storage
- Backup History
- 외부 dependency
