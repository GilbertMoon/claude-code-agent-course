from __future__ import annotations

import sys
from datetime import date


VALID_PRIORITIES = {"low", "medium", "high"}
VALID_FILTERS = {"done", "pending"}

tasks = [
    {"id": 1, "title": "Claude Code 학습하기", "done": False, "due": None, "priority": "medium"},
    {"id": 2, "title": "Agent 개념 정리하기", "done": True, "due": "2026-09-20", "priority": "high"},
    {"id": 3, "title": "실습 결과 기록하기", "done": False, "due": None, "priority": "low"},
]


def print_tasks(items):
    print("=== Task Manager ===")
    if not items:
        print("등록된 Task가 없습니다.")
        return
    for task in items:
        status = "[x]" if task["done"] else "[ ]"
        due = task["due"] or "-"
        priority = task["priority"].upper()
        print(f"{status} [{priority}] {task['id']}. {task['title']} (due: {due})")


def add_task(items, title):
    clean_title = title.strip()
    if not clean_title:
        return None
    next_id = max((task["id"] for task in items), default=0) + 1
    task = {"id": next_id, "title": clean_title, "done": False, "due": None, "priority": "medium"}
    items.append(task)
    return task


def complete_task(items, task_id):
    for task in items:
        if task["id"] == task_id:
            task["done"] = True
            return True
    return False


def set_due_date(items, task_id, due_text):
    try:
        date.fromisoformat(due_text)
    except ValueError:
        return "INVALID_DATE"
    for task in items:
        if task["id"] == task_id:
            task["due"] = due_text
            return "OK"
    return "NOT_FOUND"


def set_priority(items, task_id, priority_text):
    priority = priority_text.lower()
    if priority not in VALID_PRIORITIES:
        return "INVALID_PRIORITY"
    for task in items:
        if task["id"] == task_id:
            task["priority"] = priority
            return "OK"
    return "NOT_FOUND"


def filter_tasks(items, status_text):
    status = status_text.lower()
    if status not in VALID_FILTERS:
        return None
    if status == "done":
        return [task for task in items if task["done"]]
    return [task for task in items if not task["done"]]


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
    print("  python app.py priority <task_id> <low|medium|high>")
    print("  python app.py filter <done|pending>")
    print('  python app.py search "<keyword>"')


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
        task = add_task(tasks, sys.argv[2])
        if task is None:
            print("오류: Task 제목은 비어 있을 수 없습니다.")
            return
        print(f"Task {task['id']}를 추가했습니다.")
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
    if command == "priority":
        if len(sys.argv) != 4:
            print("오류: priority 명령에는 Task ID와 우선순위가 필요합니다.")
            return
        task_id = parse_task_id(sys.argv[2])
        if task_id is None:
            print("오류: Task ID는 숫자여야 합니다.")
            return
        result = set_priority(tasks, task_id, sys.argv[3])
        if result == "INVALID_PRIORITY":
            print("오류: priority는 low, medium, high 중 하나여야 합니다.")
            return
        if result == "NOT_FOUND":
            print(f"오류: ID {task_id}인 Task를 찾을 수 없습니다.")
            return
        print(f"Task {task_id}의 priority를 {sys.argv[3].lower()}로 설정했습니다.")
        print_tasks(tasks)
        return
    if command == "filter":
        if len(sys.argv) != 3:
            print("오류: filter 명령에는 done 또는 pending 값이 필요합니다.")
            return
        filtered = filter_tasks(tasks, sys.argv[2])
        if filtered is None:
            print("오류: filter는 done 또는 pending 중 하나여야 합니다.")
            return
        print_tasks(filtered)
        return
    if command == "search":
        print("오류: search 기능은 아직 구현되지 않았습니다.")
        return
    print(f"오류: 알 수 없는 명령입니다: {command}")
    print_usage()


if __name__ == "__main__":
    main()
