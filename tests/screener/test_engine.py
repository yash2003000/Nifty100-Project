from src.screener.engine import load_ratios


def test_load_ratios():

    df = load_ratios()

    assert len(df) > 90
