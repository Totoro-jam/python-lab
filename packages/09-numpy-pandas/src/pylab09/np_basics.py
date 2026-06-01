"""NumPy 基础：向量化、broadcasting、boolean indexing。"""

import numpy as np
from numpy.typing import NDArray


def vectorized_distance(
    points: NDArray[np.float64],
    origin: NDArray[np.float64] | None = None,
) -> NDArray[np.float64]:
    """计算点集到原点的欧氏距离（向量化，无 for 循环）。

    points: shape (n, d) — n 个 d 维点
    origin: shape (d,) — 可选原点，默认零点
    """
    if origin is None:
        origin = np.zeros(points.shape[1])
    diff = points - origin  # broadcasting
    return np.sqrt(np.sum(diff**2, axis=1))


def boolean_mask_filter(
    arr: NDArray[np.float64],
    low: float,
    high: float,
) -> NDArray[np.float64]:
    """Boolean indexing: 保留 [low, high] 范围内的元素。"""
    mask = (arr >= low) & (arr <= high)
    return arr[mask]


def moving_average(arr: NDArray[np.float64], window: int) -> NDArray[np.float64]:
    """滑动平均（使用 np.convolve）。"""
    kernel = np.ones(window) / window
    # 'valid' 模式只返回完全重叠的部分
    return np.convolve(arr, kernel, mode="valid")


def normalize(arr: NDArray[np.float64]) -> NDArray[np.float64]:
    """Min-max 归一化到 [0, 1]。"""
    min_val = arr.min()
    max_val = arr.max()
    if max_val == min_val:
        return np.zeros_like(arr)
    return (arr - min_val) / (max_val - min_val)


def fancy_indexing_demo() -> NDArray[np.int64]:
    """Fancy indexing 演示：用整数数组选行。"""
    data = np.arange(20).reshape(4, 5)
    # 选第 0, 2, 3 行
    indices = np.array([0, 2, 3])
    return data[indices]
