# 12 - Packaging: uv + ruff + 发包

> 把一个项目变成"团队能贡献、CI 能跑、用户能装"的标准 Python 包。

## 前置

- [01-fundamentals](../01-fundamentals)

## 本章目标

- `uv` 完整工作流：`init / add / sync / lock / run / build / publish`
- `pyproject.toml` 字段全集：metadata、dependencies、scripts、entry_points
- `ruff` 完整配置：lint + format + isort 一体化
- 类型检查接入：`mypy` / `pyright`
- 版本管理：`hatch-vcs`、SemVer、`bump-my-version`
- 发布到 PyPI：trusted publishing（GH Actions OIDC，无 token）
- 双轮子：纯 Python wheel vs 带 C 扩展 wheel
- pre-commit hooks（ruff、mypy、prettier-yaml）

## 推荐库

- `uv`, `ruff`, `mypy`/`pyright`, `pre-commit`, `hatch`, `bump-my-version`

## 计划要写

- 一个最小可发布包，从零到 `uv publish`
- GH Actions workflow 模板
- `.pre-commit-config.yaml`

## 自测

- `uv pip install` 和 `uv add` 区别？
- `uv.lock` 提交吗？
- ruff 默认开了哪些规则？哪些建议加？
- PyPI trusted publishing 比 token 安全在哪？

---

**TODO**: 待补充完整代码与测试。
