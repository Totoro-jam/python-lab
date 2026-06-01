"""Protocol 演示：结构化子类型（鸭子类型的类型注解版）。"""

import json
from typing import Protocol, runtime_checkable


@runtime_checkable
class Printable(Protocol):
    """任何有 __str__ 方法的对象。"""

    def __str__(self) -> str: ...


@runtime_checkable
class JsonSerializable(Protocol):
    """任何可以序列化为 JSON 的对象。"""

    def to_json(self) -> str: ...


class Config:
    """实现了 JsonSerializable 协议（无需显式继承）。"""

    def __init__(self, data: dict) -> None:
        self.data = data

    def to_json(self) -> str:
        return json.dumps(self.data)

    def __str__(self) -> str:
        return f"Config({self.data})"


def serialize(obj: JsonSerializable) -> str:
    """接受任何实现 to_json 的对象。"""
    return obj.to_json()


def display(obj: Printable) -> str:
    """接受任何有 __str__ 的对象。"""
    return str(obj)
