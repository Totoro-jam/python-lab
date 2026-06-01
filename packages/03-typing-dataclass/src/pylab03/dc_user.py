"""dataclass 方式定义 User。

演示: frozen, slots, field(default_factory), replace, asdict。
"""

from dataclasses import asdict, dataclass, field, replace
from datetime import datetime


@dataclass(frozen=True, slots=True)
class DCUser:
    """不可变 User，使用 slots 节省内存。"""

    name: str
    email: str
    age: int
    tags: tuple[str, ...] = ()
    created_at: datetime = field(default_factory=datetime.now)

    def with_tag(self, tag: str) -> "DCUser":
        """返回添加了新 tag 的副本（frozen 不可变，需要 replace）。"""
        return replace(self, tags=(*self.tags, tag))

    def to_dict(self) -> dict:
        """转为字典。"""
        return asdict(self)


@dataclass(slots=True)
class Address:
    """嵌套 dataclass 演示。"""

    street: str
    city: str
    zipcode: str = ""


@dataclass(slots=True)
class UserWithAddress:
    """组合 dataclass。"""

    user: DCUser
    address: Address
