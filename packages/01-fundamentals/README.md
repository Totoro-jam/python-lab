# 01 - Fundamentals: Python 是什么、第一个能跑能测的 Python 包

> 用最薄的依赖（仅 `pytest`）讲清楚 Python 程序的运行模型 + 项目结构 + 第一个测试。学完这章你能回答：解释器在做什么、模块怎么找、什么是 venv、`__name__ == "__main__"` 在干啥、怎么把一段函数变成可发布的包。

## 本章目标

- 理解 Python 是**解释执行的、动态类型的、一切皆对象**
- 用 `uv` 起一个项目，明白 venv / pyproject.toml / 入口脚本是怎么连起来的
- 写一个有"业务函数 + pytest 测试"的最小可工作 package
- 理解模块 / 包 / `__init__.py` / 相对 import 是什么
- 用 REPL + `breakpoint()` 调试

## 如何运行

```bash
cd packages/01-fundamentals

# 推荐：uv（一条命令搞定 venv + 装依赖）
uv sync
uv run pytest -v

# 跑 demo 入口
uv run python -m pylab01 add 1 2
# 输出：3

# 进 REPL 试 API
uv run python
>>> from pylab01.calculator import add
>>> add(2, 3)
5
```

不想装 uv 也可以：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -v
```

## 核心概念

### 1. Python 程序是怎么跑起来的

```
你写的 .py 文件
   ↓
词法 + 语法分析  → AST（抽象语法树）
   ↓
编译为 bytecode  → .pyc 缓存在 __pycache__/
   ↓
CPython 虚拟机逐条解释执行 bytecode
```

关键洞察：
- **不是"逐行解释源代码"**，而是先编译成 bytecode 再执行。所以语法错误立刻报，运行时错误才需要执行到那一行
- `.pyc` 不需要你管，是缓存。第一次 import 慢，第二次起快
- "动态类型"指**变量没有类型，对象有类型**：`x = 1; x = "hello"` 完全合法

### 2. 一切皆对象

```python
def f(): pass

f.__name__         # 'f'
f.__doc__          # None
f.tag = "ok"       # 函数对象上可以挂属性
type(f)            # <class 'function'>
type(int)          # <class 'type'>      ← 类也是对象
```

理解这点你会发现：装饰器、`functools.wraps`、`@property` 都不再神秘。

### 3. 模块、包、`__init__.py`

```
pylab01/                  ← 这是一个"包"，因为有 __init__.py
├── __init__.py           ← 标记 + 控制 from pylab01 import 啥
├── __main__.py           ← python -m pylab01 时执行这个
└── calculator.py         ← 模块（一个 .py 就是一个模块）
```

| 形式 | 解释 |
|---|---|
| `import pylab01` | 加载包，执行 `__init__.py` |
| `import pylab01.calculator` | 加载子模块 |
| `from pylab01 import calculator` | 同上，但绑定名 `calculator` |
| `from pylab01.calculator import add` | 只取一个函数 |
| `python -m pylab01 ARGS` | 把包当脚本跑，触发 `__main__.py` |

**3.3+ 后** `__init__.py` 不再是必须的（"命名空间包"），但有就是标准做法，不要省。

### 4. `if __name__ == "__main__":` 到底在干啥

```python
# calculator.py
def add(a, b): return a + b

if __name__ == "__main__":      # 只在"直接被执行"时为真
    print(add(2, 3))
```

- `python calculator.py` 时 → `__name__ == "__main__"` → 打印
- `import calculator` 时 → `__name__ == "calculator"` → 不打印

**作用**：让一个文件既能当库被 import，也能当脚本直接跑（写测试 demo 很有用）。

### 5. 虚拟环境（venv）：每个项目一个独立的 Python

```
.venv/
├── bin/python      ← 一个独立的解释器副本（链接）
├── lib/python3.11/site-packages/   ← 这个项目装的所有包都在这
└── ...
```

**为什么需要**：避免"项目 A 要 pandas 1.x、项目 B 要 pandas 2.x"互相打架，也不污染系统 Python。

`uv` 默认在每个项目下建 `.venv`，`uv run` 自动用它。

### 6. pyproject.toml：现代 Python 项目的"package.json"

```toml
[project]
name = "pylab01"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = []           # 运行时依赖

