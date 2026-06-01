"""CSV 读写测试。"""

from pathlib import Path

from pylab04.csv_stream import csv_to_dicts, stream_csv, write_csv


class TestCSV:
    def test_write_and_read(self, tmp_path: Path):
        target = tmp_path / "test.csv"
        rows = [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]
        write_csv(target, rows, fieldnames=["name", "age"])

        result = csv_to_dicts(target)
        assert len(result) == 2
        assert result[0]["name"] == "Alice"

    def test_stream_csv(self, tmp_path: Path):
        target = tmp_path / "stream.csv"
        target.write_text("x,y\n1,2\n3,4\n", encoding="utf-8")

        rows = list(stream_csv(target))
        assert rows == [{"x": "1", "y": "2"}, {"x": "3", "y": "4"}]

    def test_empty_csv(self, tmp_path: Path):
        target = tmp_path / "empty.csv"
        target.write_text("col1,col2\n", encoding="utf-8")
        assert list(stream_csv(target)) == []
