import pytest

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    validate_opm,
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    icr_label,
    icr_warning_flag,
    net_debt,
    asset_turnover,
)


# -----------------------------
# Net Profit Margin Tests
# -----------------------------

def test_net_profit_margin_normal():
    assert net_profit_margin(100, 1000) == 10.0


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(100, 0) is None


# -----------------------------
# Operating Profit Margin Tests
# -----------------------------

def test_operating_profit_margin_normal():
    assert operating_profit_margin(250, 1000) == 25.0


def test_validate_opm_mismatch():
    computed = operating_profit_margin(250, 1000)   # 25%
    source = 23.5

    assert validate_opm(computed, source) is True


# -----------------------------
# ROE Tests
# -----------------------------

def test_return_on_equity_normal():
    result = return_on_equity(
        net_profit=200,
        equity_capital=500,
        reserves=500,
    )

    assert result == 20.0


def test_return_on_equity_negative_equity():
    assert (
        return_on_equity(
            100,
            -100,
            50,
        )
        is None
    )


# -----------------------------
# ROCE Tests
# -----------------------------

def test_return_on_capital_employed_normal():
    result = return_on_capital_employed(
        operating_profit=500,
        depreciation=100,
        equity_capital=1000,
        reserves=500,
        borrowings=500,
    )

    assert result == 20.0


# -----------------------------
# ROA Tests
# -----------------------------

def test_return_on_assets_zero_assets():
    assert return_on_assets(100, 0) is None

def test_debt_to_equity_normal():
    assert debt_to_equity(500, 100, 400) == 1.0

def test_debt_to_equity_debt_free():
    assert debt_to_equity(0, 100, 400) == 0

def test_high_leverage_flag():
    assert high_leverage_flag(6, "IT") is True

def test_high_leverage_financials():
    assert high_leverage_flag(10, "Financials") is False

def test_interest_coverage_ratio_normal():
    assert interest_coverage_ratio(1000, 100, 100) == 11.0

def test_interest_coverage_ratio_zero_interest():
    assert interest_coverage_ratio(1000, 100, 0) is None

def test_icr_label_debt_free():
    assert icr_label(None) == "Debt Free"

def test_asset_turnover_normal():
    assert asset_turnover(1000, 500) == 2.0

