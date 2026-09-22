# Claude Code Agent Fast Track — 학생 실습 리소스 안내

이 폴더는 **3강 실습형 Fast Track**에서 사용하는 PUBLIC 실습 리소스의 진입점입니다.

이 저장소에는 강의안이나 강사 스크립트를 공개하지 않습니다. 여기서는 수업 중 필요한 Starter 코드, 테스트, SPEC/Plan 템플릿, `CLAUDE.md`, Custom Sub-agent 설정과 검증 리소스만 연결합니다.

---

## 1. Fast Track 전체 흐름

```text
1강
Single Agent + SPEC + Plan

        ↓

2강
Reliable Agent + CLAUDE.md + Worker / Reviewer

        ↓

3강
Multi-Agent Workflow + FIX_REQUIRED Loop
```

권장 운영 시간은 강의당 약 3시간, 총 9시간입니다.

---

## 2. 수업별 실습 경로

| 강의 | 실습 구간 | 사용 리소스 | 핵심 목적 |
|---|---|---|---|
| 1강 | Agent + SPEC + Plan | [`chapter03/starter`](../chapter03/starter/) | 작은 기능을 Single Agent에게 맡기고 검증 |
| 1강 | SPEC 작성 | [`chapter03/templates/SPEC_TEMPLATE.md`](../chapter03/templates/SPEC_TEMPLATE.md) | 완료 조건 명확화 |
| 1강 | Plan 검토 | [`chapter03/templates/PLAN_REVIEW_TEMPLATE.md`](../chapter03/templates/PLAN_REVIEW_TEMPLATE.md) | 구현 전 영향 범위 확인 |
| 2강 A | Reliable Agent | [`chapter04/starter`](../chapter04/starter/) | 실패 테스트를 이용한 검증과 수정 |
| 2강 B | Context + Reviewer | [`chapter06/starter`](../chapter06/starter/) | `CLAUDE.md`, Worker, Reviewer 실습 |
| 3강 | Multi-Agent Workflow | [`chapter07/starter`](../chapter07/starter/) | Orchestrator → Worker → Reviewer 흐름 |
| 3강 | 강제 Review Loop | [`chapter07/starter/review_case`](../chapter07/starter/review_case/) | `FIX_REQUIRED → 수정 → 재검토` 재현 |

> **중요:** 2강은 중간에 `chapter04/starter`에서 `chapter06/starter`로 실습 폴더를 이동합니다.

---

## 3. 시작 전 확인

저장소를 내려받은 뒤 루트에서 환경을 확인합니다.

### Windows PowerShell

```powershell
python --version
claude --version
git status
```

### macOS / Linux

환경에 따라 `python` 대신 `python3`를 사용할 수 있습니다.

```bash
python3 --version
claude --version
git status
```

수업에서는 각 Starter 폴더에서 Claude Code를 실행합니다.

```powershell
claude
```

---

# 4. 1강 — Single Agent + SPEC + Plan

## STEP 1. Starter로 이동

저장소 루트 기준:

```powershell
cd chapter03\starter
```

macOS / Linux:

```bash
cd chapter03/starter
```

## STEP 2. Baseline 확인

```powershell
python app.py list
python app.py complete 2
```

이 Starter에는 이미 `list`, `complete` 기능이 있습니다.

수업에서는 이 상태에서 작은 기능을 추가하며 다음 흐름을 경험합니다.

```text
REQUEST
  ↓
SPEC
  ↓
PLAN
  ↓
BUILD
  ↓
CHECK
```

## STEP 3. SPEC / Plan 템플릿 위치

```text
chapter03/templates/SPEC_TEMPLATE.md
chapter03/templates/PLAN_REVIEW_TEMPLATE.md
```

수업 지시에 따라 템플릿을 복사하거나 참고해 사용합니다.

## 1강 종료 전 확인

```powershell
python app.py list
git status
git diff
```

완료 보고만 보지 말고 실제 실행 결과와 변경 파일을 직접 확인합니다.

---

# 5. 2강 A — Test로 Reliable Agent 만들기

## STEP 1. Chapter 04 Starter로 이동

저장소 루트에서:

```powershell
cd chapter04\starter
```

## STEP 2. 초기 테스트 실행

```powershell
python -m unittest discover -s tests -v
```

이 Starter는 교육 목적상 **일부 테스트가 실패하는 상태**로 제공됩니다.

테스트 실패 자체를 없애기 위해 테스트를 삭제하거나 약화하지 않습니다.

수업에서는 다음 흐름으로 진행합니다.

```text
TEST
 ↓
FAIL
 ↓
ANALYZE
 ↓
FIX
 ↓
FULL TEST
 ↓
GIT DIFF
```

## STEP 3. 수정 후 전체 테스트

```powershell
python -m unittest discover -s tests -v
git status
git diff
```

---

# 6. 2강 B — CLAUDE.md + Worker / Reviewer

2강 후반에는 **다른 Starter로 이동합니다.**

저장소 루트에서:

```powershell
cd chapter06\starter
```

## STEP 1. 포함 리소스 확인

```text
CLAUDE.md
app.py
tests/
docs/SPEC.md
.claude/agents/worker.md
.claude/agents/reviewer.md
```

