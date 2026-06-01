"""asyncio 基础：coroutine, gather, sleep, async generator。"""

import asyncio
from collections.abc import AsyncGenerator


async def simulate_io(name: str, delay: float) -> str:
    """模拟 IO 操作（用 asyncio.sleep 而非 time.sleep）。"""
    await asyncio.sleep(delay)
    return f"{name} done after {delay}s"


async def fetch_all(tasks: list[tuple[str, float]]) -> list[str]:
    """并发执行多个模拟 IO 任务（gather 方式）。

    tasks: [(name, delay), ...]
    """
    coros = [simulate_io(name, delay) for name, delay in tasks]
    results = await asyncio.gather(*coros)
    return list(results)


async def timed_operation(timeout: float, delay: float) -> str | None:
    """演示 asyncio.timeout（3.11+）。

    如果操作超时返回 None。
    """
    try:
        async with asyncio.timeout(timeout):
            await asyncio.sleep(delay)
            return "completed"
    except TimeoutError:
        return None


async def async_range(start: int, stop: int, delay: float = 0.0) -> AsyncGenerator[int, None]:
    """异步生成器演示。"""
    for i in range(start, stop):
        if delay > 0:
            await asyncio.sleep(delay)
        yield i


async def to_thread_demo(data: list[int]) -> int:
    """asyncio.to_thread 桥接同步阻塞代码。"""
    def heavy_computation(nums: list[int]) -> int:
        # 模拟 CPU 密集操作
        return sum(x * x for x in nums)

    return await asyncio.to_thread(heavy_computation, data)
