"""CRUD 操作层：select() 表达式风格。"""

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from .models import Post, User


class UserCRUD:
    """User 增删改查。"""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, name: str, email: str) -> User:
        user = User(name=name, email=email)
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> User | None:
        return self._session.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self._session.scalars(stmt).first()

    def list_active(self) -> list[User]:
        stmt = select(User).where(User.active.is_(True)).order_by(User.name)
        return list(self._session.scalars(stmt).all())

    def get_with_posts(self, user_id: int) -> User | None:
        """使用 selectinload 防止 N+1。"""
        stmt = (
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.posts))
        )
        return self._session.scalars(stmt).first()

    def deactivate(self, user_id: int) -> User | None:
        user = self.get_by_id(user_id)
        if user is None:
            return None
        user.active = False
        self._session.commit()
        return user

    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if user is None:
            return False
        self._session.delete(user)
        self._session.commit()
        return True


class PostCRUD:
    """Post 增删改查。"""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, title: str, author_id: int, content: str = "") -> Post:
        post = Post(title=title, author_id=author_id, content=content)
        self._session.add(post)
        self._session.commit()
        self._session.refresh(post)
        return post

    def get_by_id(self, post_id: int) -> Post | None:
        return self._session.get(Post, post_id)

    def list_by_author(self, author_id: int) -> list[Post]:
        stmt = select(Post).where(Post.author_id == author_id).order_by(Post.created_at.desc())
        return list(self._session.scalars(stmt).all())

    def publish(self, post_id: int) -> Post | None:
        post = self.get_by_id(post_id)
        if post is None:
            return None
        post.published = True
        self._session.commit()
        return post
