from __future__ import annotations

import re
import sys


tasks = [
    {"id": 1, "title": "Claude Code 학습하기", "done": False, "due": None},
    {"id": 2, "title": "Agent 개념 정리하기", "done": True, "due": None},
    {"id": 3, "title": "실습 결과 기록하기", "done": False, "due": None},
]


def print_tasks(items):
    print("=== Task Manager ===")

    if not items:
        print("등록된 Task가 없습니다.")
        return

    for task in items:
        status = "[x]" if task["done"] else "[ ]"
        due = task["due"] or "-"
        print(f"{status} {task['id']}. {task['title']} (due: {due})")


def add_task(items, title):
    if title == "":
        return "EMPTY_TITLE"

    next_id = max((task["id"] for task in items), default=0) + 1
    items.append({"id": next_id, "title": title, "done": False, "due": None})
    return next_id


def complete_task(items, task_id):
    for task in items:
        if task["id"] == task_id:
            task["done"] = True
            return True
    return False


def set_due_date(items, task_id, due_text):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", due_text):
        return "INVALID_DATE"

    for task in items:
        if task["id"] == task_id:
            task["due"] = due_text
            return "OK"

    return "NOT_FOUND"


def parse_task_id(value):
    try:
        return int(value)
    except ValueError:
        return None


def print_usage():
    print("사용법:")
    print("  python app.py list")
    print('  python app.py add "<title>"')
    print("  python app.py complete <task_id>")
    print("  python app.py due <task_id> <YYYY-MM-DD>")


def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1]

    if command == "list":
        print_tasks(tasks)
        return

    if command == "add":
        if len(sys.argv) != 3:
            print("오류: add 명령에는 제목이 필요합니다.")
            return

        result = add_task(tasks, sys.argv[2])
        if result == "EMPTY_TITLE":
            print("오류: Task 제목은 비워 둘 수 없습니다.")
            return

        print(f"Task {result}를 추가했습니다.")
        print_tasks(tasks)
        return

    if command == "complete":
        if len(sys.argv) != 3:
            print("오류: complete 명령에는 Task ID가 필요합니다.")
            return

        task_id = parse_task_id(sys.argv[2])
        if task_id is None:
            print("오류: Task ID는 숫자여야 합니다.")
            return

        if not complete_task(tasks, task_id):
            print(f"오류: ID {task_id}인 Task를 찾을 수 없습니다.")
            return

        print(f"Task {task_id}를 완료 처리했습니다.")
        print_tasks(tasks)
        return

    if command == "due":
        if len(sys.argv) != 4:
            print("오류: due 명령에는 Task ID와 날짜가 필요합니다.")
            return

        task_id = parse_task_id(sys.argv[2])
        if task_id is None:
            print("오류: Task ID는 숫자여야 합니다.")
            return

        result = set_due_date(tasks, task_id, sys.argv[3])
        if result == "INVALID_DATE":
            print("오류: 날짜는 YYYY-MM-DD 형식의 실제 날짜여야 합니다.")
            return
        if result == "NOT_FOUND":
            print(f"오류: ID {task_id}인 Task를 찾을 수 없습니다.")
            return

        print(f"Task {task_id}의 마감일을 {sys.argv[3]}로 설정했습니다.")
        print_tasks(tasks)
        return

    print(f"오류: 알 수 없는 명령입니다: {command}")
    print_usage()


if __name__ == "__main__":
    main()
