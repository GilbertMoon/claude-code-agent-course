from __future__ import annotations

import sys


tasks = [
    {"id": 1, "title": "Claude Code 학습하기", "done": False},
    {"id": 2, "title": "Agent 개념 정리하기", "done": True},
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


def complete_task(items, task_id):
    for task in items:
        if task["id"] == task_id:
            task["done"] = True
            return True
    return False


def print_usage():
    print("사용법:")
    print("  python app.py list")
    print("  python app.py complete <task_id>")


def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1]

    if command == "list":
        print_tasks(tasks)
        return

    if command == "complete":
        if len(sys.argv) != 3:
            print("오류: complete 명령에는 Task ID가 필요합니다.")
            return

        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("오류: Task ID는 숫자여야 합니다.")
            return

        if not complete_task(tasks, task_id):
            print(f"오류: ID {task_id}인 Task를 찾을 수 없습니다.")
            return

        print(f"Task {task_id}를 완료 처리했습니다.")
        print_tasks(tasks)
        return

    print(f"오류: 알 수 없는 명령입니다: {command}")
    print_usage()


if __name__ == "__main__":
    main()
