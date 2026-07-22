import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "db/nifty100.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


@st.cache_data(ttl=600)
def run_query(query, params=None):
    conn = get_connection()

    if params:
        df = pd.read_sql(query, conn, params=params)
    else:
        df = pd.read_sql(query, conn)

    conn.close()
    return df


# ===========================
# MASTER TABLES
# ===========================

@st.cache_data(ttl=600)
def get_companies():
    return run_query("SELECT * FROM companies")


@st.cache_data(ttl=600)
def get_company(company_id):
    df = run_query(
        "SELECT * FROM companies WHERE id=?",
        (company_id,)
    )
    return df.iloc[0] if not df.empty else None


@st.cache_data(ttl=600)
def get_sectors():
    return run_query("SELECT * FROM sectors")


@st.cache_data(ttl=600)
def get_sector(company_id):
    return run_query(
        "SELECT * FROM sectors WHERE company_id=?",
        (company_id,)
    )


# ===========================
# FINANCIAL RATIOS
# ===========================

@st.cache_data(ttl=600)
def get_ratios():
    return run_query("SELECT * FROM financial_ratios")


@st.cache_data(ttl=600)
def get_company_ratios(company_id):
    return run_query(
        """
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        ORDER BY year DESC
        """,
        (company_id,)
    )


# ===========================
# MARKET CAP
# ===========================

@st.cache_data(ttl=600)
def get_market_cap():
    return run_query("SELECT * FROM market_cap")


@st.cache_data(ttl=600)
def get_company_market_cap(company_id):
    return run_query(
        """
        SELECT *
        FROM market_cap
        WHERE company_id=?
        ORDER BY year DESC
        """,
        (company_id,)
    )


# ===========================
# PROFIT & LOSS
# ===========================

@st.cache_data(ttl=600)
def get_profit_loss():
    return run_query("SELECT * FROM profitandloss")


@st.cache_data(ttl=600)
def get_company_profit_loss(company_id):
    return run_query(
        """
        SELECT *
        FROM profitandloss
        WHERE company_id=?
        ORDER BY year DESC
        """,
        (company_id,)
    )


# ===========================
# BALANCE SHEET
# ===========================

@st.cache_data(ttl=600)
def get_balance_sheet():
    return run_query("SELECT * FROM balancesheet")


@st.cache_data(ttl=600)
def get_company_balance_sheet(company_id):
    return run_query(
        """
        SELECT *
        FROM balancesheet
        WHERE company_id=?
        ORDER BY year DESC
        """,
        (company_id,)
    )


# ===========================
# CASHFLOW
# ===========================

@st.cache_data(ttl=600)
def get_cashflow():
    return run_query("SELECT * FROM cashflow")


@st.cache_data(ttl=600)
def get_company_cashflow(company_id):
    return run_query(
        """
        SELECT *
        FROM cashflow
        WHERE company_id=?
        ORDER BY year DESC
        """,
        (company_id,)
    )


# ===========================
# ANALYSIS
# ===========================

@st.cache_data(ttl=600)
def get_analysis():
    return run_query("SELECT * FROM analysis")


@st.cache_data(ttl=600)
def get_company_analysis(company_id):
    return run_query(
        """
        SELECT *
        FROM analysis
        WHERE company_id=?
        """,
        (company_id,)
    )


# ===========================
# PEER GROUPS
# ===========================

@st.cache_data(ttl=600)
def get_peer_groups():
    return run_query("SELECT * FROM peer_groups")


@st.cache_data(ttl=600)
def get_company_peers(company_id):
    return run_query(
        """
        SELECT *
        FROM peer_groups
        WHERE peer_group_name = (
            SELECT peer_group_name
            FROM peer_groups
            WHERE company_id=?
            LIMIT 1
        )
        """,
        (company_id,)
    )


# ===========================
# PEER PERCENTILES
# ===========================

@st.cache_data(ttl=600)
def get_peer_percentiles():
    return run_query("SELECT * FROM peer_percentiles")


# ===========================
# STOCK PRICES
# ===========================

@st.cache_data(ttl=600)
def get_stock_prices():
    return run_query("SELECT * FROM stock_prices")


@st.cache_data(ttl=600)
def get_company_stock_prices(company_id):
    return run_query(
        """
        SELECT *
        FROM stock_prices
        WHERE company_id=?
        ORDER BY date
        """,
        (company_id,)
    )


# ===========================
# DOCUMENTS
# ===========================

@st.cache_data(ttl=600)
def get_documents():
    return run_query("SELECT * FROM documents")


@st.cache_data(ttl=600)
def get_company_documents(company_id):
    return run_query(
        """
        SELECT *
        FROM documents
        WHERE company_id=?
        ORDER BY Year DESC
        """,
        (company_id,)
    )


# ===========================
# PROS & CONS
# ===========================

@st.cache_data(ttl=600)
def get_pros_cons():
    return run_query("SELECT * FROM prosandcons")


@st.cache_data(ttl=600)
def get_company_pros_cons(company_id):
    return run_query(
        """
        SELECT *
        FROM prosandcons
        WHERE company_id=?
        """,
        (company_id,)
    )
