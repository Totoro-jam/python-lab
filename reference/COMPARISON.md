# 主流库横向对比

## 1. 包管理 / 依赖

| | uv | pip + venv | poetry | pdm | conda |
|---|---|---|---|---|---|
| 速度 | **极快**（Rust） | 慢 | 中（自带 resolver 慢） | 中 | 中 |
| 锁文件 | ✅ `uv.lock` | ❌ | ✅ `poetry.lock` | ✅ `pdm.lock` | ✅ `environment.yml` |
| 虚拟环境 | 自动 | 手动 venv | 自动 | 自动 | 自带 env |
| 安装 Python 本身 | ✅ | ❌ | ❌ | ❌ | ✅ |
| 推荐 | **新项目首选** | 学习/CI 兼容 | 老项目 | 老项目 | 数据科学（带 C 依赖） |

**结论：2025+ 新项目无脑选 uv**。比 poetry 快 10-100 倍，能装/管 Python 解释器本身。

---

## 2. 代码检查 / 格式化

| | ruff | flake8 + black + isort | pylint | mypy | pyright |
|---|---|---|---|---|---|
| 速度 | **极快** | 慢 | 慢 | 中 | 快 |
| Lint | ✅ | ✅ | ✅ 最严 | ❌ | ❌ |
| Format | ✅ | 需 black | ❌ | ❌ | ❌ |
| Import sort | ✅ | 需 isort | ❌ | ❌ | ❌ |
| 类型检查 | ❌ | ❌ | 部分 | ✅ | ✅ |

**结论**：lint + format 用 `ruff` 一个搞定（替代 flake8/black/isort）。类型检查二选一：`mypy` 生态老、`pyright` 快（VSCode 默认）。

---

## 3. HTTP 客户端

| | httpx | requests | aiohttp | urllib3 |
|---|---|---|---|---|
| sync 支持 | ✅ | ✅ | ❌ | ✅ |
| async 支持 | ✅ | ❌ | ✅ | ❌ |
| HTTP/2 | ✅ | ❌ | ❌ | ❌ |
| 类型注解 | ✅ 完整 | ⚠️ 部分 | ⚠️ | ⚠️ |
| 学习曲线 | API 类 requests | 最简单 | 异步原生 | 偏底层 |
| 推荐 | **新项目** | 老项目维持 | aiohttp 老 stack | 极少直接用 |

**结论**：新项目用 `httpx`，sync/async 同一套 API。`requests` 仍是世界上下载量最高的库，老项目别迁移。

---

## 4. Web 框架

| | FastAPI | Flask | Django | Starlette | Sanic | Litestar |
|---|---|---|---|---|---|---|
| API 优先 | ✅ | 中 | ❌（全栈） | ✅ 底层 | ✅ | ✅ |
| async 原生 | ✅ | 3.x 部分 | 4.x 部分 | ✅ | ✅ | ✅ |
| pydantic 集成 | ✅ 一等 | 需第三方 | ❌（用 DRF） | ❌ | ❌ | ✅ |
| 自动 OpenAPI | ✅ | 需第三方 | DRF 部分 | ❌ | ✅ | ✅ |
| ORM | 不绑定 | 不绑定 | 自带 | 不绑定 | 不绑定 | 不绑定 |
| 生态 | 中（爆发期） | 巨大 | 巨大 | 小（底层） | 小 | 小 |
| 推荐 | **API/微服务** | 简单服务 | 全栈 / CMS | 写框架 | 高性能 | FastAPI 替代 |

**结论**：纯 API → FastAPI；全栈带后台 → Django；轻量 → Flask。

---

## 5. ORM / 数据库层

| | SQLAlchemy 2.x | Django ORM | Peewee | SQLModel | Tortoise |
|---|---|---|---|---|---|
| 复杂查询 | ✅ 最强 | ✅ | ⚠️ | ✅（基于 SQLAlchemy） | ⚠️ |
| async | ✅ 2.x | 4.x 部分 | ❌ | ✅ | ✅ |
| 迁移 | alembic | 内置 | 第三方 | alembic | aerich |
| 学习曲线 | 陡 | 简单 | 简单 | 中 | 中 |
| 推荐 | **生产/复杂** | Django 项目 | 小脚本 | FastAPI + SQLA | aiosql 替代 |

**结论**：FastAPI/Flask 默认 `SQLAlchemy 2.x`；Django 项目用自带 ORM；不要为了简洁选 Peewee（功能跟不上）。

---

## 6. 数据校验 / 序列化

| | pydantic v2 | dataclasses | attrs | marshmallow | msgspec |
|---|---|---|---|---|---|
| Runtime 校验 | ✅ | ❌ | ⚠️（validators） | ✅ | ✅ |
| 速度 | 快（Rust 核心） | 最快 | 快 | 中 | **极快** |
| FastAPI 集成 | ✅ 一等 | ❌ | ❌ | 老 | ✅ |
| 生态 | 巨大 | stdlib | 中 | 中 | 小 |

**结论**：API/配置边界用 `pydantic v2`；内部纯数据用 `dataclasses`；性能极致用 `msgspec`。

---

## 7. 测试

| | pytest | unittest | nose2 |
|---|---|---|---|
| 语法 | 函数 + assert | 类 + self.assertX | 类 |
| Fixture | ✅ 极强 | setUp/tearDown | 同 unittest |
| 参数化 | ✅ `parametrize` | 不优雅 | ⚠️ |
| 插件 | 巨大（pytest-cov / -xdist / -mock） | 少 | 少 |
| 推荐 | **新项目** | stdlib 没办法 | ❌ |

**结论**：除非环境装不了第三方，否则 `pytest`。

---

## 8. CLI

| | typer | click | argparse | fire | docopt |
|---|---|---|---|---|---|
| 基于 | click + 类型注解 | 装饰器 | stdlib | 自省函数签名 | docstring |
| 类型注解驱动 | ✅ | ❌ | ❌ | ✅ | ❌ |
| 子命令 | ✅ | ✅ | ⚠️ | ✅ | ⚠️ |
| help 美观 | ✅（rich） | ✅ | 朴素 | 朴素 | 朴素 |
| 推荐 | **新项目** | 复杂场景 | 极简脚本 | 实验 | 维护风险 |

**结论**：`typer` = `click` + 类型注解，FastAPI 同作者，体验最好。

---

## 9. 异步运行时

| | asyncio | anyio | trio | curio |
|---|---|---|---|---|
| stdlib | ✅ | ❌ | ❌ | ❌ |
| 结构化并发 | ❌（手写） | ✅ | ✅ 首创 | ✅ |
| 跨运行时 | ❌ | ✅（asyncio + trio） | ❌ | ❌ |
| 推荐 | 默认 | 写库 | 想要更安全的 API | 实验 |

**结论**：99% 项目用 `asyncio`；写库时如果想兼容 trio，用 `anyio`。

---

## 10. 真实项目栈推荐（2026 视角）

**Web API 服务**：
```
FastAPI + pydantic v2 + httpx + SQLAlchemy 2.x (async) + alembic
+ pytest + ruff + mypy + uv + Docker
```

**数据脚本/分析**：
```
uv + numpy + pandas (or polars) + matplotlib/plotly
+ jupyterlab + ruff
```

**CLI 工具**：
```
typer + rich + httpx + pydantic + pytest + uv
```

**机器学习训练**：
```
uv + numpy + pandas + scikit-learn / pytorch + matplotlib
+ wandb/mlflow + ruff
```
