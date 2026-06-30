from src.analytics.cashflow_kpis import (
    calculate_fcf,
    cfo_quality_score,
    capex_intensity,
    fcf_conversion_rate,
    capital_allocation_pattern
)

def test_fcf():
    assert (
        calculate_fcf(
            1000,
            -400
        )
        == 600
    )
def test_high_quality():

    assert (
        cfo_quality_score(
            120,
            100
        )
        == "High Quality"
    )


def test_moderate():

    assert (
        cfo_quality_score(
            75,
            100
        )
        == "Moderate"
    )


def test_accrual_risk():

    assert (
        cfo_quality_score(
            20,
            100
        )
        == "Accrual Risk"
    )


def test_pat_zero():

    assert (
        cfo_quality_score(
            100,
            0
        )
        is None
    )
def test_asset_light():

    value, label = capex_intensity(
        -20,
        1000
    )

    assert label == "Asset Light"


def test_moderate_capex():

    value, label = capex_intensity(
        -50,
        1000
    )

    assert label == "Moderate"


def test_capital_intensive():

    value, label = capex_intensity(
        -200,
        1000
    )

    assert label == "Capital Intensive"


def test_sales_zero():

    value, label = capex_intensity(
        -200,
        0
    )

    assert value is None
def test_fcf_conversion():

    assert (
        fcf_conversion_rate(
            500,
            1000
        )
        == 50.0
    )


def test_fcf_conversion_zero_profit():

    assert (
        fcf_conversion_rate(
            500,
            0
        )
        is None
    )
def test_reinvestor():

    assert (
        capital_allocation_pattern(
            100,
            -50,
            -20
        )
        == "Reinvestor"
    )


def test_liquidating_assets():

    assert (
        capital_allocation_pattern(
            100,
            50,
            -20
        )
        == "Liquidating Assets"
    )


def test_distress_signal():

    assert (
        capital_allocation_pattern(
            -100,
            50,
            20
        )
        == "Distress Signal"
    )


def test_growth_funded_by_debt():

    assert (
        capital_allocation_pattern(
            -100,
            -50,
            20
        )
        == "Growth Funded by Debt"
    )


def test_cash_accumulator():

    assert (
        capital_allocation_pattern(
            100,
            50,
            20
        )
        == "Cash Accumulator"
    )


def test_pre_revenue():

    assert (
        capital_allocation_pattern(
            -100,
            -50,
            -20
        )
        == "Pre-Revenue"
    )


def test_mixed():

    assert (
        capital_allocation_pattern(
            100,
            -50,
            20
        )
        == "Mixed"
    )
