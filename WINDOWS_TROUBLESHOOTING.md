# Windows Troubleshooting

이 문서는 Windows + PowerShell 환경에서 실습 중 환경 문제가 발생했을 때 사용하는 보조 자료입니다.

정상 동작하는 환경에서는 아래 설정을 미리 적용할 필요가 없습니다.

## 한글 출력이 깨지는 경우

먼저 현재 코드 페이지를 확인합니다.

```powershell
chcp
```

필요한 경우 현재 터미널 세션만 UTF-8 코드 페이지로 변경합니다.

```powershell
chcp 65001
```

Python 실행에서 UTF-8 모드가 필요한 환경이라면 현재 PowerShell 세션에서 다음을 사용할 수 있습니다.

```powershell
$env:PYTHONUTF8 = "1"
```

그 다음 문제가 발생한 명령을 다시 실행합니다.

중요:

- `chcp 65001`은 모든 환경의 필수 설정이 아닙니다.
- 정상 출력되는 환경은 변경하지 않습니다.
- 코드 자체 문제인지 터미널 표시 문제인지 먼저 구분합니다.

## Python 경로 확인

```powershell
python --version
Get-Command python
```

## Claude Code 경로 확인

```powershell
claude --version
Get-Command claude
```

## Git 상태 확인

강제 초기화 전에 먼저 다음을 확인합니다.

```powershell
git status
git diff
git branch --show-current
```

교육용 실패 실험 뒤에는 이번 실험에서 만든 변경만 원복합니다.

다음 명령은 개인 작업까지 지울 수 있으므로 이유를 모르는 상태에서 사용하지 않습니다.

```text
git reset --hard
git clean -fd
git restore .
```
