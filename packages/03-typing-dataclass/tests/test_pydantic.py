"""pydantic User 测试。"""

import pytest
from pydantic import ValidationError

from pylab03.pydantic_user import PydanticUser, PaginatedResponse


class TestPydanticUser:
    def test_valid_user(self):
        u = PydanticUser(name="Alice", email="alice@example.com", age=25)
        assert u.name == "Alice"
        assert u.age == 25

    def test_invalid_email(self):
        with pytest.raises(ValidationError):
            PydanticUser(name="Alice", email="not-an-email", age=25)

    def test_age_negative_rejected(self):
        with pytest.raises(ValidationError):
            PydanticUser(name="Alice", email="a@b.com", age=-1)

    def test_name_stripped(self):
        u = PydanticUser(name="  Alice  ", email="a@b.com", age=25)
        assert u.name == "Alice"

    def test_tags_lowercased(self):
        u = PydanticUser(name="Alice", email="a@b.com", age=25, tags=["Admin", "DEV"])
        assert u.tags == ["admin", "dev"]

    def test_under_13_with_email_rejected(self):
        with pytest.raises(ValidationError, match="under 13"):
            PydanticUser(name="Kid", email="kid@example.com", age=10)

    def test_model_dump(self):
        u = PydanticUser(name="Alice", email="a@b.com", age=25)
        d = u.model_dump(exclude={"created_at"})
        assert d == {"name": "Alice", "email": "a@b.com", "age": 25, "tags": []}

    def test_model_validate(self):
        data = {"name": "Bob", "email": "bob@x.com", "age": 30}
        u = PydanticUser.model_validate(data)
        assert u.name == "Bob"


class TestPaginatedResponse:
    def test_generic_response(self):
        resp = PaginatedResponse[str](items=["a", "b"], total=2)
        assert resp.items == ["a", "b"]
        assert resp.page == 1
