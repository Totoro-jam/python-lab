"""Pandas 数据分析：load, clean, groupby, merge。"""

import io

import pandas as pd

# 内嵌 CSV 数据（避免外部文件依赖）
_SALES_CSV = """\
date,product,category,quantity,price
2024-01-01,Widget A,Electronics,10,29.99
2024-01-01,Widget B,Electronics,5,49.99
2024-01-02,Gadget X,Home,8,19.99
2024-01-02,Widget A,Electronics,12,29.99
2024-01-03,Gadget Y,Home,3,39.99
2024-01-03,Widget B,Electronics,7,49.99
2024-01-04,Tool Z,Tools,15,9.99
2024-01-04,Widget A,Electronics,6,29.99
2024-01-05,Gadget X,Home,20,19.99
2024-01-05,Tool Z,Tools,10,9.99
"""


def load_sales_data() -> pd.DataFrame:
    """加载示例销售数据，返回清洗后的 DataFrame。"""
    df = pd.read_csv(io.StringIO(_SALES_CSV), parse_dates=["date"])
    df["revenue"] = df["quantity"] * df["price"]
    return df


def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """按类别汇总：总销量、总收入。"""
    return (
        df.groupby("category", as_index=False)
        .agg(
            total_quantity=("quantity", "sum"),
            total_revenue=("revenue", "sum"),
        )
        .sort_values("total_revenue", ascending=False)
        .reset_index(drop=True)
    )


def top_products(df: pd.DataFrame, n: int = 3) -> pd.DataFrame:
    """收入 Top N 产品。"""
    return (
        df.groupby("product", as_index=False)
        .agg(total_revenue=("revenue", "sum"))
        .nlargest(n, "total_revenue")
        .reset_index(drop=True)
    )


def daily_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """按日汇总收入（时间序列）。"""
    return df.groupby("date", as_index=False).agg(revenue=("revenue", "sum"))
