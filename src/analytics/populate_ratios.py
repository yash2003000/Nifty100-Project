import sqlite3
import pandas as pd

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    debt_to_equity,
    interest_coverage_ratio,
    asset_turnover
)

from src.analytics.cashflow_kpis import (
    calculate_fcf,
    capex_intensity
)
from src.analytics.cagr import calculate_cagr

# ------------------------------------
# DATABASE CONNECTION
# ------------------------------------

conn = sqlite3.connect("db/nifty100.db")

# ------------------------------------
# LOAD TABLES
# ------------------------------------

pl = pd.read_sql(
    "SELECT * FROM profitandloss",
    conn
)

bs = pd.read_sql(
    "SELECT * FROM balancesheet",
    conn
)

cf = pd.read_sql(
    "SELECT * FROM cashflow",
    conn
)

# ------------------------------------
# MERGE DATA
# ------------------------------------

df = (
    pl.merge(
        bs,
        on=["company_id", "year"],
        how="left"
    )
    .merge(
        cf,
        on=["company_id", "year"],
        how="left"
    )
)

print("Merged Shape:", df.shape)

# ------------------------------------
# KPI CALCULATIONS
# ------------------------------------

df["net_profit_margin_pct"] = df.apply(
    lambda x: net_profit_margin(
        x["net_profit"],
        x["sales"]
    ),
    axis=1
)

df["operating_profit_margin_pct"] = df.apply(
    lambda x: operating_profit_margin(
        x["operating_profit"],
        x["sales"]
    ),
    axis=1
)

df["return_on_equity_pct"] = df.apply(
    lambda x: return_on_equity(
        x["net_profit"],
        x["equity_capital"],
        x["reserves"]
    ),
    axis=1
)

df["debt_to_equity"] = df.apply(
    lambda x: debt_to_equity(
        x["borrowings"],
        x["equity_capital"],
        x["reserves"]
    ),
    axis=1
)

df["interest_coverage"] = df.apply(
    lambda x: interest_coverage_ratio(
        x["operating_profit"],
        x["other_income"],
        x["interest"]
    ),
    axis=1
)

df["asset_turnover"] = df.apply(
    lambda x: asset_turnover(
        x["sales"],
        x["total_assets"]
    ),
    axis=1
)

df["free_cash_flow_cr"] = df.apply(
    lambda x: calculate_fcf(
        x["operating_activity"],
        x["investing_activity"]
    ),
    axis=1
)

df["capex_cr"] = df.apply(
    lambda x: capex_intensity(
        x["investing_activity"],
        x["sales"]
    )[0],
    axis=1
)

# ------------------------------------
# EXISTING FIELDS
# ------------------------------------

df["earnings_per_share"] = df["eps"]

df["book_value_per_share"] = (
    (df["equity_capital"] + df["reserves"])
    / df["equity_capital"]
)

df["dividend_payout_ratio_pct"] = df["dividend_payout"]

df["total_debt_cr"] = df["borrowings"]

df["cash_from_operations_cr"] = df["operating_activity"]

# ------------------------------------
# 5 YEAR CAGR CALCULATIONS
# ------------------------------------

df = df.sort_values(
    ["company_id", "year"]
)

df["revenue_cagr_5yr"] = None
df["pat_cagr_5yr"] = None
df["eps_cagr_5yr"] = None

for company in df["company_id"].unique():

    company_df = df[
        df["company_id"] == company
    ].copy()

    company_df = company_df.sort_values(
        "year"
    )

    for i in range(5, len(company_df)):

        current_idx = company_df.index[i]

        start_sales = company_df.iloc[i - 5]["sales"]
        end_sales = company_df.iloc[i]["sales"]

        start_pat = company_df.iloc[i - 5]["net_profit"]
        end_pat = company_df.iloc[i]["net_profit"]

        start_eps = company_df.iloc[i - 5]["eps"]
        end_eps = company_df.iloc[i]["eps"]

        revenue_cagr, _ = calculate_cagr(
            start_sales,
            end_sales,
            5
        )

        pat_cagr, _ = calculate_cagr(
            start_pat,
            end_pat,
            5
        )

        eps_cagr, _ = calculate_cagr(
            start_eps,
            end_eps,
            5
        )

        df.loc[
            current_idx,
            "revenue_cagr_5yr"
        ] = revenue_cagr

        df.loc[
            current_idx,
            "pat_cagr_5yr"
        ] = pat_cagr

        df.loc[
            current_idx,
            "eps_cagr_5yr"
        ] = eps_cagr

        # ------------------------------------
# COMPOSITE QUALITY SCORE
# ------------------------------------

df["composite_quality_score"] = (
    df["return_on_equity_pct"].fillna(0)
    +
    df["net_profit_margin_pct"].fillna(0)
    +
    df["asset_turnover"].fillna(0)
)


# ------------------------------------
# PREVIEW
# ------------------------------------
print(df.columns.tolist())
ratio_df = df[
    [
        "company_id",
        "year",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "return_on_equity_pct",
        "debt_to_equity",
        "interest_coverage",
        "asset_turnover",
        "free_cash_flow_cr",
        "capex_cr",
        "earnings_per_share",
        "book_value_per_share",
        "dividend_payout_ratio_pct",
        "total_debt_cr",
        "cash_from_operations_cr",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr",
        "composite_quality_score",
    ]
]

ratio_df.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)

print("financial_ratios table populated")
print("Rows:", len(ratio_df))

conn.close()

