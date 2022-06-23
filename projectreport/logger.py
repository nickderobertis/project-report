import logging
from enum import Enum

from pydantic import BaseSettings, validator
from rich.logging import RichHandler


class LogLevel(str, Enum):
    INFO = "INFO"
    DEBUG = "DEBUG"


class LoggingConfig(BaseSettings):
    level: LogLevel = LogLevel.INFO

    class Config:
        env_prefix = "PROJECT_REPORT_LOG_"

    @validator("level", pre=True)
    def cast_log_level(cls, v):
        if isinstance(v, LogLevel):
            return v
        level = str(v).casefold().strip()
        if level == "info":
            return LogLevel.INFO
        elif level == "debug":
            return LogLevel.DEBUG
        raise ValueError(f"invalid log level {level}")


def create_logger() -> logging.Logger:
    logger = logging.getLogger("project-report")
    logger.setLevel(LOGGING_CONFIG.level.value)
    logger.addHandler(RichHandler(rich_tracebacks=True))
    return logger


LOGGING_CONFIG = LoggingConfig()
logger = create_logger()

if __name__ == "__main__":
    logger.info("info level")
    logger.debug("debug level")
    try:
        raise ValueError("exception")
    except ValueError as e:
        logger.exception(e)
