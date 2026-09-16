# SPEC — Task 상태 필터 기능

## 1. 목표

기존 Task Manager에 완료 여부로 Task를 필터링하는 CLI 기능을 추가합니다.

## 2. 사용 방법

```text
python app.py filter done
python app.py filter pending
```

## 3. 성공 조건

- `filter done`은 `done == True`인 Task만 출력합니다.
- `filter pending`은 `done == False`인 Task만 출력합니다.
- `done`, `pending` 값은 대소문자를 구분하지 않습니다.
- 지원하지 않는 filter 값은 오류로 처리합니다.
- 잘못된 filter 값으로 Task 데이터가 변경되면 안 됩니다.
- 기존 `list`, `add`, `complete`, `due`, `priority` 기능은 그대로 동작해야 합니다.
- 기존 출력 형식 `[상태] [PRIORITY] ID. 제목 (due: 날짜)`를 재사용합니다.
- 외부 dependency를 추가하지 않습니다.

## 4. 구현 범위

필요한 경우 다음을 추가할 수 있습니다.

- 상태를 기준으로 Task 목록을 반환하는 함수
- `filter` CLI command 처리
- usage 출력의 filter 명령 안내

## 5. 제외 범위

이번 작업에서는 다음을 하지 않습니다.

- 데이터 영구 저장
- 여러 조건을 동시에 조합하는 필터
- 날짜 기반 필터
- priority 기반 필터
- 정렬 기능 추가
- UI/Web 기능 추가
- 기존 데이터 구조 리팩터링

## 6. 검증

전체 테스트:

```powershell
python -m unittest discover -s tests -v
```

수동 확인:

```powershell
python app.py filter done
python app.py filter pending
python app.py filter DONE
python app.py filter unknown
```

모든 기존 기능 테스트와 filter 관련 테스트가 통과해야 합니다.
