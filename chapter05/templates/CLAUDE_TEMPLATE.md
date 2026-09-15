# Project Instructions

## Goal

Maintain the Task Manager with small, verifiable changes while preserving existing behavior.

## Development Rules

- Read the relevant code before editing it.
- Change only files required by the current task.
- Do not add unrequested features.
- Avoid broad refactoring unless the task requires it.
- Use the Python standard library only.
- Ask before adding any external dependency.
- Preserve existing CLI commands and output behavior unless the task explicitly changes them.

## Verification

- Run `python -m unittest discover -s tests -v` after code changes.
- If a test fails, analyze the cause before changing code.
- Do not weaken, delete, or bypass existing tests just to make them pass.
- Before finishing, review the changed files and summarize what changed.

## Git

- Review `git diff` before reporting completion.
- Do not commit unless the user explicitly asks for a commit.
