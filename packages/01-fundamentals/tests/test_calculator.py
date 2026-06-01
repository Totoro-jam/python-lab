"""演示 pytest 最常用的几种写法。

约定：
- 文件名 test_*.py
- 函数名 test_*
- 用普通 assert（pytest 会重写 AST 提供漂亮的失败信息）
"""

import pytest

from pylab01 import add, divide, is_even


# === AAA 结构：基础用法 ===

def test_add_positive():
    # Arrange / Act
    result = add(1, 2)
    # Assert
    assert result == 3


def test_add_with_zero():
    assert add(5, 0) == 5


# === parametrize：同一逻辑跑多组数据 ===

@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (1, 2, 3),
        (-1, -2, -3),
        (0, 0, 0),
        (1.5, 2.5, 4.0),
    ],
)
def test_add_table(a, b, expected):
    assert add(a, b) == expected


# === 浮点用 pytest.approx ===

def test_floats_use_approx():
    # 0.1 + 0.2 ≠ 0.3，浮点比较必须 approx
    assert add(0.1, 0.2) == pytest.approx(0.3)


# === 异常断言 ===

def test_divide_by_zero_raises():
    with pytest.raises(ValueError, match="cannot divide by zero"):
        divide(1, 0)


def test_divide_normal():
    assert divide(10, 2) == 5


# === 用 class 分组（可选风格，pytest 不强制） ===

class TestIsEven:
    def test_even_returns_true(self):
        assert is_even(4) is True

    def test_odd_returns_false(self):
        assert is_even(3) is False

    def test_zero_is_even(self):
        assert is_even(0) is True

    @pytest.mark.parametrize("n", [-2, -4, -100])
    def test_negative_even(self, n):
        assert is_even(n) is True
