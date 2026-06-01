"""数据容器实战：Counter, defaultdict, deque, heapq, bisect。"""

from collections import Counter, defaultdict, deque
from collections.abc import Iterable, Iterator
from itertools import islice


def top_n_words(text: str, n: int = 3) -> list[tuple[str, int]]:
    """统计文本中出现频率最高的 n 个词。"""
    words = text.lower().split()
    return Counter(words).most_common(n)


def group_by_key[K, V](items: Iterable[tuple[K, V]]) -> dict[K, list[V]]:
    """按 key 分组，返回 {key: [values...]}。"""
    result: dict[K, list[V]] = defaultdict(list)
    for key, value in items:
        result[key].append(value)
    return dict(result)


def sliding_window[T](iterable: Iterable[T], size: int) -> Iterator[tuple[T, ...]]:
    """滑动窗口，使用 deque 实现 O(1) 移动。

    >>> list(sliding_window([1,2,3,4,5], 3))
    [(1, 2, 3), (2, 3, 4), (3, 4, 5)]
    """
    it = iter(iterable)
    window = deque(islice(it, size), maxlen=size)
    if len(window) == size:
        yield tuple(window)
    for item in it:
        window.append(item)
        yield tuple(window)


def merge_sorted(*iterables: Iterable[int]) -> list[int]:
    """合并多个已排序序列（使用 heapq）。"""
    import heapq
    return list(heapq.merge(*iterables))


def insort_demo(sorted_list: list[int], value: int) -> list[int]:
    """bisect 保持有序插入。"""
    import bisect
    bisect.insort(sorted_list, value)
    return sorted_list