## STEP 2. 초기 테스트 확인

```powershell
python -m unittest discover -s tests -v
```

아직 구현되지 않은 `filter` 관련 테스트는 초기 상태에서 실패할 수 있습니다.

## STEP 3. Custom Sub-agent 확인

현재 폴더에서 Claude Code를 시작합니다.

```powershell
claude
```

Claude Code 입력창에서 `@`를 눌러 다음 Agent가 보이는지 확인합니다.

```text
worker (agent)
reviewer (agent)
```

수동 mention 형식은 다음과 같습니다.

```text
@agent-worker
@agent-reviewer
```

수업에서는 역할을 다음처럼 분리합니다.

```text
Worker
→ 구현

Reviewer
→ 검증
→ PASS 또는 FIX_REQUIRED
```

## 2강 종료 전 확인

```powershell
python -m unittest discover -s tests -v
git status
git diff
```

---

# 7. 3강 — Multi-Agent Workflow

## STEP 1. Chapter 07 Starter로 이동

저장소 루트에서:

```powershell
cd chapter07\starter
```

## STEP 2. Baseline 확인

```powershell
python app.py list
python -m unittest discover -s tests -v
```

`search` 기능은 [`docs/SPEC.md`](../chapter07/starter/docs/SPEC.md)에 정의되어 있으며 Starter에서는 아직 완성되지 않은 상태입니다.

## STEP 3. Agent 확인

```powershell
claude
```

입력창의 `@` 메뉴 또는 다음 mention을 사용합니다.

```text
@agent-worker
@agent-reviewer
```

3강의 핵심 흐름은 다음과 같습니다.

```text
Human
  ↓
Orchestrator
  ↓
Worker
  ↓
Reviewer
  ├─ PASS
  │    ↓
  │  Human Review
  │
  └─ FIX_REQUIRED
         ↓
       Worker
         ↓
      Reviewer
```

---

## 8. FIX_REQUIRED Loop 실습

첫 구현이 바로 PASS하더라도 Review Loop를 학습할 수 있도록 별도 리소스가 준비되어 있습니다.

```text
chapter07/starter/review_case/
```

실행:

```powershell
python -m unittest discover -s review_case -v
```

수업 지시에 따라 다음 흐름을 확인합니다.

```text
Reviewer
→ FIX_REQUIRED
→ 수정 Task 정리
→ Worker 수정
→ Reviewer 재검토
→ PASS
```

중요한 것은 Agent 수가 아니라 **누가 구현하고, 누가 검증하며, 어떤 조건에서 다시 작업하는지가 명확한가**입니다.

---

# 9. 실습 공통 규칙

Fast Track에서는 다음 규칙을 공통으로 사용합니다.

- 관련 코드를 먼저 읽습니다.
- 요구한 범위 안에서만 수정합니다.
- 외부 dependency를 임의로 추가하지 않습니다.
- 테스트를 통과시키기 위해 기존 테스트를 삭제하거나 약화하지 않습니다.
- 변경 후 전체 테스트 또는 지정된 검증 명령을 실행합니다.
- 완료 보고 전 `git diff`를 확인합니다.
- Agent 결과와 Human Review를 구분합니다.

---

# 10. 실습 상태가 섞였을 때

각 강의는 정해진 Starter 상태를 기준으로 진행합니다.

이전 실습 변경이 남아 있으면 다음 수업 결과가 달라질 수 있습니다.

먼저 확인합니다.

```powershell
git status
git diff
```

변경 사항이 있다면 임의로 삭제하지 말고, 수업에서 안내한 원복 방법을 사용하거나 **새로운 로컬 복사본에서 해당 Starter를 다시 시작하는 방법**이 가장 안전합니다.

---

# 11. Fast Track 완료 체크

3강이 끝났을 때 다음을 직접 설명할 수 있는지 확인합니다.

- [ ] Claude Code가 일반 코드 답변 도구와 어떻게 다른지 설명할 수 있다.
- [ ] 성공 조건을 SPEC으로 정리할 수 있다.
- [ ] 구현 전에 Plan을 검토해야 하는 이유를 설명할 수 있다.
- [ ] Agent의 완료 보고와 테스트 결과를 구분할 수 있다.
- [ ] `CLAUDE.md`에 둘 규칙과 SPEC에 둘 요구사항을 구분할 수 있다.
- [ ] Worker와 Reviewer의 책임을 구분할 수 있다.
- [ ] `PASS`와 `FIX_REQUIRED`를 상태로 사용할 수 있다.
- [ ] Multi-Agent가 항상 Single Agent보다 좋은 것은 아니라는 점을 설명할 수 있다.

Fast Track의 핵심 원칙은 다음 한 줄입니다.

> **Start Simple → Make It Reliable → Split When Needed → Measure → Optimize**

---

## 12. 전체 Chapter 실습으로 확장하기

Fast Track 이후에는 저장소의 Chapter 01~10 리소스를 이용해 전체 과정으로 확장할 수 있습니다.

Fast Track은 전체 과정을 대체하는 별도 코드베이스가 아닙니다. **기존 Chapter 리소스를 재사용하는 빠른 학습 경로**입니다.
