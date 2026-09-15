# SPEC — Task 상태 필터 기능

## 목표

기존 Task Manager에 완료 여부로 Task를 필터링하는 CLI 기능을 추가합니다.

## 사용 방법

```text
python app.py filter done
python app.py filter pending
```

## 성공 조건

- `filter done`은 `done == True`인 Task만 출력합니다.
- `filter pending`은 `done == False`인 Task만 출력합니다.
- `done`, `pending` 값은 대소문자를 구분하지 않습니다.
- 지원하지 않는 filter 값은 오류로 처리합니다.
- 잘못된 filter 값으로 Task 데이터가 변경되면 안 됩니다.
- 기존 `list`, `add`, `complete`, `due`, `priority` 기능은 그대로 동작해야 합니다.
- 기존 출력 형식을 재사용합니다.
- 외부 dependency를 추가하지 않습니다.

## 제외 범위

- 데이터 영구 저장
- 여러 조건 조합 필터
- 날짜/priority 기반 필터
- 정렬 기능
- UI/Web 기능
- 기존 데이터 구조 리팩터링

## 검증

```powershell
python -m unittest discover -s tests -v
```

```powershell
python app.py filter done
python app.py filter pending
python app.py filter DONE
python app.py filter unknown
```
