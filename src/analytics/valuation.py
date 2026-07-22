import os
import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"

OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ======================================================
# Load Database
# ======================================================

conn = sqlite3.connect(DB_PATH)

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

sectors = pd.read_sql(
    "SELECT * FROM sectors",
    conn
)

market = pd.read_sql(
    "SELECT * FROM market_cap",
    conn
)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

cashflow = pd.read_sql(
    "SELECT * FROM cashflow",
    conn
)

conn.close()


# ======================================================
# Convert numeric columns
# ======================================================

market_cols = [
    "market_cap_crore",
    "pe_ratio",
    "pb_ratio",
    "ev_ebitda"
]

for col in market_cols:

    if col in market.columns:

        market[col] = pd.to_numeric(
            market[col],
            errors="coerce"
        )


ratio_cols = [
    "free_cash_flow_cr"
]

for col in ratio_cols:

    if col in ratios.columns:

        ratios[col] = pd.to_numeric(
            ratios[col],
            errors="coerce"
        )


if "free_cash_flow_cr" not in ratios.columns:

    if "free_cash_flow_cr" in cashflow.columns:

        ratios = ratios.merge(

            cashflow[
                [
                    "company_id",
                    "year",
                    "free_cash_flow_cr"
                ]
            ],

            on=[
                "company_id",
                "year"
            ],

            how="left"
        )


# ======================================================
# Ignore TTM rows
# ======================================================

market = market[
    market["year"] != "TTM"
].copy()

ratios = ratios[
    ratios["year"] != "TTM"
].copy()


# ======================================================
# Latest Market Cap
# ======================================================

market_latest = (

    market

    .sort_values("year")

    .groupby("company_id")

    .tail(1)

)


# ======================================================
# Latest Financial Ratios
# ======================================================

ratios_latest = (

    ratios

    .sort_values("year")

    .groupby("company_id")

    .tail(1)

)


# ======================================================
# Merge everything
# ======================================================

df = companies.merge(

    sectors[
        [
            "company_id",
            "broad_sector"
        ]
    ],

    left_on="id",

    right_on="company_id",

    how="left"

)
df = df.drop(columns=["company_id"])


df = df.merge(

    market_latest[
        [
            "company_id",
            "market_cap_crore",
            "pe_ratio",
            "pb_ratio",
            "ev_ebitda"
        ]
    ],

    left_on="id",

    right_on="company_id",

    how="left"

)
df = df.drop(columns=["company_id"])


df = df.merge(

    ratios_latest[
        [
            "company_id",
            "free_cash_flow_cr"
        ]
    ],

    left_on="id",

    right_on="company_id",

    how="left"

)
df = df.drop(columns=["company_id"])

# ======================================================
# FCF Yield
# ======================================================

df["FCF_yield_pct"] = (

    df["free_cash_flow_cr"]

    /

    df["market_cap_crore"]

) * 100


df["FCF_yield_pct"] = df["FCF_yield_pct"].round(2)
# ======================================================
# Sector Median P/E
# ======================================================

sector_pe = (

    df.groupby("broad_sector")["pe_ratio"]

    .median()

    .reset_index()

    .rename(
        columns={
            "pe_ratio": "sector_median_pe"
        }
    )

)

df = df.merge(

    sector_pe,

    on="broad_sector",

    how="left"

)


# ======================================================
# Calculate 5-Year Median P/E
# ======================================================

market_5yr = market.copy()

market_5yr["year_num"] = pd.to_numeric(
    market_5yr["year"],
    errors="coerce"
)

market_5yr = market_5yr.dropna(
    subset=["year_num"]
)

latest_year = int(
    market_5yr["year_num"].max()
)

market_5yr = market_5yr[
    market_5yr["year_num"] >= latest_year - 4
]

median_5yr = (

    market_5yr.groupby("company_id")["pe_ratio"]

    .median()

    .reset_index()

    .rename(
        columns={
            "pe_ratio": "five_year_median_pe"
        }
    )

)

df = df.merge(

    median_5yr,

    left_on="id",

    right_on="company_id",

    how="left"

)
df = df.drop(columns=["company_id"])

# ======================================================
# PE vs Sector Median %
# ======================================================

df["PE_vs_sector_median_pct"] = (

    (

        df["pe_ratio"]

        -

        df["sector_median_pe"]

    )

    /

    df["sector_median_pe"]

) * 100

df["PE_vs_sector_median_pct"] = (

    df["PE_vs_sector_median_pct"]

    .round(2)

)


# ======================================================
# Valuation Flag Logic
# ======================================================

def valuation_flag(row):

    pe = row["pe_ratio"]

    sector = row["sector_median_pe"]

    if pd.isna(pe):

        return "Fair"

    if pd.isna(sector):

        return "Fair"

    if pe > sector * 1.5:

        return "Caution"

    elif pe < sector * 0.7:

        return "Discount"

    else:

        return "Fair"


df["flag"] = df.apply(

    valuation_flag,

    axis=1

)
# ======================================================
# Final Output
# ======================================================

summary = df[
    [
        "id",
        "company_name",
        "broad_sector",
        "pe_ratio",
        "pb_ratio",
        "ev_ebitda",
        "FCF_yield_pct",
        "five_year_median_pe",
        "PE_vs_sector_median_pct",
        "flag"
    ]
].copy()

summary.rename(
    columns={
        "id": "company_id",
        "broad_sector": "sector",
        "pe_ratio": "P/E",
        "pb_ratio": "P/B",
        "ev_ebitda": "EV/EBITDA",
        "five_year_median_pe": "5yr_median_PE"
    },
    inplace=True
)

summary = summary.sort_values(
    "company_name"
).reset_index(drop=True)


# ======================================================
# Export valuation_summary.xlsx
# ======================================================

summary_path = os.path.join(
    OUTPUT_DIR,
    "valuation_summary.xlsx"
)

with pd.ExcelWriter(
    summary_path,
    engine="openpyxl"
) as writer:

    summary.to_excel(
        writer,
        index=False,
        sheet_name="Valuation Summary"
    )


# ======================================================
# Export valuation_flags.csv
# ======================================================

flags = summary[
    summary["flag"].isin(
        [
            "Caution",
            "Discount"
        ]
    )
].copy()

flags_path = os.path.join(
    OUTPUT_DIR,
    "valuation_flags.csv"
)

flags.to_csv(
    flags_path,
    index=False
)


# ======================================================
# Console Summary
# ======================================================

print("=" * 60)
print("VALUATION MODULE COMPLETED")
print("=" * 60)

print(f"Companies Processed : {len(summary)}")
print(f"Caution Flags      : {(summary['flag']=='Caution').sum()}")
print(f"Discount Flags     : {(summary['flag']=='Discount').sum()}")
print(f"Fair               : {(summary['flag']=='Fair').sum()}")

print()

print("Files Generated")

print(f"✓ {summary_path}")
print(f"✓ {flags_path}")

print("=" * 60)
