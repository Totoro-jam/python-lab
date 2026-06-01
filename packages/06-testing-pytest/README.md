# 06 - Testing: pytest 进阶 + hypothesis + coverage

> 01 章用了 pytest 但只是皮毛。这章把 fixture / plugin / mock / 属性测试讲透。

## 前置

- [01-fundamentals](../01-fundamentals)

## 本章目标

- fixture：作用域 (`function/class/module/session`)、`yield` 清理、`autouse`、参数化 fixture
- `monkeypatch` 改 env/属性/方法；`tmp_path` 临时目录；`capsys` 抓输出
- `pytest-mock`（mocker）vs 原生 `unittest.mock`
- 表驱动 `@pytest.mark.parametrize` 进阶（ids、indirect）
- `hypothesis`：属性测试，让框架帮你找 corner case
- coverage：`pytest-cov`、阈值、`--cov-branch`
- 并行：`pytest-xdist`、随机顺序 `pytest-randomly`

## 推荐库

- `pytest`, `pytest-mock`, `pytest-cov`, `pytest-asyncio`, `pytest-xdist`, `pytest-randomly`, `hypothesis`

## 计划要写

- `src/`: 一个有外部依赖的服务（DB + HTTP），演示如何隔离
- `tests/`: fixture 工厂模式、hypothesis 实战、断言风格演化

## 自测

- `session` scope fixture 什么时候 setup / teardown？
- `monkeypatch` 和 `unittest.mock.patch` 区别？
- hypothesis 的 shrink 是干啥的？
- coverage 100% 意味着没 bug 吗？

---

**TODO**: 待补充完整代码与测试。
