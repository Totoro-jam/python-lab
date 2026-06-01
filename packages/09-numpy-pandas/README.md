# 09 - NumPy + Pandas: 数据处理基本功

> 数据科学/ML 的两块基石。学完能用向量化思路替代 Python for 循环，能在 DataFrame 上做主流分析操作。

## 前置

- [01-fundamentals](../01-fundamentals), [02-data-structures](../02-data-structures)

## 本章目标

**NumPy**:
- `ndarray` vs Python list（内存布局、类型、广播）
- 向量化与 ufunc（为啥 100 倍快）
- 索引：boolean、fancy、`np.where`
- shape / reshape / axis 的几何直觉

**Pandas**:
- Series / DataFrame / Index
- `read_csv` / `read_parquet` 的常见参数
- `loc` / `iloc` / `at` / `iat`
- `groupby` + `agg`、`merge` 五种 how、`pivot_table`
- 时间序列（`pd.to_datetime`、resample）
- 何时不要用 pandas（→ polars / duckdb）

## 推荐库

- `numpy`, `pandas`, `pyarrow`（parquet）；可选对比 `polars`

## 计划要写

- `src/`: 真实数据集（自带 csv），从 load → clean → groupby → 输出
- `tests/`: 用 `pd.testing.assert_frame_equal`

## 自测

- `arr.shape = (3, 4)` 意味着啥？ `axis=0` 是行还是列？
- pandas 的 `SettingWithCopyWarning` 是怎么来的？怎么避免？
- `merge(how="left")` 和 SQL `LEFT JOIN` 完全等价吗？
- `df.iterrows()` 为啥被劝退？

---

**TODO**: 待补充完整代码与测试。
