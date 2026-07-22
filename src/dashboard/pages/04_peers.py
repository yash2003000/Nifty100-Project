import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.db import (
    get_peer_groups,
    get_companies,
    get_ratios
)

st.title("👥 Peer Comparison Dashboard")

# ---------------------------------------------------
# Helper Function
# ---------------------------------------------------

def display_value(value, decimals=2):
    if pd.isna(value):
        return "N/A"
    return f"{value:.{decimals}f}"

peer_groups = get_peer_groups()
companies = get_companies()
ratios = get_ratios()

# ---------------------------------------------------
# Latest financial data
# ---------------------------------------------------

latest = (
    ratios.sort_values("year")
    .groupby("company_id")
    .tail(1)
)

# ---------------------------------------------------
# Company Mapping
# ---------------------------------------------------

company_map = dict(
    zip(
        companies["id"],
        companies["company_name"]
    )
)

peer_groups["company_name"] = (
    peer_groups["company_id"]
    .map(company_map)
)

latest["company_name"] = (
    latest["company_id"]
    .map(company_map)
)

# ---------------------------------------------------
# Peer Group Selection
# ---------------------------------------------------

group_names = sorted(
    peer_groups["peer_group_name"].dropna().unique()
)

selected_group = st.selectbox(
    "Peer Group",
    group_names
)

group_df = peer_groups[
    peer_groups["peer_group_name"] == selected_group
]

company_names = sorted(
    group_df["company_name"].dropna().tolist()
)

selected_name = st.selectbox(
    "Select Company",
    company_names
)

selected_company = (
    group_df[
        group_df["company_name"] == selected_name
    ]["company_id"]
    .iloc[0]
)

peer_company_ids = group_df["company_id"].tolist()

benchmark = group_df[
    group_df["is_benchmark"] == 1
]

benchmark_name = ""

if not benchmark.empty:
    benchmark_name = benchmark.iloc[0]["company_name"]

# ---------------------------------------------------
# Members
# ---------------------------------------------------

st.subheader("Peer Group Members")

members = group_df[
    ["company_name"]
].copy()

members["Benchmark"] = members[
    "company_name"
].apply(
    lambda x: "⭐" if x == benchmark_name else ""
)

st.dataframe(
    members,
    use_container_width=True,
    hide_index=True
)

if benchmark_name:
    st.success(
        f"Benchmark Company : {benchmark_name}"
    )

st.divider()

# ---------------------------------------------------
# Radar Chart
# ---------------------------------------------------

st.subheader("Radar Comparison")

metrics = {
    "return_on_equity_pct": "ROE",
    "net_profit_margin_pct": "Net Margin",
    "revenue_cagr_5yr": "Revenue CAGR",
    "pat_cagr_5yr": "PAT CAGR",
    "interest_coverage": "Interest Cover",
    "asset_turnover": "Asset Turnover",
    "composite_quality_score": "Quality Score"
}

selected_row = latest[
    latest["company_id"] == selected_company
]

peer_avg = latest[
    latest["company_id"].isin(peer_company_ids)
]

company_values = []

peer_values = []

labels = []

for column, label in metrics.items():

    labels.append(label)

    company_values.append(
        float(
            selected_row[column]
            .fillna(0)
            .iloc[0]
        )
    )

    peer_values.append(
        float(
            peer_avg[column]
            .fillna(0)
            .mean()
        )
    )

fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=company_values,
        theta=labels,
        fill="toself",
        name=selected_name
    )
)

fig.add_trace(
    go.Scatterpolar(
        r=peer_values,
        theta=labels,
        fill="toself",
        name="Peer Average"
    )
)

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True
        )
    ),
    height=550,
    showlegend=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ---------------------------------------------------
# KPI Cards
# ---------------------------------------------------

company = selected_row.iloc[0]

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "ROE %",
    display_value(company["return_on_equity_pct"])
)

c2.metric(
    "Net Margin %",
    display_value(company["net_profit_margin_pct"])
)

c3.metric(
    "Revenue CAGR %",
    display_value(company["revenue_cagr_5yr"])
)

c4.metric(
    "Quality Score",
    display_value(company["composite_quality_score"])
)

st.divider()

# ---------------------------------------------------
# Comparison Table
# ---------------------------------------------------

st.subheader("Peer Comparison Table")

table = latest[
    latest["company_id"].isin(peer_company_ids)
][
    [
        "company_name",
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "interest_coverage",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "composite_quality_score"
    ]
].copy()

table.columns = [
    "Company",
    "ROE %",
    "Net Margin %",
    "Debt/Equity",
    "Interest Cover",
    "Revenue CAGR %",
    "PAT CAGR %",
    "Quality Score"
]

table = table.sort_values(
    "Quality Score",
    ascending=False
)
table = table.fillna("N/A")

st.dataframe(
    table.style.highlight_max(
        subset=["Quality Score"],
        color="#1f6f43"
    ),
    use_container_width=True,
    hide_index=True
)