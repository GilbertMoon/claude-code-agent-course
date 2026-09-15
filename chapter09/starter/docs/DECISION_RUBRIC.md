# Agent Team Decision Rubric

각 설계 제안을 아래 기준으로 평가합니다.

| 기준 | 질문 |
|---|---|
| Simplicity | 초보자 프로젝트에 지나치게 복잡하지 않은가? |
| Data Safety | 사용자 데이터를 조용히 잃을 가능성이 없는가? |
| Predictability | 동작을 사용자가 쉽게 예측할 수 있는가? |
| Testability | 실제 사용자 파일 없이 자동 테스트할 수 있는가? |
| Compatibility | 기존 CLI 기능을 깨뜨리지 않는가? |
| Recovery | 실패 상황에서 복구 경로가 있는가? |
| Scope | 현재 범위 밖으로 불필요하게 확장하지 않는가? |

## Reviewer별 우선 관점

### UX Reviewer
- 오류 메시지 이해 가능성
- 저장 동작의 예측 가능성
- 데이터 손실 경험

### Architecture Reviewer
- 책임 분리
- 결합도
- 최소 구조
- 복구 가능성

### QA Reviewer
- 정상/오류 시나리오의 테스트 가능성
- 실제 사용자 데이터와 테스트 데이터 격리
- Regression 기준

## 최종 판정

```text
AGREE
AGREE_WITH_CONDITION
NEEDS_HUMAN_DECISION
```

합의되지 않은 내용을 Lead가 임의로 숨기지 않습니다.
