import streamlit as st
import pandas as pd
import plotly.express as px

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from utils.db import (
    get_companies,
    get_sectors,
    get_market_cap,
    get_ratios,
    get_profit_loss
)

st.title("🏭 Sector Analysis")

companies = get_companies()
sectors = get_sectors()
market = get_market_cap()
ratios = get_ratios()
pl = get_profit_loss()

# --------------------------------------------------
# Latest record PER COMPANY
# --------------------------------------------------

ratios_latest = ratios[
    ratios["return_on_equity_pct"].notna()
].copy()

ratios_latest = (
    ratios_latest
    .groupby("company_id")
    .tail(1)
)

pl_latest = (
    pl
    .groupby("company_id")
    .tail(1)
)

market_latest = (
    market
    .groupby("company_id")
    .tail(1)
)

# --------------------------------------------------
# Merge datasets
# --------------------------------------------------

df = sectors.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

df = df.merge(
    ratios_latest[
        ["company_id", "return_on_equity_pct"]
    ],
    on="company_id",
    how="left"
)

df = df.merge(
    pl_latest[
        ["company_id", "sales"]
    ],
    on="company_id",
    how="left"
)

df = df.merge(
    market_latest[
        ["company_id", "market_cap_crore"]
    ],
    on="company_id",
    how="left"
)


# --------------------------------------------------
# Sector selector
# --------------------------------------------------

sector_list = sorted(
    sectors["broad_sector"].dropna().unique()
)

selected_sector = st.selectbox(
    "Select Sector",
    sector_list
)
sector_df = df[
    df["broad_sector"] == selected_sector
]

sector_df_chart = sector_df.dropna(
    subset=[
        "sales",
        "return_on_equity_pct"
    ]
)

# --------------------------------------------------
# Bubble Chart
# --------------------------------------------------

st.subheader("Revenue vs ROE Bubble Chart")

fig = px.scatter(
    sector_df_chart,
    x="sales",
    y="return_on_equity_pct",
    size="market_cap_crore",
    color="sub_sector",
    hover_name="company_id",
    title=f"{selected_sector} Companies"
)

fig.update_layout(
    height=650
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Sector Median KPIs
# --------------------------------------------------

st.subheader("Sector Median KPIs")

median_df = pd.DataFrame({
    "Metric": [
        "ROE",
        "Revenue",
        "Market Cap"
    ],
    "Value": [
        sector_df["return_on_equity_pct"].median(),
        sector_df["sales"].median(),
        sector_df["market_cap_crore"].median()
    ]
})

# normalize values so ROE is visible
median_df["Normalized"] = (
    median_df["Value"]
    / median_df["Value"].max()
) * 100

bar_fig = px.bar(
    median_df,
    x="Metric",
    y="Normalized",
    text="Value",
    title=f"{selected_sector} Median Metrics (Normalized)"
)

bar_fig.update_layout(
    height=500
)

st.plotly_chart(
    bar_fig,
    use_container_width=True
)

