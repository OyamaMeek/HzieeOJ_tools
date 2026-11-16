# HzieeOJ Tools

从实训管理平台读取题面，为 PyCharm 项目生成按题号命名的 Python 文件。每个新文件的开头包含题名、描述、输入输出格式和样例。

在 macOS 终端运行以下命令。需要 Python 3.9 或更新版本、已安装的 Google Chrome，以及能访问实训平台的校园网或 VPN。

```bash
git clone https://github.com/OyamaMeek/HzieeOJ_tools.git
cd HzieeOJ_tools
python3 -m venv .venv
.venv/bin/python -m pip install playwright
.venv/bin/python export_assignments.py "/path/to/py-labs/assignments" \
  --course-url 'https://training.example/dashboard/myProject?courseId=123'
```

将示例路径换为你的 `assignments` 目录，并从浏览器复制「我的实训」页完整地址填入 `--course-url`。脚本会打开独立的 Chrome 窗口。如终端提示登录，在该窗口登录后回到终端按回车。

脚本每次选择课程列表里编号最大的 U 单元，生成 `assignments/单元号-YYMMDD/题号.py`。可用 `--unit 5` 指定 U05。重跑时保留同名文件，继续生成缺少的文件。

## 测试

```bash
.venv/bin/python -m unittest discover -s tests -v
```
