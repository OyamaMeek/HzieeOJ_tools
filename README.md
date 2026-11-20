# HzieeOJ Tools

从实训管理平台读取题面，为 PyCharm 项目生成按题号命名的 Python 文件。每个新文件的开头包含题名、描述、输入输出格式和样例。

需要 macOS、Python 3.9 或更新版本、已安装的 Google Chrome，以及能访问实训平台的校园网或 VPN。

## 一键运行

在项目根目录创建本地配置文件 `config.local.json`，在 `assignments` 字段填写已有作业目录的绝对路径，例如：

```json
{
  "assignments": "/path/to/py-labs/assignments"
}
```

双击 `run.command`，脚本会读取配置中的作业目录，再提示输入「我的实训」页完整地址。没有配置文件时，会提示输入作业目录。修改作业位置时，直接编辑 `config.local.json`；该文件已加入 Git 忽略规则。配置格式错误或目录无效时会报错并停止。

脚本会自动创建虚拟环境、安装 Playwright 并开始导出；首次安装依赖需要联网。运行结束后按回车关闭窗口。

也可以在终端克隆并运行：

```bash
git clone https://github.com/OyamaMeek/HzieeOJ_tools.git
cd HzieeOJ_tools
./run.command
```

在终端指定参数时，直接传给 `run.command`，此时使用参数中的作业目录：

```bash
./run.command "/path/to/py-labs/assignments" \
  --course-url 'https://training.example/dashboard/myProject?courseId=123'
```

将示例路径换为你的 `assignments` 目录，并从浏览器复制「我的实训」页完整地址填入 `--course-url`。脚本会打开独立的 Chrome 窗口。如终端提示登录，在该窗口登录后回到终端按回车。

脚本每次选择课程列表里编号最大的 U 单元，生成 `assignments/单元号-YYMMDD/题号.py`。可用 `--unit 5` 指定 U05。重跑时保留同名文件，继续生成缺少的文件。

生成的标题和题面注释每行最多 35 个字符（包含 `# ` 前缀），超出时自动换行。中文、英文、空格均按单个字符计数，保留原有缩进和换行，省略空白行。

## 测试

```bash
.venv/bin/python -m unittest discover -s tests -v
```
