"""hypothesis 属性测试：让框架帮你找 corner case。"""

import pytest

hypothesis = pytest.importorskip("hypothesis")
from hypothesis import given, assume, settings  # noqa: E402
from hypothesis import strategies as st  # noqa: E402

from pylab06.user_service import InMemoryUserRepo, UserService


class TestHypothesis:
    @given(
        name=st.text(min_size=1, max_size=50).filter(lambda s: s.strip()),
        email=st.from_regex(r"[a-z]+@[a-z]+\.[a-z]+", fullmatch=True),
    )
    @settings(max_examples=30)
    def test_register_never_crashes(self, name: str, email: str):
        """任意合法输入都不应导致未处理异常。"""
        repo = InMemoryUserRepo()
        service = UserService(repo=repo)
        user = service.register(name, email)
        assert user.id > 0
        assert user.email == email

    @given(n=st.integers(min_value=0, max_value=50))
    @settings(max_examples=20)
    def test_list_active_count(self, n: int):
        """注册 n 个用户后，active 列表长度 == n。"""
        repo = InMemoryUserRepo()
        service = UserService(repo=repo)
        for i in range(n):
            service.register(f"user{i}", f"user{i}@test.com")
        assert len(repo.list_active()) == n
