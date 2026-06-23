import sqlite3

conn = sqlite3.connect("db/nifty100.db")
cursor = conn.cursor()

tables = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
    "documents",
    "prosandcons",
    "sectors",
    "stock_prices",
    "peer_groups",
    "market_cap",
    "financial_ratios"
]

print("=" * 50)
print("DAY 5 DATABASE VALIDATION")
print("=" * 50)

for table in tables:
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<20} {count}")
    except Exception as e:
        print(f"{table:<20} ERROR -> {e}")

print("\n" + "=" * 50)

# Total tables check
cursor.execute("""
SELECT count(*)
FROM sqlite_master
WHERE type='table'
""")

table_count = cursor.fetchone()[0]

print(f"Total Tables Found: {table_count}")

conn.close()
