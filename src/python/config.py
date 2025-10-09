import json
from typing import List, Any, Optional, Union, Dict
import logging
from colorlog import ColoredFormatter


file = open("../config.json", "r")
CONFIG: Dict[str, Any] = json.loads(file.read())
file.close()


def update_config(key: str, value: Any) -> Any:
    v = CONFIG.get(key)

    CONFIG[key] = value

    with open("../config.json", "w") as f:
        f.write(json.dumps(CONFIG))

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

# logger.error(CONFIG)
