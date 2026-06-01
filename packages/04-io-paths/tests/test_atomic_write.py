"""原子写测试。"""

from pathlib import Path

from pylab04.atomic_write import atomic_write_json, atomic_write_text, read_json, read_jsonl


class TestAtomicWrite:
    def test_write_text(self, tmp_path: Path):
        target = tmp_path / "out.txt"
        atomic_write_text(target, "hello world")
        assert target.read_text(encoding="utf-8") == "hello world"

    def test_write_json(self, tmp_path: Path):
        target = tmp_path / "data.json"
        atomic_write_json(target, {"key": "value"})
        result = read_json(target)
        assert result == {"key": "value"}

    def test_write_creates_parent_dirs(self, tmp_path: Path):
        target = tmp_path / "a" / "b" / "c.txt"
        atomic_write_text(target, "nested")
        assert target.read_text(encoding="utf-8") == "nested"

    def test_read_jsonl(self, tmp_path: Path):
        f = tmp_path / "data.jsonl"
        f.write_text('{"a":1}\n{"b":2}\n', encoding="utf-8")
        result = read_jsonl(f)
        assert result == [{"a": 1}, {"b": 2}]
