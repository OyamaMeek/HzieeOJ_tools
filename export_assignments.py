import argparse
import re
from datetime import date
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from playwright.sync_api import Error, TimeoutError, expect, sync_playwright


UNIT_TITLE = re.compile(r"^U([0-9]+)")


def parse_course_url(value):
    try:
        url = urlsplit(value)
        if (
            url.scheme in ("http", "https")
            and url.hostname
            and url.username is None
            and url.port != 0
            and url.path == "/dashboard/myProject"
            and parse_qs(url.query).get("courseId")
        ):
            return url
    except ValueError:
        pass
    raise argparse.ArgumentTypeError("请提供包含 courseId 的课程列表地址")


def write_problem(target, title, body):
    lines = [
        f"# {line[start:start + 33]}"
        for line in [title, *body.splitlines()]
        if line.strip()
        for start in range(0, len(line), 33)
    ]
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        output = target.open("x", encoding="utf-8")
    except FileExistsError:
        return False
    try:
        with output:
            output.write("\n".join(lines) + "\n")
    except OSError:
        target.unlink()
        raise
    return True


def select_unit(titles, requested):
    units = {}
    for title in titles:
        title = title.strip()
        match = UNIT_TITLE.match(title)
        if match:
            units[int(match[1])] = title
    if not units:
        raise ValueError("课程列表没有可读取的 U 单元")
    unit = max(units) if requested is None else requested
    if unit not in units:
        raise ValueError(f"课程列表中没有 U{unit:02d}")
    return unit, units[unit]


def export_unit(page, course_url, requested, assignments):
    origin = course_url._replace(path="", query="", fragment="").geturl()
    detail_url = re.compile(rf"^{re.escape(origin)}/taskDetail(?:[?#]|$)", re.IGNORECASE)
    unit_titles = page.get_by_text(UNIT_TITLE)
    page.goto(course_url.geturl(), wait_until="domcontentloaded")
    try:
        unit_titles.first.wait_for(timeout=5000)
    except TimeoutError:
        input("请在打开的 Chrome 中登录，并确认课程可以访问。完成后按回车继续：")
        page.goto(course_url.geturl(), wait_until="domcontentloaded")
        unit_titles.first.wait_for()

    unit, unit_name = select_unit(unit_titles.all_inner_texts(), requested)
    destination = assignments / f"{unit}-{date.today():%y%m%d}"
    print(f"正在导出 {unit_name}", flush=True)
    unit_title = page.get_by_text(unit_name, exact=True)
    card = unit_title.locator("xpath=ancestor::div[.//tr][1]")
    rows = []
    for row in card.locator("tr:has(> td)").all():
        cells = row.locator("td")
        number = cells.nth(0).inner_text().strip()
        if re.fullmatch(r"[1-9][0-9]*", number):
            title = cells.nth(1).inner_text().strip()
            rows.append((int(number), title, row))
    if not rows or [number for number, _, _ in rows] != list(range(1, len(rows) + 1)):
        raise ValueError(f"U{unit:02d} 的题目序号缺失或不连续")

    created = 0
    for number, title, row in rows:
        target = destination / f"{number}.py"
        if target.is_file():
            print(f"已保留 {target.name}  {title}", flush=True)
            continue

        print(f"正在读取第 {number} 题  {title}", flush=True)
        action = row.locator("a").filter(has_text=re.compile(r"^\s*(开始任务|查看)\s*$"))
        with page.expect_popup() as popup_event:
            action.click()
        popup = popup_event.value
        try:
            popup.wait_for_url(detail_url)
            popup.get_by_text(title, exact=True).wait_for()
            body = popup.locator('[id^="w-e-textarea-"][contenteditable="false"]')
            expect(body).to_have_text(re.compile(r"\S"), use_inner_text=True, timeout=15000)
            saved = write_problem(target, title, body.inner_text().strip("\r\n"))
        finally:
            popup.close()

        created += saved
        print(f"{'已生成' if saved else '已保留'} {target.name}", flush=True)
    print(f"共 {len(rows)} 题，新增 {created} 个，保留 {len(rows) - created} 个。目录：{destination}")


def main():
    parser = argparse.ArgumentParser(description="将实训题面导出为 Python 文件头注释")
    parser.add_argument("assignments", type=Path, help="PyCharm 项目的 assignments 目录")
    parser.add_argument("--course-url", required=True, type=parse_course_url, help="实训平台的「我的实训」课程列表地址")
    parser.add_argument("--unit", type=int, help="指定实训单元号，默认读取编号最大的 U 单元")
    args = parser.parse_args()
    if args.unit is not None and args.unit < 1:
        parser.error("单元号必须为正整数")
    if not args.assignments.is_dir():
        parser.error(f"作业目录不存在：{args.assignments}")

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(channel="chrome", headless=False)
            try:
                export_unit(browser.new_page(), args.course_url, args.unit, args.assignments.resolve())
            finally:
                browser.close()
    except (Error, OSError, ValueError, EOFError) as error:
        parser.exit(1, f"导出中止：{error}\n")


if __name__ == "__main__":
    main()
