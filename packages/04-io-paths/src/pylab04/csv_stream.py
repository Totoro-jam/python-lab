"""CSV 流式读写：正确处理编码和换行。"""

import csv
from collections.abc import Generator
from pathlib import Path


def stream_csv(path: Path) -> Generator[dict[str, str], None, None]:
    """流式逐行读取 CSV（DictReader）。

    关键: newline="" 交给 csv 模块处理换行，encoding="utf-8" 显式指定。
    """
    with path.open(mode="r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    """写 CSV 文件。"""
    with path.open(mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_to_dicts(path: Path) -> list[dict[str, str]]:
    """一次性读取小 CSV 到内存。"""
    return list(stream_csv(path))
