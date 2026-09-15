def search_tasks(items, keyword):
    if not keyword:
        return []

    return [task for task in items if keyword in task["title"]]
