def calculate_fcf(
    operating_activity,
    investing_activity
):
    """
    Free Cash Flow

    FCF = CFO + CFI
    """

    return (
        operating_activity
        + investing_activity
    )
def cfo_quality_score(
    cfo,
    pat
):
    """
    CFO / PAT Quality Score
    """

    if pat == 0:
        return None

    ratio = cfo / pat

    if ratio > 1:
        return "High Quality"

    if ratio >= 0.5:
        return "Moderate"

    return "Accrual Risk"
def capex_intensity(
    investing_activity,
    sales
):
    """
    CapEx Intensity
    """

    if sales == 0:
        return None, None

    value = (
        abs(investing_activity)
        / sales
    ) * 100

    if value < 3:
        label = "Asset Light"

    elif value <= 8:
        label = "Moderate"

    else:
        label = "Capital Intensive"

    return round(value, 2), label
def fcf_conversion_rate(
    fcf,
    operating_profit
):
    """
    FCF Conversion Rate
    """

    if operating_profit == 0:
        return None

    return round(
        (
            fcf
            / operating_profit
        ) * 100,
        2
    )
def capital_allocation_pattern(
    cfo,
    cfi,
    cff
):
    """
    Capital Allocation Pattern
    """

    signs = (
        "+" if cfo > 0 else "-",
        "+" if cfi > 0 else "-",
        "+" if cff > 0 else "-"
    )

    patterns = {
        ("+", "-", "-"): "Reinvestor",
        ("+", "+", "-"): "Liquidating Assets",
        ("-", "+", "+"): "Distress Signal",
        ("-", "-", "+"): "Growth Funded by Debt",
        ("+", "+", "+"): "Cash Accumulator",
        ("-", "-", "-"): "Pre-Revenue",
        ("+", "-", "+"): "Mixed"
    }

    return patterns.get(
        signs,
        "Unknown"
    )
