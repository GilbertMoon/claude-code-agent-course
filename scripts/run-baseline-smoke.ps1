$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'

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

Write-Host "Claude Code Agent Course - Windows Baseline Smoke"
Write-Host "Repository: $RepoRoot"
python --version
git --version

Invoke-Step 'Compile Chapter 01-10 starter Python' {
    1..10 | ForEach-Object {
        $chapter = 'chapter{0:D2}/starter' -f $_
        python -m compileall -q $chapter
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }
}

Invoke-Step 'Chapter 01 baseline' {
    Push-Location chapter01/starter
    try { python app.py } finally { Pop-Location }
}

Invoke-Step 'Chapter 02 baseline' {
    Push-Location chapter02/starter
    try { python app.py list } finally { Pop-Location }
}

Invoke-Step 'Chapter 03 baseline' {
    Push-Location chapter03/starter
    try {
        python app.py list
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        python app.py complete 2
    } finally { Pop-Location }
}

Invoke-Step 'Chapter 04 intentional baseline' {
    Push-Location chapter04/starter
    try {
        @'
import unittest
suite = unittest.defaultTestLoader.discover('tests')
result = unittest.TextTestRunner(verbosity=1).run(suite)
issues = len(result.failures) + len(result.errors)
assert result.testsRun == 7, f'expected 7 tests, got {result.testsRun}'
assert issues == 2, f'expected exactly 2 intentional issues, got {issues}'
print('PASS: 7 tests with exactly 2 intentional issues')
'@ | python -
    } finally { Pop-Location }
}

Invoke-Step 'Chapter 05 regression' {
    Push-Location chapter05/starter
    try { python -m unittest discover -s tests -v } finally { Pop-Location }
}

Invoke-Step 'Chapter 06 intentional filter baseline' {
    Push-Location chapter06/starter
    try {
        @'
import unittest
suite = unittest.defaultTestLoader.discover('tests')
result = unittest.TextTestRunner(verbosity=1).run(suite)
issues = len(result.failures) + len(result.errors)
assert result.testsRun == 16, f'expected 16 tests, got {result.testsRun}'
assert issues == 4, f'expected exactly 4 intentional filter issues, got {issues}'
print('PASS: 16 tests with exactly 4 intentional filter issues')
'@ | python -
    } finally { Pop-Location }
}

Invoke-Step 'Chapter 07 intentional search baseline' {
    Push-Location chapter07/starter
    try {
        @'
import unittest
suite = unittest.defaultTestLoader.discover('tests')
result = unittest.TextTestRunner(verbosity=1).run(suite)
issues = len(result.failures) + len(result.errors)
assert result.testsRun == 21, f'expected 21 tests, got {result.testsRun}'
assert issues == 5, f'expected exactly 5 intentional search issues, got {issues}'
print('PASS: 21 tests with exactly 5 intentional search issues')
'@ | python -
    } finally { Pop-Location }
}

Invoke-Step 'Chapter 08 regression' {
    Push-Location chapter08/starter
    try { python -m unittest tests.test_app -v } finally { Pop-Location }
}

Invoke-Step 'Chapter 09 regression' {
    Push-Location chapter09/starter
    try { python -m unittest tests.test_app -v } finally { Pop-Location }
}

Invoke-Step 'Chapter 10 regression' {
    Push-Location chapter10/starter
    try { python -m unittest tests.test_app -v } finally { Pop-Location }
}

Invoke-Step 'Chapter 10 intentional persistence baseline' {
    Push-Location chapter10/starter
    try {
        @'
import unittest
suite = unittest.defaultTestLoader.loadTestsFromName('evaluation.test_persistence')
result = unittest.TextTestRunner(verbosity=1).run(suite)
issues = len(result.failures) + len(result.errors)
assert result.testsRun == 7, f'expected 7 tests, got {result.testsRun}'
assert issues > 0, 'persistence starter unexpectedly passes all evaluation tests'
print(f'PASS: 7 persistence tests with {issues} expected starter issues')
'@ | python -
    } finally { Pop-Location }
}

Write-Host ""
Write-Host '========================================'
Write-Host 'BASELINE SMOKE: PASS'
Write-Host '========================================'
Write-Host 'Next: run only Claude-specific smoke checks from the PRIVATE guide.'
