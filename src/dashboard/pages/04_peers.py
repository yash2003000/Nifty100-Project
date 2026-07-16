import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.db import (
    get_peer_groups,
    get_companies,
    get_ratios
)

st.title("👥 Peer Comparison")

peer_groups = get_peer_groups()
companies = get_companies()
ratios = get_ratios()

group_names = sorted(
    peer_groups["peer_group_name"].unique()
)

selected_group = st.selectbox(
    "Select Peer Group",
    group_names
)

group_df = peer_groups[
    peer_groups["peer_group_name"] == selected_group
]

peer_companies = group_df["company_id"].tolist()

selected_company = st.selectbox(
    "Select Company",
    peer_companies
)

benchmark_company = group_df[
    group_df["is_benchmark"] == 1
]["company_id"]

if len(benchmark_company) > 0:
    benchmark_company = benchmark_company.iloc[0]
else:
    benchmark_company = None

st.subheader("Peer Group Members")

peer_table = group_df.copy()

peer_table["Benchmark"] = peer_table["company_id"].apply(
    lambda x: "⭐" if x == benchmark_company else ""
)

st.dataframe(
    peer_table[
        ["company_id", "Benchmark"]
    ],
    use_container_width=True
)

st.divider()

st.subheader("Radar Chart")

latest = ratios.sort_values("year").groupby(
    "company_id"
).tail(1)

metrics = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "interest_coverage",
    "asset_turnover",
    "earnings_per_share",
    "book_value_per_share"
]

selected_row = latest[
    latest["company_id"] == selected_company
]

peer_avg = latest[
    latest["company_id"].isin(peer_companies)
][metrics].mean()

if not selected_row.empty:

    company_values = (
        selected_row[metrics]
        .fillna(0)
        .iloc[0]
        .tolist()
    )

    peer_values = (
        peer_avg
        .fillna(0)
        .tolist()
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=company_values,
            theta=metrics,
            fill="toself",
            name=selected_company
        )
    )

    fig.add_trace(
        go.Scatterpolar(
            r=peer_values,
            theta=metrics,
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
        showlegend=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

st.subheader(
    "Peer KPI Comparison"
)

peer_kpis = latest[
    latest["company_id"].isin(peer_companies)
][
    [
        "company_id",
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "composite_quality_score"
    ]
]

st.dataframe(
    peer_kpis,
    use_container_width=True
)

if benchmark_company:
    st.success(
        f"Benchmark Company: {benchmark_company}"
    )
    