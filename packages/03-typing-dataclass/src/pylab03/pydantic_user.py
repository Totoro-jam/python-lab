"""pydantic v2 方式定义 User。

演示: BaseModel, Field, validator, model_validator, model_dump, model_validate。
"""

from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field, field_validator, model_validator

T = TypeVar("T")


class PydanticUser(BaseModel):
    """带运行时校验的 User。"""

    name: str = Field(min_length=1, max_length=50)
    email: str = Field(pattern=r"^[\w.+-]+@[\w-]+\.[\w.]+$")
    age: int = Field(ge=0, le=150)
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name cannot be blank")
        return v.strip()

    @field_validator("tags")
    @classmethod
    def tags_lowercase(cls, v: list[str]) -> list[str]:
        return [tag.lower() for tag in v]

    @model_validator(mode="after")
    def check_age_for_email(self) -> "PydanticUser":
        """13 岁以下不允许注册邮箱（演示 model_validator）。"""
        if self.age < 13 and self.email:
            raise ValueError("users under 13 cannot register with email")
        return self


class PaginatedResponse(BaseModel, Generic[T]):
    """泛型分页响应（pydantic v2 支持 Generic）。"""

    items: list[T]
    total: int
    page: int = 1
    page_size: int = 20
