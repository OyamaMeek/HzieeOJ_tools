import json
import shutil
import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]


class LauncherTest(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".work"
        scratch.mkdir(exist_ok=True)
        work = TemporaryDirectory(prefix="启动配置 ", dir=scratch)
        self.addCleanup(work.cleanup)
        self.work = Path(work.name)
        for name in ("run.command", "export_assignments.py"):
            shutil.copy2(ROOT / name, self.work / name)
        (self.work / ".venv").symlink_to(ROOT / ".venv", target_is_directory=True)

    def run_launcher(self, *args, input=""):
        launcher = self.work / "run.command"
        self.assertTrue(launcher.is_file(), "缺少一键启动入口 run.command")
        return subprocess.run(
            [str(launcher), *args],
            cwd=ROOT.parent,
            input=input,
            capture_output=True,
            text=True,
            timeout=30,
        )

    def test_help_from_another_working_directory(self):
        result = self.run_launcher("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--course-url", result.stdout)
        self.assertIn("--unit", result.stdout)

    def test_forwards_arguments_and_preserves_error_exit_code(self):
        (self.work / "config.local.json").write_text("{", encoding="utf-8")
        scratch = ROOT / ".work"
        scratch.mkdir(exist_ok=True)
        with TemporaryDirectory(prefix="作业 目录 ", dir=scratch) as work:
            result = self.run_launcher(
                work,
                "--course-url", "https://training.example/dashboard/myProject?courseId=123",
                "--unit", "0",
            )
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("单元号必须为正整数", result.stderr)

    def test_prompts_for_directory_and_course_url(self):
        result = self.run_launcher(input=f"{ROOT}\nhttps://training.example/\n")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("请提供包含 courseId 的课程列表地址", result.stderr)

    def test_stops_when_interactive_input_is_incomplete(self):
        result = self.run_launcher()
        self.assertNotEqual(result.returncode, 0)

    def test_reads_configured_directory_without_prompting_for_it(self):
        assignments = self.work / "不存在的 作业目录"
        (self.work / "config.local.json").write_text(
            json.dumps({"assignments": str(assignments)}, ensure_ascii=False), encoding="utf-8"
        )
        result = self.run_launcher(
            input="https://training.example/dashboard/myProject?courseId=123\n"
        )
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn(f"作业目录不存在：{assignments}", result.stderr)

    def test_rejects_invalid_configured_directory(self):
        for config in ([], {}, {"assignments": ""}, {"assignments": 7}, {"assignments": "relative"}):
            with self.subTest(config=config):
                (self.work / "config.local.json").write_text(json.dumps(config), encoding="utf-8")
                result = self.run_launcher()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("assignments 必须为作业目录的绝对路径", result.stderr)

    def test_rejects_malformed_json(self):
        (self.work / "config.local.json").write_text("{", encoding="utf-8")
        result = self.run_launcher()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("JSONDecodeError", result.stderr)


if __name__ == "__main__":
    unittest.main()
