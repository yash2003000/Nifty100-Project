import yaml

from src.screener.engine import run_screener


CONFIG_FILE = "config/screener_config.yaml"


def load_presets():

    with open(
        CONFIG_FILE,
        "r"
    ) as file:

        return yaml.safe_load(file)


def run_preset(name):

    presets = load_presets()

    filters = presets[name]

    return run_screener(filters)
