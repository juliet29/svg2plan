import logging, json, logging.config
from turtle import setup
from pathlib import Path

LOG_CONFIG_PATH = "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/svg2plan/_scripts/log_setter/log_config.json"

def setup_logging():
    with open(LOG_CONFIG_PATH) as f_in:
        data = json.load(f_in)
        data["formatters"]["detailed"]["format"] = (
            "%(levelname)s|%(module)-10s" + "%(message)s"
        )
    logging.config.dictConfig(data)  # type: ignore

setup_logging()
logger = logging.getLogger("svg2plan")

