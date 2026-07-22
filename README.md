# 📊 Nifty100 Financial Analytics Platform

A comprehensive financial analytics platform for analyzing Nifty100 companies using **Python, Pandas, SQLite, Plotly, Streamlit, and Excel reporting**.

The project automates financial data ingestion, validation, ratio computation, peer comparison, stock screening, valuation analysis, and interactive dashboard visualization.

---

# 🚀 Project Overview

The platform provides an end-to-end workflow for financial analysis:

- Automated ETL pipeline
- Data Quality Validation
- SQLite Financial Database
- Financial Ratio Engine
- Composite Quality Scoring
- Stock Screening Engine
- Peer Comparison Engine
- Capital Allocation Analysis
- Interactive Streamlit Dashboard
- Valuation Module
- Excel & CSV Report Generation

---

# 🏗 Technology Stack

- Python
- Pandas
- NumPy
- SQLite
- Streamlit
- Plotly
- OpenPyXL
- Matplotlib
- Git
- GitHub

---

# 📁 Project Structure

```
src/
│
├── analytics/
│   ├── valuation.py
│   ├── peer.py
│   ├── radar.py
│   ├── ratios.py
│   └── ...
│
├── dashboard/
│   ├── app.py
│   ├── pages/
│   │
│   ├── 01_home.py
│   ├── 02_profile.py
│   ├── 03_screener.py
│   ├── 04_peers.py
│   ├── 05_trends.py
│   ├── 06_sectors.py
│   ├── 07_capital.py
│   └── 08_reports.py
│
├── etl/
│
└── utils/

db/
output/
reports/
tests/
config/
```

---

# ✅ Sprint 1 – Data Foundation

### Completed

- Environment Setup
- Excel Loader
- Data Normalization
- Data Quality Validation
- SQLite Database Schema
- Database Loader

### Outputs

- SQLite Database
- Data Quality Reports
- Validation Logs

---

# ✅ Sprint 2 – Financial Ratio Engine

Implemented financial ratio computation for every company.

### Ratios Generated

- ROE
- ROCE
- Net Profit Margin
- Operating Profit Margin
- Debt to Equity
- Interest Coverage
- Asset Turnover
- Revenue CAGR
- PAT CAGR
- EPS CAGR
- Free Cash Flow
- Composite Quality Score

### Outputs

- financial_ratios table
- Ratio Reports
- Validation Reports

---

# ✅ Sprint 3 – Screener & Peer Comparison

## Financial Screener

Implemented predefined screeners:

- Quality Compounder
- Value Pick
- Growth Accelerator
- Dividend Champion
- Debt-Free Blue Chip
- Turnaround Watch

## Peer Comparison Engine

Implemented:

- 11 Peer Groups
- Peer Percentile Rankings
- Benchmark Company Identification
- Radar Chart Visualizations

### Outputs

- screener_output.xlsx
- peer_comparison.xlsx
- Radar Charts
- Peer Percentile Database

---

# ✅ Sprint 4 – Dashboard & Valuation Module

Implemented a complete interactive Streamlit dashboard consisting of **8 analytics screens**.

---

# 📈 Dashboard Screens

## 1. Home Dashboard

Displays:

- Average ROE
- Median P/E
- Median Debt/Equity
- Revenue CAGR
- Debt-Free Companies
- Sector Distribution
- Top Quality Companies

---

## 2. Company Profile

Displays:

- Company Information
- Company Logo
- Financial KPIs
- Revenue History
- Net Profit History
- ROE Trend
- ROCE Trend
- Growth Analysis
- Pros & Cons

---

## 3. Financial Screener

Features:

- Multi-metric filtering
- Live screening
- Preset Screeners
- CSV Export

---

## 4. Peer Comparison

Features:

- Peer Group Selection
- Benchmark Company
- Radar Comparison Chart
- KPI Comparison
- Peer Ranking Table

---

## 5. Trend Analysis

Features:

- Multi-metric Comparison
- YoY Growth Visualization
- Historical Financial Trends

---

## 6. Sector Analysis

Features:

- Sector Bubble Chart
- Sector KPI Comparison
- Revenue vs ROE Analysis

---

## 7. Capital Allocation Map

Features:

- Interactive Treemap
- Capital Allocation Patterns
- Company-wise Pattern Explorer
- Pattern Statistics
- CSV Download

---

## 8. Annual Reports

Features:

- Company Search
- Available Annual Reports
- Direct BSE PDF Links
- Report Availability Detection

---

# 💰 Valuation Module

Implemented:

- Free Cash Flow Yield
- Sector Median P/E
- Five-Year Median P/E
- Valuation Flags

Companies are classified as:

- ✅ Fair
- ⚠️ Caution
- 💰 Discount

### Outputs

- valuation_summary.xlsx
- valuation_flags.csv

---

# 📊 Generated Outputs

Database

```
db/
└── nifty100.db
```

Reports

```
output/

screener_output.xlsx

peer_comparison.xlsx

valuation_summary.xlsx

valuation_flags.csv

load_audit.csv

dq_report.txt
```

Visualizations

```
reports/

radar_charts/
```

---

# ▶ Running the Dashboard

Start the dashboard using:

```bash
streamlit run src/dashboard/app.py
```

The dashboard launches at:

```
http://localhost:8501
```

---

# 🧪 Test Coverage

Implemented automated validation for:

- ETL
- Data Quality
- Ratio Engine
- Cash Flow KPIs
- CAGR Engine
- Screener Logic
- Preset Validation

### Result

```
81 / 81 Tests Passed
```

---

# 📌 Key Features

- Automated Financial ETL Pipeline
- SQLite Analytical Database
- Financial Ratio Engine
- Composite Quality Scoring
- Interactive Streamlit Dashboard
- Capital Allocation Analysis
- Annual Report Explorer
- Peer Comparison Engine
- Radar Charts
- Sector Analytics
- Stock Screener
- Valuation Module
- CSV & Excel Export
- Cached Database Queries
- Interactive Plotly Visualizations

---

# 📷 Dashboard Overview

### Home Screen

Displays market summary KPIs, sector distribution and top quality companies.

### Company Profile

Shows detailed financial metrics, historical trends and company insights.

### Screener

Filter companies dynamically using multiple financial parameters.

### Peer Comparison

Compare companies against industry peers with radar charts and KPI tables.

### Trend Analysis

Visualize long-term financial trends across multiple metrics.

### Sector Analysis

Compare companies within sectors using interactive bubble charts.

### Capital Allocation

Explore capital allocation patterns using treemap visualization.

### Annual Reports

Access historical BSE annual reports directly from the dashboard.

---

# ✅ Project Status

| Sprint | Status |
|---------|--------|
| Sprint 1 | ✅ Completed |
| Sprint 2 | ✅ Completed |
| Sprint 3 | ✅ Completed |
| Sprint 4 | ✅ Completed |

---

# 👨‍💻 Developed By

Yash Chowdhary

B.Tech Computer Science & Engineering

KIIT University