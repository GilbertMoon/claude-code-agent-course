$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

function Invoke-Step {
    param(
        [string]$Name,
        [scriptblock]$Action
    )

    Write-Host ""
    Write-Host "=== $Name ==="
    & $Action
    if ($LASTEXITCODE -ne 0) {
        throw "$Name failed with exit code $LASTEXITCODE"
    }
}

function Assert-PathExists {
    param([string]$Path)
    if (-not (Test-Path $Path)) {
        throw "Required Fast Track resource is missing: $Path"
    }
    Write-Host "OK: $Path"
}

Write-Host 'Claude Code Agent Course - Fast Track Smoke Test'
Write-Host "Repository: $RepoRoot"
python --version
git --version

if (Get-Command claude -ErrorAction SilentlyContinue) {
    claude --version
} else {
    Write-Host 'INFO: Claude Code CLI is not installed in this environment.'
    Write-Host '      CI validates resource contracts only; interactive Agent recognition must be checked locally.'
}

Invoke-Step 'Fast Track required resource paths' {
    @(
        'fast-track/README.md',
        'chapter03/starter/app.py',
        'chapter03/templates/SPEC_TEMPLATE.md',
        'chapter03/templates/PLAN_REVIEW_TEMPLATE.md',
        'chapter04/starter/app.py',
        'chapter04/starter/tests/test_app.py',
        'chapter06/starter/CLAUDE.md',
        'chapter06/starter/docs/SPEC.md',
        'chapter06/starter/.claude/agents/worker.md',
        'chapter06/starter/.claude/agents/reviewer.md',
        'chapter06/starter/tests/test_app.py',
        'chapter07/starter/CLAUDE.md',
        'chapter07/starter/docs/SPEC.md',
        'chapter07/starter/.claude/agents/worker.md',
        'chapter07/starter/.claude/agents/reviewer.md',
        'chapter07/starter/tests/test_app.py',
        'chapter07/starter/review_case/search_candidate.py',
        'chapter07/starter/review_case/test_search_candidate.py'
    ) | ForEach-Object { Assert-PathExists $_ }
}

Invoke-Step 'Compile Fast Track Python resources' {
    python -m compileall -q chapter03/starter chapter04/starter chapter06/starter chapter07/starter
}

Invoke-Step 'Lecture 1 - Chapter 03 starter CLI' {
    Push-Location chapter03/starter
    try {
        python app.py list
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        python app.py complete 2
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    } finally { Pop-Location }
}

Invoke-Step 'Lecture 2A - Chapter 04 intentional Reliable Agent baseline' {
    Push-Location chapter04/starter
    try {
        @'
import unittest
suite = unittest.defaultTestLoader.discover('tests')
result = unittest.TextTestRunner(verbosity=1).run(suite)
assert result.testsRun == 7, f'expected 7 tests, got {result.testsRun}'
assert len(result.failures) == 2, f'expected 2 intentional failures, got {len(result.failures)}'
assert len(result.errors) == 0, f'expected 0 errors, got {len(result.errors)}'
print('PASS: Chapter 04 = 7 tests / 2 intentional failures / 0 errors')
'@ | python -
    } finally { Pop-Location }
}

Invoke-Step 'Lecture 2B - Chapter 06 intentional filter baseline' {
    Push-Location chapter06/starter
    try {
        @'
import unittest
suite = unittest.defaultTestLoader.discover('tests')
result = unittest.TextTestRunner(verbosity=1).run(suite)
assert result.testsRun == 16, f'expected 16 tests, got {result.testsRun}'
assert len(result.failures) == 0, f'expected 0 failures, got {len(result.failures)}'
assert len(result.errors) == 4, f'expected 4 intentional filter errors, got {len(result.errors)}'
print('PASS: Chapter 06 = 16 tests / 0 failures / 4 intentional filter errors')
'@ | python -
    } finally { Pop-Location }
}

Invoke-Step 'Lecture 3 - Chapter 07 intentional search baseline' {
    Push-Location chapter07/starter
    try {
        @'
import unittest
suite = unittest.defaultTestLoader.discover('tests')
result = unittest.TextTestRunner(verbosity=1).run(suite)
assert result.testsRun == 21, f'expected 21 tests, got {result.testsRun}'
assert len(result.failures) == 0, f'expected 0 failures, got {len(result.failures)}'
assert len(result.errors) == 5, f'expected 5 intentional search errors, got {len(result.errors)}'
print('PASS: Chapter 07 = 21 tests / 0 failures / 5 intentional search errors')
'@ | python -
    } finally { Pop-Location }
}

Invoke-Step 'Lecture 3 - review_case intentional FIX_REQUIRED baseline' {
    Push-Location chapter07/starter
    try {
        @'
import unittest
suite = unittest.defaultTestLoader.loadTestsFromName('review_case.test_search_candidate')
result = unittest.TextTestRunner(verbosity=1).run(suite)
assert result.testsRun == 4, f'expected 4 review_case tests, got {result.testsRun}'
assert len(result.failures) == 3, f'expected 3 intentional review failures, got {len(result.failures)}'
assert len(result.errors) == 0, f'expected 0 errors, got {len(result.errors)}'
print('PASS: review_case = 4 tests / 3 intentional failures / 0 errors')
'@ | python -
    } finally { Pop-Location }
}

Write-Host ""
Write-Host '========================================'
Write-Host 'FAST TRACK RESOURCE SMOKE: PASS'
Write-Host '========================================'
Write-Host 'Validated:'
Write-Host '- Lecture 1 starter CLI and templates'
Write-Host '- Lecture 2 intentional Reliable Agent and filter baselines'
Write-Host '- Lecture 3 intentional search and FIX_REQUIRED baselines'
Write-Host '- CLAUDE.md / SPEC / Worker / Reviewer resource presence'
Write-Host ''
Write-Host 'Manual local check still required:'
Write-Host '- Claude Code interactive Plan Mode behavior'
Write-Host '- @ picker / @agent-worker / @agent-reviewer runtime recognition'
