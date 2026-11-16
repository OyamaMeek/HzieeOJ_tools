import ast
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from export_assignments import parse_course_url, select_unit, write_problem


class ExportAssignmentsTest(unittest.TestCase):
    def test_accepts_course_url(self):
        url = "https://training.example/dashboard/myProject?courseId=123"
        self.assertEqual(parse_course_url(url).geturl(), url)

    def test_rejects_invalid_course_url_before_launching_browser(self):
        result = subprocess.run(
            [sys.executable, "export_assignments.py", ".", "--course-url", "https://training.example/"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("请提供包含 courseId 的课程列表地址", result.stderr)

    def test_selects_latest_unit_or_explicit_unit(self):
        titles = [
            "U10_单元十",
            "U01-单元一",
            "U03 - 单元三",
        ]
        self.assertEqual(select_unit(titles, None), (10, "U10_单元十"))
        self.assertEqual(select_unit(titles, 3), (3, "U03 - 单元三"))
        with self.assertRaisesRegex(ValueError, "U06"):
            select_unit(titles, 6)
        with self.assertRaisesRegex(ValueError, "没有.*单元"):
            select_unit([], None)

    def test_writes_problem_comment_and_preserves_existing_file(self):
        title = "整数求和"
        body = "描述：求两个整数的和。\n\n样例输入：\n1\n2\n样例输出：\n3"
        scratch = Path(__file__).resolve().parents[1] / ".work"
        scratch.mkdir(exist_ok=True)
        with TemporaryDirectory(dir=scratch) as work:
            target = Path(work) / "5-270101" / "1.py"
            self.assertTrue(write_problem(target, title, body))
            contents = target.read_text(encoding="utf-8")
            self.assertEqual(
                contents,
                "# 整数求和\n# 描述：求两个整数的和。\n#\n# 样例输入：\n# 1\n# 2\n# 样例输出：\n# 3\n",
            )
            self.assertEqual(ast.parse(contents).body, [])

            edited = contents + "\nanswer = 30\n"
            target.write_text(edited, encoding="utf-8")
            self.assertFalse(write_problem(target, title, body))
            self.assertEqual(target.read_text(encoding="utf-8"), edited)
