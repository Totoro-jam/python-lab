# 07 - HTTP Clients: requests vs httpx

> 99% Python 项目要发 HTTP 请求。学完知道何时用 requests、何时用 httpx、怎么处理重试/超时/连接复用。

## 前置

- [01-fundamentals](../01-fundamentals), [05-async](../05-async)

## 本章目标

- `requests`：Session、超时（**永远**带）、retries、headers、stream
- `httpx`：sync 与 async 同一套 API；HTTP/2；连接池
- 重试策略：`tenacity` / `httpx.HTTPTransport(retries=...)`
- 测试 HTTP：`responses`（mock requests）vs `respx`（mock httpx）vs `pytest-httpserver`（真实小 server）
- 不要做的事：忽略超时、把 response 整个读进内存、不重用 Session

## 推荐库

- `httpx`（推荐新项目）、`requests`（老项目）、`tenacity`、`respx`

## 计划要写

- `src/`: 写一个带重试 + 超时 + log 的 client wrapper
- `tests/`: 用 respx mock 各种 HTTP 错误码

## 自测

- 不带 timeout 的 requests 会怎样？
- Session 解决什么问题？
- httpx async 和 requests + ThreadPool 各自适合什么场景？

---

**TODO**: 待补充完整代码与测试。
