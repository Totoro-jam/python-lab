"""FastAPI 应用：路由、依赖注入、异常处理。"""

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query

from .models import PaginatedTodos, TodoCreate, TodoResponse, TodoUpdate
from .store import TodoStore

# 全局 store 实例（生产中用 DB session）
_store = TodoStore()


def get_store() -> TodoStore:
    """依赖注入：获取 store 实例。"""
    return _store


def create_app(store: TodoStore | None = None) -> FastAPI:
    """应用工厂，支持注入自定义 store（测试用）。"""
    app = FastAPI(title="Todo API", version="0.1.0")

    if store:
        app.dependency_overrides[get_store] = lambda: store

    @app.post("/todos", response_model=TodoResponse, status_code=201)
    def create_todo(
        body: TodoCreate,
        s: Annotated[TodoStore, Depends(get_store)],
    ) -> TodoResponse:
        item = s.create(title=body.title, description=body.description, priority=body.priority)
        return TodoResponse(
            id=item.id,
            title=item.title,
            description=item.description,
            priority=item.priority,
            completed=item.completed,
            created_at=item.created_at,
        )

    @app.get("/todos", response_model=PaginatedTodos)
    def list_todos(
        s: Annotated[TodoStore, Depends(get_store)],
        page: Annotated[int, Query(ge=1)] = 1,
        page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    ) -> PaginatedTodos:
        items, total = s.list_all(page=page, page_size=page_size)
        return PaginatedTodos(
            items=[
                TodoResponse(
                    id=i.id,
                    title=i.title,
                    description=i.description,
                    priority=i.priority,
                    completed=i.completed,
                    created_at=i.created_at,
                )
                for i in items
            ],
            total=total,
            page=page,
            page_size=page_size,
        )

    @app.get("/todos/{todo_id}", response_model=TodoResponse)
    def get_todo(
        todo_id: int,
        s: Annotated[TodoStore, Depends(get_store)],
    ) -> TodoResponse:
        item = s.get(todo_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        return TodoResponse(
            id=item.id,
            title=item.title,
            description=item.description,
            priority=item.priority,
            completed=item.completed,
            created_at=item.created_at,
        )

    @app.patch("/todos/{todo_id}", response_model=TodoResponse)
    def update_todo(
        todo_id: int,
        body: TodoUpdate,
        s: Annotated[TodoStore, Depends(get_store)],
    ) -> TodoResponse:
        updates = body.model_dump(exclude_unset=True)
        item = s.update(todo_id, **updates)
        if item is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        return TodoResponse(
            id=item.id,
            title=item.title,
            description=item.description,
            priority=item.priority,
            completed=item.completed,
            created_at=item.created_at,
        )

    @app.delete("/todos/{todo_id}", status_code=204)
    def delete_todo(
        todo_id: int,
        s: Annotated[TodoStore, Depends(get_store)],
    ) -> None:
        if not s.delete(todo_id):
            raise HTTPException(status_code=404, detail="Todo not found")

    return app
