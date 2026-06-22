import pandas as pd
import sqlite3

conn = sqlite3.connect("db/nifty100.db")

pl = pd.read_sql("SELECT * FROM profitandloss", conn)
bs = pd.read_sql("SELECT * FROM balancesheet", conn)
cf = pd.read_sql("SELECT * FROM cashflow", conn)

print("Profit & Loss:", pl.shape)
print("Balance Sheet:", bs.shape)
print("Cash Flow:", cf.shape)

df = pl.merge(
    bs,
    on=["company_id", "year"],
    how="inner"
)

df = df.merge(
    cf,
    on=["company_id", "year"],
    how="inner"
)

print("\nMerged Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())
print(df.columns.tolist())

df["net_profit_margin_pct"] = (
    df["net_profit"] / df["sales"]
) * 100

df["return_on_equity_pct"] = (
    df["net_profit"]
    /
    (
        df["equity_capital"]
        + df["reserves"]
    )
) * 100

df["debt_to_equity"] = (
    df["borrowings"]
    /
    (
        df["equity_capital"]
        + df["reserves"]
    )
)

df["asset_turnover"] = (
    df["sales"]
    /
    df["total_assets"]
)

df["free_cash_flow"] = (
    df["operating_activity"]
    +
    df["investing_activity"]
)

print(
    df[
        [
            "company_id",
            "year",
            "net_profit_margin_pct",
            "return_on_equity_pct",
            "debt_to_equity",
            "asset_turnover",
            "free_cash_flow"
        ]
    ].head()
)

financial_ratios = df[
    [
        "company_id",
        "year",
        "net_profit_margin_pct",
        "return_on_equity_pct",
        "debt_to_equity",
        "asset_turnover",
        "free_cash_flow"
    ]
]

print("\nFinancial Ratios Dataset:")
print(financial_ratios.head())

print("\nShape:")
print(financial_ratios.shape)

financial_ratios.to_excel(
    "data/financial_ratios.xlsx",
    index=False
)

print("Excel file saved successfully!")

financial_ratios.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)

print("Database table created successfully!")

print("\nNull Values:")
print(financial_ratios.isnull().sum())

print("\nDuplicate Rows:")
print(financial_ratios.duplicated().sum())
