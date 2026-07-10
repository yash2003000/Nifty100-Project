# Nifty100 Financial Analytics Platform

A comprehensive financial analytics platform built using Python, Pandas, SQLite, and Excel reporting for Nifty100 companies.

---

## Project Overview

This project automates the ingestion, validation, transformation, analysis, screening, and peer comparison of financial data for Nifty100 companies.

The platform provides:

- Automated ETL pipelines
- Financial ratio computation
- Data quality validation
- Stock screening engine
- Peer percentile rankings
- Radar chart visualizations
- Excel-based analytical reports

---

## Sprint 1 – Data Foundation

### Completed

- Environment Setup
- Excel Loader & Normaliser
- Data Quality Validation
- SQLite Database Schema
- Database Loader
- Financial Data Integration

### Outputs

- Data Quality Reports
- SQLite Database
- Validation Logs

---

## Sprint 2 – Financial Ratio Engine

### Completed

- Profitability Ratios
- Leverage Ratios
- Cash Flow KPIs
- Growth Metrics
- Composite Quality Score

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
- Free Cash Flow Metrics

### Outputs

- financial_ratios table
- Ratio Reports
- Validation Reports

---

## Sprint 3 – Screener & Peer Comparison Engine

### Financial Screener

Implemented 6 predefined screeners:

- Quality Compounder
- Value Pick
- Growth Accelerator
- Dividend Champion
- Debt-Free Blue Chip
- Turnaround Watch

### Peer Comparison Engine

Implemented:

- 11 Peer Groups
- 10 Financial Ranking Metrics
- Percentile Rankings
- Benchmark Identification

### Radar Charts

Generated company-level radar charts comparing:

- ROE
- ROCE
- NPM
- D/E
- FCF
- PAT CAGR
- Revenue CAGR
- Composite Score

### Outputs

- output/screener_output.xlsx
- output/peer_comparison.xlsx
- reports/radar_charts/
- peer_percentiles table

---

## Technology Stack

- Python
- Pandas
- NumPy
- SQLite
- OpenPyXL
- Matplotlib
- Git
- GitHub

---

## Project Structure

```
src/
├── etl/
├── kpi/
├── screener/
├── analytics/

db/
output/
reports/
tests/
config/
```

---

## Status

Sprint 1 ✅ Complete

Sprint 2 ✅ Complete

Sprint 3 ✅ Complete

Current Status: Ready for Sprint 4
