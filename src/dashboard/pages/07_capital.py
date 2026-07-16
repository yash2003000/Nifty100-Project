import streamlit as st
import pandas as pd
import plotly.express as px

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from utils.db import (
    get_companies,
    get_market_cap
)

import sqlite3

st.title("🏦 Capital Structure Analysis")

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------

conn = sqlite3.connect("db/nifty100.db")

companies = get_companies()
market = get_market_cap()

bs = pd.read_sql(
    "SELECT * FROM balancesheet",
    conn
)

# ---------------------------------------------------
# Latest Balance Sheet Record per Company
# ---------------------------------------------------

bs_latest = (
    bs.sort_values("year")
      .groupby("company_id")
      .tail(1)
)

market_latest = (
    market.sort_values("year")
          .groupby("company_id")
          .tail(1)
)

# ---------------------------------------------------
# Merge
# ---------------------------------------------------

df = bs_latest.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

df = df.merge(
    market_latest[
        [
            "company_id",
            "market_cap_crore"
        ]
    ],
    on="company_id",
    how="left"
)

# ---------------------------------------------------
# Clean Data
# ---------------------------------------------------

numeric_cols = [
    "equity_capital",
    "reserves",
    "borrowings",
    "total_assets",
    "market_cap_crore"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

# ---------------------------------------------------
# Debt vs Equity Bubble Chart
# ---------------------------------------------------

st.subheader("Debt vs Equity Structure")

chart_df = df.dropna(
    subset=[
        "borrowings",
        "equity_capital",
        "market_cap_crore"
    ]
)

chart_df = chart_df[
    chart_df["market_cap_crore"] > 0
]
st.write("Chart Rows:", len(chart_df))

fig = px.scatter(
    chart_df,
    x="equity_capital",
    y="borrowings",
    size="market_cap_crore",
    size_max=60,
    hover_name="company_id",
    title="Debt vs Equity"
)

fig.update_layout(height=650)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# Top Borrowers
# ---------------------------------------------------

st.subheader("Top 15 Borrowers")

borrow_df = (
    df.sort_values(
        "borrowings",
        ascending=False
    )
    .head(15)
)

borrow_fig = px.bar(
    borrow_df,
    x="company_id",
    y="borrowings",
    title="Highest Debt Companies"
)

st.plotly_chart(
    borrow_fig,
    use_container_width=True
)

# ---------------------------------------------------
# Largest Equity Capital
# ---------------------------------------------------

st.subheader("Largest Equity Capital")

equity_df = (
    df.sort_values(
        "equity_capital",
        ascending=False
    )
    .head(15)
)

equity_fig = px.bar(
    equity_df,
    x="company_id",
    y="equity_capital",
    title="Largest Equity Base"
)

st.plotly_chart(
    equity_fig,
    use_container_width=True
)

# ---------------------------------------------------
# Capital Efficiency
# ---------------------------------------------------

st.subheader("Capital Snapshot")

snapshot = pd.DataFrame({
    "Metric": [
        "Median Debt",
        "Median Equity",
        "Median Assets"
    ],
    "Value": [
        df["borrowings"].median(),
        df["equity_capital"].median(),
        df["total_assets"].median()
    ]
})

snap_fig = px.bar(
    snapshot,
    x="Metric",
    y="Value"
)

st.plotly_chart(
    snap_fig,
    use_container_width=True
)

# ---------------------------------------------------
# Raw Data
# ---------------------------------------------------

with st.expander("View Data"):
    st.dataframe(
        df[
            [
                "company_id",
                "equity_capital",
                "borrowings",
                "total_assets",
                "market_cap_crore"
            ]
        ]
    )
