import sqlite3

from etl.loader import (
    load_companies,
    load_profitandloss,
    load_balancesheet,
    load_cashflow,
    load_analysis,
    load_documents,
    load_prosandcons,
    load_sectors,
    load_stock_prices,
    load_peer_groups,
    load_market_cap,
    load_financial_ratios
)

conn = sqlite3.connect("db/nifty100.db")

load_companies().to_sql(
    "companies",
    conn,
    if_exists="replace",
    index=False
)

load_profitandloss().to_sql(
    "profitandloss",
    conn,
    if_exists="replace",
    index=False
)

load_balancesheet().to_sql(
    "balancesheet",
    conn,
    if_exists="replace",
    index=False
)

load_cashflow().to_sql(
    "cashflow",
    conn,
    if_exists="replace",
    index=False
)

load_analysis().to_sql(
    "analysis",
    conn,
    if_exists="replace",
    index=False
)

load_documents().to_sql(
    "documents",
    conn,
    if_exists="replace",
    index=False
)

load_prosandcons().to_sql(
    "prosandcons",
    conn,
    if_exists="replace",
    index=False
)
load_sectors().to_sql(
    "sectors",
    conn,
    if_exists="replace",
    index=False
)

load_stock_prices().to_sql(
    "stock_prices",
    conn,
    if_exists="replace",
    index=False
)

load_peer_groups().to_sql(
    "peer_groups",
    conn,
    if_exists="replace",
    index=False
)

load_market_cap().to_sql(
    "market_cap",
    conn,
    if_exists="replace",
    index=False
)

load_financial_ratios().to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)
conn.close()

print("Database Loaded Successfully!")
