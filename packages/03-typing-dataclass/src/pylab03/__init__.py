"""pylab03 — typing, dataclass, pydantic 三种方式定义结构化数据。"""

from .dc_user import DCUser
from .pydantic_user import PydanticUser
from .typed_dict_user import UserDict, create_user_dict
from .protocols import Printable, JsonSerializable

__all__ = [
    "DCUser",
    "PydanticUser",
    "UserDict",
    "create_user_dict",
    "Printable",
    "JsonSerializable",
]
