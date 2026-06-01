# 05 - Async: asyncio + httpx async + anyio

> Python 异步模型。学完能区分 sync / threaded / async 三种并发，写出能跑满 IO 的协程代码。

## 前置

- [01-fundamentals](../01-fundamentals), [04-io-paths](../04-io-paths)

## 本章目标

- 理解 event loop / coroutine / task / future
- `async def` + `await` 的语义；`asyncio.gather` / `asyncio.wait` / `asyncio.TaskGroup`（3.11+）
- 超时 (`asyncio.timeout`)、取消 (cancel) 与传播
- 同步代码桥接：`asyncio.to_thread`、`run_in_executor`
- 结构化并发的现代写法（TaskGroup）
- 为什么不要在协程里调 `requests.get`、`time.sleep`

## 推荐库

- stdlib: `asyncio`
- 第三方: `httpx[http2]`、`aiofiles`、`anyio`（跨运行时）、`uvloop`（更快的 loop）

## 计划要写

- `src/`: 并发抓 100 个 URL（对比串行/线程池/async 三种）
- `tests/`: `pytest-asyncio`，mock event loop

## 自测

- `await` 干了啥？ 没 `await` 直接调用协程会发生什么？
- 在协程里 `time.sleep(1)` 会怎样？
- `asyncio.gather(return_exceptions=True)` 啥用？
- TaskGroup vs gather 区别？

---

**TODO**: 待补充完整代码与测试。
