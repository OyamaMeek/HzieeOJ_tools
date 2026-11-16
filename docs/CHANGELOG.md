# 开发记录

## [2026-11-16 17:28] 导出实训题面为 Python 注释

- **需求/问题描述**
  > 获取实训单元的各道题面，在 PyCharm 作业目录下按当天日期创建子目录，将题面写在题号对应的 Python 文件开头。

- **实际实现的功能与改动**
  - 使用本机 Chrome 打开实训课程，默认按 U05 的题号读取题面，逐行添加 Python 注释，保留同名文件。
  - 通过 Python 3.9.6 验证第 1 题的题面格式、样例换行、已有文件保护、命令帮助及单元号校验。
  - 当前直接访问平台超时，浏览器已加载页面可确认题目列表与第 1 题。在线批量导出未验证。

- **涉及文件**
  - `export_assignments.py`
  - `tests/test_export_assignments.py`
  - `README.md`、`.gitignore`、`memory/`、`docs/CHANGELOG.md`

- **Git 提交**：当前工具目录无 Git 仓库，无法提交或推送。

---

## [2026-11-16 17:42] 默认读取最新 U 单元

- **需求/问题描述**
  > 每次运行时读取最新的 U 单元。

- **实际实现的功能与改动**
  - 从课程列表按数字选择编号最大的 U 单元，可用 `--unit` 指定单元。输出目录使用实际选中的编号和当天日期。
  - 两项本地测试通过，覆盖页面顺序变化、显式指定、单元缺失、题面注释格式和同名文件保护。命令帮助与无效单元号检查通过。在线导出未复测。

- **涉及文件**
  - `export_assignments.py`、`tests/test_export_assignments.py`、`README.md`、`memory/`、`docs/CHANGELOG.md`

- **Git 提交**：当前工具目录无 Git 仓库，无法提交或推送。

---

## [2026-11-16 17:51] 准备 GitHub 开源

- **需求/问题描述**
  > 准备将实训题面导出工具公开到 GitHub。

- **实际实现的功能与改动**
  - 通过 `--course-url` 传入课程地址，详情页地址按课程所在站点匹配。公开示例与测试使用自编内容。
  - 更新 README 的安装、运行和测试说明，忽略本地作业、开发记录、虚拟环境和临时文件。
  - 四项本地测试通过，命令帮助正常，公开文件未检出原校内地址、实际课程编号、作业题面或本机绝对路径。未复测在线导出。

- **涉及文件**
  - `export_assignments.py`、`tests/test_export_assignments.py`、`README.md`、`.gitignore`、`docs/CHANGELOG.md`、`memory/`

- **Git 提交**：`2a1e79f feat: publish HzieeOJ assignment exporter`。

---

## [2026-11-16 17:53] 发布首个版本

- **需求/问题描述**
  > 配置 GitHub 远端并推送工具。

- **实际实现的功能与改动**
  - 初始化 `main` 分支，将 `origin` 设为 `https://github.com/OyamaMeek/HzieeOJ_tools.git`。
  - 四项本地测试通过，命令帮助正常。
  - 首个提交已推送至 `origin/main`，并设置上游跟踪。

- **涉及文件**
  - `.gitignore`、`README.md`、`export_assignments.py`、`tests/test_export_assignments.py`、`docs/CHANGELOG.md`

- **Git 提交**：`2a1e79f feat: publish HzieeOJ assignment exporter`。

---

## [2026-11-16 18:09] 导出题面时省略空行

- **需求/问题描述**
  > 自动去除题面导出时产生的空白注释行。

- **实际实现的功能与改动**
  - 跳过题面中的空行和仅含空白字符的行，保留有内容的行及其原始缩进。
  - 用回归测试复现多余注释，修复后四项本地测试通过。

- **涉及文件**
  - `export_assignments.py`、`tests/test_export_assignments.py`、`docs/CHANGELOG.md`

- **Git 提交**：`64ee463 fix: omit blank lines from exported problems`。

---

## [2026-11-16 22:27] 题面注释每行最多 35 个字符

- **需求/问题描述**：
  > 一行最多 35 个字符，超过后自动换行。

- **实际实现的功能与改动**：
  - 标题和题面按每段 33 个字符切分，加上 `# ` 前缀后每行最多 35 个字符。保留原有字符、缩进和换行，继续跳过空白行并保护已有文件。
  - 新增回归测试，先确认旧实现失败，修复后五项 unittest 全部通过；命令帮助和 `git diff --check` 通过。未复测在线导出。

- **涉及文件**：
  - `export_assignments.py` (+6 / -2)
  - `tests/test_export_assignments.py` (+18 / -0)
  - `README.md` (+2 / -0)、`docs/CHANGELOG.md`

- **Git 提交**：`f5ba579 fix: wrap exported comments at 35 characters`。用户确认后已推送至 `origin/main`，并核对远端提交与本地一致。
