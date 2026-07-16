import streamlit as st
import pandas as pd
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from utils.db import (
    get_ratios,
    get_market_cap,
    get_companies,
    get_sectors
)

st.title("🔍 Financial Screener")

ratios = get_ratios()
market = get_market_cap()
companies = get_companies()
sectors = get_sectors()

latest_year = ratios["year"].dropna().unique()[-1]

ratios = ratios[ratios["year"] == latest_year]

df = (
    ratios
    .merge(companies, left_on="company_id", right_on="id")
    .merge(sectors, on="company_id")
)

st.sidebar.header("Filters")

roe_min = st.sidebar.slider(
    "ROE %",
    -50.0,
    100.0,
    10.0
)

de_max = st.sidebar.slider(
    "Debt To Equity",
    0.0,
    10.0,
    2.0
)

fcf_min = st.sidebar.slider(
    "Free Cash Flow",
    float(df["free_cash_flow_cr"].min()),
    float(df["free_cash_flow_cr"].max()),
    0.0
)

rev_min = st.sidebar.slider(
    "Revenue CAGR",
    -50.0,
    100.0,
    5.0
)

pat_min = st.sidebar.slider(
    "PAT CAGR",
    -50.0,
    100.0,
    5.0
)

filtered = df[
    (df["return_on_equity_pct"] >= roe_min)
    &
    (df["debt_to_equity"] <= de_max)
    &
    (df["free_cash_flow_cr"] >= fcf_min)
    &
    (df["revenue_cagr_5yr"] >= rev_min)
    &
    (df["pat_cagr_5yr"] >= pat_min)
]

st.subheader(
    f"{len(filtered)} companies match your filters"
)

show_cols = [
    "company_id",
    "company_name",
    "broad_sector",
    "return_on_equity_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "composite_quality_score"
]

st.dataframe(
    filtered[show_cols],
    use_container_width=True
)

csv = filtered[show_cols].to_csv(index=False)

st.download_button(
    "⬇ Download CSV",
    csv,
    "screener_results.csv",
    "text/csv"
)
