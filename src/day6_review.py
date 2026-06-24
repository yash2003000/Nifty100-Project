import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT company_id,
COUNT(DISTINCT year) as year_count
FROM profitandloss
GROUP BY company_id
HAVING COUNT(DISTINCT year) < 5
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()
