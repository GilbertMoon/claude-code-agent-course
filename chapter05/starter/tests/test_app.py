import unittest

import app


class TaskManagerTests(unittest.TestCase):
    def setUp(self):
        self.items = [
            {"id": 1, "title": "첫 번째", "done": False, "due": None},
            {"id": 2, "title": "두 번째", "done": True, "due": "2026-09-20"},
        ]

    def test_add_task(self):
        task = app.add_task(self.items, "새 작업")
        self.assertIsNotNone(task)
        self.assertEqual(task["id"], 3)
        self.assertEqual(task["title"], "새 작업")
        self.assertFalse(task["done"])
        self.assertIsNone(task["due"])

    def test_add_task_rejects_blank_title(self):
        task = app.add_task(self.items, "   ")
        self.assertIsNone(task)
        self.assertEqual(len(self.items), 2)

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

    def test_parse_task_id(self):
        self.assertEqual(app.parse_task_id("7"), 7)
        self.assertIsNone(app.parse_task_id("abc"))


if __name__ == "__main__":
    unittest.main()
