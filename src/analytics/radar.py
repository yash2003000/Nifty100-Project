import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

DB_PATH = "db/nifty100.db"
OUTPUT_DIR = "reports/radar_charts"

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)


METRICS = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "pat_cagr_5yr",
    "revenue_cagr_5yr",
    "asset_turnover",
    "composite_quality_score"
]


def load_latest_ratios():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT *
    FROM financial_ratios
    WHERE year = 'TTM'
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def load_peer_groups():

    conn = sqlite3.connect(DB_PATH)

    peer = pd.read_sql(
        """
        SELECT DISTINCT
            company_id,
            peer_group_name
        FROM peer_percentiles
        """,
        conn,
    )

    conn.close()

    return peer


def minmax_scale(series):

    if series.max() == series.min():
        return pd.Series([50] * len(series))

    return (
        (series - series.min())
        /
        (series.max() - series.min())
        * 100
    )


def prepare_data():

    ratios = load_latest_ratios()

    peer = load_peer_groups()

    df = ratios.merge(peer, on="company_id")

    for metric in METRICS:

        if metric not in df.columns:
            continue

        if metric == "debt_to_equity":

            scaled = minmax_scale(df[metric])

            df[f"{metric}_score"] = 100 - scaled

        else:

            df[f"{metric}_score"] = minmax_scale(df[metric])

    return df


def create_radar_chart(
    company_row,
    peer_avg,
    company_name
):

    labels = [
        "ROE",
        "NPM",
        "D/E",
        "FCF",
        "PAT CAGR",
        "REV CAGR",
        "AT",
        "COMP"
    ]

    company_values = [
        company_row["return_on_equity_pct_score"],
        company_row["net_profit_margin_pct_score"],
        company_row["debt_to_equity_score"],
        company_row["free_cash_flow_cr_score"],
        company_row["pat_cagr_5yr_score"],
        company_row["revenue_cagr_5yr_score"],
        company_row["asset_turnover_score"],
        company_row["composite_quality_score_score"]
    ]

    peer_values = [
        peer_avg["return_on_equity_pct_score"],
        peer_avg["net_profit_margin_pct_score"],
        peer_avg["debt_to_equity_score"],
        peer_avg["free_cash_flow_cr_score"],
        peer_avg["pat_cagr_5yr_score"],
        peer_avg["revenue_cagr_5yr_score"],
        peer_avg["asset_turnover_score"],
        peer_avg["composite_quality_score_score"]
    ]

    angles = np.linspace(
        0,
        2*np.pi,
        len(labels),
        endpoint=False
    )

    company_values += company_values[:1]
    peer_values += peer_values[:1]

    angles = np.concatenate(
        [angles, [angles[0]]]
    )

    fig = plt.figure(figsize=(8, 8))

    ax = plt.subplot(111, polar=True)

    ax.plot(
        angles,
        company_values,
        linewidth=2
    )

    ax.fill(
        angles,
        company_values,
        alpha=0.25
    )

    ax.plot(
        angles,
        peer_values,
        linestyle="--",
        linewidth=2
    )

    ax.set_xticks(angles[:-1])

    ax.set_xticklabels(labels)

    ax.set_title(
        f"{company_name} Peer Comparison",
        pad=20
    )

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/{company_name}_radar.png"
    )

    plt.close()


def generate_all_radars():

    df = prepare_data()

    peer_groups = df["peer_group_name"].unique()

    total = 0

    for group in peer_groups:

        group_df = df[
            df["peer_group_name"] == group
        ]

        score_cols = [
            c
            for c in group_df.columns
            if c.endswith("_score")
        ]

        peer_avg = (
            group_df[score_cols]
            .mean()
        )

        for _, row in group_df.iterrows():

            create_radar_chart(
                row,
                peer_avg,
                row["company_id"]
            )

            total += 1

    print(
        f"{total} radar charts generated"
    )


if __name__ == "__main__":
    generate_all_radars()
