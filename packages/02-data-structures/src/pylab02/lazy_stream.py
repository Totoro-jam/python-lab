"""惰性流处理：itertools + 生成器。"""

from collections.abc import Generator, Iterable, Iterator
from functools import cache, partial, reduce
from itertools import accumulate, chain
from pathlib import Path
from typing import TypeVar

T = TypeVar("T")


def stream_large_file(path: Path) -> Generator[str, None, None]:
    """逐行流式读取大文件，不加载全部到内存。"""
    with path.open(encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")


def chunked(iterable: Iterable[T], size: int) -> Iterator[list[T]]:
    """将可迭代对象按 size 切片。

    >>> list(chunked([1,2,3,4,5], 2))
    [[1, 2], [3, 4], [5]]
    """
    it = iter(iterable)
    while True:
        chunk = []
        try:
            for _ in range(size):
                chunk.append(next(it))
        except StopIteration:
            if chunk:
                yield chunk
            return
        yield chunk


def flatten(nested: Iterable[Iterable[T]]) -> Iterator[T]:
    """展平嵌套可迭代对象，等同 chain.from_iterable。"""
    return chain.from_iterable(nested)


def running_total(numbers: Iterable[int | float]) -> list[int | float]:
    """累加前缀和。"""
    return list(accumulate(numbers))


@cache
def fibonacci(n: int) -> int:
    """functools.cache 缓存递归（等效 lru_cache(maxsize=None)）。"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def make_multiplier(factor: int):
    """partial 演示：创建固定因子的乘法函数。"""
    return partial(lambda x, f: x * f, f=factor)


def compose_pipeline(*functions):
    """reduce 演示：组合多个函数为管道。"""
    return reduce(lambda f, g: lambda x: g(f(x)), functions)
