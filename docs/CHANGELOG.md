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

---

## [2026-11-16 22:32] 按现有脚本重新排版本地 U05

- **需求/问题描述**：
  > 根据现有脚本重新排版本地作业。

- **实际实现的功能与改动**：
  - 调整本地 U05 的 10 个题目文件，统一使用 `# ` 注释前缀、省略空白注释，并按每行至多 35 个字符换行。
  - 原文件已保存到工具工作区的 `.work/u05-original/`。保留题面字符及作业仓库原有暂存和未跟踪状态。
  - 10 个文件均与现有 `write_problem` 输出逐字一致，题面字符及 AST 比对通过，5 项 unittest 全部通过；未访问线上课程，未执行题目程序。

- **涉及文件**：
  - 本地作业目录 `assignments/5-261116/1.py` 至 `10.py`
  - 工具仓库 `docs/CHANGELOG.md`；本地忽略目录 `.work/`、`memory/`

- **Git 提交**：`cdb664b docs: record local U05 comment reformatting`。本地作业文件保留在原工作区，未纳入工具仓库。

---

## [2026-11-20 22:03] 新增 macOS 一键启动脚本

- **需求/问题描述**：
  > 做一个一键脚本。

- **实际实现的功能与改动**：
  - 新增可双击的 `run.command`，按需创建虚拟环境、安装 Playwright，提示输入作业目录和课程地址后调用现有导出器，也可传入原有 CLI 参数。
  - 交互终端运行结束后等待回车，保留错误退出码；更新 README 的一键运行说明。
  - 4 项新增测试先确认缺少入口时失败，实现后 9 项 unittest、Shell 语法及 diff 检查通过。真实 TTY 验证错误显示、回车关闭和退出码 2。
  - 在含空格的全新目录中实际创建虚拟环境、安装 Playwright 1.60.0，并成功运行命令帮助，退出码为 0。未验证 Finder 双击或在线课程导出。

- **涉及文件**：
  - `run.command`、`tests/test_launcher.py`、`README.md`、`docs/CHANGELOG.md`；本地忽略目录 `memory/`、`.work/`。

- **Git 提交**：`a2f4cf3 feat: add one-click macOS launcher`，已普通推送至 `origin/main`。

---

## [2026-11-20 22:14] 从本地 JSON 配置读取作业目录

- **需求/问题描述**：
  > 将作业目录保存在本地 JSON 配置文件中。

- **实际实现的功能与改动**：
  - 无参数启动时读取 `config.local.json` 的 `assignments` 字段，通过 Python 标准库解析 JSON 并校验目录字段；缺少配置文件时继续提示输入目录，CLI 参数仍可直接指定目录。
  - 本地配置填入已确认存在的作业目录并加入 Git 忽略规则，README 说明配置格式和运行方式。
  - 新增测试先复现缺少 JSON 配置读取的行为，再实现读取；12 项 unittest 全部通过，覆盖含空格路径、无效 JSON、缺失或错误类型字段、相对路径及 CLI 参数优先。Shell 语法、diff 检查与 Git 忽略规则验证通过。未复测在线导出。

- **涉及文件**：
  - `run.command`、`tests/test_launcher.py`、`.gitignore`、`README.md`、`docs/CHANGELOG.md`。
  - 本地忽略文件 `config.local.json`，以及本地记录 `memory/`。

- **Git 提交**：待提交。
