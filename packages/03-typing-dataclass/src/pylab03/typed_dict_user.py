"""TypedDict 方式定义 User。

TypedDict 只做类型注解，不做运行时校验，适合 JSON 数据的类型标注。
"""

from typing import NotRequired, Required, TypedDict


class UserDict(TypedDict):
    """TypedDict: 仅类型检查，无运行时开销。"""

    name: Required[str]
    email: Required[str]
    age: Required[int]
    tags: NotRequired[list[str]]


def create_user_dict(name: str, email: str, age: int) -> UserDict:
    """工厂函数创建 UserDict。"""
    return UserDict(name=name, email=email, age=age)


class PartialUserDict(TypedDict, total=False):
    """所有字段可选的 User（用于 PATCH 更新）。"""

    name: str
    email: str
    age: int
    tags: list[str]
