# 11 - ORM: SQLAlchemy 2.x + Alembic

> Python 生态最强的 ORM。学完能正确使用 session、关系、事务，并用 alembic 管理 schema 迁移。

## 前置

- [03-typing-dataclass](../03-typing-dataclass), [10-web-fastapi](../10-web-fastapi)

## 本章目标

- SQLAlchemy 2.x 风格：`Mapped[X]`、`mapped_column`、`select()` 表达式
- session 生命周期、`begin()` 上下文管理器、commit/rollback
- 关系：one-to-many、many-to-many、`back_populates`、lazy 策略
- 防 N+1：`selectinload` / `joinedload`
- async 模式（`AsyncEngine`、`AsyncSession`）
- Alembic 迁移：autogenerate、手写、上线流程
- 何时直接用原生 SQL（`text()`）

## 推荐库

- `sqlalchemy>=2.0`, `alembic`, `aiosqlite` / `asyncpg`（async 驱动）

## 计划要写

- `src/`: User + Post 经典关系、CRUD + 复杂查询
- `tests/`: 用 SQLite in-memory + transaction rollback per test

## 自测

- 1.x 的 `Query` 和 2.x 的 `select()` 区别？为啥换？
- lazy='select' / 'joined' / 'selectin' / 'raise' 各自什么时候用？
- session 关掉之后访问对象属性会怎样？
- alembic autogenerate 哪些改动它检测不到？

---

**TODO**: 待补充完整代码与测试。
