import sqlite3
import pandas as pd
import numpy as np

DB_PATH = "db/nifty100.db"


def load_ratios():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
    f.*,
    s.broad_sector
    FROM financial_ratios f
    LEFT JOIN sectors s
    ON f.company_id = s.company_id
    """

    df = pd.read_sql(query, conn)
    # Remove TTM rows
    df = df[df["year"] != "TTM"].copy()

    # Keep latest annual record per company
    df = (
    df.sort_values(["company_id", "year"])
      .groupby("company_id")
      .tail(1)
      .reset_index(drop=True)
)

    conn.close()

    return df


def apply_filter(df, column, minimum=None, maximum=None):
    """
    Generic filter helper
    """

    if minimum is not None:
        df = df[df[column] >= minimum]

    if maximum is not None:
        df = df[df[column] <= maximum]

    return df

def normalize(series):
    s = series.fillna(series.median())

    p10 = s.quantile(0.10)
    p90 = s.quantile(0.90)

    s = s.clip(lower=p10, upper=p90)

    return (
        (s - s.min())
        /
        (s.max() - s.min())
    ) * 100

def calculate_composite_score(df):

    roe_score = normalize(
        df["return_on_equity_pct"]
    )

    npm_score = normalize(
        df["net_profit_margin_pct"]
    )

    revenue_score = normalize(
        df["revenue_cagr_5yr"]
    )

    pat_score = normalize(
        df["pat_cagr_5yr"]
    )

    fcf_score = normalize(
        df["free_cash_flow_cr"]
    )

    icr_score = normalize(
        df["interest_coverage"]
            .replace(np.inf, 1000)
    )

    de_score = (
        100 -
        normalize(
            df["debt_to_equity"]
        )
    )

    score = (
        roe_score * 0.25 +
        npm_score * 0.10 +
        revenue_score * 0.15 +
        pat_score * 0.15 +
        fcf_score * 0.20 +
        de_score * 0.10 +
        icr_score * 0.05
    )

    return score.round(2)

def run_screener(filters):
    """
    Apply screener filters
    """

    df = load_ratios()

    for metric, condition in filters.items():

        # Interest Coverage special handling
        if metric == "interest_coverage":

            df["interest_coverage"] = (
                df["interest_coverage"]
                .fillna(float("inf"))
            )

        # Debt-to-Equity special handling
        if (
            metric == "debt_to_equity"
            and "broad_sector" in df.columns
        ):

            financials = df[
                df["broad_sector"] == "Financials"
            ]

            others = df[
                df["broad_sector"] != "Financials"
            ]

            others = apply_filter(
                others,
                metric,
                minimum=condition.get("min"),
                maximum=condition.get("max")
            )

            df = pd.concat(
                [financials, others],
                ignore_index=True
            )

            continue

        df = apply_filter(
            df,
            metric,
            minimum=condition.get("min"),
            maximum=condition.get("max")
        )

    # Placeholder score
    df["composite_quality_score"] = (
    calculate_composite_score(df)
    )

    return df.sort_values(
        by="composite_quality_score",
        ascending=False
    )
