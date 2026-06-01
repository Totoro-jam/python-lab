"""原子写：先写临时文件再 rename，避免写到一半崩溃导致文件损坏。"""

import json
import tempfile
from pathlib import Path
from typing import Any


def atomic_write_text(path: Path, content: str, encoding: str = "utf-8") -> None:
    """原子写文本文件。

    策略: 写入同目录临时文件 → fsync → rename（同文件系统 rename 是原子操作）。
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        mode="w",
        dir=path.parent,
        suffix=".tmp",
        delete=False,
        encoding=encoding,
    ) as tmp:
        tmp.write(content)
        tmp.flush()
        # 确保数据落盘
        import os
        os.fsync(tmp.fileno())
        tmp_path = Path(tmp.name)

    tmp_path.rename(path)


def atomic_write_json(path: Path, data: Any, indent: int = 2) -> None:
    """原子写 JSON 文件。"""
    content = json.dumps(data, ensure_ascii=False, indent=indent)
    atomic_write_text(path, content)


def read_json(path: Path) -> Any:
    """读取 JSON 文件，显式指定 UTF-8 编码。"""
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict]:
    """逐行读取 JSONL 文件。"""
    results: list[dict] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                results.append(json.loads(line))
    return results
