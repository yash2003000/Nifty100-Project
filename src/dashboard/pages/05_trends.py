import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from utils.db import (
    get_profit_loss,
    get_cashflow,
    get_balance_sheet
)

st.title("📈 Financial Trend Analysis")

pl = get_profit_loss()
cf = get_cashflow()
bs = get_balance_sheet()

companies = sorted(pl["company_id"].dropna().unique())

company = st.selectbox(
    "Select Company",
    companies
)

metric_options = {
    "Revenue": ("sales", pl),
    "Net Profit": ("net_profit", pl),
    "Operating Margin %": ("opm_percentage", pl),
    "EPS": ("eps", pl),
    "Operating Cash Flow": ("operating_activity", cf),
    "Net Cash Flow": ("net_cash_flow", cf),
    "Reserves": ("reserves", bs),
    "Borrowings": ("borrowings", bs)
}

selected_metrics = st.multiselect(
    "Select Metrics (Maximum 3)",
    list(metric_options.keys()),
    default=["Revenue"]
)

selected_metrics = selected_metrics[:3]

st.divider()

fig = go.Figure()

summary = []

export_df = pd.DataFrame()

for metric in selected_metrics:

    column, source = metric_options[metric]

    temp = source[
        source["company_id"] == company
    ].copy()

    temp = temp.sort_values("year")

    temp[column] = pd.to_numeric(
        temp[column],
        errors="coerce"
    )

    fig.add_trace(
        go.Scatter(
            x=temp["year"],
            y=temp[column],
            mode="lines+markers",
            name=metric
        )
    )

    yoy = temp[column].pct_change() * 100

    for x, y, pct in zip(
        temp["year"],
        temp[column],
        yoy
    ):
        if pd.notna(pct):
            fig.add_annotation(
                x=x,
                y=y,
                text=f"{pct:.1f}%",
                showarrow=False,
                font=dict(size=9)
            )

    latest_value = temp[column].dropna()

    if len(latest_value):

        summary.append(
            (
                metric,
                latest_value.iloc[-1]
            )
        )

    export_df["Year"] = temp["year"]
    export_df[metric] = temp[column]

fig.update_layout(
    title=f"{company} Financial Trends",
    height=650,
    hovermode="x unified",
    xaxis_title="Financial Year",
    yaxis_title="Value",
    legend_title="Metrics"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader("Latest Values")

cols = st.columns(
    max(
        len(summary),
        1
    )
)

for i, (metric, value) in enumerate(summary):

    cols[i].metric(
        metric,
        f"{value:,.2f}"
    )

st.divider()

st.subheader("Trend Data")

st.dataframe(
    export_df,
    use_container_width=True,
    hide_index=True
)

csv = export_df.to_csv(
    index=False
)

st.download_button(
    "⬇ Download CSV",
    csv,
    file_name=f"{company}_trend_data.csv",
    mime="text/csv"
)