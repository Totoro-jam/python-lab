"""Pydantic 模型：请求/响应 schema。"""

from datetime import datetime
from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    """创建 Todo 的请求体。"""
    title: str = Field(min_length=1, max_length=200)
    description: str = ""
    priority: int = Field(default=0, ge=0, le=5)


class TodoUpdate(BaseModel):
    """更新 Todo 的请求体（所有字段可选）。"""
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    priority: int | None = Field(default=None, ge=0, le=5)
    completed: bool | None = None


class TodoResponse(BaseModel):
    """Todo 响应体。"""
    id: int
    title: str
    description: str
    priority: int
    completed: bool
    created_at: datetime


class PaginatedTodos(BaseModel):
    """分页列表响应。"""
    items: list[TodoResponse]
    total: int
    page: int
    page_size: int
