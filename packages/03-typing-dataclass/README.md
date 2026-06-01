# 03 - Typing / dataclass / pydantic

> 让 Python 项目"类型友好"。学完这章你能写出 IDE 跳转/补全/红线都精准的现代 Python 代码，知道何时用 `dataclass`、何时用 `pydantic`、何时用 `Protocol`。

## 前置

- [01-fundamentals](../01-fundamentals)

## 本章目标

- 掌握 `typing` 必会：`Optional / Union / list[X] / dict[K,V] / Callable / Literal / Final / TypedDict / Protocol / TypeVar / Generic`
- `dataclass` 全套：`frozen / slots / field(default_factory) / replace / asdict`
- `pydantic v2`：`BaseModel`、字段校验、自定义 validator、`model_dump` / `model_validate`
- 静态类型检查：`mypy --strict` vs `pyright`，配什么、容忍什么
- 何时选 dataclass、何时选 pydantic、何时选 NamedTuple

## 推荐库

- stdlib: `typing`, `dataclasses`
- 第三方: `pydantic` (v2), `attrs`（可选），`mypy` / `pyright`

## 计划要写

- `src/`: 三个对比文件 —— 同一份 User schema 分别用 dataclass / TypedDict / pydantic 实现
- `tests/`: 验证序列化、校验失败时的错误信息
- README 核心：runtime 校验 vs 仅类型注解；mypy/pyright 的盲点

## 自测

- `list[int]` 和 `List[int]` 区别？哪个推荐？
- `frozen=True` 和 `slots=True` 各自解决啥问题？
- pydantic v1 vs v2 主要差异？
- `Protocol` 比 `ABC` 好在哪？

---

**TODO**: 待补充完整代码与测试。
