from .cagr import *
def calculate_cagr(start_value, end_value, years):
    """
    CAGR Formula

    ((end/start) ** (1/years) - 1) * 100
    """

    if years <= 0:
        return None, "INVALID_YEARS"

    if start_value == 0:
        return None, "ZERO_BASE"

    if start_value > 0 and end_value > 0:

        cagr = (
            (end_value / start_value) **
            (1 / years) - 1
        ) * 100

        return round(cagr, 2), None

    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    return None, "UNKNOWN"
def validate_history(data_points, required_years):

    if len(data_points) < required_years + 1:
        return False

    return True
