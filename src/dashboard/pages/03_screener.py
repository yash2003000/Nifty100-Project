import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from utils.db import (
    get_ratios,
    get_companies,
    get_sectors
)

st.title("🔍 Financial Screener")

# ==========================================================
# Load Data
# ==========================================================

ratios = get_ratios()
companies = get_companies()
sectors = get_sectors()

# Latest available year
# Find latest year where ROE exists

# ----------------------------------------------------
# Choose latest year having valid ROE AND FCF data
# ----------------------------------------------------

ratios["return_on_equity_pct"] = pd.to_numeric(
    ratios["return_on_equity_pct"],
    errors="coerce"
)

ratios["free_cash_flow_cr"] = pd.to_numeric(
    ratios["free_cash_flow_cr"],
    errors="coerce"
)

year_summary = (
    ratios.groupby("year")
    .agg(
        roe_count=("return_on_equity_pct", "count"),
        fcf_count=("free_cash_flow_cr", "count"),
    )
    .reset_index()
)

valid_years = year_summary[
    (year_summary["roe_count"] > 50)
    &
    (year_summary["fcf_count"] > 50)
]

latest_year = valid_years.iloc[-1]["year"]

ratios = ratios[
    ratios["year"] == latest_year
]

st.caption(f"Financial Year : {latest_year}")

df = (
    ratios
    .merge(
        companies,
        left_on="company_id",
        right_on="id",
        how="left"
    )
    .merge(
        sectors,
        on="company_id",
        how="left"
    )
)

# ==========================================================
# Sidebar Filters
# ==========================================================

st.sidebar.header("Filters")
st.sidebar.subheader("Quick Presets")

preset = st.sidebar.radio(
    "Choose a preset",
    [
        "Custom",
        "⭐ Quality",
        "📈 Growth",
        "💰 Value",
        "💵 Dividend",
        "🛡 Debt-Free",
        "🔄 Turnaround"
    ]
)
# Sector Filter
sector_options = ["All"] + sorted(
    df["broad_sector"].dropna().unique().tolist()
)

selected_sector = st.sidebar.selectbox(
    "Sector",
    sector_options
)

# Company Search
company_search = st.sidebar.text_input(
    "Search Company"
)

# ROE
roe_min = st.sidebar.slider(
    "Minimum ROE %",
    -50.0,
    100.0,
    10.0
)

# Debt / Equity
de_max = st.sidebar.slider(
    "Maximum Debt/Equity",
    0.0,
    10.0,
    2.0
)

# Free Cash Flow

fcf_series = pd.to_numeric(
    df["free_cash_flow_cr"],
    errors="coerce"
).dropna()

if len(fcf_series) == 0:
    fcf_series = pd.Series([0.0])

fcf_min = st.sidebar.slider(
    "Minimum Free Cash Flow",
    min_value=float(fcf_series.min()),
    max_value=float(fcf_series.max()) + 1,
    value=float(fcf_series.min())
)

# Revenue CAGR
rev_min = st.sidebar.slider(
    "Minimum Revenue CAGR %",
    -50.0,
    100.0,
    5.0
)

# PAT CAGR
pat_min = st.sidebar.slider(
    "Minimum PAT CAGR %",
    -50.0,
    100.0,
    5.0
)

# ==========================================================
# Operating Profit Margin
# ==========================================================

opm_min = st.sidebar.slider(
    "Minimum Operating Profit Margin %",
    -50.0,
    100.0,
    10.0
)

# ==========================================================
# Interest Coverage
# ==========================================================

icr_min = st.sidebar.slider(
    "Minimum Interest Coverage",
    0.0,
    100.0,
    2.0
)

# ==========================================================
# Dividend Payout Ratio
# ==========================================================

dividend_min = st.sidebar.slider(
    "Minimum Dividend Payout %",
    0.0,
    100.0,
    0.0
)

# ==========================================
# Apply Presets
# ==========================================

