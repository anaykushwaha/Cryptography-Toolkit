# logger.py

# Logging Utilities for the Entire Cryptography Toolkit

# Contains centralized logging configuration, logger creation,
# file and console handlers, log formatting, and helper functions
# used to record application activity and errors.


from __future__ import annotations

import logging
from pathlib import Path
from typing import (
    Any,
)

from .constants import (
    DEFAULT_LOG_LEVEL,
    LOG_FORMAT,
    LOG_DATE_FORMAT,
    DEFAULT_LOG_DIRECTORY,
    DEFAULT_LOG_FILENAME,
)


# Log Level Mapping

LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


# Internal Helpers


def _normalize_level(
    level: str | int,
) -> int:
    # Converts a log level name or integer into a logging level

    if isinstance(
        level,
        int,
    ):
        return level

    if not isinstance(
        level,
        str,
    ):
        raise TypeError(
            "level must be a string or integer."
        )

    normalized = level.upper()

    if normalized not in LOG_LEVELS:
        raise ValueError(
            f"Unknown log level: {level}"
        )

    return LOG_LEVELS[
        normalized
    ]


def _build_formatter() -> logging.Formatter:
    # Creates the standard formatter used by the toolkit

    return logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT,
    )


def _ensure_directory(
    directory: Path,
) -> Path:
    # Creates a logging directory if it does not exist

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return directory


# Logger Creation


def get_logger(
    name: str = "cryptography_toolkit",
    *,
    level: str | int = DEFAULT_LOG_LEVEL,
) -> logging.Logger:
    # Returns a configured logger for the requested name

    if not isinstance(
        name,
        str,
    ):
        raise TypeError(
            "name must be a string."
        )

    if not name.strip():
        raise ValueError(
            "name cannot be empty."
        )

    logger = logging.getLogger(
        name
    )

    logger.setLevel(
        _normalize_level(
            level
        )
    )

    return logger


def create_console_handler(
    *,
    level: str | int = DEFAULT_LOG_LEVEL,
) -> logging.StreamHandler:
    # Creates a console logging handler

    handler = logging.StreamHandler()

    handler.setLevel(
        _normalize_level(
            level
        )
    )

    handler.setFormatter(
        _build_formatter()
    )

    return handler


def create_file_handler(
    path: str | Path,
    *,
    level: str | int = DEFAULT_LOG_LEVEL,
) -> logging.FileHandler:
    # Creates a file logging handler

    file_path = Path(
        path
    )

    _ensure_directory(
        file_path.parent
    )

    handler = logging.FileHandler(
        file_path,
        encoding="utf-8",
    )

    handler.setLevel(
        _normalize_level(
            level
        )
    )

    handler.setFormatter(
        _build_formatter()
    )

    return handler


# Logger Configuration


def configure_logger(
    logger: logging.Logger,
    *,
    level: str | int = DEFAULT_LOG_LEVEL,
    console: bool = True,
    file: bool = False,
    log_directory: str | Path = DEFAULT_LOG_DIRECTORY,
    filename: str = DEFAULT_LOG_FILENAME,
) -> logging.Logger:
    # Configures handlers and levels for an existing logger

    if not isinstance(
        logger,
        logging.Logger,
    ):
        raise TypeError(
            "logger must be a logging.Logger instance."
        )

    logger.setLevel(
        _normalize_level(
            level
        )
    )

    if console:
        logger.addHandler(
            create_console_handler(
                level=level
            )
        )

    if file:
        log_path = (
            Path(log_directory)
            / filename
        )

        logger.addHandler(
            create_file_handler(
                log_path,
                level=level,
            )
        )

    return logger


def setup_logger(
    name: str = "cryptography_toolkit",
    *,
    level: str | int = DEFAULT_LOG_LEVEL,
    console: bool = True,
    file: bool = False,
    log_directory: str | Path = DEFAULT_LOG_DIRECTORY,
    filename: str = DEFAULT_LOG_FILENAME,
) -> logging.Logger:
    # Creates and configures a logger in one operation

    logger = get_logger(
        name,
        level=level,
    )

    if not logger.handlers:
        configure_logger(
            logger,
            level=level,
            console=console,
            file=file,
            log_directory=log_directory,
            filename=filename,
        )

    return logger


# Handler Management


def clear_handlers(
    logger: logging.Logger,
) -> None:
    # Removes every handler from a logger

    if not isinstance(
        logger,
        logging.Logger,
    ):
        raise TypeError(
            "logger must be a logging.Logger instance."
        )

    for handler in logger.handlers[:]:
        logger.removeHandler(
            handler
        )
        handler.close()


def add_console_handler(
    logger: logging.Logger,
    *,
    level: str | int = DEFAULT_LOG_LEVEL,
) -> logging.StreamHandler:
    # Adds a console handler to a logger

    if not isinstance(
        logger,
        logging.Logger,
    ):
        raise TypeError(
            "logger must be a logging.Logger instance."
        )

    handler = create_console_handler(
        level=level
    )

    logger.addHandler(
        handler
    )

    return handler


def add_file_handler(
    logger: logging.Logger,
    path: str | Path,
    *,
    level: str | int = DEFAULT_LOG_LEVEL,
) -> logging.FileHandler:
    # Adds a file handler to a logger

    if not isinstance(
        logger,
        logging.Logger,
    ):
        raise TypeError(
            "logger must be a logging.Logger instance."
        )

    handler = create_file_handler(
        path,
        level=level,
    )

    logger.addHandler(
        handler
    )

    return handler


# Logging Helpers


def debug(
    logger: logging.Logger,
    message: str,
    *args: Any,
) -> None:
    # Records a debug-level message

    logger.debug(
        message,
        *args,
    )


def info(
    logger: logging.Logger,
    message: str,
    *args: Any,
) -> None:
    # Records an informational message

    logger.info(
        message,
        *args,
    )


def warning(
    logger: logging.Logger,
    message: str,
    *args: Any,
) -> None:
    # Records a warning-level message

    logger.warning(
        message,
        *args,
    )


def error(
    logger: logging.Logger,
    message: str,
    *args: Any,
) -> None:
    # Records an error-level message

    logger.error(
        message,
        *args,
    )


def critical(
    logger: logging.Logger,
    message: str,
    *args: Any,
) -> None:
    # Records a critical-level message

    logger.critical(
        message,
        *args,
    )


def exception(
    logger: logging.Logger,
    message: str,
    *args: Any,
) -> None:
    # Records an exception with traceback information

    logger.exception(
        message,
        *args,
    )


# Module Exports

__all__ = [
    "LOG_LEVELS",
    "get_logger",
    "create_console_handler",
    "create_file_handler",
    "configure_logger",
    "setup_logger",
    "clear_handlers",
    "add_console_handler",
    "add_file_handler",
    "debug",
    "info",
    "warning",
    "error",
    "critical",
    "exception",
] 

