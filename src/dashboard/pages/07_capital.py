import streamlit as st
import pandas as pd
import plotly.express as px

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from utils.db import (
    get_companies,
    get_balance_sheet,
    get_market_cap,
    get_ratios
)

st.title("🏦 Capital Allocation Map")

# =====================================================
# Load Data
# =====================================================

companies = get_companies()
balance = get_balance_sheet()
market = get_market_cap()
ratios = get_ratios()

# =====================================================
# Latest Financial Data (Ignore TTM)
# =====================================================

balance = balance.copy()

if "year" in balance.columns:
    balance = balance[balance["year"] != "TTM"]

balance = (
    balance
    .sort_values("year")
    .groupby("company_id", as_index=False)
    .last()
)

market = market.copy()

if "year" in market.columns:
    market = market[market["year"] != "TTM"]

market = (
    market
    .sort_values("year")
    .groupby("company_id", as_index=False)
    .last()
)

ratios = ratios.copy()

if "year" in ratios.columns:
    ratios = ratios[ratios["year"] != "TTM"]

ratios = (
    ratios
    .sort_values("year")
    .groupby("company_id", as_index=False)
    .last()
)

# =====================================================
# Merge
# =====================================================

df = companies.merge(
    balance,
    left_on="id",
    right_on="company_id",
    how="left"
)

df = df.merge(
    market[
        [
            "company_id",
            "market_cap_crore"
        ]
    ],
    on="company_id",
    how="left"
)

df = df.merge(
    ratios[
        [
            "company_id",
            "return_on_equity_pct",
            "debt_to_equity",
            "free_cash_flow_cr",
            "revenue_cagr_5yr",
            "pat_cagr_5yr",
            "dividend_payout_ratio_pct",
            "composite_quality_score"
        ]
    ],
    on="company_id",
    how="left"
)

# =====================================================
# Numeric Conversion
# =====================================================

numeric_cols = [

    "market_cap_crore",
    "return_on_equity_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "dividend_payout_ratio_pct",
    "composite_quality_score"

]

for col in numeric_cols:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

# =====================================================
# Capital Allocation Pattern Classification
# =====================================================

def classify(row):

    roe = row["return_on_equity_pct"]
    de = row["debt_to_equity"]
    fcf = row["free_cash_flow_cr"]
    rev = row["revenue_cagr_5yr"]
    pat = row["pat_cagr_5yr"]
    div = row["dividend_payout_ratio_pct"]
    score = row["composite_quality_score"]

    if pd.notna(score) and score >= 80:
        return "⭐ Quality Compounder"

    if pd.notna(div) and div >= 40:
        return "💰 Dividend"

    if pd.notna(de) and de <= 0.30:
        return "🟢 Debt Free"

    if pd.notna(de) and de >= 2:
        return "🔴 High Debt"

    if (
        pd.notna(rev)
        and pd.notna(pat)
        and rev >= 15
        and pat >= 15
    ):
        return "🚀 Growth"

    if (
        pd.notna(fcf)
        and fcf > 0
    ):
        return "💵 Cash Rich"

    if (
        pd.notna(roe)
        and roe >= 20
    ):
        return "🏆 High ROE"

    return "📊 Balanced"

df["Capital Pattern"] = df.apply(
    classify,
    axis=1
)

# =====================================================
# KPI Cards
# =====================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Companies",
        len(df)
    )

with c2:
    st.metric(
        "Patterns",
        df["Capital Pattern"].nunique()
    )

with c3:
    st.metric(
        "Median Debt/Equity",
        round(
            df["debt_to_equity"].median(),
            2
        )
    )

with c4:
    st.metric(
        "Median ROE %",
        round(
            df["return_on_equity_pct"].median(),
            2
        )
    )

st.divider()

# =====================================================
# Treemap
# =====================================================

st.subheader("Capital Allocation Treemap")

treemap = px.treemap(

    df,

    path=[
        "Capital Pattern",
        "company_name"
    ],

    values="market_cap_crore",

    color="Capital Pattern",

    hover_data=[
        "company_id",
        "return_on_equity_pct",
        "debt_to_equity",
        "free_cash_flow_cr"
    ]
)

treemap.update_layout(
    height=700
)

st.plotly_chart(
    treemap,
    use_container_width=True
)

st.divider()
# =====================================================
# Pattern Explorer
# =====================================================

st.subheader("Explore Capital Allocation Pattern")

patterns = sorted(df["Capital Pattern"].dropna().unique())

selected_pattern = st.selectbox(
    "Select Pattern",
    patterns
)

pattern_df = (
    df[df["Capital Pattern"] == selected_pattern]
    .sort_values(
        "market_cap_crore",
        ascending=False
    )
)

st.success(
    f"{len(pattern_df)} companies belong to '{selected_pattern}'"
)

# =====================================================
# Companies Table
# =====================================================

display = pattern_df[
    [
        "company_name",
        "company_id",
        "market_cap_crore",
        "return_on_equity_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "revenue_cagr_5yr",
        "pat_cagr_5yr"
    ]
].rename(
    columns={
        "company_name": "Company",
        "company_id": "Ticker",
        "market_cap_crore": "Market Cap (Cr)",
        "return_on_equity_pct": "ROE %",
        "debt_to_equity": "Debt/Equity",
        "free_cash_flow_cr": "Free Cash Flow (Cr)",
        "revenue_cagr_5yr": "Revenue CAGR %",
        "pat_cagr_5yr": "PAT CAGR %"
    }
)

st.dataframe(
    display,
    use_container_width=True
)

st.divider()

# =====================================================
# Pattern Statistics
# =====================================================

st.subheader("Pattern Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average ROE",
        (
            f"{pattern_df['return_on_equity_pct'].mean():.2f}%"
            if pattern_df["return_on_equity_pct"].notna().any()
            else "N/A"
        )
    )

with col2:
    st.metric(
        "Average Debt/Equity",
        (
            f"{pattern_df['debt_to_equity'].mean():.2f}"
            if pattern_df["debt_to_equity"].notna().any()
            else "N/A"
        )
    )

with col3:
    st.metric(
        "Average FCF",
        (
            f"{pattern_df['free_cash_flow_cr'].mean():,.0f}"
            if pattern_df["free_cash_flow_cr"].notna().any()
            else "N/A"
        )
    )

st.divider()

# =====================================================
# Download CSV
# =====================================================

csv = display.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Pattern Companies",
    data=csv,
    file_name=f"{selected_pattern.replace(' ', '_')}.csv",
    mime="text/csv"
)

# =====================================================
# Raw Data
# =====================================================

with st.expander("View Raw Data"):
    st.dataframe(
        df,
        use_container_width=True
    )