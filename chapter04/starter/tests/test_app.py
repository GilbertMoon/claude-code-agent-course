import unittest

from app import add_task, set_due_date


class TaskValidationTests(unittest.TestCase):
    def setUp(self):
        self.items = [
            {"id": 1, "title": "기존 Task", "done": False, "due": None},
        ]

    def test_add_valid_title(self):
        result = add_task(self.items, "새 Task")
        self.assertEqual(result, 2)
        self.assertEqual(self.items[-1]["title"], "새 Task")

    def test_add_empty_title_is_rejected(self):
        result = add_task(self.items, "")
        self.assertEqual(result, "EMPTY_TITLE")
        self.assertEqual(len(self.items), 1)

    def test_add_whitespace_only_title_is_rejected(self):
        result = add_task(self.items, "   ")
        self.assertEqual(result, "EMPTY_TITLE")
        self.assertEqual(len(self.items), 1)

    def test_valid_due_date_is_accepted(self):
        result = set_due_date(self.items, 1, "2026-09-30")
        self.assertEqual(result, "OK")
        self.assertEqual(self.items[0]["due"], "2026-09-30")

    def test_invalid_date_format_is_rejected(self):
        result = set_due_date(self.items, 1, "2026/09/30")
        self.assertEqual(result, "INVALID_DATE")
        self.assertIsNone(self.items[0]["due"])

    def test_nonexistent_calendar_date_is_rejected(self):
        result = set_due_date(self.items, 1, "2026-02-30")
        self.assertEqual(result, "INVALID_DATE")
        self.assertIsNone(self.items[0]["due"])

    def test_due_date_for_unknown_id_is_rejected(self):
        result = set_due_date(self.items, 99, "2026-09-30")
        self.assertEqual(result, "NOT_FOUND")


if __name__ == "__main__":
    unittest.main()
