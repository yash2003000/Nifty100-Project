import pytest

from src.etl.normaliser import normalize_ticker, normalize_year


# ----------------------------------------------------
# normalize_ticker() Tests
# ----------------------------------------------------

def test_ticker_uppercase():
    assert normalize_ticker("TCS") == "TCS"


def test_ticker_lowercase():
    assert normalize_ticker("tcs") == "TCS"


def test_ticker_mixed_case():
    assert normalize_ticker("TcS") == "TCS"


def test_ticker_with_spaces():
    assert normalize_ticker("  TCS  ") == "TCS"


def test_ticker_lowercase_spaces():
    assert normalize_ticker("  tcs  ") == "TCS"


def test_ticker_none():
    assert normalize_ticker(None) is None


def test_ticker_empty_string():
    assert normalize_ticker("") == ""


def test_ticker_single_character():
    assert normalize_ticker("a") == "A"


def test_ticker_numeric():
    assert normalize_ticker("123") == "123"


def test_ticker_alphanumeric():
    assert normalize_ticker("abc123") == "ABC123"


def test_ticker_special_character():
    assert normalize_ticker("M&M") == "M&M"


def test_ticker_dash():
    assert normalize_ticker("abc-def") == "ABC-DEF"


def test_ticker_long_name():
    assert normalize_ticker("relianceindustries") == "RELIANCEINDUSTRIES"


def test_ticker_tabs():
    assert normalize_ticker("\tTCS\t") == "TCS"


def test_ticker_newline():
    assert normalize_ticker("\ninfosys\n") == "INFOSYS"

    # ----------------------------------------------------
# normalize_year() Tests (1–10)
# ----------------------------------------------------

def test_year_mar24():
    assert normalize_year("Mar-24") == "2024-03"


def test_year_apr24():
    assert normalize_year("Apr-24") == "2024-04"


def test_year_dec23():
    assert normalize_year("Dec-23") == "2023-12"


def test_year_jan22():
    assert normalize_year("Jan-22") == "2022-01"


def test_year_feb21():
    assert normalize_year("Feb-21") == "2021-02"


def test_year_with_spaces():
    assert normalize_year("  Mar-24  ") == "2024-03"


def test_year_none():
    assert normalize_year(None) is None


def test_year_aug20():
    assert normalize_year("Aug-20") == "2020-08"


def test_year_sep19():
    assert normalize_year("Sep-19") == "2019-09"


def test_year_oct18():
    assert normalize_year("Oct-18") == "2018-10"
    # ----------------------------------------------------
# normalize_year() Tests (11–20)
# ----------------------------------------------------

def test_year_nov17():
    assert normalize_year("Nov-17") == "2017-11"


def test_year_jul16():
    assert normalize_year("Jul-16") == "2016-07"


def test_year_jun15():
    assert normalize_year("Jun-15") == "2015-06"


def test_year_may14():
    assert normalize_year("May-14") == "2014-05"


def test_year_apr13():
    assert normalize_year("Apr-13") == "2013-04"


def test_year_mar12():
    assert normalize_year("Mar-12") == "2012-03"


def test_year_feb11():
    assert normalize_year("Feb-11") == "2011-02"


def test_year_jan10():
    assert normalize_year("Jan-10") == "2010-01"


def test_year_dec09():
    assert normalize_year("Dec-09") == "2009-12"


def test_year_oct08():
    assert normalize_year("Oct-08") == "2008-10"
    