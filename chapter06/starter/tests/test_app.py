import unittest

import app


class TaskManagerTests(unittest.TestCase):
    def setUp(self):
        self.items = [
            {"id": 1, "title": "첫 번째", "done": False, "due": None, "priority": "medium"},
            {"id": 2, "title": "두 번째", "done": True, "due": "2026-09-20", "priority": "high"},
            {"id": 3, "title": "세 번째", "done": False, "due": None, "priority": "low"},
        ]

    def test_add_task(self):
        task = app.add_task(self.items, "새 작업")
        self.assertIsNotNone(task)
        self.assertEqual(task["id"], 4)
        self.assertEqual(task["title"], "새 작업")
        self.assertFalse(task["done"])
        self.assertIsNone(task["due"])
        self.assertEqual(task["priority"], "medium")

    def test_add_task_rejects_blank_title(self):
        task = app.add_task(self.items, "   ")
        self.assertIsNone(task)
        self.assertEqual(len(self.items), 3)

    def test_complete_existing_task(self):
        self.assertTrue(app.complete_task(self.items, 1))
        self.assertTrue(self.items[0]["done"])

    def test_complete_missing_task(self):
        self.assertFalse(app.complete_task(self.items, 99))

    def test_set_due_date(self):
        result = app.set_due_date(self.items, 1, "2026-10-01")
        self.assertEqual(result, "OK")
        self.assertEqual(self.items[0]["due"], "2026-10-01")

    def test_set_due_date_rejects_invalid_date(self):
        result = app.set_due_date(self.items, 1, "2026-02-30")
        self.assertEqual(result, "INVALID_DATE")

    def test_set_due_date_missing_task(self):
        result = app.set_due_date(self.items, 99, "2026-10-01")
        self.assertEqual(result, "NOT_FOUND")

    def test_set_priority(self):
        result = app.set_priority(self.items, 1, "high")
        self.assertEqual(result, "OK")
        self.assertEqual(self.items[0]["priority"], "high")

    def test_set_priority_is_case_insensitive(self):
        result = app.set_priority(self.items, 1, "LOW")
        self.assertEqual(result, "OK")
        self.assertEqual(self.items[0]["priority"], "low")

    def test_set_priority_rejects_invalid_value(self):
        result = app.set_priority(self.items, 1, "urgent")
        self.assertEqual(result, "INVALID_PRIORITY")
        self.assertEqual(self.items[0]["priority"], "medium")

    def test_set_priority_missing_task(self):
        result = app.set_priority(self.items, 99, "high")
        self.assertEqual(result, "NOT_FOUND")

    def test_parse_task_id(self):
        self.assertEqual(app.parse_task_id("7"), 7)
        self.assertIsNone(app.parse_task_id("abc"))

    def test_filter_done_tasks(self):
        result = app.filter_tasks(self.items, "done")
        self.assertEqual([task["id"] for task in result], [2])

    def test_filter_pending_tasks(self):
        result = app.filter_tasks(self.items, "pending")
        self.assertEqual([task["id"] for task in result], [1, 3])

    def test_filter_is_case_insensitive(self):
        result = app.filter_tasks(self.items, "DONE")
        self.assertEqual([task["id"] for task in result], [2])

    def test_filter_rejects_invalid_status(self):
        self.assertIsNone(app.filter_tasks(self.items, "all"))


if __name__ == "__main__":
    unittest.main()
