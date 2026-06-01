# python-lab

Python 通识实验场。学完后能看懂 95% 的现代 Python 代码、能维护它们、能用主流库搭出生产可用的脚手架。

## 这个仓库不是什么

- 不是某个库的官方文档替代（要查细节直接看 docs.python.org / fastapi.tiangolo.com 更全）
- 不是"7 天精通 Python"那种速成
- 不会回避"为什么这样设计"——理解 why 才能维护

## 这个仓库是什么

- **可跑代码 + 解释 why 的双轨**。每章一个独立包，自带 `pyproject.toml`、源码、测试，直接 `uv sync && uv run pytest` 就跑
- **围绕最流行的库组织**：typing、pytest、httpx、fastapi、numpy/pandas、sqlalchemy、rich/typer……每章选当下生态中"事实标准"的那一个
- **工程化基线**：不只是会写 `print()`，还知道 ruff / uv / pyproject.toml / type checker 在生产里怎么配

## 学习路径

| 章节 | 主题 | 主要库 | 难度 |
|---|---|---|---|
| [01-fundamentals](packages/01-fundamentals) | 语法、控制流、函数、模块 | stdlib | ⭐ |
| [02-data-structures](packages/02-data-structures) | list/dict/set/tuple + collections + itertools + functools | stdlib | ⭐⭐ |
| [03-typing-dataclass](packages/03-typing-dataclass) | typing、dataclass、Protocol、TypedDict、pydantic | typing, dataclasses, pydantic | ⭐⭐ |
| [04-io-paths](packages/04-io-paths) | pathlib、json、csv、configparser、logging | stdlib | ⭐⭐ |
| [05-async](packages/05-async) | asyncio、async/await、aiohttp、anyio | asyncio, aiohttp | ⭐⭐⭐ |
| [06-testing-pytest](packages/06-testing-pytest) | pytest、fixture、parametrize、hypothesis、coverage | pytest, hypothesis | ⭐⭐⭐ |
| [07-http-clients](packages/07-http-clients) | requests vs httpx、重试、超时、session | requests, httpx | ⭐⭐ |
| [08-cli-rich-click](packages/08-cli-rich-click) | typer/click 命令行 + rich 终端美化 | typer, click, rich | ⭐⭐ |
| [09-numpy-pandas](packages/09-numpy-pandas) | ndarray、向量化、DataFrame、groupby、merge | numpy, pandas | ⭐⭐⭐ |
| [10-web-fastapi](packages/10-web-fastapi) | FastAPI + pydantic 模型 + 依赖注入 + OpenAPI | fastapi, uvicorn | ⭐⭐⭐ |
| [11-orm-sqlalchemy](packages/11-orm-sqlalchemy) | SQLAlchemy 2.x、session、迁移、关系 | sqlalchemy, alembic | ⭐⭐⭐⭐ |
| [12-packaging-uv-ruff](packages/12-packaging-uv-ruff) | uv 依赖管理、ruff 检查、pyproject、发包 | uv, ruff, hatch | ⭐⭐ |

强烈建议**按顺序学**。每章 README 顶部都有"前置条件"明确依赖哪几章。

## 速查参考（随用随翻）

- [reference/PYTHONIC_CHEATSHEET.md](reference/PYTHONIC_CHEATSHEET.md) — Pythonic 写法一页速查（推导式、解包、上下文管理器……）
- [reference/STDLIB_MAP.md](reference/STDLIB_MAP.md) — 标准库按用途分类速查
- [reference/PATTERNS.md](reference/PATTERNS.md) — 常用模式（dataclass、context manager、generator、decorator）
- [reference/ANTIPATTERNS.md](reference/ANTIPATTERNS.md) — 反模式（可变默认参数、裸 except、循环里 +=……）
- [reference/COMPARISON.md](reference/COMPARISON.md) — requests vs httpx、pip vs uv、pytest vs unittest、fastapi vs flask vs django

## 怎么用

### 第一次

```bash
# 安装 uv（推荐的依赖管理器）
# 更多安装方式见 https://github.com/astral-sh/uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 跑某一章
cd packages/01-fundamentals
uv sync
uv run pytest

# 进 REPL 试代码
uv run python
```

如果只装了 pip 也能用，每个章节都同时给 `pip install -e .` 的命令。

### 根目录跑全部测试

```bash
uv run pytest
```

基于 [uv workspaces](https://docs.astral.sh/uv/concepts/workspaces/)，一条命令即可运行所有章节的测试。

### 日常学习

每章的 README 都有：
1. **本章目标**（你学完应该能干什么）
2. **如何运行**（具体命令）
3. **核心概念**（why，带例子）
4. **代码导读**（src / tests 之间的关系）
5. **常见坑**（踩过才知道的）
6. **延伸阅读**（官方文档定位）

## 学习心法

- **看 README → 跑测试 → 故意改坏代码看测试是否报错**——确认你的测试不是装饰
- **REPL 永远开着**——Python 的杀手锏是交互式，看到不懂的 API 立刻 `>>> help(x)` / `>>> dir(x)`
- **每章学完，凭记忆写一个 mini demo**——记不住就回看

## 给维护者（将来的你）

- 添新章节请放在 `packages/NN-name/`，数字越大越靠后
- 每个包必须能独立 `uv sync && uv run pytest`，**不依赖根目录依赖**
- 速查文档（reference/）只放跨章节通用知识，章节内特有的写进各自的 README
