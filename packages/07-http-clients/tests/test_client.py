"""HTTP Client 测试（使用 respx mock httpx）。"""

import pytest

try:
    import respx
    from httpx import Response

    HAS_RESPX = True
except ImportError:
    HAS_RESPX = False

from pylab07.client import HttpClient


@pytest.mark.skipif(not HAS_RESPX, reason="respx not installed")
class TestHttpClient:
    @respx.mock
    def test_get_success(self):
        respx.get("https://api.example.com/users").mock(
            return_value=Response(200, json={"users": []})
        )
        with HttpClient(base_url="https://api.example.com") as client:
            resp = client.get("/users")
            assert resp.ok
            assert resp.status_code == 200
            assert resp.json() == {"users": []}

    @respx.mock
    def test_post_success(self):
        respx.post("https://api.example.com/users").mock(
            return_value=Response(201, json={"id": 1})
        )
        with HttpClient(base_url="https://api.example.com") as client:
            resp = client.post("/users", json={"name": "Alice"})
            assert resp.status_code == 201

    @respx.mock
    def test_404_not_retried(self):
        route = respx.get("https://api.example.com/missing").mock(
            return_value=Response(404, text="not found")
        )
        with HttpClient(base_url="https://api.example.com", max_retries=3) as client:
            resp = client.get("/missing")
            assert resp.status_code == 404
            assert route.call_count == 1  # 4xx 不重试

    @respx.mock
    def test_500_retried(self):
        route = respx.get("https://api.example.com/fail").mock(
            return_value=Response(500, text="error")
        )
        with HttpClient(
            base_url="https://api.example.com",
            max_retries=3,
            retry_delay=0.01,
        ) as client:
            resp = client.get("/fail")
            assert resp.status_code == 500
            assert route.call_count == 3  # 重试 3 次

    @respx.mock
    def test_elapsed_tracked(self):
        respx.get("https://api.example.com/ping").mock(
            return_value=Response(200, text="pong")
        )
        with HttpClient(base_url="https://api.example.com") as client:
            resp = client.get("/ping")
            assert resp.elapsed_ms >= 0
