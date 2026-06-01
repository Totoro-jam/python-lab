"""惰性流处理测试。"""

from pathlib import Path

from pylab02.lazy_stream import (
    chunked,
    compose_pipeline,
    fibonacci,
    flatten,
    make_multiplier,
    running_total,
    stream_large_file,
)


class TestChunked:
    def test_even_split(self):
        assert list(chunked([1, 2, 3, 4], 2)) == [[1, 2], [3, 4]]

    def test_uneven_split(self):
        assert list(chunked([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]

    def test_empty(self):
        assert list(chunked([], 3)) == []


class TestStreamLargeFile:
    def test_reads_lines(self, tmp_path: Path):
        f = tmp_path / "data.txt"
        f.write_text("line1\nline2\nline3\n", encoding="utf-8")
        result = list(stream_large_file(f))
        assert result == ["line1", "line2", "line3"]


class TestFlatten:
    def test_basic(self):
        assert list(flatten([[1, 2], [3], [4, 5]])) == [1, 2, 3, 4, 5]


class TestRunningTotal:
    def test_basic(self):
        assert running_total([1, 2, 3, 4]) == [1, 3, 6, 10]


class TestFibonacci:
    def test_base_cases(self):
        assert fibonacci(0) == 0
        assert fibonacci(1) == 1

    def test_larger(self):
        assert fibonacci(10) == 55


class TestMakeMultiplier:
    def test_basic(self):
        double = make_multiplier(2)
        assert double(5) == 10


class TestComposePipeline:
    def test_basic(self):
        def add_one(x):
            return x + 1

        def double(x):
            return x * 2

        pipeline = compose_pipeline(add_one, double)
        assert pipeline(3) == 8  # (3+1)*2
