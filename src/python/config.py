import json
from typing import List, Any, Optional, Union, Dict
import logging
from colorlog import ColoredFormatter
import os

file = open("../config.json", "r")
CONFIG: Dict[str, Any] = json.loads(file.read())
file.close()


def config_validate():
    for v in CONFIG.values():
        if type(v) is dict:
            val = v.get("value")
            if v.get("type") is None:
                logger.warning("[CONFIG] Always require a type")
                continue
            if v.get("type") == "directory":
                if not os.path.exists(os.path.abspath(val)):
                    logger.info(f"Creating Directory {os.path.abspath(val)}")
                    os.makedirs(os.path.abspath(val))


def get_config(key: str) -> Any:

    v = CONFIG.get(key)
    if type(v) is dict:
        if v["type"] == "directory":
            v = os.path.abspath(v["value"])
        else:
            v = v["value"]
    return v


def update_config(key: str, value: Any) -> Any:
    v = CONFIG.get(key)

    if type(v) is dict:
        CONFIG[key]["value"] = value
    else:
        CONFIG[key] = value

    with open("../config.json", "w") as f:
        f.write(json.dumps(CONFIG))

    config_validate()
    return v


# Create a logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set the desired logging level

# Create a console handler
handler = logging.StreamHandler()

# Create a ColoredFormatter
formatter = ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s %(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)

# Set the formatter on the handler
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

config_validate()
