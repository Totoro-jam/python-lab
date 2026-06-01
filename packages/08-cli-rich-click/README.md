# 08 - CLI: typer + rich

> 把 Python 脚本变成体验好的命令行工具。学完能产出带子命令、自动补全、漂亮输出、进度条的 CLI。

## 前置

- [01-fundamentals](../01-fundamentals), [03-typing-dataclass](../03-typing-dataclass)

## 本章目标

- `typer`：基于类型注解的 CLI（FastAPI 同作者）
- `click`：底层装饰器风格（typer 基于此）
- `rich`：表格、面板、语法高亮、进度条、Markdown 渲染
- 多命令、子命令、option 默认值与 callback
- shell 自动补全（bash/zsh/fish）

## 推荐库

- `typer`（首选）、`click`、`rich`、`questionary`（交互问答）

## 计划要写

- `src/`: 一个文件同步工具 CLI（`sync push/pull`），带进度条
- `tests/`: `typer.testing.CliRunner`

## 自测

- `typer` 比 `argparse` 强在哪？
- `rich.Progress` 和 tqdm 谁更现代？
- click 的 `@click.pass_context` 在干啥？

---

**TODO**: 待补充完整代码与测试。
