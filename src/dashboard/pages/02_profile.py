import streamlit as st

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from utils.db import get_companies

st.title("🏢 Company Profile")

companies = get_companies()

company_list = sorted(
    companies["company_name"].dropna().unique()
)

selected_company = st.selectbox(
    "Select Company",
    company_list
)

company = companies[
    companies["company_name"] == selected_company
].iloc[0]

st.subheader(company["company_name"])

# Logo
if str(company["company_logo"]).startswith("http"):
    st.image(company["company_logo"], width=120)

# Links
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"[🌐 Website]({company['website']})"
    )

with col2:
    st.markdown(
        f"[📈 NSE Profile]({company['nse_profile']})"
    )

with col3:
    st.markdown(
        f"[📊 BSE Profile]({company['bse_profile']})"
    )

st.divider()

# About Company
st.subheader("About Company")

about_text = company["about_company"]

if about_text and str(about_text) != "nan":
    st.write(about_text)
else:
    st.info("Company description not available.")

st.divider()

# Metrics
st.subheader("Key Metrics")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "ROE %",
    f"{company['roe_percentage']:.2f}"
)

c2.metric(
    "ROCE %",
    f"{company['roce_percentage']:.2f}"
)

c3.metric(
    "Book Value",
    f"{company['book_value']:.2f}"
)

c4.metric(
    "Face Value",
    f"{company['face_value']:.2f}"
)