if preset == "⭐ Quality":
    roe_min = 18
    de_max = 0.5
    rev_min = 10
    pat_min = 10
    opm_min = 15
    icr_min = 5
    dividend_min = 0

elif preset == "📈 Growth":
    roe_min = 15
    de_max = 2
    rev_min = 15
    pat_min = 15
    opm_min = 10
    icr_min = 2
    dividend_min = 0

elif preset == "💰 Value":
    roe_min = 12
    de_max = 1
    rev_min = 5
    pat_min = 5
    opm_min = 10
    icr_min = 2
    dividend_min = 20

elif preset == "💵 Dividend":
    roe_min = 10
    de_max = 2
    rev_min = 0
    pat_min = 0
    opm_min = 0
    icr_min = 1
    dividend_min = 40

elif preset == "🛡 Debt-Free":
    roe_min = 10
    de_max = 0
    rev_min = 5
    pat_min = 5
    opm_min = 10
    icr_min = 5
    dividend_min = 0

elif preset == "🔄 Turnaround":
    roe_min = 0
    de_max = 3
    rev_min = 0
    pat_min = 0
    opm_min = 0
    icr_min = 1
    dividend_min = 0

# ==========================================================
# Apply Filters
# ==========================================================

filtered = df.copy()

filtered = filtered[
    filtered["return_on_equity_pct"].fillna(-999) >= roe_min
]

filtered = filtered[
    filtered["debt_to_equity"].fillna(999) <= de_max
]

filtered = filtered[
    pd.to_numeric(
        filtered["free_cash_flow_cr"],
        errors="coerce"
    ).fillna(-999999) >= fcf_min
]

filtered = filtered[
    filtered["revenue_cagr_5yr"].fillna(-999) >= rev_min
]

filtered = filtered[
    filtered["pat_cagr_5yr"].fillna(-999) >= pat_min
]

filtered = filtered[
    filtered["operating_profit_margin_pct"].fillna(-999) >= opm_min
]

filtered = filtered[
    filtered["interest_coverage"].fillna(-999) >= icr_min
]

filtered = filtered[
    filtered["dividend_payout_ratio_pct"].fillna(-999) >= dividend_min
]

if selected_sector != "All":
    filtered = filtered[
        filtered["broad_sector"] == selected_sector
    ]

if company_search:
    filtered = filtered[
        filtered["company_name"].str.contains(
            company_search,
            case=False,
            na=False
        )
    ]

filtered = filtered.sort_values(
    "composite_quality_score",
    ascending=False,
    na_position="last"
)


# ==========================================================
# Results
# ==========================================================

st.subheader("📋 Screening Results")

st.success(
    f"Showing {len(filtered)} companies out of {len(df)}"
)

columns = [
    "company_name",
    "broad_sector",
    "return_on_equity_pct",
    "operating_profit_margin_pct",
    "debt_to_equity",
    "interest_coverage",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "dividend_payout_ratio_pct",
    "composite_quality_score"
]
display_df = filtered[columns].copy()

display_df.columns = [
    "Company",
    "Sector",
    "ROE %",
    "Operating Margin %",
    "Debt/Equity",
    "Interest Coverage",
    "Free Cash Flow",
    "Revenue CAGR %",
    "PAT CAGR %",
    "Dividend Payout %",
    "Quality Score"
]
# Round numeric columns
numeric_cols = [
    "ROE %",
    "Operating Margin %",
    "Debt/Equity",
    "Interest Coverage",
    "Free Cash Flow",
    "Revenue CAGR %",
    "PAT CAGR %",
    "Dividend Payout %",
    "Quality Score"
]

display_df[numeric_cols] = display_df[numeric_cols].round(2)

# Replace NaN with N/A
display_df = display_df.fillna("N/A")

st.dataframe(
    display_df,
    use_container_width=True
)

# ==========================================================
# Download CSV
# ==========================================================

csv = display_df.to_csv(index=False)

st.download_button(
    "⬇ Download Results",
    csv,
    file_name="financial_screener.csv",
    mime="text/csv"
)
