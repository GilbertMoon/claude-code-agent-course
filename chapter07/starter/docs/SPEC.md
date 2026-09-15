# Search Feature SPEC

## Goal

Task 제목에서 키워드를 검색하는 기능을 추가합니다.

## CLI

```text
python app.py search <keyword>
```

## Functional Requirements

1. Task의 `title`에서 부분 문자열을 검색합니다.
2. 검색은 대소문자를 구분하지 않습니다.
3. 검색어 앞뒤 공백은 제거합니다.
4. 공백 제거 후 검색어가 비어 있으면 invalid input으로 처리합니다.
5. 검색 결과가 있으면 기존 Task 출력 형식을 사용합니다.
6. 검색 결과가 없으면 `검색 결과가 없습니다.`를 출력합니다.
7. 기존 `list`, `add`, `complete`, `due`, `priority`, `filter` 기능은 그대로 동작해야 합니다.

## Function Contract

```python
search_tasks(items, keyword)
```

- 정상 검색: 일치하는 Task list
- 일치 없음: `[]`
- blank keyword: `None`

## Constraints

- 외부 dependency를 추가하지 않습니다.
- 불필요한 리팩터링을 하지 않습니다.
- 기존 테스트를 삭제하거나 약화하지 않습니다.
- 구현 후 전체 테스트를 실행합니다.

## Done

- 모든 테스트 통과
- SPEC 충족
- 기존 기능 회귀 없음
- 불필요한 파일 변경 없음
- Reviewer `PASS`
- Human Review 완료
