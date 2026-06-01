# Pythonic 写法速查

> "能用 C 风格 for 循环写出来" ≠ "Pythonic"。下面这些是看一眼就能识别"写过 Python"的标志。

---

## 1. 推导式（comprehension）

```python
squares = [x * x for x in range(10)]
evens   = [x for x in range(10) if x % 2 == 0]
matrix  = [[i * j for j in range(3)] for i in range(3)]

# 字典 / 集合推导
name2age = {p.name: p.age for p in people}
unique   = {x.lower() for x in words}

# 生成器表达式（不开内存，按需算）
total = sum(x * x for x in range(10_000_000))
```

**反例：能 1 行推导式做的事不要 for + append**。

---

## 2. 解包

```python
a, b = b, a                          # 交换不需要临时变量
first, *rest = [1, 2, 3, 4]          # first=1, rest=[2,3,4]
*head, last  = [1, 2, 3, 4]          # head=[1,2,3], last=4
name, _, age = "Alice|30|F".split("|")  # _ 表示丢弃

# 字典解包
defaults = {"timeout": 30, "retries": 3}
opts = {**defaults, "timeout": 60}   # 覆盖 timeout，保留 retries

# 函数参数解包
def f(a, b, c): ...
args = (1, 2, 3)
f(*args)
kwargs = {"a": 1, "b": 2, "c": 3}
f(**kwargs)
```

---

## 3. enumerate / zip

```python
for i, x in enumerate(items):        # ✅ 而不是 for i in range(len(items)): items[i]
    ...

for k, v in zip(keys, values):       # 并行遍历
    ...

for k, v in zip(keys, values, strict=True):   # 3.10+，长度不等就报错
    ...
```

---

## 4. 上下文管理器（with）

```python
with open("a.txt") as f:                       # 自动关闭
    data = f.read()

with open("a.txt") as fr, open("b.txt", "w") as fw:
    fw.write(fr.read())

# 临时改变状态
from contextlib import contextmanager

@contextmanager
def timing(name):
    import time; t0 = time.time()
    yield
    print(f"{name}: {time.time()-t0:.3f}s")

with timing("query"):
    do_query()
```

---

## 5. 三种字符串格式化（只用 f-string 就行）

```python
name = "Alice"; age = 30
f"{name} is {age}"                   # ✅ 默认
f"{age:>5}"                          # 右对齐宽 5
f"{1/3:.4f}"                         # 小数 4 位
f"{name=}"                           # 调试神器：输出 name='Alice'
f"{value:_}"                         # 千分位下划线：1_000_000
```

---

## 6. dict 常用招

```python
d.get("k", default)                  # 不在就给默认
d.setdefault("k", []).append(x)      # 第一次给空 list，之后 append

from collections import defaultdict, Counter
groups = defaultdict(list)
for x in items:
    groups[x.kind].append(x)

cnt = Counter(words)                 # 计数
cnt.most_common(5)                   # top 5
```

---

## 7. 真假值与 None 比较

```python
if x:                                # ✅ 空 list/dict/str 都 falsy
if not items: ...                    # ✅ 不要 `if len(items) == 0`

if x is None: ...                    # ✅ 不要 `if x == None`
if x is not None: ...
```

---

## 8. 异常

```python
try:
    risky()
except ValueError as e:              # 永远抓具体类
    log.warning("bad value: %s", e)
except (KeyError, IndexError):       # 多类用元组
    ...
except Exception as e:               # 兜底（少用）
    raise RuntimeError("...") from e # 保留原因链

# 资源清理用 finally 或 with
```

**反模式**：`except:` 或 `except Exception: pass`——吃掉所有错误。

---

## 9. 切片（slice）

```python
a[start:stop:step]
a[:n]           # 前 n 个
a[-n:]          # 后 n 个
a[::-1]         # 反转
a[::2]          # 每隔一个
s = "hello"; s[::-1]   # "olleh"
```

---

## 10. 列表/字典扁平化

```python
# 二维 list 展开
flat = [x for row in matrix for x in row]

# 多个 dict 合并
merged = {**d1, **d2, **d3}

# Python 3.9+
combined = d1 | d2 | d3
```

---

## 11. 生成器（yield）

```python
def chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i+n]

# 用法：按需迭代，省内存
for batch in chunks(huge_list, 1000):
    process(batch)
```

---

## 12. dataclass / namedtuple（结构化数据）

```python
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class Point:
    x: float
    y: float

# 不用写 __init__/__repr__/__eq__
```

---

## 13. 函数式三件套（少用，但要看得懂）

```python
list(map(str.upper, words))          # 推导式 [w.upper() for w in words] 更 Pythonic
list(filter(None, items))            # 去掉所有 falsy
from functools import reduce
reduce(lambda acc, x: acc + x, nums, 0)
```

---

## 14. itertools / functools 杀手锏

```python
from itertools import chain, groupby, islice, product, combinations
chain.from_iterable([[1,2],[3,4]])         # 扁平
list(islice(infinite_gen, 10))             # 取前 10
list(product([1,2],[3,4]))                 # 笛卡尔积
list(combinations([1,2,3], 2))             # 组合

from functools import cache, lru_cache, partial
@cache                                      # 3.9+
def fib(n): return n if n<2 else fib(n-1)+fib(n-2)

add5 = partial(add, 5)                     # 偏函数
```

---

## 15. 路径（pathlib > os.path）

```python
from pathlib import Path
p = Path("data") / "raw" / "x.csv"          # 拼路径
p.exists(); p.is_file(); p.suffix; p.stem
p.read_text(encoding="utf-8")
list(Path(".").glob("**/*.py"))             # 递归 glob
```

---

## 16. 简单 logging（不要 print 调试）

```python
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)
log.info("loaded %d rows", n)               # ✅ 用 %s 占位，惰性
```
