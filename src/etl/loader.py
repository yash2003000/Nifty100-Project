import pandas as pd
from pathlib import Path

RAW_DATA_PATH = Path("data/raw")
def load_companies():
    file_path = RAW_DATA_PATH / "companies.xlsx"

    df = pd.read_excel(file_path, header=1)

    return df
def load_profitandloss():
    file_path = RAW_DATA_PATH / "profitandloss.xlsx"

    df = pd.read_excel(file_path, header=1)

    return df
def load_balancesheet():
    file_path = RAW_DATA_PATH / "balancesheet.xlsx"

    df = pd.read_excel(file_path, header=1)

    return df


def load_cashflow():
    file_path = RAW_DATA_PATH / "cashflow.xlsx"

    df = pd.read_excel(file_path, header=1)

    return df


def load_analysis():
    file_path = RAW_DATA_PATH / "analysis.xlsx"

    df = pd.read_excel(file_path, header=1)

    return df
def load_documents():
    file_path = RAW_DATA_PATH / "documents.xlsx"

    df = pd.read_excel(file_path, header=1)

    return df


def load_prosandcons():
    file_path = RAW_DATA_PATH / "prosandcons.xlsx"

    df = pd.read_excel(file_path, header=1)

    return df

def load_sectors():
    file_path = RAW_DATA_PATH / "sectors.xlsx"
    df = pd.read_excel(file_path)
    return df


def load_stock_prices():
    file_path = RAW_DATA_PATH / "stock_prices.xlsx"
    df = pd.read_excel(file_path)
    return df


def load_peer_groups():
    file_path = RAW_DATA_PATH / "peer_groups.xlsx"
    df = pd.read_excel(file_path)
    return df


def load_market_cap():
    file_path = RAW_DATA_PATH / "market_cap.xlsx"
    df = pd.read_excel(file_path)
    return df


def load_financial_ratios():
    file_path = RAW_DATA_PATH / "financial_ratios.xlsx"
    df = pd.read_excel(file_path)
    return df
