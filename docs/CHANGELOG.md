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

- **Git 提交**：当前工具目录无 Git 仓库。目标公开仓库为空，等待许可证及发布确认。

---

## [2026-11-16 17:53] 发布首个版本

- **需求/问题描述**
  > 配置 GitHub 远端并推送工具。

- **实际实现的功能与改动**
  - 初始化 `main` 分支，将 `origin` 设为 `https://github.com/OyamaMeek/HzieeOJ_tools.git`。
  - 四项本地测试通过，命令帮助正常。

- **涉及文件**
  - `.gitignore`、`README.md`、`export_assignments.py`、`tests/test_export_assignments.py`、`docs/CHANGELOG.md`

- **Git 提交**：待提交。
