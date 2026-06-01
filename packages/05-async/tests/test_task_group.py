"""TaskGroup 测试。"""

import asyncio
import pytest

from pylab05.task_group import cancel_demo, parallel_fetch, process_with_timeout


class TestParallelFetch:
    async def test_all_succeed(self):
        items = [("x", 0.01), ("y", 0.01)]
        results = await parallel_fetch(items)
        assert results == ["x ok", "y ok"]

    async def test_empty(self):
        results = await parallel_fetch([])
        assert results == []


class TestProcessWithTimeout:
    async def test_short_items_succeed(self):
        items = ["ab", "cd"]
        results = await process_with_timeout(items, timeout_per_item=5.0)
        assert results["ab"] == "processed:ab"
        assert results["cd"] == "processed:cd"

    async def test_long_item_times_out(self):
        # 每个字符 0.1s，长度 20 = 2s > timeout 0.5s
        items = ["a" * 20]
        results = await process_with_timeout(items, timeout_per_item=0.5)
        assert results["a" * 20] is None


class TestCancelDemo:
    async def test_cancel(self):
        result = await cancel_demo()
        assert result == "cancelled"