[project.optional-dependencies]
dev = ["pytest>=8"]         # 开发依赖（pip install -e ".[dev]"）

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**取代了**：`setup.py` + `requirements.txt` + `Pipfile` + 一堆配置散在各处。

### 7. pytest：发现 + 跑测试

约定（不需要任何配置）：
- 文件名 `test_*.py` 或 `*_test.py`
- 类名 `Test*`（**不**写 `__init__`，否则跳过）
- 函数名 `test_*`
- 用普通 `assert`，pytest 用 AST rewrite 给你漂亮的失败信息

```python
def test_add():
    assert add(2, 3) == 5
```

失败时 pytest 输出 `2 + 3 == 5` 实际值是啥，比 `unittest.TestCase.assertEqual(...)` 干净 10 倍。

## 代码导读

```
01-fundamentals/
├── pyproject.toml           ← 项目元数据 + 依赖 + pytest 配置
├── src/
│   └── pylab01/
│       ├── __init__.py      ← 包标记 + re-export 公开 API
│       ├── __main__.py      ← 入口：python -m pylab01 add 1 2
│       └── calculator.py    ← 业务逻辑
└── tests/
    └── test_calculator.py   ← pytest 测试
```

阅读顺序：
1. `pyproject.toml`（看一个 Python 项目长啥样）
2. `src/pylab01/calculator.py`（被测代码）
3. `tests/test_calculator.py`（怎么测）
4. `src/pylab01/__main__.py`（怎么当 CLI 跑）

**`src/` 布局 vs flat 布局**：`src/` 布局强制让你"装包之后才能 import"，避免"开发时能 import 因为 cwd 在根目录，装完用户却 import 不到"的陷阱。新项目都用 `src/`。

## 常见坑

### 坑 1：循环 import

```python
# a.py
from b import B

# b.py
from a import A     # 跑起来直接 ImportError
```

修法：
- 重新设计：通常说明这俩模块该合并或都依赖第三个
- 不得已：在函数内部 `import`，延迟到调用时

### 坑 2：相对 import 在脚本里用不了

```python
# pylab01/calculator.py
from .helpers import x      # ✅ 当包 import 时 OK
                            # ❌ python calculator.py 直接跑时报错
```

直接跑文件时 Python 不知道这是"哪个包的成员"。改用 `python -m pylab01.calculator`。

### 坑 3：`pip install pkg` ≠ `pip install -e .`

| | 含义 |
|---|---|
| `pip install pkg` | 装第三方包 |
| `pip install .` | 把**当前项目**装进 site-packages，改源码不生效 |
| `pip install -e .` | 同上但**可编辑模式**，源码改完立刻生效（开发用） |

uv 默认就是 editable，等价于 `pip install -e ".[dev]"`。

### 坑 4：assert 在 `python -O` 下被去掉

```python
def transfer(amount):
    assert amount > 0, "must be positive"   # 上线时 assert 失效，校验绕过
```

业务校验用 `raise ValueError(...)`，`assert` 留给测试和不变量调试。

### 坑 5：mutable 默认参数（常见陷阱）

```python
def append(item, target=[]):    # 所有调用共享同一个 list
    target.append(item); return target
append("a")  # ["a"]
append("b")  # ["a", "b"]  ← 不是新 list！
```

修法：`target=None` 然后函数内 `if target is None: target = []`。

## 延伸阅读

- [Python 官方教程](https://docs.python.org/3/tutorial/)
- [uv 文档](https://docs.astral.sh/uv/)
- [pytest 入门](https://docs.pytest.org/en/stable/getting-started.html)
- [PEP 621 — pyproject.toml 元数据](https://peps.python.org/pep-0621/)
- [src layout vs flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)

## 自测

合上代码，回答：

1. `.pyc` 是什么？我能删吗？
2. `__init__.py` 是必须的吗？省了会怎样？
3. `if __name__ == "__main__":` 在解决什么问题？
4. `pip install .` 和 `pip install -e .` 区别？我开发时用哪个？
5. pytest 为什么不用写 `unittest.TestCase`？
6. 为什么默认参数不要写 `def f(items=[])`？

下一章：`02-data-structures` —— list/dict/set/tuple、`collections`、`itertools`、`functools` 一网打尽。
