from src.analytics.cagr import (
    calculate_cagr,
    validate_history
)
def test_normal_cagr():

    value, flag = calculate_cagr(
        100,
        200,
        5
    )

    assert round(value, 2) == 14.87
    assert flag is None
def test_decline_to_loss():

    value, flag = calculate_cagr(
        100,
        -50,
        5
    )

    assert value is None
    assert flag == "DECLINE_TO_LOSS"
def test_turnaround():

    value, flag = calculate_cagr(
        -50,
        100,
        5
    )

    assert value is None
    assert flag == "TURNAROUND"
def test_both_negative():

    value, flag = calculate_cagr(
        -100,
        -50,
        5
    )

    assert value is None
    assert flag == "BOTH_NEGATIVE"
def test_zero_base():

    value, flag = calculate_cagr(
        0,
        100,
        5
    )

    assert value is None
    assert flag == "ZERO_BASE"
def test_invalid_years():

    value, flag = calculate_cagr(
        100,
        200,
        0
    )

    assert value is None
    assert flag == "INVALID_YEARS"
def test_insufficient_history():

    result = validate_history(
        [1, 2, 3],
        5
    )

    assert result is False
def test_sufficient_history():

    result = validate_history(
        [1, 2, 3, 4, 5, 6],
        5
    )

    assert result is True
def test_same_values():

    value, flag = calculate_cagr(
        100,
        100,
        5
    )

    assert value == 0
def test_large_growth():

    value, flag = calculate_cagr(
        100,
        1000,
        10
    )

    assert value > 0
    assert flag is None
    