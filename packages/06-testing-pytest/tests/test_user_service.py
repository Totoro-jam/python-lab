"""UserService 测试：fixture 工厂、monkeypatch、parametrize。"""

import pytest
from pylab06.user_service import InMemoryUserRepo, User, UserService

# --- Fixture 工厂模式 ---


@pytest.fixture
def repo() -> InMemoryUserRepo:
    return InMemoryUserRepo()


@pytest.fixture
def service(repo: InMemoryUserRepo) -> UserService:
    return UserService(repo=repo)


@pytest.fixture
def user_factory(service: UserService):
    """Fixture 工厂：返回一个创建用户的函数。"""

    def _create(name: str = "Alice", email: str = "alice@example.com") -> User:
        return service.register(name, email)

    return _create


# --- 基础测试 ---


class TestRegister:
    def test_register_success(self, service: UserService):
        user = service.register("Bob", "bob@example.com")
        assert user.name == "Bob"
        assert user.id > 0

    def test_register_strips_name(self, service: UserService):
        user = service.register("  Alice  ", "a@b.com")
        assert user.name == "Alice"

    @pytest.mark.parametrize(
        ("name", "email", "error_match"),
        [
            ("", "a@b.com", "name cannot be empty"),
            ("   ", "a@b.com", "name cannot be empty"),
            ("Alice", "invalid", "invalid email"),
        ],
        ids=["empty-name", "blank-name", "bad-email"],
    )
    def test_register_validation(
        self, service: UserService, name: str, email: str, error_match: str
    ):
        with pytest.raises(ValueError, match=error_match):
            service.register(name, email)


class TestGetUser:
    def test_found(self, service: UserService, user_factory):
        created = user_factory()
        found = service.get_user(created.id)
        assert found == created

    def test_not_found(self, service: UserService):
        with pytest.raises(LookupError, match="not found"):
            service.get_user(999)


class TestDeactivate:
    def test_deactivate(self, service: UserService, user_factory):
        user = user_factory()
        deactivated = service.deactivate(user.id)
        assert deactivated.active is False
        assert deactivated.id == user.id
