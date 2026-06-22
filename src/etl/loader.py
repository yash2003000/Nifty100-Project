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
