"""带重试、超时、日志的 HTTP Client Wrapper。"""

import logging
import time
from dataclasses import dataclass
from typing import Any

import httpx

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class HttpResponse:
    """统一的响应结构。"""

    status_code: int
    body: str
    headers: dict[str, str]
    elapsed_ms: float

    @property
    def ok(self) -> bool:
        return 200 <= self.status_code < 300

    def json(self) -> Any:
        import json
        return json.loads(self.body)


class HttpClient:
    """封装 httpx 的 HTTP 客户端。

    特性:
    - 每个请求都有超时（默认 10s）
    - 可配置重试（仅对 5xx 和网络错误重试）
    - 连接池复用（通过 httpx.Client）
    - 请求/响应日志
    """

    def __init__(
        self,
        base_url: str = "",
        timeout: float = 10.0,
        max_retries: int = 3,
        retry_delay: float = 0.5,
        headers: dict[str, str] | None = None,
    ) -> None:
        self._base_url = base_url
        self._timeout = timeout
        self._max_retries = max_retries
        self._retry_delay = retry_delay
        self._client = httpx.Client(
            base_url=base_url,
            timeout=timeout,
            headers=headers or {},
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "HttpClient":
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    def get(self, path: str, **kwargs: Any) -> HttpResponse:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> HttpResponse:
        return self._request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> HttpResponse:
        return self._request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> HttpResponse:
        return self._request("DELETE", path, **kwargs)

    def _request(self, method: str, path: str, **kwargs: Any) -> HttpResponse:
        """执行请求，支持重试。"""
        last_error: Exception | None = None

        for attempt in range(1, self._max_retries + 1):
            try:
                logger.debug("HTTP %s %s (attempt %d)", method, path, attempt)
                start = time.perf_counter()
                resp = self._client.request(method, path, **kwargs)
                elapsed = (time.perf_counter() - start) * 1000

                result = HttpResponse(
                    status_code=resp.status_code,
                    body=resp.text,
                    headers=dict(resp.headers),
                    elapsed_ms=elapsed,
                )

                # 仅对 5xx 重试
                if resp.status_code >= 500 and attempt < self._max_retries:
                    logger.warning("Server error %d, retrying...", resp.status_code)
                    time.sleep(self._retry_delay)
                    continue

                return result

            except (httpx.ConnectError, httpx.TimeoutException) as e:
                last_error = e
                logger.warning("Request failed: %s (attempt %d)", e, attempt)
                if attempt < self._max_retries:
                    time.sleep(self._retry_delay)

        raise httpx.ConnectError(f"All {self._max_retries} retries failed") from last_error
