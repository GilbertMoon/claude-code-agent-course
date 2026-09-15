# Merge Conflict Fixture

## Task A
별도 Worktree에서 `shared_config.py`를 다음처럼 변경하고 Commit합니다.

```python
LABEL = "Task Manager A"
```

## Task B
같은 Base에서 만든 다른 Worktree에서 다음처럼 변경하고 Commit합니다.

```python
LABEL = "Task Manager B"
```

Main Branch에서 A를 먼저 Merge한 뒤 B를 Merge해 같은 한 줄의 Merge Conflict를 관찰합니다.

```text
Worktree Isolation ≠ Conflict-free Merge
```
