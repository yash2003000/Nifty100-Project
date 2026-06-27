"""
Financial Ratio Engine

Sprint 2 - Day 8
Implements profitability and efficiency ratios.
"""


def net_profit_margin(net_profit, sales):
    """
    Net Profit Margin (%)

    Formula:
    (Net Profit / Sales) * 100
    """

    if sales == 0:
        return None

    return (net_profit / sales) * 100


def operating_profit_margin(operating_profit, sales):
    """
    Operating Profit Margin (%)

    Formula:
    (Operating Profit / Sales) * 100
    """

    if sales == 0:
        return None

    return (operating_profit / sales) * 100
def return_on_equity(net_profit, equity_capital, reserves):
    """
    Return on Equity (ROE)

    Formula:
    Net Profit / (Equity Capital + Reserves) × 100
    """

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return (net_profit / equity) * 100


def return_on_capital_employed(
    operating_profit,
    depreciation,
    equity_capital,
    reserves,
    borrowings,
):
    """
    Return on Capital Employed (ROCE)

    Formula:
    EBIT / (Equity + Reserves + Borrowings) × 100
    """

    ebit = operating_profit - depreciation

    capital = equity_capital + reserves + borrowings

    if capital <= 0:
        return None

    return (ebit / capital) * 100
def return_on_assets(net_profit, total_assets):
    """
    Return on Assets (ROA)

    Formula:
    Net Profit / Total Assets × 100
    """

    if total_assets == 0:
        return None

    return (net_profit / total_assets) * 100


def validate_opm(computed_opm, source_opm):
    """
    Compare computed OPM with source OPM.

    Returns True if difference is greater than 1%.
    """

    if computed_opm is None or source_opm is None:
        return False

    return abs(computed_opm - source_opm) > 1
def debt_to_equity(borrowings, equity_capital, reserves):
    """
    Debt to Equity Ratio
    """

    equity = equity_capital + reserves

    if borrowings == 0:
        return 0

    if equity <= 0:
        return None

    return round(borrowings / equity, 2)
def high_leverage_flag(de_ratio, broad_sector):
    """
    Flag highly leveraged companies
    """

    if de_ratio is None:
        return False

    if broad_sector == "Financials":
        return False

    return de_ratio > 5
def interest_coverage_ratio(
    operating_profit,
    other_income,
    interest
):
    """
    Interest Coverage Ratio
    """

    if interest == 0:
        return None

    return round(
        (operating_profit + other_income) / interest,
        2
    )
def icr_label(icr):
    """
    Label debt free companies
    """

    if icr is None:
        return "Debt Free"

    return ""
def icr_warning_flag(icr):
    """
    Warn if company may struggle
    to cover interest payments
    """

    if icr is None:
        return False

    return icr < 1.5
def net_debt(
    borrowings,
    investments
):
    """
    Net Debt
    """

    return borrowings - investments
def asset_turnover(
    sales,
    total_assets
):
    """
    Asset Turnover Ratio
    """

    if total_assets == 0:
        return None

    return round(
        sales / total_assets,
        2
    )
