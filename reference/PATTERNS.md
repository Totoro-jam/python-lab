# Python 常用模式

行业代码里反复出现的几个套路，看多了就发现都是这些。

---

## 1. 上下文管理器 (`with`)

```python
# 自动管理资源（打开/关闭、加锁/解锁、临时改/恢复）
class Timer:
    def __enter__(self):
        import time; self.t0 = time.time(); return self
    def __exit__(self, *exc):
        print(f"took {time.time()-self.t0:.3f}s")

with Timer():
    do_work()

# 更轻量：contextmanager 装饰器
from contextlib import contextmanager
@contextmanager
def chdir(path):
    import os; cwd = os.getcwd(); os.chdir(path)
    try: yield
    finally: os.chdir(cwd)
```

**信号**：见到 try/finally 在多处重复 → 提取成上下文管理器。

---

## 2. 装饰器 (decorator)

```python
from functools import wraps

def retry(times=3):
    def deco(fn):
        @wraps(fn)   # 保留原函数 __name__/__doc__
        def wrapper(*a, **kw):
            for i in range(times):
                try: return fn(*a, **kw)
                except Exception:
                    if i == times - 1: raise
        return wrapper
    return deco

@retry(times=5)
def fetch(url): ...
```

**经验**：装饰器适合"横切关注点"——计时、重试、缓存、鉴权、日志。不要用装饰器替代正常组合。

---

## 3. 生成器 / 协程 (`yield`)

```python
# 惰性流：处理无法装内存的大数据
def read_lines(path):
    with open(path) as f:
        for line in f:                 # 文件对象本身就是行生成器
            yield line.rstrip()

for line in read_lines("huge.log"):
    process(line)
```

**反例**：把生成器结果整个 `list(...)` 化——失去 lazy 优势。除非确实要全量。

---

## 4. dataclass / Pydantic（结构化数据）

```python
# 内部领域对象 → dataclass
@dataclass(frozen=True, slots=True)
class Address:
    city: str
    zipcode: str

# 边界（API 输入输出）→ pydantic
from pydantic import BaseModel, EmailStr
class UserIn(BaseModel):
    name: str
    email: EmailStr
```

**判断**：要不要 runtime 校验？要 → pydantic；纯内部传值 → dataclass。

---

## 5. 工厂 + 注册表

```python
HANDLERS: dict[str, Callable] = {}

def register(name):
    def deco(fn):
        HANDLERS[name] = fn
        return fn
    return deco

@register("ping")
def _(req): return {"pong": True}

# 调用
HANDLERS[req.kind](req)
```

适合"插件式"扩展（新增一个 handler 文件就行，不改 dispatch 代码）。

---

## 6. 策略 (Strategy) ≈ 高阶函数

```python
def process(items, *, key=lambda x: x.id, reducer=sum):
    return reducer(key(x) for x in items)
```

Python 是一等函数语言，**绝大多数"策略模式"=传函数**，不需要类。

---

## 7. 责任链（pipeline / middleware）

```python
def pipeline(*funcs):
    def run(x):
        for f in funcs:
            x = f(x)
        return x
    return run

clean = pipeline(strip, lower, dedupe)
result = clean(raw)
```

FastAPI / Django 的 middleware 都是这个模型。

---

## 8. Protocol（结构子类型）

```python
from typing import Protocol

class Reader(Protocol):
    def read(self, n: int) -> bytes: ...

def consume(r: Reader) -> bytes:
    return r.read(1024)
```

**好处**：不用让你的类继承某个基类，只要长得像 `Reader` 就能传进去（duck typing 的类型版）。

---

## 9. ABC（抽象基类）

```python
from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def save(self, key: str, val: bytes) -> None: ...
    @abstractmethod
    def load(self, key: str) -> bytes: ...
```

适合"想强制子类实现某些方法"。但要先想想 Protocol 是不是更好。

---

## 10. 单例 / 模块级常量

Python 模块本身就是单例（import 只执行一次）。**不需要写 Singleton 类**——把"全局唯一"放在模块顶层就行。

```python
# config.py
SETTINGS = load_config()           # 模块加载时执行一次

# 其他文件
from .config import SETTINGS
```

---

## 11. 依赖注入（DI）

```python
# 显式 DI：参数传入依赖
def send_email(user, *, smtp_client):
    smtp_client.send(user.email, ...)

# 测试时传 mock
send_email(user, smtp_client=FakeSmtp())
```

**信号**：函数内部硬编码外部依赖（`smtplib.SMTP(...)`）→ 难测 → 改 DI。

---

## 12. 命令模式：CLI sub-command（typer）

```python
import typer
app = typer.Typer()

@app.command()
def add(name: str): ...

@app.command()
def remove(name: str): ...

if __name__ == "__main__":
    app()
```

写出来天然就是 `mycli add NAME` / `mycli remove NAME`，比 argparse 简单 10 倍。

---

## 13. 不可变 + 复制 (immutable + copy)

```python
@dataclass(frozen=True)
class Settings:
    timeout: int = 30
    retries: int = 3

# 修改 = 复制
from dataclasses import replace
new = replace(old_settings, timeout=60)
```

**适合**：配置、领域值对象、React-style state。

---

## 14. EAFP > LBYL

```python
# EAFP (Easier to Ask Forgiveness than Permission) ✅ Pythonic
try:
    return d[k]
except KeyError:
    return default

# LBYL (Look Before You Leap) ⚠️ 多线程下有 race
if k in d:
    return d[k]
return default
```

但日常 `d.get(k, default)` 更短。EAFP 主要用于"检查代价高"的场景。
