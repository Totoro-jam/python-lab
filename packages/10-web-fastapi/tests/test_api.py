"""FastAPI 集成测试：使用 TestClient。"""

import pytest
from fastapi.testclient import TestClient

from pylab10.app import create_app
from pylab10.store import TodoStore


@pytest.fixture
def client() -> TestClient:
    """每个测试用独立的 store。"""
    store = TodoStore()
    app = create_app(store=store)
    return TestClient(app)


class TestCreateTodo:
    def test_create_success(self, client: TestClient):
        resp = client.post("/todos", json={"title": "Buy milk", "priority": 2})
        assert resp.status_code == 201
        data = resp.json()
        assert data["title"] == "Buy milk"
        assert data["priority"] == 2
        assert data["completed"] is False
        assert "id" in data

    def test_create_validation_error(self, client: TestClient):
        resp = client.post("/todos", json={"title": "", "priority": 2})
        assert resp.status_code == 422

    def test_create_priority_out_of_range(self, client: TestClient):
        resp = client.post("/todos", json={"title": "x", "priority": 10})
        assert resp.status_code == 422


class TestListTodos:
    def test_empty_list(self, client: TestClient):
        resp = client.get("/todos")
        assert resp.status_code == 200
        data = resp.json()
        assert data["items"] == []
        assert data["total"] == 0

    def test_with_items(self, client: TestClient):
        client.post("/todos", json={"title": "A"})
        client.post("/todos", json={"title": "B"})
        resp = client.get("/todos")
        data = resp.json()
        assert data["total"] == 2
        assert len(data["items"]) == 2

    def test_pagination(self, client: TestClient):
        for i in range(5):
            client.post("/todos", json={"title": f"Item {i}"})
        resp = client.get("/todos?page=1&page_size=2")
        data = resp.json()
        assert len(data["items"]) == 2
        assert data["total"] == 5


class TestGetTodo:
    def test_found(self, client: TestClient):
        create_resp = client.post("/todos", json={"title": "Test"})
        todo_id = create_resp.json()["id"]
        resp = client.get(f"/todos/{todo_id}")
        assert resp.status_code == 200
        assert resp.json()["title"] == "Test"

    def test_not_found(self, client: TestClient):
        resp = client.get("/todos/999")
        assert resp.status_code == 404


class TestUpdateTodo:
    def test_update_title(self, client: TestClient):
        create_resp = client.post("/todos", json={"title": "Old"})
        todo_id = create_resp.json()["id"]
        resp = client.patch(f"/todos/{todo_id}", json={"title": "New"})
        assert resp.status_code == 200
        assert resp.json()["title"] == "New"

    def test_mark_completed(self, client: TestClient):
        create_resp = client.post("/todos", json={"title": "Task"})
        todo_id = create_resp.json()["id"]
        resp = client.patch(f"/todos/{todo_id}", json={"completed": True})
        assert resp.json()["completed"] is True


class TestDeleteTodo:
    def test_delete_success(self, client: TestClient):
        create_resp = client.post("/todos", json={"title": "Del me"})
        todo_id = create_resp.json()["id"]
        resp = client.delete(f"/todos/{todo_id}")
        assert resp.status_code == 204

        # 确认已删除
        resp = client.get(f"/todos/{todo_id}")
        assert resp.status_code == 404

    def test_delete_not_found(self, client: TestClient):
        resp = client.delete("/todos/999")
        assert resp.status_code == 404
