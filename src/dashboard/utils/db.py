import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "db/nifty100.db"


@st.cache_data(ttl=600)
def get_companies():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM companies", conn)
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_ratios():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM financial_ratios", conn)
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_sectors():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM sectors", conn)
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_profit_loss():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM profitandloss", conn)
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_pros_cons():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM prosandcons", conn)
    conn.close()
    return df