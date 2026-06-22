def normalize_ticker(value):
    """
    Convert company ticker to uppercase and remove spaces.
    Example:
    ' tcs ' -> 'TCS'
    """
    if value is None:
        return None

    return str(value).strip().upper()


def normalize_year(value):
    """
    Convert:
    Mar-24 -> 2024-03
    Mar-23 -> 2023-03
    """
    if value is None:
        return None

    value = str(value).strip()

    month_map = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12"
    }

    month = value[:3]
    year = value[-2:]

    year = "20" + year

    return f"{year}-{month_map[month]}"