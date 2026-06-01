"""asyncio 基础测试。"""

import asyncio
import pytest

from pylab05.basics import async_range, fetch_all, timed_operation, to_thread_demo


class TestFetchAll:
    async def test_concurrent_results(self):
        tasks = [("a", 0.01), ("b", 0.01), ("c", 0.01)]
        results = await fetch_all(tasks)
        assert len(results) == 3
        assert "a done" in results[0]

    async def test_empty_tasks(self):
        results = await fetch_all([])
        assert results == []


class TestTimedOperation:
    async def test_completes_in_time(self):
        result = await timed_operation(timeout=1.0, delay=0.01)
        assert result == "completed"

    async def test_timeout_returns_none(self):
        result = await timed_operation(timeout=0.01, delay=1.0)
        assert result is None


class TestAsyncRange:
    async def test_basic(self):
        values = [v async for v in async_range(0, 5)]
        assert values == [0, 1, 2, 3, 4]

    async def test_empty(self):
        values = [v async for v in async_range(5, 5)]
        assert values == []


class TestToThread:
    async def test_computation(self):
        result = await to_thread_demo([1, 2, 3])
        assert result == 14  # 1+4+9
