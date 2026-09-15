# Experiment B — Plan + Single Agent Prompt

`docs/PERSISTENCE_SPEC.md`를 읽고 먼저 Plan Mode에서 구현 계획만 작성해 주세요. 아직 파일을 수정하지 마세요.

Plan에는 다음을 포함하세요.

```text
수정 파일
데이터 파일 경로
missing file 처리
corrupt JSON 처리
저장 시점
atomic save 방법
기존 명령 영향 범위
Evaluation / Regression Test 순서
```

불명확한 점은 구현 전에 질문합니다. 사람이 Plan을 승인한 뒤 구현하고 다음을 실행합니다.

```text
python -m unittest evaluation.test_persistence -v
python -m unittest tests.test_app -v
```

테스트 파일은 수정하지 마세요.
