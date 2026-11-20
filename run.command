#!/bin/bash
set -euo pipefail

if [[ $# -eq 0 && -t 0 ]]; then
    trap 'status=$?; read -r -p "按回车关闭窗口……" || true; exit "$status"' EXIT
fi

cd "$(dirname "$0")"

if [[ ! -x .venv/bin/python ]]; then
    if ! command -v python3 >/dev/null; then
        printf '请先安装 Python 3.9 或更新版本，再重新运行。\n' >&2
        exit 1
    fi
    printf '正在创建 Python 虚拟环境……\n'
    python3 -m venv .venv
fi

if ! .venv/bin/python -m pip show playwright >/dev/null 2>&1; then
    printf '正在安装 Playwright……\n'
    .venv/bin/python -m pip install playwright
fi

if [[ $# -eq 0 ]]; then
    if [[ -e config.local.json ]]; then
        assignments=$(.venv/bin/python -c '
import json
import sys
from pathlib import Path

config = json.loads(Path("config.local.json").read_text(encoding="utf-8"))
directory = config.get("assignments") if isinstance(config, dict) else None
if not isinstance(directory, str) or not Path(directory).is_absolute():
    sys.exit("config.local.json 中的 assignments 必须为作业目录的绝对路径。")
print(directory)
')
    else
        read -r -p '请输入 assignments 目录的绝对路径（无需引号）：' assignments
    fi
    read -r -p '请粘贴「我的实训」课程列表完整地址：' course_url
    set -- "$assignments" --course-url "$course_url"
fi

.venv/bin/python export_assignments.py "$@"
