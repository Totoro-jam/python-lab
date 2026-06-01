"""Pandas 测试。"""

import pandas as pd
import pytest
from pylab09.pd_analysis import (
    daily_revenue,
    load_sales_data,
    sales_by_category,
    top_products,
)


@pytest.fixture
def sales_df() -> pd.DataFrame:
    return load_sales_data()


class TestLoadSalesData:
    def test_columns(self, sales_df: pd.DataFrame):
        assert "revenue" in sales_df.columns
        assert "date" in sales_df.columns

    def test_revenue_calculated(self, sales_df: pd.DataFrame):
        row = sales_df.iloc[0]
        assert row["revenue"] == pytest.approx(row["quantity"] * row["price"])

    def test_date_parsed(self, sales_df: pd.DataFrame):
        assert pd.api.types.is_datetime64_any_dtype(sales_df["date"])


class TestSalesByCategory:
    def test_groupby(self, sales_df: pd.DataFrame):
        result = sales_by_category(sales_df)
        assert len(result) == 3  # Electronics, Home, Tools
        assert result.columns.tolist() == ["category", "total_quantity", "total_revenue"]
        # Electronics 收入应最高
        assert result.iloc[0]["category"] == "Electronics"


class TestTopProducts:
    def test_top_3(self, sales_df: pd.DataFrame):
        result = top_products(sales_df, n=3)
        assert len(result) == 3
        assert "total_revenue" in result.columns


class TestDailyRevenue:
    def test_daily(self, sales_df: pd.DataFrame):
        result = daily_revenue(sales_df)
        assert len(result) == 5  # 5 unique dates
        assert result["revenue"].sum() == pytest.approx(sales_df["revenue"].sum())
