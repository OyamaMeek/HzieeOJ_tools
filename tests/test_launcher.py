import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]


class LauncherTest(unittest.TestCase):
    def run_launcher(self, *args, input=""):
        launcher = ROOT / "run.command"
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


if __name__ == "__main__":
    unittest.main()
