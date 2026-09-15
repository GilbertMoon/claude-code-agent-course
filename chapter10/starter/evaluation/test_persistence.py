import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import storage


PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_PATH = PROJECT_ROOT / "app.py"


class PersistenceEvaluationTests(unittest.TestCase):
    def sample_items(self):
        return [
            {"id": 1, "title": "한글 Task", "done": False, "due": None, "priority": "medium"},
            {"id": 2, "title": "Agent 검증", "done": True, "due": "2026-09-30", "priority": "high"},
        ]

    def run_app(self, data_file, *args):
        env = os.environ.copy()
        env["TASKS_FILE"] = str(data_file)
        return subprocess.run(
            [sys.executable, str(APP_PATH), *args],
            cwd=PROJECT_ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_missing_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "missing.json"
            self.assertEqual(storage.load_tasks(path), [])

    def test_save_and_load_round_trip_preserves_unicode(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tasks.json"
            items = self.sample_items()
            storage.save_tasks(path, items)
            self.assertEqual(storage.load_tasks(path), items)
            self.assertIn("한글 Task", path.read_text(encoding="utf-8"))

    def test_corrupt_json_raises_value_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tasks.json"
            path.write_text("{broken json", encoding="utf-8")
            with self.assertRaises(ValueError):
                storage.load_tasks(path)

    def test_successful_save_leaves_no_temp_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            path = directory / "tasks.json"
            storage.save_tasks(path, self.sample_items())
            leftovers = [p for p in directory.iterdir() if p != path]
            self.assertEqual(leftovers, [])

    def test_complete_persists_across_processes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tasks.json"
            storage.save_tasks(path, self.sample_items())

            result = self.run_app(path, "complete", "1")
            self.assertEqual(result.returncode, 0)
            self.assertIn("완료 처리했습니다", result.stdout)

            second = self.run_app(path, "list")
            self.assertEqual(second.returncode, 0)
            self.assertIn("[x] [MEDIUM] 1. 한글 Task", second.stdout)

    def test_failed_mutation_does_not_change_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tasks.json"
            storage.save_tasks(path, self.sample_items())
            before = path.read_text(encoding="utf-8")

            result = self.run_app(path, "complete", "99")
            self.assertEqual(result.returncode, 0)
            self.assertIn("찾을 수 없습니다", result.stdout)
            self.assertEqual(path.read_text(encoding="utf-8"), before)

    def test_corrupt_file_is_not_overwritten_by_app(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tasks.json"
            original = "{broken json"
            path.write_text(original, encoding="utf-8")

            result = self.run_app(path, "list")
            self.assertEqual(result.returncode, 0)
            self.assertIn("오류: Task 데이터 파일을 읽을 수 없습니다.", result.stdout)
            self.assertEqual(path.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
