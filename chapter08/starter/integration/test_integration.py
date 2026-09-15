import subprocess
import sys
import unittest


class IntegrationTests(unittest.TestCase):
    def run_app(self, *args):
        return subprocess.run(
            [sys.executable, "app.py", *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_stats_command(self):
        result = self.run_app("stats")
        self.assertEqual(result.returncode, 0)
        self.assertIn("total: 3", result.stdout)
        self.assertIn("completed: 1", result.stdout)
        self.assertIn("pending: 2", result.stdout)
        self.assertIn("high_priority: 1", result.stdout)

    def test_export_command(self):
        result = self.run_app("export")
        self.assertEqual(result.returncode, 0)
        self.assertTrue(result.stdout.startswith("id,title,done,due,priority\n"))
        self.assertIn("Claude Code 학습하기", result.stdout)
        self.assertIn("true,2026-09-20,high", result.stdout)


if __name__ == "__main__":
    unittest.main()
