"""ORM 测试：SQLite in-memory + transaction rollback per test。"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from pylab11.models import Base, Post, User
from pylab11.crud import PostCRUD, UserCRUD


@pytest.fixture
def session():
    """每个测试独立的 in-memory SQLite session。"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with sessionmaker(engine)() as sess:
        yield sess


@pytest.fixture
def user_crud(session: Session) -> UserCRUD:
    return UserCRUD(session)


@pytest.fixture
def post_crud(session: Session) -> PostCRUD:
    return PostCRUD(session)


class TestUserCRUD:
    def test_create_and_get(self, user_crud: UserCRUD):
        user = user_crud.create("Alice", "alice@example.com")
        assert user.id is not None
        assert user.name == "Alice"

        found = user_crud.get_by_id(user.id)
        assert found is not None
        assert found.email == "alice@example.com"

    def test_get_by_email(self, user_crud: UserCRUD):
        user_crud.create("Bob", "bob@example.com")
        found = user_crud.get_by_email("bob@example.com")
        assert found is not None
        assert found.name == "Bob"

    def test_list_active(self, user_crud: UserCRUD):
        user_crud.create("A", "a@x.com")
        user_crud.create("B", "b@x.com")
        active = user_crud.list_active()
        assert len(active) == 2

    def test_deactivate(self, user_crud: UserCRUD):
        user = user_crud.create("Alice", "alice@x.com")
        user_crud.deactivate(user.id)
        active = user_crud.list_active()
        assert len(active) == 0

    def test_delete_cascades_posts(self, user_crud: UserCRUD, post_crud: PostCRUD):
        user = user_crud.create("Alice", "alice@x.com")
        post_crud.create("Post 1", user.id)
        user_crud.delete(user.id)
        # Post 应该被级联删除
        assert post_crud.get_by_id(1) is None

    def test_get_nonexistent(self, user_crud: UserCRUD):
        assert user_crud.get_by_id(999) is None


class TestPostCRUD:
    def test_create_and_get(self, user_crud: UserCRUD, post_crud: PostCRUD):
        user = user_crud.create("Alice", "alice@x.com")
        post = post_crud.create("My Post", user.id, content="Hello world")
        assert post.id is not None
        assert post.title == "My Post"
        assert post.published is False

    def test_list_by_author(self, user_crud: UserCRUD, post_crud: PostCRUD):
        user = user_crud.create("Alice", "alice@x.com")
        post_crud.create("Post 1", user.id)
        post_crud.create("Post 2", user.id)
        posts = post_crud.list_by_author(user.id)
        assert len(posts) == 2

    def test_publish(self, user_crud: UserCRUD, post_crud: PostCRUD):
        user = user_crud.create("Alice", "alice@x.com")
        post = post_crud.create("Draft", user.id)
        published = post_crud.publish(post.id)
        assert published is not None
        assert published.published is True


class TestRelationships:
    def test_user_posts_relationship(self, user_crud: UserCRUD, post_crud: PostCRUD):
        user = user_crud.create("Alice", "alice@x.com")
        post_crud.create("Post A", user.id)
        post_crud.create("Post B", user.id)

        user_with_posts = user_crud.get_with_posts(user.id)
        assert user_with_posts is not None
        assert len(user_with_posts.posts) == 2

    def test_post_author_relationship(self, user_crud: UserCRUD, post_crud: PostCRUD, session: Session):
        user = user_crud.create("Alice", "alice@x.com")
        post = post_crud.create("My Post", user.id)
        # 通过 post.author 反向获取 User
        assert post.author.name == "Alice"
