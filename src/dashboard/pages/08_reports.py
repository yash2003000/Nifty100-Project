import streamlit as st
import pandas as pd

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from utils.db import (
    get_companies,
    get_documents
)

# =====================================================
# Page Config
# =====================================================

st.title("📑 Annual Reports")

companies = get_companies()
documents = get_documents()

# =====================================================
# Merge Company Details
# =====================================================

df = documents.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

# =====================================================
# Company Search
# =====================================================

company_list = sorted(
    df["company_name"].dropna().unique()
)

selected_company = st.selectbox(
    "Search Company",
    company_list
)

company_df = df[
    df["company_name"] == selected_company
].copy()

if company_df.empty:
    st.error("Company not found.")
    st.stop()

company_df = company_df.sort_values(
    "Year",
    ascending=False
)

company_info = company_df.iloc[0]

# =====================================================
# Company Information
# =====================================================

st.subheader("Company Information")

col1, col2 = st.columns([1, 2])

with col1:

    if (
        pd.notna(company_info["company_logo"])
        and str(company_info["company_logo"]).strip() != ""
    ):
        st.image(
            company_info["company_logo"],
            width=120
        )

with col2:

    st.markdown(
        f"## {company_info['company_name']}"
    )

    st.write(
        f"**Ticker :** {company_info['company_id']}"
    )

    if "broad_sector" in company_df.columns:
        st.write(
            f"**Sector :** {company_info['broad_sector']}"
        )

    if (
        pd.notna(company_info["website"])
        and str(company_info["website"]).strip() != ""
    ):
        st.markdown(
            f"🌐 {company_info['website']}"
        )

st.divider()

# =====================================================
# Report Summary
# =====================================================

st.subheader("Report Summary")

c1, c2 = st.columns(2)

with c1:
    st.metric(
        "Reports Available",
        len(company_df)
    )

with c2:
    st.metric(
        "Latest Report",
        int(company_df["Year"].max())
    )

st.divider()

# =====================================================
# Annual Reports
# =====================================================

st.subheader("Available Annual Reports")

for _, row in company_df.iterrows():

    report_url = ""

    if pd.notna(row["Annual_Report"]):
        report_url = str(row["Annual_Report"]).strip()

    with st.container():

        col1, col2, col3 = st.columns(
            [1, 2, 4]
        )

        with col1:

            st.markdown(
                f"### {int(row['Year'])}"
            )

        with col2:

            if report_url != "":
                st.success("Available")
            else:
                st.error("Unavailable")
        with col3:

            if report_url != "":

                st.markdown(
                    f"[📄 Open Annual Report]({report_url})"
                )

            else:

                st.caption(
                    "Report unavailable"
                )

st.divider()

# =====================================================
# Reports Table
# =====================================================

st.subheader("Report History")

table = company_df[
    [
        "Year",
        "Annual_Report"
    ]
].copy()

table["Status"] = table["Annual_Report"].apply(
    lambda x:
    "✅ Available"
    if pd.notna(x) and str(x).strip() != ""
    else "❌ Unavailable"
)

st.dataframe(
    table,
    use_container_width=True
)

st.divider()

# =====================================================
# Latest Report Shortcut
# =====================================================

latest = company_df.iloc[0]

latest_url = ""

if pd.notna(latest["Annual_Report"]):
    latest_url = str(latest["Annual_Report"]).strip()

st.subheader("Latest Annual Report")

if latest_url != "":

    st.success(
        f"Latest Report : FY {int(latest['Year'])}"
    )

    st.link_button(
        "📄 Open Latest Report",
        latest_url
    )

else:

    st.error(
        "Latest report unavailable."
    )

st.divider()

# =====================================================
# Download Links
# =====================================================

st.subheader("Download Links")

available = company_df[
    company_df["Annual_Report"].notna()
].copy()

if len(available):

    for _, row in available.iterrows():

        st.markdown(
            f"**FY {int(row['Year'])}**"
        )

        st.link_button(
            f"Open FY {int(row['Year'])} Report",
            row["Annual_Report"]
        )

else:

    st.warning(
        "No downloadable reports available."
    )

st.divider()

# =====================================================
# Report Statistics
# =====================================================

st.subheader("Statistics")

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "Total Reports",
        len(company_df)
    )

with c2:

    st.metric(
        "Available",
        len(
            company_df[
                company_df["Annual_Report"].notna()
            ]
        )
    )

with c3:

    st.metric(
        "Missing",
        len(
            company_df[
                company_df["Annual_Report"].isna()
            ]
        )
    )

st.divider()

# =====================================================
# Raw Data
# =====================================================

with st.expander("View Raw Data"):

    st.dataframe(
        company_df,
        use_container_width=True
    )