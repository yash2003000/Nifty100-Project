CREATE TABLE companies (
    company_id TEXT,
    company_name TEXT
);

CREATE TABLE profitandloss (
    company_id TEXT,
    year TEXT
);

CREATE TABLE balancesheet (
    company_id TEXT,
    year TEXT
);

CREATE TABLE cashflow (
    company_id TEXT,
    year TEXT
);

CREATE TABLE analysis (
    company_id TEXT
);

CREATE TABLE documents (
    company_id TEXT
);

CREATE TABLE prosandcons (
    company_id TEXT
);

CREATE TABLE sectors (
    company_id TEXT
);

CREATE TABLE stock_prices (
    company_id TEXT
);

CREATE TABLE peer_groups (
    company_id TEXT
);

CREATE TABLE financial_ratios (
    company_id TEXT,
    year TEXT
);

CREATE TABLE load_audit (
    table_name TEXT,
    rows_loaded INTEGER,
    load_timestamp TEXT,
    status TEXT
);
