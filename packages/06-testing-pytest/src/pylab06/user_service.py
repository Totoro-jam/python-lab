"""带外部依赖的服务层：演示如何通过接口隔离做到可测试。"""

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True, slots=True)
class User:
    id: int
    name: str
    email: str
    active: bool = True


class UserRepo(Protocol):
    """用户仓储接口（Protocol 让 mock 更自然）。"""

    def get_by_id(self, user_id: int) -> User | None: ...
    def save(self, user: User) -> User: ...
    def list_active(self) -> list[User]: ...


class InMemoryUserRepo:
    """内存实现，用于测试。"""

    def __init__(self) -> None:
        self._store: dict[int, User] = {}
        self._next_id: int = 1

    def get_by_id(self, user_id: int) -> User | None:
        return self._store.get(user_id)

    def save(self, user: User) -> User:
        if user.id == 0:
            user = User(id=self._next_id, name=user.name, email=user.email, active=user.active)
            self._next_id += 1
        self._store[user.id] = user
        return user

    def list_active(self) -> list[User]:
        return [u for u in self._store.values() if u.active]


class NotificationService(Protocol):
    """通知服务接口。"""

    def send_welcome(self, email: str) -> bool: ...


class UserService:
    """业务逻辑层，依赖注入 repo 和 notifier。"""

    def __init__(self, repo: UserRepo, notifier: NotificationService | None = None) -> None:
        self._repo = repo
        self._notifier = notifier

    def register(self, name: str, email: str) -> User:
        """注册用户并发送欢迎通知。"""
        if not name.strip():
            raise ValueError("name cannot be empty")
        if "@" not in email:
            raise ValueError("invalid email")

        user = self._repo.save(User(id=0, name=name.strip(), email=email))

        if self._notifier:
            self._notifier.send_welcome(email)

        return user

    def get_user(self, user_id: int) -> User:
        """获取用户，不存在则抛异常。"""
        user = self._repo.get_by_id(user_id)
        if user is None:
            raise LookupError(f"user {user_id} not found")
        return user

    def deactivate(self, user_id: int) -> User:
        """停用用户。"""
        user = self.get_user(user_id)
        deactivated = User(id=user.id, name=user.name, email=user.email, active=False)
        return self._repo.save(deactivated)
