import logging

from app.api.config import settings
from loguru import logger

LOG_PATH = settings.log_path
if not LOG_PATH.exists():
    LOG_PATH.mkdir()
LOG_LEVEL = logging.DEBUG
LOGGING_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"


def format_handler(handler):
    handler.setLevel(LOG_LEVEL)
    handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
    return handler


def get_file_handler(log_file_name: str, dir_: str = None) -> logging.FileHandler:
    file_path = LOG_PATH / f"{log_file_name}.log"
    if dir_:
        file_path = LOG_PATH / dir_ / f"{log_file_name}.log"
    return format_handler(logging.FileHandler(file_path))


def get_stream_handler(log_file_name: str, dir_: str = None) -> logging.StreamHandler:
    file_path = LOG_PATH / f"{log_file_name}.log"
    if dir_:
        file_path = LOG_PATH / dir_ / f"{log_file_name}.log"
    return format_handler(logging.StreamHandler(file_path))


# aiohttp
aiohttp_file_handler = get_file_handler("gd_weather")
aiohttp_logger = logging.getLogger("aiohttp")
aiohttp_logger.addHandler(aiohttp_file_handler)

aiohttp_stream_handler = get_stream_handler("gd_weather")
aiohttp_stream_logger = logging.getLogger("aiohttp")
aiohttp_stream_logger.addHandler(aiohttp_stream_handler)

logger.add(sink=LOG_PATH / "gd_weather.log")
