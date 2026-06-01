"""日志工厂测试。"""

import logging
from pathlib import Path

from pylab04.log_factory import setup_logging


class TestLogging:
    def test_basic_setup(self):
        logger = setup_logging(level=logging.DEBUG)
        assert logger.name == "pylab04"
        assert logger.level == logging.DEBUG

    def test_file_handler(self, tmp_path: Path):
        log_file = tmp_path / "app.log"
        logger = setup_logging(log_file=log_file)
        # 由于 logger 可能已经创建过，清理后重新测试
        logger.handlers.clear()
        logger = setup_logging(log_file=log_file)
        logger.info("test message")

        # 确保文件被创建且有内容
        assert log_file.exists()
        content = log_file.read_text(encoding="utf-8")
        assert "test message" in content
