"""数据库引擎和 session 管理。"""

from collections.abc import Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from .models import Base


def create_engine_and_tables(url: str = "sqlite:///:memory:") -> Engine:
    """创建引擎并建表（适合演示和测试）。"""
    engine = create_engine(url, echo=False)
    Base.metadata.create_all(engine)
    return engine


def get_session(engine: Engine) -> Generator[Session, None, None]:
    """session 生成器（适合依赖注入）。"""
    session_factory = sessionmaker(engine)
    with session_factory() as session:
        yield session
