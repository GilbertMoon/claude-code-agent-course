# Project Rules

## Goal

Implement only the behavior required by `docs/SPEC.md` while preserving existing Task Manager behavior.

## Workflow

1. Read `docs/SPEC.md` before changing code.
2. Inspect the smallest relevant set of files.
3. Make only necessary changes.
4. Run the full test suite after code changes.
5. Report changed files, test results, and unresolved issues.

## Development Rules

- Use only the Python standard library.
- Do not add dependencies without explicit approval.
- Do not perform unrelated refactoring.
- Do not change tests only to make them pass.
- Preserve existing CLI behavior unless the SPEC explicitly changes it.

## Agent Roles

- Main Claude coordinates the work and makes decisions.
- `worker` implements approved changes and runs tests.
- `reviewer` verifies the implementation and must not modify files.

## Human Checkpoint

Before final commit, the human reviews the full test result and `git diff`.
