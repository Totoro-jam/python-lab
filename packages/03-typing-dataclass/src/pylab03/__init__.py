"""pylab03 — typing, dataclass, pydantic 三种方式定义结构化数据。"""

from .dc_user import DCUser
from .protocols import JsonSerializable, Printable
from .pydantic_user import PydanticUser
from .typed_dict_user import UserDict, create_user_dict

__all__ = [
    "DCUser",
    "PydanticUser",
    "UserDict",
    "create_user_dict",
    "Printable",
    "JsonSerializable",
]
