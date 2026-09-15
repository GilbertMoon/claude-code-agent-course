import unittest

from review_case.search_candidate import search_tasks


class SearchCandidateTests(unittest.TestCase):
    def setUp(self):
        self.items = [
            {"id": 1, "title": "Claude Code 학습하기"},
            {"id": 2, "title": "Agent 개념 정리하기"},
            {"id": 3, "title": "실습 결과 기록하기"},
        ]

    def test_partial_match(self):
        result = search_tasks(self.items, "Agent")
        self.assertEqual([task["id"] for task in result], [2])

    def test_case_insensitive(self):
        result = search_tasks(self.items, "claude")
        self.assertEqual([task["id"] for task in result], [1])

    def test_trims_keyword(self):
        result = search_tasks(self.items, "  결과  ")
        self.assertEqual([task["id"] for task in result], [3])

    def test_blank_keyword_is_invalid(self):
        self.assertIsNone(search_tasks(self.items, "   "))


if __name__ == "__main__":
    unittest.main()
