"""pylab01 — 章节 01 的示例包。

__init__.py 标记这个目录是一个 Python 包；
顶层 re-export 让用户能写 `from pylab01 import add` 而不是
`from pylab01.calculator import add`。
"""

from .calculator import add, divide, is_even

__all__ = ["add", "divide", "is_even"]
__version__ = "0.1.0"
