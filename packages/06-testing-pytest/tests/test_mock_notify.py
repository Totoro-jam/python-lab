"""Mock 演示：unittest.mock 模拟外部依赖。"""

import os
from unittest.mock import Mock

from pylab06.user_service import InMemoryUserRepo, UserService


class TestNotification:
    def test_welcome_sent_on_register(self):
        """验证注册时调用了通知服务。"""
        repo = InMemoryUserRepo()
        mock_notifier = Mock()
        mock_notifier.send_welcome.return_value = True

        service = UserService(repo=repo, notifier=mock_notifier)
        service.register("Alice", "alice@example.com")

        mock_notifier.send_welcome.assert_called_once_with("alice@example.com")

    def test_notifier_called_with_correct_email(self):
        """多次注册，验证每次调用正确。"""
        repo = InMemoryUserRepo()
        mock_notifier = Mock()
        service = UserService(repo=repo, notifier=mock_notifier)

        service.register("A", "a@x.com")
        service.register("B", "b@x.com")

        assert mock_notifier.send_welcome.call_count == 2

    def test_register_works_without_notifier(self):
        """没有 notifier 也能注册。"""
        repo = InMemoryUserRepo()
        service = UserService(repo=repo, notifier=None)
        user = service.register("Bob", "bob@example.com")
        assert user.name == "Bob"


class TestMonkeypatch:
    def test_env_variable(self, monkeypatch):
        """monkeypatch 修改环境变量。"""
        monkeypatch.setenv("APP_ENV", "testing")
        assert os.environ["APP_ENV"] == "testing"

    def test_capsys(self, capsys):
        """capsys 捕获 stdout。"""
        print("hello")
        captured = capsys.readouterr()
        assert captured.out == "hello\n"

    def test_monkeypatch_attr(self, monkeypatch):
        """monkeypatch 修改模块属性。"""
        import pylab06.user_service as mod

        monkeypatch.setattr(mod, "__name__", "patched")
        assert mod.__name__ == "patched"
