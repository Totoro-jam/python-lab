"""容器工具测试。"""

import pytest

from pylab02.containers import (
    group_by_key,
    insort_demo,
    merge_sorted,
    sliding_window,
    top_n_words,
)


class TestTopNWords:
    def test_basic(self):
        text = "apple banana apple cherry banana apple"
        result = top_n_words(text, 2)
        assert result == [("apple", 3), ("banana", 2)]

    def test_empty(self):
        assert top_n_words("", 3) == []

    def test_case_insensitive(self):
        text = "Hello hello HELLO"
        assert top_n_words(text, 1) == [("hello", 3)]


class TestGroupByKey:
    def test_basic(self):
        items = [("a", 1), ("b", 2), ("a", 3)]
        result = group_by_key(items)
        assert result == {"a": [1, 3], "b": [2]}

    def test_empty(self):
        assert group_by_key([]) == {}


class TestSlidingWindow:
    def test_basic(self):
        result = list(sliding_window([1, 2, 3, 4, 5], 3))
        assert result == [(1, 2, 3), (2, 3, 4), (3, 4, 5)]

    def test_window_equals_length(self):
        result = list(sliding_window([1, 2, 3], 3))
        assert result == [(1, 2, 3)]

    def test_window_larger_than_input(self):
        result = list(sliding_window([1, 2], 5))
        assert result == []


class TestMergeSorted:
    def test_basic(self):
        assert merge_sorted([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]

    def test_empty(self):
        assert merge_sorted([], [1, 2]) == [1, 2]


class TestInsort:
    def test_basic(self):
        assert insort_demo([1, 3, 5], 4) == [1, 3, 4, 5]
