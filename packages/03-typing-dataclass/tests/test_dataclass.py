"""dataclass User 测试。"""

import pytest
from pylab03.dc_user import DCUser


class TestDCUser:
    def test_create(self):
        u = DCUser(name="Alice", email="a@b.com", age=30)
        assert u.name == "Alice"
        assert u.age == 30

    def test_frozen_cannot_mutate(self):
        u = DCUser(name="Bob", email="b@b.com", age=25)
        with pytest.raises(AttributeError):
            u.name = "Charlie"  # type: ignore[misc]

    def test_with_tag(self):
        u = DCUser(name="Alice", email="a@b.com", age=30)
        u2 = u.with_tag("admin")
        assert u2.tags == ("admin",)
        assert u.tags == ()  # 原对象不变

    def test_to_dict(self):
        u = DCUser(name="Alice", email="a@b.com", age=30, tags=("dev",))
        d = u.to_dict()
        assert d["name"] == "Alice"
        assert d["tags"] == ("dev",)

    def test_slots_no_dict(self):
        u = DCUser(name="Alice", email="a@b.com", age=30)
        assert not hasattr(u, "__dict__")
