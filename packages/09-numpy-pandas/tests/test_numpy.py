"""NumPy 测试。"""

import numpy as np
import pytest

from pylab09.np_basics import (
    boolean_mask_filter,
    moving_average,
    normalize,
    vectorized_distance,
)


class TestVectorizedDistance:
    def test_2d_points(self):
        points = np.array([[3.0, 4.0], [0.0, 0.0], [1.0, 0.0]])
        result = vectorized_distance(points)
        expected = np.array([5.0, 0.0, 1.0])
        np.testing.assert_allclose(result, expected)

    def test_with_origin(self):
        points = np.array([[4.0, 0.0]])
        origin = np.array([1.0, 0.0])
        result = vectorized_distance(points, origin)
        np.testing.assert_allclose(result, [3.0])


class TestBooleanMask:
    def test_filter_range(self):
        arr = np.array([1.0, 5.0, 3.0, 8.0, 2.0])
        result = boolean_mask_filter(arr, 2.0, 5.0)
        expected = np.array([5.0, 3.0, 2.0])
        np.testing.assert_array_equal(result, expected)

    def test_empty_result(self):
        arr = np.array([1.0, 2.0, 3.0])
        result = boolean_mask_filter(arr, 10.0, 20.0)
        assert len(result) == 0


class TestMovingAverage:
    def test_basic(self):
        arr = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        result = moving_average(arr, 3)
        expected = np.array([2.0, 3.0, 4.0])
        np.testing.assert_allclose(result, expected)


class TestNormalize:
    def test_basic(self):
        arr = np.array([0.0, 5.0, 10.0])
        result = normalize(arr)
        np.testing.assert_allclose(result, [0.0, 0.5, 1.0])

    def test_constant_array(self):
        arr = np.array([3.0, 3.0, 3.0])
        result = normalize(arr)
        np.testing.assert_array_equal(result, [0.0, 0.0, 0.0])
