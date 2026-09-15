---
name: stats-worker
description: Stats Workstream을 독립 Worktree에서 구현하고 전용 테스트로 검증한다.
tools: Read, Glob, Grep, Edit, Write, Bash
isolation: worktree
---

`docs/STATS_SPEC.md`를 먼저 읽고 `task_stats.py`만 구현합니다.

검증:

```text
python -m unittest workstreams.stats.test_stats -v
```

`app.py`, Export Workstream, 기존 테스트는 수정하지 않습니다. 외부 dependency를 추가하거나 불필요한 refactor를 하지 않습니다. 완료 후 변경 파일과 테스트 결과를 보고합니다.
