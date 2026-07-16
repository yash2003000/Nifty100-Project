import streamlit as st
import plotly.express as px
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

st.title("📈 Trend Analysis")

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
    "OPM %": ("opm_percentage", pl),
    "EPS": ("eps", pl),
    "Operating Cash Flow": ("operating_activity", cf),
    "Net Cash Flow": ("net_cash_flow", cf),
    "Reserves": ("reserves", bs),
    "Borrowings": ("borrowings", bs)
}

selected_metrics = st.multiselect(
    "Select up to 3 metrics",
    list(metric_options.keys()),
    default=["Revenue"]
)

selected_metrics = selected_metrics[:3]

fig = px.line()

for metric_name in selected_metrics:

    column_name, source_df = metric_options[metric_name]

    temp = source_df[
        source_df["company_id"] == company
    ].copy()

    temp = temp.sort_values("year")

    fig.add_scatter(
        x=temp["year"],
        y=temp[column_name],
        mode="lines+markers",
        name=metric_name
    )

    yoy = temp[column_name].pct_change() * 100

    for x, y, pct in zip(
        temp["year"],
        temp[column_name],
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

fig.update_layout(
    height=700,
    xaxis_title="Year",
    yaxis_title="Value"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
