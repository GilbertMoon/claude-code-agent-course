import unittest

from task_stats import calculate_stats


class StatsTests(unittest.TestCase):
    def test_calculates_counts(self):
        items = [
            {"done": False, "priority": "medium"},
            {"done": True, "priority": "high"},
            {"done": False, "priority": "high"},
        ]
        self.assertEqual(
            calculate_stats(items),
            {"total": 3, "completed": 1, "pending": 2, "high_priority": 2},
        )

    def test_empty_list(self):
        self.assertEqual(
            calculate_stats([]),
            {"total": 0, "completed": 0, "pending": 0, "high_priority": 0},
        )


if __name__ == "__main__":
    unittest.main()
