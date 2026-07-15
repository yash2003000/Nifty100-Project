import streamlit as st
import plotly.express as px

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from utils.db import (
    get_companies,
    get_ratios,
    get_sectors
)

st.title("🏠 Home Dashboard")

companies = get_companies()
ratios = get_ratios()
sectors = get_sectors()

year = st.sidebar.selectbox(
    "Select Year",
    sorted(ratios["year"].dropna().unique(), reverse=True)
)

ratios = ratios[ratios["year"] == year]

latest = ratios.sort_values("year").groupby("company_id").tail(1)

avg_roe = latest["return_on_equity_pct"].mean()

median_de = latest["debt_to_equity"].median()

median_rev = latest["revenue_cagr_5yr"].median()

debt_free = (latest["debt_to_equity"] <= 0).sum()

total_companies = companies["company_name"].nunique()

median_pe = 0

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric(
    "Average ROE",
    f"{avg_roe:.2f}%"
)

c2.metric(
    "Median P/E",
    f"{median_pe:.2f}"
)

c3.metric(
    "Median D/E",
    f"{median_de:.2f}"
)

c4.metric(
    "Total Companies",
    total_companies
)

c5.metric(
    "Median Revenue CAGR",
    f"{median_rev:.2f}%"
)

c6.metric(
    "Debt-Free Companies",
    debt_free
)

st.divider()

st.subheader("Sector Breakdown")

sector_counts = sectors["broad_sector"].value_counts().reset_index()
sector_counts.columns = ["Sector", "Count"]

fig = px.pie(
    sector_counts,
    names="Sector",
    values="Count",
    hole=0.5
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Top 5 Companies by Composite Quality Score")

top5 = latest.nlargest(
    5,
    "composite_quality_score"
)[
    [
        "company_id",
        "composite_quality_score",
        "return_on_equity_pct"
    ]
]

st.dataframe(top5, use_container_width=True)
