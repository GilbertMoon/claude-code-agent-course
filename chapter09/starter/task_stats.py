from __future__ import annotations


def calculate_stats(items):
    total = len(items)
    completed = sum(1 for task in items if task["done"])
    high_priority = sum(1 for task in items if task["priority"] == "high")

    return {
        "total": total,
        "completed": completed,
        "pending": total - completed,
        "high_priority": high_priority,
    }
