"""演示用计算器：被测对象。

注意点：
- 函数签名带类型注解（typing 那一章会展开讲）
- 异常用具体的 ValueError，不裸 raise
- docstring 演示"""


def add(a: float, b: float) -> float:
    """两数之和。整数 + 整数 → 整数；浮点 → 浮点。"""
    return a + b


def divide(a: float, b: float) -> float:
    """a / b。b 为 0 时抛 ValueError（不要用 ZeroDivisionError 让调用方猜原因）。"""
    if b == 0:
        raise ValueError("cannot divide by zero")
    return a / b


def is_even(n: int) -> bool:
    """n 是不是偶数。"""
    return n % 2 == 0
