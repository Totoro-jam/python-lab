"""日志配置工厂：取代 print 的正确姿势。"""

import logging
import sys
from pathlib import Path


def setup_logging(
    level: int = logging.INFO,
    log_file: Path | None = None,
    fmt: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
) -> logging.Logger:
    """配置根 logger，返回一个可用的 logger 实例。

    - 总是输出到 stderr（不干扰 stdout 的数据管道）
    - 可选输出到文件
    """
    logger = logging.getLogger("pylab04")
    logger.setLevel(level)

    # 避免重复添加 handler
    if logger.handlers:
        return logger

    formatter = logging.Formatter(fmt)

    # stderr handler
    console = logging.StreamHandler(sys.stderr)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # 文件 handler（可选）
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
