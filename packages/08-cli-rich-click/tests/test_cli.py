"""CLI 测试：使用 typer.testing.CliRunner。"""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from pylab08.cli import app

runner = CliRunner()


class TestStats:
    def test_current_dir(self, tmp_path: Path):
        (tmp_path / "a.txt").write_text("hello")
        (tmp_path / "b.py").write_text("world")
        result = runner.invoke(app, ["stats", str(tmp_path)])
        assert result.exit_code == 0
        assert "2" in result.output  # 2 files

    def test_with_pattern(self, tmp_path: Path):
        (tmp_path / "a.txt").write_text("hello")
        (tmp_path / "b.py").write_text("world")
        result = runner.invoke(app, ["stats", str(tmp_path), "--pattern", "*.py"])
        assert result.exit_code == 0
        assert "1" in result.output

    def test_not_a_directory(self):
        result = runner.invoke(app, ["stats", "/nonexistent_path_xyz"])
        assert result.exit_code == 1

    def test_table_output(self, tmp_path: Path):
        (tmp_path / "test.txt").write_text("data")
        result = runner.invoke(app, ["stats", str(tmp_path), "--table"])
        assert result.exit_code == 0
        assert "test.txt" in result.output


class TestFind:
    def test_find_by_name(self, tmp_path: Path):
        (tmp_path / "readme.md").write_text("# hi")
        (tmp_path / "other.txt").write_text("x")
        result = runner.invoke(app, ["find", str(tmp_path), "--name", "readme"])
        assert result.exit_code == 0
        assert "readme.md" in result.output

    def test_find_by_suffix(self, tmp_path: Path):
        (tmp_path / "a.py").write_text("x")
        (tmp_path / "b.txt").write_text("y")
        result = runner.invoke(app, ["find", str(tmp_path), "--suffix", ".py"])
        assert result.exit_code == 0
        assert "a.py" in result.output
        assert "b.txt" not in result.output


class TestVersion:
    def test_version(self):
        result = runner.invoke(app, ["version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output
