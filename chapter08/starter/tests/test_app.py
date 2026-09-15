import unittest

import app


class TaskManagerTests(unittest.TestCase):
    def setUp(self):
        self.items = [
            {"id": 1, "title": "Claude Code 학습하기", "done": False, "due": None, "priority": "medium"},
            {"id": 2, "title": "Agent 개념 정리하기", "done": True, "due": "2026-09-20", "priority": "high"},
            {"id": 3, "title": "실습 결과 기록하기", "done": False, "due": None, "priority": "low"},
        ]

    def test_add_task(self):
        task = app.add_task(self.items, "새 작업")
        self.assertIsNotNone(task)
        self.assertEqual(task["id"], 4)
        self.assertEqual(task["priority"], "medium")

    def test_add_task_rejects_blank_title(self):
        self.assertIsNone(app.add_task(self.items, "   "))

    def test_complete_existing_task(self):
        self.assertTrue(app.complete_task(self.items, 1))
        self.assertTrue(self.items[0]["done"])

    def test_complete_missing_task(self):
        self.assertFalse(app.complete_task(self.items, 99))

    def test_set_due_date(self):
        self.assertEqual(app.set_due_date(self.items, 1, "2026-10-01"), "OK")

    def test_set_due_date_rejects_invalid_date(self):
        self.assertEqual(app.set_due_date(self.items, 1, "2026-02-30"), "INVALID_DATE")

    def test_set_due_date_missing_task(self):
        self.assertEqual(app.set_due_date(self.items, 99, "2026-10-01"), "NOT_FOUND")

    def test_set_priority(self):
        self.assertEqual(app.set_priority(self.items, 1, "high"), "OK")
        self.assertEqual(self.items[0]["priority"], "high")

    def test_set_priority_is_case_insensitive(self):
        self.assertEqual(app.set_priority(self.items, 1, "LOW"), "OK")

    def test_set_priority_rejects_invalid_value(self):
        self.assertEqual(app.set_priority(self.items, 1, "urgent"), "INVALID_PRIORITY")

    def test_set_priority_missing_task(self):
        self.assertEqual(app.set_priority(self.items, 99, "high"), "NOT_FOUND")

    def test_parse_task_id(self):
        self.assertEqual(app.parse_task_id("7"), 7)
        self.assertIsNone(app.parse_task_id("abc"))

    def test_filter_done_tasks(self):
        self.assertEqual([task["id"] for task in app.filter_tasks(self.items, "done")], [2])

    def test_filter_pending_tasks(self):
        self.assertEqual([task["id"] for task in app.filter_tasks(self.items, "pending")], [1, 3])

    def test_filter_is_case_insensitive(self):
        self.assertEqual([task["id"] for task in app.filter_tasks(self.items, "DONE")], [2])

    def test_filter_rejects_invalid_status(self):
        self.assertIsNone(app.filter_tasks(self.items, "all"))

    def test_search_matches_partial_title(self):
        self.assertEqual([task["id"] for task in app.search_tasks(self.items, "Agent")], [2])

    def test_search_is_case_insensitive(self):
        self.assertEqual([task["id"] for task in app.search_tasks(self.items, "claude")], [1])

    def test_search_trims_keyword(self):
        self.assertEqual([task["id"] for task in app.search_tasks(self.items, "  결과  ")], [3])

    def test_search_blank_keyword_is_invalid(self):
        self.assertIsNone(app.search_tasks(self.items, "   "))

    def test_search_no_match_returns_empty_list(self):
        self.assertEqual(app.search_tasks(self.items, "없는검색어"), [])


if __name__ == "__main__":
    unittest.main()
