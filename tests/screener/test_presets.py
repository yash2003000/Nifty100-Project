from src.screener.presets import load_presets


def test_presets_exist():

    presets = load_presets()

    assert len(presets) == 6
    