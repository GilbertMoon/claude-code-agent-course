# Experiment D — Agent Team Prompt (Optional)

이 실험은 Agent Teams를 사용할 수 있는 환경에서만 수행합니다.

`docs/PERSISTENCE_SPEC.md`를 읽고 작은 Agent Team을 구성해 JSON Persistence 구현 방안을 검토하고 완성해 주세요.

권장 역할:

```text
Lead
├── storage-reviewer
├── implementation-reviewer
└── qa-reviewer
```

- Team을 3명보다 크게 만들지 마세요.
- 각 Teammate는 먼저 독립 검토합니다.
- 발견한 위험과 반론을 서로 공유합니다.
- 구현 책임이 중복되지 않도록 Lead가 조정합니다.
- 테스트 파일은 수정하지 않습니다.
- 외부 dependency를 추가하지 않습니다.

완료 조건:

```text
python -m unittest evaluation.test_persistence -v
python -m unittest tests.test_app -v
```

최종 보고에는 Teammate 수, 실제 의사결정이 바뀐 사례, coordination overhead, 전체 테스트, Team 필요성 판단을 포함합니다.
