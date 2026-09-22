# Claude Code Agent Course Resources

이 저장소는 Claude Code Agent 강의를 위한 **공개 실습 리소스 저장소**입니다.

강의안, 블로그 원고, 도서 원고는 이 저장소에 공개하지 않습니다.

이 저장소에는 다음과 같은 실습용 자료만 제공합니다.

- Starter 코드
- 실습용 샘플 프로젝트
- 템플릿
- 샘플 데이터
- 테스트 파일
- 공개 가능한 Agent 설정 예제
- 블로그 및 실습에서 사용하는 이미지/다이어그램

각 Chapter의 강의 내용은 별도의 블로그 또는 실제 수업에서 제공하며, 이 저장소에서는 실습에 필요한 파일만 내려받아 사용합니다.

## 3강 Fast Track

Chapter 01~10 전체 과정 전에 핵심 Agent Workflow를 빠르게 실습하려면 다음 학생용 진입 안내를 사용합니다.

- [`fast-track/README.md`](fast-track/README.md)

Fast Track은 별도의 코드를 복제하지 않고 기존 Chapter 리소스를 다음 순서로 재사용합니다.

```text
1강  chapter03
 ↓
2강  chapter04 → chapter06
 ↓
3강  chapter07
```

핵심 흐름은 다음과 같습니다.

```text
Single Agent
→ Reliable Agent
→ Multi-Agent Workflow
```

## Starter와 테스트 안내

일부 Chapter의 Starter는 학습 목표를 위해 **의도적으로 미완성 기능이나 실패 테스트를 포함**합니다.

예를 들어 학생이 문제를 발견하고 Agent를 이용해 해결하는 과정을 실습하도록 초기 실패 상태 자체가 교육 계약의 일부일 수 있습니다.

따라서 개별 Starter에서 테스트가 실패한다고 해서 저장소가 항상 잘못된 상태라는 뜻은 아닙니다.

저장소 전체 리소스의 기준 상태는 다음 Windows GitHub Actions Workflow가 자동 검증합니다.

```text
.github/workflows/resource-smoke.yml
```

이 Workflow는 정상 Chapter의 PASS뿐 아니라 각 Chapter에 정의된 **의도된 초기 실패 개수와 미구현 상태**도 함께 확인합니다.

## Windows에서 Baseline 한 번에 확인

저장소 루트에서 다음 스크립트를 실행하면 GitHub Actions와 같은 Baseline 검증을 로컬에서 한 번에 수행할 수 있습니다.

```powershell
.\scripts\run-baseline-smoke.ps1
```

스크립트는 Python UTF-8 출력을 활성화하고 Chapter 01~10의 문법, 기본 CLI, 회귀 테스트, 의도된 실패 계약을 비파괴 방식으로 확인합니다.

Claude Code의 Plan Mode, Custom Sub-agent, Worktree, Agent Teams 같은 기능은 이 Baseline 스크립트의 대상이 아니며 실제 Claude Code 환경에서 별도로 확인합니다.
