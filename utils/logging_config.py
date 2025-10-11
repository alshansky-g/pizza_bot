import logging
import sys

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        level = record.levelname
        if level not in logger._core.levels:  # type: ignore
            level = "INFO"
        logger.log(level, record.getMessage())


# Очищаем стандартные обработчики и ставим наш
logging.basicConfig(handlers=[InterceptHandler()], level=0)

# Если хочешь видеть только нужные логгеры, можно фильтровать:
logging.getLogger("aiogram").setLevel(logging.INFO)

# Настройка loguru (опционально формат)
logger.remove()
logger.add(
    sys.stderr,
    level="DEBUG",
    format="<g>{time:HH:mm:ss}</> | <level>{level}</> | <c>{module}</> | <level>{message}</>",
)
