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

# --------------------------------------------------
# Load Data
# --------------------------------------------------

companies = get_companies()
sectors = get_sectors()
market = get_market_cap()
ratios = get_ratios()
pl = get_profit_loss()

# --------------------------------------------------
# Latest data per company
# Ignore TTM rows
# --------------------------------------------------

# Financial Ratios
ratios_latest = ratios.copy()

ratios_latest = ratios_latest[
    ratios_latest["year"] != "TTM"
]

ratios_latest = (
    ratios_latest
    .sort_values("year")
    .groupby("company_id", as_index=False)
    .last()
)

# Profit & Loss
pl_latest = pl.copy()

pl_latest = pl_latest[
    pl_latest["year"] != "TTM"
]

pl_latest = (
    pl_latest
    .sort_values("year")
    .groupby("company_id", as_index=False)
    .last()
)

# Market Cap
market_latest = market.copy()

if "year" in market_latest.columns:

    market_latest = market_latest[
        market_latest["year"] != "TTM"
    ]

    market_latest = (
        market_latest
        .sort_values("year")
        .groupby("company_id", as_index=False)
        .last()
    )

# --------------------------------------------------
# Merge
# --------------------------------------------------

df = sectors.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

df = df.merge(
    ratios_latest[
        [
            "company_id",
            "return_on_equity_pct"
        ]
    ],
    on="company_id",
    how="left"
)

df = df.merge(
    pl_latest[
        [
            "company_id",
            "sales"
        ]
    ],
    on="company_id",
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

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

sector_list = sorted(
    df["broad_sector"].dropna().unique()
)

selected_sector = st.selectbox(
    "Select Sector",
    sector_list
)

sector_df = df[
    df["broad_sector"] == selected_sector
].copy()

if sector_df.empty:
    st.warning("No companies found.")
    st.stop()

sector_df["market_cap_crore"] = sector_df[
    "market_cap_crore"
].fillna(1)

# --------------------------------------------------
# KPIs
# --------------------------------------------------

st.subheader("Sector Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Companies",
        len(sector_df)
    )

with c2:
    st.metric(
        "Median ROE %",
        round(
            sector_df["return_on_equity_pct"].median(),
            2
        )
    )

with c3:
    st.metric(
        "Median Revenue",
        f"{sector_df['sales'].median():,.0f}"
    )

with c4:
    st.metric(
        "Median Market Cap",
        f"{sector_df['market_cap_crore'].median():,.0f}"
    )

st.divider()

# --------------------------------------------------
# Bubble Chart
# --------------------------------------------------

st.subheader("Revenue vs ROE")

bubble_df = sector_df.copy()

bubble_df["sales"] = pd.to_numeric(
    bubble_df["sales"],
    errors="coerce"
)

bubble_df["return_on_equity_pct"] = pd.to_numeric(
    bubble_df["return_on_equity_pct"],
    errors="coerce"
)

bubble_df["market_cap_crore"] = pd.to_numeric(
    bubble_df["market_cap_crore"],
    errors="coerce"
)

bubble_df = bubble_df.dropna(
    subset=[
        "sales",
        "return_on_equity_pct"
    ]
)

fig = px.scatter(
    bubble_df,
    x="sales",
    y="return_on_equity_pct",
    size="market_cap_crore",
    color="sub_sector",
    hover_name="company_name",
    hover_data=[
        "company_id",
        "market_cap_crore"
    ],
    title=f"{selected_sector} Companies",
    size_max=60
)

fig.update_layout(
    height=700,
    xaxis_title="Revenue",
    yaxis_title="ROE (%)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# Median KPI Chart
# --------------------------------------------------

st.subheader("Sector Median KPIs")

median_df = pd.DataFrame({

    "Metric": [
        "ROE %",
        "Revenue",
        "Market Cap"
    ],

    "Value": [

        sector_df["return_on_equity_pct"].median(),

        sector_df["sales"].median(),

        sector_df["market_cap_crore"].median()

    ]

})

median_df["Normalized"] = (

    median_df["Value"]

    / median_df["Value"].max()

) * 100

bar = px.bar(

    median_df,

    x="Metric",

    y="Normalized",

    text="Value",

    title="Median KPIs"

)

bar.update_layout(

    height=500

)

st.plotly_chart(

    bar,

    use_container_width=True

)

st.divider()

# --------------------------------------------------
# Sector Companies
# --------------------------------------------------

st.subheader("Companies in Sector")

show = sector_df[
    [
        "company_name",
        "sub_sector",
        "sales",
        "return_on_equity_pct",
        "market_cap_crore"
    ]
].rename(
    columns={
        "sales":"Revenue",
        "return_on_equity_pct":"ROE %",
        "market_cap_crore":"Market Cap"
    }
)

st.dataframe(
    show,
    use_container_width=True
)

st.download_button(
    "⬇ Download Sector Data",
    show.to_csv(index=False),
    file_name=f"{selected_sector}_sector.csv",
    mime="text/csv"
)