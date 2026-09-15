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
        print(f"{task['id']}. {task['title']}")


def main():
    print_tasks(tasks)


if __name__ == "__main__":
    main()
