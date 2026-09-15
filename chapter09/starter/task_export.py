from __future__ import annotations

import csv
import io


FIELDS = ("id", "title", "done", "due", "priority")


def tasks_to_csv(items):
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()

    for task in items:
        writer.writerow(
            {
                "id": task["id"],
                "title": task["title"],
                "done": "true" if task["done"] else "false",
                "due": task["due"] or "",
                "priority": task["priority"],
            }
        )

    return buffer.getvalue()
