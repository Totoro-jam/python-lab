"""内存存储层（演示用，生产用数据库）。"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class TodoItem:
    id: int
    title: str
    description: str
    priority: int
    completed: bool
    created_at: datetime


class TodoStore:
    """线程安全的内存 Todo 存储。"""

    def __init__(self) -> None:
        self._items: dict[int, TodoItem] = {}
        self._next_id = 1

    def create(self, title: str, description: str = "", priority: int = 0) -> TodoItem:
        item = TodoItem(
            id=self._next_id,
            title=title,
            description=description,
            priority=priority,
            completed=False,
            created_at=datetime.now(),
        )
        self._items[item.id] = item
        self._next_id += 1
        return item

    def get(self, todo_id: int) -> TodoItem | None:
        return self._items.get(todo_id)

    def list_all(self, page: int = 1, page_size: int = 20) -> tuple[list[TodoItem], int]:
        all_items = sorted(self._items.values(), key=lambda x: x.created_at, reverse=True)
        total = len(all_items)
        start = (page - 1) * page_size
        return all_items[start : start + page_size], total

    def update(self, todo_id: int, **kwargs) -> TodoItem | None:
        item = self._items.get(todo_id)
        if item is None:
            return None
        for key, value in kwargs.items():
            if value is not None and hasattr(item, key):
                object.__setattr__(item, key, value)
        return item

    def delete(self, todo_id: int) -> bool:
        return self._items.pop(todo_id, None) is not None
