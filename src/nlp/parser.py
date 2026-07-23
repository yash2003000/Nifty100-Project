import re
import os
import sqlite3
import pandas as pd

from src.dashboard.utils.db import (
    get_analysis,
    get_ratios
)


# =====================================================
# Output Folder
# =====================================================

OUTPUT_DIR = "output"

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# =====================================================
# Regex Pattern
# =====================================================

PATTERN = re.compile(

    r"(\d+)\s*Years?:?\s*([\-\d.]+)%",

    flags=re.IGNORECASE

)


# =====================================================
# Target Fields
# =====================================================

TARGET_FIELDS = [

    "compounded_sales_growth",

    "compounded_profit_growth",

    "stock_price_cagr",

    "roe"

]


# =====================================================
# Load Data
# =====================================================

analysis = get_analysis().copy()

ratios = get_ratios().copy()


print()

print("=" * 60)

print("Analysis rows :", len(analysis))

print("Ratio rows    :", len(ratios))

print("=" * 60)

print()


# =====================================================
# Parse Function
# =====================================================

def parse_metric(text):

    """
    Example

    10 Years: 21%

    Returns

    (10,21.0)

    """

    if pd.isna(text):

        return None, None

    text = str(text).strip()

    match = PATTERN.search(text)

    if match:

        period = int(match.group(1))

        value = float(match.group(2))

        return period, value

    return None, None


# =====================================================
# Parse Analysis Table
# =====================================================

parsed_rows = []

failure_rows = []


for _, row in analysis.iterrows():

    company = row["company_id"]

    for metric in TARGET_FIELDS:

        text = row.get(metric)

        period, value = parse_metric(text)

        if period is None:

            failure_rows.append(

                {

                    "company_id": company,

                    "metric_type": metric,

                    "original_text": text

                }

            )

        else:

            parsed_rows.append(

                {

                    "company_id": company,

                    "metric_type": metric,

                    "period_years": period,

                    "value_pct": value

                }

            )
            # =====================================================
# Convert to DataFrames
# =====================================================

parsed_df = pd.DataFrame(parsed_rows)

failure_df = pd.DataFrame(failure_rows)


# =====================================================
# Save Parsed Output
# =====================================================

parsed_path = os.path.join(
    OUTPUT_DIR,
    "analysis_parsed.csv"
)

parsed_df.to_csv(
    parsed_path,
    index=False
)


# =====================================================
# Save Parse Failures
# =====================================================

failure_path = os.path.join(
    OUTPUT_DIR,
    "parse_failures.csv"
)

failure_df.to_csv(
    failure_path,
    index=False
)


# =====================================================
# Latest Ratio Data
# =====================================================

latest_ratios = (

    ratios

    .sort_values("year")

    .groupby("company_id")

    .tail(1)

).copy()


# =====================================================
# Mapping Parsed Metric
# =====================================================

metric_map = {

    "compounded_sales_growth": "revenue_cagr_5yr",

    "compounded_profit_growth": "pat_cagr_5yr",

    "roe": "return_on_equity_pct"

}


validation_rows = []


# =====================================================
# Cross Validation
# =====================================================

for _, row in parsed_df.iterrows():

    company = row["company_id"]

    metric = row["metric_type"]

    parsed_value = row["value_pct"]

    if metric == "stock_price_cagr":

        continue

    ratio_column = metric_map.get(metric)

    if ratio_column is None:

        continue

    ratio_row = latest_ratios[

        latest_ratios["company_id"] == company

    ]

    if ratio_row.empty:

        continue

    computed_value = ratio_row.iloc[0][ratio_column]

    if pd.isna(computed_value):

        continue

    difference = abs(

        parsed_value - computed_value

    )

    validation_rows.append(

        {

            "company_id": company,

            "metric_type": metric,

            "parsed_value_pct": round(parsed_value,2),

            "computed_value_pct": round(float(computed_value),2),

            "difference_pct": round(difference,2),

            "manual_review": (

                "YES"

                if difference > 5

                else "NO"

            )

        }

    )
    # =====================================================
# Cross Validation Report
# =====================================================

validation_df = pd.DataFrame(validation_rows)

validation_path = os.path.join(
    OUTPUT_DIR,
    "analysis_cross_validation.csv"
)

validation_df.to_csv(
    validation_path,
    index=False
)


# =====================================================
# Manual Review Summary
# =====================================================

manual_review_count = 0

if not validation_df.empty:

    manual_review_count = (

        validation_df["manual_review"]

        == "YES"

    ).sum()


# =====================================================
# Console Summary
# =====================================================

print("=" * 60)
print("NLP ANALYSIS PARSER COMPLETED")
print("=" * 60)

print(f"Parsed Records      : {len(parsed_df)}")
print(f"Parse Failures      : {len(failure_df)}")
print(f"Validation Records  : {len(validation_df)}")
print(f"Manual Reviews      : {manual_review_count}")

print()
print("Files Generated")
print(f"✓ {parsed_path}")
print(f"✓ {failure_path}")
print(f"✓ {validation_path}")

print("=" * 60)
