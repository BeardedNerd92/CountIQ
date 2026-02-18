from __future__ import annotations
import logging
import sys
from inventory.logging.json_formatter import JsonFormatter

def get_configured_logger() -> logging.Logger:
    logger = logging.getLogger("countiq")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    for h in logger.handlers:
        if isinstance(h, logging.StreamHandler):
            return logger
                    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
    return logger
