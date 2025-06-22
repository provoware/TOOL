import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, "app.log"),
    maxBytes=1_000_000,
    backupCount=5,
    encoding="utf-8",
)

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[_handler],
    format="%(asctime)s | %(levelname)-7s | %(message)s",
)


def log_info(message: str) -> None:
    logging.info(message)


def log_debug(message: str) -> None:
    logging.debug(message)


def log_error(message: str, exc: Exception | None = None) -> None:
    if exc:
        logging.error(f"{message} | {exc}")
    else:
        logging.error(message)
