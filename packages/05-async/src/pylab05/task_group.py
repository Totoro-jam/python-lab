"""TaskGroup（3.11+）：结构化并发，比 gather 更安全。"""

import asyncio


async def _worker(name: str, delay: float, should_fail: bool = False) -> str:
    """模拟工作任务。"""
    await asyncio.sleep(delay)
    if should_fail:
        raise RuntimeError(f"{name} failed!")
    return f"{name} ok"


async def parallel_fetch(items: list[tuple[str, float]]) -> list[str]:
    """使用 TaskGroup 并发执行任务。

    TaskGroup 优势：如果任何子任务抛异常，会自动取消其他任务。
    """
    results: list[str] = []

    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(_worker(name, delay)) for name, delay in items]

    results = [t.result() for t in tasks]
    return results


async def process_with_timeout(
    items: list[str],
    timeout_per_item: float = 1.0,
) -> dict[str, str | None]:
    """对每个 item 设置独立超时。"""
    results: dict[str, str | None] = {}

    async def _process(item: str) -> tuple[str, str | None]:
        try:
            async with asyncio.timeout(timeout_per_item):
                # 模拟不同处理时间
                delay = len(item) * 0.1
                await asyncio.sleep(delay)
                return item, f"processed:{item}"
        except TimeoutError:
            return item, None

    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(_process(item)) for item in items]

    for t in tasks:
        key, val = t.result()
        results[key] = val

    return results


async def cancel_demo() -> str:
    """演示任务取消与异常传播。"""
    async def long_task() -> str:
        try:
            await asyncio.sleep(100)
            return "done"
        except asyncio.CancelledError:
            return "cancelled"

    task = asyncio.create_task(long_task())
    await asyncio.sleep(0.01)
    task.cancel()

    try:
        return await task
    except asyncio.CancelledError:
        return "cancelled"
