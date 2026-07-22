import streamlit as st
import pandas as pd
import numpy as np

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from utils.db import (
    get_companies,
    get_ratios,
    get_market_cap,
    get_analysis,
    get_pros_cons,
    get_documents,
    get_sectors
)

st.title("🏢 Company Profile")

companies = get_companies()
ratios = get_ratios()
market = get_market_cap()
analysis = get_analysis()
pros_cons = get_pros_cons()
documents = get_documents()
sectors = get_sectors()


def display_value(value, prefix="", suffix="", decimals=2):
    if pd.isna(value):
        return "N/A"

    if isinstance(value, (int, float, np.number)):
        return f"{prefix}{value:.{decimals}f}{suffix}"

    return str(value)


company_list = sorted(companies["company_name"].dropna().unique())

selected_company = st.selectbox(
    "Select Company",
    company_list
)

company = companies[
    companies["company_name"] == selected_company
].iloc[0]

company_id = company["id"]


ratio = ratios[
    ratios["company_id"] == company_id
].sort_values("year")

if len(ratio):
    ratio = ratio.iloc[-1]
else:
    ratio = pd.Series(dtype=object)


market_row = market[
    market["company_id"] == company_id
].sort_values("year")

if len(market_row):
    market_row = market_row.iloc[-1]
else:
    market_row = pd.Series(dtype=object)


analysis_row = analysis[
    analysis["company_id"] == company_id
]

if len(analysis_row):
    analysis_row = analysis_row.iloc[0]
else:
    analysis_row = pd.Series(dtype=object)


sector_row = sectors[
    sectors["company_id"] == company_id
]

if len(sector_row):
    sector_row = sector_row.iloc[0]
else:
    sector_row = pd.Series(dtype=object)


pros_row = pros_cons[
    pros_cons["company_id"] == company_id
]

if len(pros_row):
    pros_row = pros_row.iloc[0]
else:
    pros_row = pd.Series(dtype=object)


reports = documents[
    documents["company_id"] == company_id
].sort_values("Year", ascending=False)


st.subheader(company["company_name"])

if str(company["company_logo"]).startswith("http"):
    st.image(company["company_logo"], width=120)

col1, col2, col3 = st.columns(3)

with col1:
    if pd.notna(company["website"]):
        st.markdown(f"[🌐 Website]({company['website']})")

with col2:
    if pd.notna(company["nse_profile"]):
        st.markdown(f"[📈 NSE Profile]({company['nse_profile']})")

with col3:
    if pd.notna(company["bse_profile"]):
        st.markdown(f"[📊 BSE Profile]({company['bse_profile']})")

st.divider()

st.subheader("About Company")

if pd.notna(company["about_company"]):
    st.write(company["about_company"])
else:
    st.info("Description not available.")

st.divider()

st.subheader("Company Information")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Broad Sector",
    display_value(sector_row.get("broad_sector"))
)

c2.metric(
    "Sub Sector",
    display_value(sector_row.get("sub_sector"))
)

c3.metric(
    "Market Cap Category",
    display_value(sector_row.get("market_cap_category"))
)

st.divider()

st.subheader("Financial Metrics")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "ROE %",
    display_value(company["roe_percentage"], suffix="%")
)

c2.metric(
    "ROCE %",
    display_value(company["roce_percentage"], suffix="%")
)

c3.metric(
    "Book Value",
    display_value(company["book_value"])
)

c4.metric(
    "Face Value",
    display_value(company["face_value"])
)

st.divider()

st.subheader("Market Valuation")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Market Cap (Cr)",
    display_value(market_row.get("market_cap_crore"))
)

c2.metric(
    "P/E Ratio",
    display_value(market_row.get("pe_ratio"))
)

c3.metric(
    "P/B Ratio",
    display_value(market_row.get("pb_ratio"))
)

c4.metric(
    "Dividend Yield %",
    display_value(
        market_row.get("dividend_yield_pct"),
        suffix="%"
    )
)

st.divider()

st.subheader("Growth Analysis")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Sales CAGR",
    display_value(
        analysis_row.get("compounded_sales_growth")
    )
)

c2.metric(
    "Profit CAGR",
    display_value(
        analysis_row.get("compounded_profit_growth")
    )
)

c3.metric(
    "Stock Price CAGR",
    display_value(
        analysis_row.get("stock_price_cagr")
    )
)

st.divider()

st.subheader("Pros & Cons")

left, right = st.columns(2)

with left:
    st.success("Pros")

    if pd.notna(pros_row.get("pros")):
        st.write(pros_row["pros"])
    else:
        st.write("N/A")

with right:
    st.error("Cons")

    if pd.notna(pros_row.get("cons")):
        st.write(pros_row["cons"])
    else:
        st.write("N/A")

st.divider()

st.subheader("Annual Reports")

if len(reports):

    report_df = reports[["Year", "Annual_Report"]].copy()

    report_df.rename(
        columns={
            "Annual_Report": "Report Link"
        },
        inplace=True
    )

    st.dataframe(
        report_df,
        use_container_width=True
    )

else:
    st.info("No reports available.")
    