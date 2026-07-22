import streamlit as st
import plotly.express as px
import pandas as pd
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from utils.db import (
    get_companies,
    get_ratios,
    get_sectors,
    get_market_cap
)

st.set_page_config(page_title="NIFTY 100 Dashboard", layout="wide")

st.title("🏠 NIFTY 100 Financial Dashboard")

st.markdown("### Market Overview")

companies = get_companies()
ratios = get_ratios()
sectors = get_sectors()
market = get_market_cap()

# ----------------------------
# Sidebar
# ----------------------------

year = st.sidebar.selectbox(
    "Financial Year",
    sorted(ratios["year"].dropna().unique(), reverse=True)
)

latest_ratios = ratios[ratios["year"] == year]
latest_market = market[market["year"] == year]

# ----------------------------
# KPIs
# ----------------------------

import pandas as pd

avg_roe = latest_ratios["return_on_equity_pct"].mean()
median_de = latest_ratios["debt_to_equity"].median()
median_rev = latest_ratios["revenue_cagr_5yr"].median()
median_pe = latest_market["pe_ratio"].median()

avg_roe = None if pd.isna(avg_roe) else avg_roe
median_de = None if pd.isna(median_de) else median_de
median_rev = None if pd.isna(median_rev) else median_rev
median_pe = None if pd.isna(median_pe) else median_pe

debt_free = (
    latest_ratios["debt_to_equity"] <= 0
).sum()

total_companies = companies["company_name"].nunique()

c1, c2, c3 = st.columns(3)

c4, c5, c6 = st.columns(3)

c1.metric(
    "Companies",
    total_companies
)

c2.metric(
    "Average ROE",
    "N/A" if avg_roe is None else f"{avg_roe:.2f}%"
)

c3.metric(
    "Median P/E",
    "N/A" if median_pe is None else f"{median_pe:.2f}"
)

c4.metric(
    "Median Debt/Equity",
    "N/A" if median_de is None else f"{median_de:.2f}"
)

c5.metric(
    "Revenue CAGR (Median)",
    "N/A" if median_rev is None else f"{median_rev:.2f}%"
)

c6.metric(
    "Debt Free Companies",
    debt_free
)

st.divider()

# ----------------------------
# Sector Distribution
# ----------------------------

st.subheader("Sector Distribution")

sector_counts = (
    sectors["broad_sector"]
    .value_counts()
    .reset_index()
)

sector_counts.columns = [
    "Sector",
    "Companies"
]

fig = px.pie(
    sector_counts,
    names="Sector",
    values="Companies",
    hole=0.45
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ----------------------------
# Top Quality Companies
# ----------------------------

st.subheader("Top Companies by Composite Quality Score")

top = latest_ratios.merge(
    companies[
        [
            "id",
            "company_name"
        ]
    ],
    left_on="company_id",
    right_on="id"
)

top = top.sort_values(
    "composite_quality_score",
    ascending=False
)

top = top[
    [
        "company_name",
        "composite_quality_score",
        "return_on_equity_pct",
        "revenue_cagr_5yr"
    ]
].head(10)

top.columns = [
    "Company",
    "Quality Score",
    "ROE %",
    "Revenue CAGR %"
]

st.dataframe(
    top,
    use_container_width=True,
    hide_index=True
)