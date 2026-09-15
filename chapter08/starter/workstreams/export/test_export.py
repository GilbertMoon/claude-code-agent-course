import csv
import io
import unittest

from task_export import tasks_to_csv


class ExportTests(unittest.TestCase):
    def test_exports_header_and_rows(self):
        items = [
            {"id": 1, "title": "A, B", "done": False, "due": None, "priority": "medium"},
            {"id": 2, "title": "완료", "done": True, "due": "2026-09-20", "priority": "high"},
        ]
        rows = list(csv.DictReader(io.StringIO(tasks_to_csv(items))))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["title"], "A, B")
        self.assertEqual(rows[0]["done"], "false")
        self.assertEqual(rows[0]["due"], "")
        self.assertEqual(rows[1]["done"], "true")
        self.assertEqual(rows[1]["priority"], "high")

    def test_empty_list_exports_header_only(self):
        rows = list(csv.DictReader(io.StringIO(tasks_to_csv([]))))
        self.assertEqual(rows, [])


if __name__ == "__main__":
    unittest.main()
