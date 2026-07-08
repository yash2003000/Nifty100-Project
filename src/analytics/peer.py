import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"
PEER_FILE = "data/raw/peer_groups.xlsx"


def load_peer_data():

    conn = sqlite3.connect(DB_PATH)

    ratios = pd.read_sql("""
        SELECT *
        FROM financial_ratios
    """, conn)

    ratios = ratios[
    ratios["year"] != "TTM"
    ]

    conn.close()

    peer = pd.read_excel(PEER_FILE)

    ratios = ratios.sort_values(
        ["company_id", "year"]
    )

    ratios = (
        ratios.groupby("company_id")
        .tail(1)
        .reset_index(drop=True)
    )

    df = peer.merge(
        ratios,
        on="company_id",
        how="left"
    )

    return df
def percentile_rank(series, reverse=False):

    ranks = series.rank(
        pct=True,
        method="average"
    )

    if reverse:
        ranks = 1 - ranks

    return ranks * 100
def compute_peer_percentiles():

    df = load_peer_data()

    metrics = {
        "return_on_equity_pct": False,
        "operating_profit_margin_pct": False,
        "net_profit_margin_pct": False,
        "debt_to_equity": True,
        "free_cash_flow_cr": False,
        "pat_cagr_5yr": False,
        "revenue_cagr_5yr": False,
        "eps_cagr_5yr": False,
        "interest_coverage": False,
        "asset_turnover": False
    }

    results = []

    for group in df["peer_group_name"].unique():

        group_df = df[
            df["peer_group_name"] == group
        ].copy()

        for metric, reverse in metrics.items():

            group_df[f"{metric}_pct"] = percentile_rank(
                group_df[metric],
                reverse=reverse
            )

            temp = group_df[
                [
                    "company_id",
                    "peer_group_name",
                    "year"
                ]
            ].copy()

            temp["metric"] = metric
            temp["value"] = group_df[metric]
            temp["percentile_rank"] = (
                group_df[f"{metric}_pct"]
            )

            results.append(temp)

    return pd.concat(
        results,
        ignore_index=True
    )
def save_peer_percentiles():

    result = compute_peer_percentiles()

    conn = sqlite3.connect(DB_PATH)

    result.to_sql(
        "peer_percentiles",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print(
        "peer_percentiles table created"
    )
