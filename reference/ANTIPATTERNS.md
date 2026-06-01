# Python 反模式（必须避开）

> 见到下面任何一种，立刻在 PR 上 -1。

---

## 1. 可变默认参数 ❌

```python
def add(x, items=[]):       # ❌ items 在函数对象上只有一份
    items.append(x)
    return items

add(1)  # [1]
add(2)  # [1, 2] —— 不是新的空 list！
```

修法：

```python
def add(x, items=None):
    if items is None: items = []
    items.append(x)
    return items
```

**为什么这么设计**：默认值在函数定义时求值，不是调用时。

---

## 2. 裸 except ❌

```python
try:
    risky()
except:                     # ❌ 吃掉所有 Exception，连 KeyboardInterrupt 都吞
    pass
```

修法：抓具体异常，必要时 `except Exception` 但要日志。

---

## 3. 用 == None / == True ❌

```python
if x == None: ...           # ❌
if x == True: ...           # ❌
```

修法：`is None` / `is True`（或直接 `if x:`）。

---

## 4. `for i in range(len(items))` ❌

```python
for i in range(len(items)):
    print(items[i])         # ❌ 多此一举
```

修法：

```python
for item in items: ...
for i, item in enumerate(items): ...   # 需要下标时
```

---

## 5. 字符串 + 拼接成循环 ❌

```python
s = ""
for x in items:
    s += str(x)             # ❌ 每次复制整个字符串，O(n²)
```

修法：

```python
s = "".join(str(x) for x in items)
```

---

## 6. `if len(x) == 0` ❌

```python
if len(items) == 0: ...     # ❌ 啰嗦
```

修法：`if not items: ...`。空 list/dict/str 都 falsy。

---

## 7. 用 `dict.keys()` 遍历 ❌

```python
for k in d.keys():          # ❌ keys() 多余
    ...

for k in d:                 # ✅ dict 默认遍历 keys
    ...

for k, v in d.items():      # ✅ 需要 v 时
    ...
```

---

## 8. `type(x) == X` ❌

```python
if type(x) == list: ...     # ❌ 不认子类
if isinstance(x, list): ... # ✅
```

---

## 9. 用 dict 当 namespace ❌

```python
config = {}
config["host"] = "x"
config["port"] = 80
# 后面 config["pot"] = 81  ← typo 不报错
```

修法：用 `dataclass` 或 `pydantic`，typo IDE 直接红线。

---

## 10. 在循环里 import ❌

```python
def f():
    for x in items:
        import json         # ❌ import 缓存，循环里没意义但有开销
```

修法：放文件顶部。

---

## 11. `assert` 当生产校验 ❌

```python
def transfer(amount):
    assert amount > 0, "must be positive"   # ❌ python -O 时 assert 被去掉
```

修法：

```python
if amount <= 0:
    raise ValueError("amount must be positive")
```

`assert` 只用于**测试** + **不变量调试**，不用于业务校验。

---

## 12. mock 自己要测的东西 ❌

```python
def test_save():
    with patch("mymodule.save") as m:
        save(...)
        m.assert_called_once()   # 测了个寂寞
```

测的就是 mock 自己。改成只 mock 边界（DB / 网络）。

---

## 13. 函数参数类型 = `dict` / `list` ❌

```python
def process(data: dict): ...   # ❌ 啥都能塞，IDE 帮不了你
```

修法：

```python
def process(data: dict[str, int]): ...      # 退一步
def process(data: User): ...                 # 一步到位用 dataclass/pydantic
```

---

## 14. 全局可变状态 ❌

```python
CACHE = {}

def fetch(x):
    if x not in CACHE: CACHE[x] = _real(x)
    return CACHE[x]
```

测试间会污染。**至少**包一层类或用 `functools.cache`：

```python
from functools import cache
@cache
def fetch(x): return _real(x)   # 函数自带缓存，可 .cache_clear()
```

---

## 15. 不用 logging，print 大法 ❌

```python
print("debug: x =", x)          # ❌ 无级别、无时间戳、不能关
```

修法：`logging.debug/info/warning/error`，配 `logging.basicConfig` 一次。

---

## 16. 异步里 sync 阻塞 ❌

```python
async def handler():
    data = requests.get(url)    # ❌ 阻塞整个事件循环
```

修法：用 `httpx.AsyncClient` 或 `aiohttp`。如果非要调 sync 库，`await asyncio.to_thread(sync_fn, args)`。

---

## 17. `Exception` → `str` 后再处理 ❌

```python
try: ...
except Exception as e:
    if "timeout" in str(e): retry()   # ❌ 异常 message 不是 API
```

修法：

```python
except TimeoutError: retry()
```

---

## 18. 在 `__init__.py` 里写业务代码 ❌

`__init__.py` 主要是 re-export（`from .x import Y`），不要往里塞业务逻辑——import 路径会变得诡异。

---

## 19. 过度继承 ❌

```python
class A(B, C, D, E): ...     # 多继承 + 深层 → MRO 灾难
```

修法：**组合优于继承**。绝大多数情况用一个属性持有依赖即可。

---

## 20. flaky 测试 retry ✅ 修，❌ 重试

CI 加 `pytest-rerunfailures` 重试 3 次压住红色 → 几个月后所有人对测试失去信任。flaky 必须立刻修或 quarantine。
