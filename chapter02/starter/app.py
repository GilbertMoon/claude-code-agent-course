from __future__ import annotations

import sys


tasks = [
    {"id": 1, "title": "Claude Code 학습하기", "done": False},
    {"id": 2, "title": "Agent 개념 정리하기", "done": False},
    {"id": 3, "title": "실습 결과 기록하기", "done": False},
]


def print_tasks(items):
    print("=== Task Manager ===")

    if not items:
        print("등록된 Task가 없습니다.")
        return

    for task in items:
        status = "[x]" if task["done"] else "[ ]"
        print(f"{status} {task['id']}. {task['title']}")


def print_usage():
    print("사용법:")
    print("  python app.py list")


def main():
    args = sys.argv[1:]

    if not args or args[0] == "list":
        print_tasks(tasks)
        return

    print(f"지원하지 않는 명령입니다: {args[0]}")
    print_usage()


if __name__ == "__main__":
    main()
