# Chapter 05 Starter — Task Manager

이 폴더는 Chapter 05 실습용 Starter 프로젝트입니다.

Python 표준 라이브러리만 사용합니다.

## 실행

```bash
python app.py list
python app.py add "새 작업"
python app.py complete 1
python app.py due 1 2026-10-01
```

## 테스트

```bash
python -m unittest discover -s tests -v
```

현재 Starter의 모든 테스트가 통과해야 합니다.

## 실습용 Context 파일

`chapter05/templates/CLAUDE_TEMPLATE.md`와 `CONTEXT_COMPARISON.md`를 함께 사용합니다.
