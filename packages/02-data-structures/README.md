# 02 - Data Structures: list / dict / set / tuple + collections + itertools + functools

> Python 数据结构的"内功"。学完这章你能在大多数题里挑出最合适的容器，不再用 `for i in range(len(x))` 写 Python。

## 前置

- [01-fundamentals](../01-fundamentals)

## 本章目标

- 掌握 4 大内置容器（list、tuple、dict、set）的复杂度与适用场景
- 用 `collections.{Counter, defaultdict, deque, OrderedDict}` 解决 80% 的容器问题
- 用 `itertools.{chain, groupby, islice, product, combinations, accumulate}` 写出函数式风格的迭代
- 用 `functools.{cache, lru_cache, partial, reduce, wraps}` 解决缓存与装饰器
- 推导式 vs map/filter；生成器 vs list

## 推荐库 / 模块

- stdlib: `collections`, `itertools`, `functools`, `heapq`, `bisect`
- 第三方（可选）：`more-itertools`（itertools 的超集）

## 计划要写

- `src/`: 几个真实数据问题（top-N 词频、按 key 分组、滑窗、惰性流处理）
- `tests/`: 每个工具一个 demo + 边界 case
- README 核心概念：list 是 O(n) 删头、deque 是 O(1)、dict 用哈希、set 也用哈希、Counter 是 dict 子类……

## 自测

- `dict[k]` 和 `dict.get(k)` 区别？
- `Counter("aaab").most_common(1)` 返回啥？
- `itertools.chain` vs `chain.from_iterable` 区别？
- `lru_cache(maxsize=None)` 和 `cache` 一样吗？

---

**TODO**: 待补充完整代码与测试。维护者填章节时参考 [01-fundamentals](../01-fundamentals/README.md) 的结构。
