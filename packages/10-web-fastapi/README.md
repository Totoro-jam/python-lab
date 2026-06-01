# 10 - Web: FastAPI

> 当下最现代的 Python API 框架。学完能搭出带 OpenAPI、依赖注入、auth、async DB 的生产级服务。

## 前置

- [03-typing-dataclass](../03-typing-dataclass), [05-async](../05-async)

## 本章目标

- 路由、路径参数、query、body、`Annotated`
- pydantic 模型作为请求/响应 schema
- 依赖注入（`Depends`）：DB session、auth、当前用户
- Background task、Event handlers（startup/shutdown）
- 自动生成 OpenAPI + Swagger UI + ReDoc
- 中间件、CORS、异常处理
- 测试：`TestClient`（基于 httpx）

## 推荐库

- `fastapi`, `uvicorn[standard]`, `pydantic v2`, `httpx`（test client），可选 `sqlmodel`

## 计划要写

- `src/`: 一个 Todo API（CRUD + auth + pagination）
- `tests/`: 集成测试 + 启动 DB fixture

## 自测

- `Depends(get_db)` 在干啥？scope 怎么控？
- 为什么不要把 sync 函数路由跑在 async 框架里？
- `response_model` 和返回类型注解区别？
- OpenAPI 文档怎么定制 tag / description？

---

**TODO**: 待补充完整代码与测试。
