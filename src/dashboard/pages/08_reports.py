import streamlit as st
import pandas as pd
import plotly.express as px

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from utils.db import (
    get_companies,
    get_ratios
)

st.title("📊 Investment Reports")

companies = get_companies()
ratios = get_ratios()

# ------------------------------------
# Latest ratios per company
# ------------------------------------

ratios = (
    ratios
    .sort_values("year")
    .groupby("company_id")
    .tail(1)
)

df = ratios.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

# ------------------------------------
# Top Quality Companies
# ------------------------------------

st.header("🏆 Top Quality Companies")

quality_df = (
    df.sort_values(
        "composite_quality_score",
        ascending=False
    )
    .head(15)
)

fig_quality = px.bar(
    quality_df,
    x="company_id",
    y="composite_quality_score",
    title="Top Quality Stocks"
)

st.plotly_chart(
    fig_quality,
    use_container_width=True
)

# ------------------------------------
# Top ROE
# ------------------------------------

st.header("💰 Highest ROE")

roe_df = (
    df.sort_values(
        "return_on_equity_pct",
        ascending=False
    )
    .head(15)
)

fig_roe = px.bar(
    roe_df,
    x="company_id",
    y="return_on_equity_pct",
    title="Highest ROE Stocks"
)

st.plotly_chart(
    fig_roe,
    use_container_width=True
)

# ------------------------------------
# Revenue CAGR
# ------------------------------------

st.header("📈 Revenue Growth Leaders")

growth_df = (
    df.sort_values(
        "revenue_cagr_5yr",
        ascending=False
    )
    .head(15)
)

fig_growth = px.bar(
    growth_df,
    x="company_id",
    y="revenue_cagr_5yr",
    title="Top Revenue CAGR"
)

st.plotly_chart(
    fig_growth,
    use_container_width=True
)

# ------------------------------------
# Free Cash Flow
# ------------------------------------

st.header("💵 Free Cash Flow Leaders")

fcf_df = (
    df.sort_values(
        "free_cash_flow_cr",
        ascending=False
    )
    .head(15)
)

fig_fcf = px.bar(
    fcf_df,
    x="company_id",
    y="free_cash_flow_cr",
    title="Highest Free Cash Flow"
)

st.plotly_chart(
    fig_fcf,
    use_container_width=True
)

# ------------------------------------
# Composite Ranking Table
# ------------------------------------

st.header("📋 Investment Scorecard")

report_df = df[
    [
        "company_id",
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "free_cash_flow_cr",
        "composite_quality_score"
    ]
].copy()

report_df = report_df.sort_values(
    "composite_quality_score",
    ascending=False
)

st.dataframe(
    report_df,
    use_container_width=True
)

# ------------------------------------
# Download CSV
# ------------------------------------

csv = report_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Report",
    data=csv,
    file_name="nifty100_report.csv",
    mime="text/csv"
)

# ------------------------------------
# Summary
# ------------------------------------

st.header("📝 Market Summary")

best_quality = report_df.iloc[0]["company_id"]

st.success(
    f"Highest Quality Company: {best_quality}"
)
