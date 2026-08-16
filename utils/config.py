# config.py

# Configuration Management for the Entire Cryptography Toolkit

# Contains application configuration, default settings,
# configuration validation, configuration loading, and
# configuration manipulation utilities.


from __future__ import annotations

from pathlib import Path
from typing import Any

from .constants import (
    PROJECT_NAME,
    PROJECT_VERSION,
    DEFAULT_ENCODING,
    DEFAULT_LANGUAGE,
    DEFAULT_THEME,
    DEFAULT_TIMEOUT,
    DEFAULT_PROGRESS_WIDTH,
    DEFAULT_TABLE_WIDTH,
    DEFAULT_LOG_LEVEL,
    DEFAULT_LOG_DIRECTORY,
    DEFAULT_LOG_FILENAME,
    DEFAULT_CHUNK_SIZE,
    MIN_CHUNK_SIZE,
    MAX_CHUNK_SIZE,
    DEFAULT_NGRAM_SIZE,
    DEFAULT_TOP_CANDIDATES,
    DEFAULT_FREQUENCY_PRECISION,
    DEFAULT_SCORE_PRECISION,
    DEFAULT_ENTROPY_PRECISION,
    DEFAULT_IOC_PRECISION,
)


# Default Configuration


DEFAULT_CONFIG = {
    "application": {
        "name": PROJECT_NAME,
        "version": PROJECT_VERSION,
        "language": DEFAULT_LANGUAGE,
        "theme": DEFAULT_THEME,
    },

    "encoding": {
        "default": DEFAULT_ENCODING,
    },

    "analysis": {
        "ngram_size": DEFAULT_NGRAM_SIZE,
        "top_candidates": DEFAULT_TOP_CANDIDATES,
        "frequency_precision": DEFAULT_FREQUENCY_PRECISION,
        "score_precision": DEFAULT_SCORE_PRECISION,
        "entropy_precision": DEFAULT_ENTROPY_PRECISION,
        "ioc_precision": DEFAULT_IOC_PRECISION,
    },

    "streaming": {
        "chunk_size": DEFAULT_CHUNK_SIZE,
        "min_chunk_size": MIN_CHUNK_SIZE,
        "max_chunk_size": MAX_CHUNK_SIZE,
    },

    "application_limits": {
        "timeout": DEFAULT_TIMEOUT,
        "progress_width": DEFAULT_PROGRESS_WIDTH,
        "table_width": DEFAULT_TABLE_WIDTH,
    },

    "logging": {
        "level": DEFAULT_LOG_LEVEL,
        "directory": DEFAULT_LOG_DIRECTORY,
        "filename": DEFAULT_LOG_FILENAME,
    },
}


# Configuration Class


class Config:
    # Represents the runtime configuration of the toolkit

    def __init__(
        self,
        values: dict[str, Any] | None = None,
    ) -> None:
        # Creates a configuration object

        self._values = self._copy_defaults()

        if values is not None:
            self.update(
                values
            )

    # Internal Helpers

    @staticmethod
    def _copy_defaults() -> dict[str, Any]:
        # Creates a copy of the default configuration

        return {
            section: values.copy()
            if isinstance(values, dict)
            else values
            for section, values
            in DEFAULT_CONFIG.items()
        }

    @staticmethod
    def _validate_section(
        section: str,
    ) -> None:
        # Validates a configuration section name

        if not isinstance(
            section,
            str,
        ):
            raise TypeError(
                "Configuration section must be a string."
            )

        if not section.strip():
            raise ValueError(
                "Configuration section cannot be empty."
            )

    @staticmethod
    def _validate_key(
        key: str,
    ) -> None:
        # Validates a configuration key

        if not isinstance(
            key,
            str,
        ):
            raise TypeError(
                "Configuration key must be a string."
            )

        if not key.strip():
            raise ValueError(
                "Configuration key cannot be empty."
            )

    # Access

    def get(
        self,
        section: str,
        key: str,
        default: Any = None,
    ) -> Any:
        # Retrieves a configuration value

        self._validate_section(
            section
        )

        self._validate_key(
            key
        )

        return self._values.get(
            section,
            {},
        ).get(
            key,
            default,
        )

    def set(
        self,
        section: str,
        key: str,
        value: Any,
    ) -> None:
        # Sets a configuration value

        self._validate_section(
            section
        )

        self._validate_key(
            key
        )

        if section not in self._values:
            self._values[section] = {}

        self._values[section][key] = value

    def has(
        self,
        section: str,
        key: str,
    ) -> bool:
        # Determines whether a configuration value exists

        self._validate_section(
            section
        )

        self._validate_key(
            key
        )

        return (
            section in self._values
            and key in self._values[section]
        )

    def section(
        self,
        section: str,
    ) -> dict[str, Any]:
        # Returns an entire configuration section

        self._validate_section(
            section
        )

        if section not in self._values:
            return {}

        return self._values[
            section
        ].copy()

    def remove(
        self,
        section: str,
        key: str,
    ) -> bool:
        # Removes a configuration value

        self._validate_section(
            section
        )

        self._validate_key(
            key
        )

        if not self.has(
            section,
            key,
        ):
            return False

        del self._values[
            section
        ][key]

        return True

    # Updates

    def update(
        self,
        values: dict[str, Any],
    ) -> None:
        # Updates the configuration with new values

        if not isinstance(
            values,
            dict,
        ):
            raise TypeError(
                "Configuration values must be a dictionary."
            )

        for section, section_values in values.items():

            self._validate_section(
                section
            )

            if not isinstance(
                section_values,
                dict,
            ):
                raise TypeError(
                    "Configuration sections must be dictionaries."
                )

            if section not in self._values:
                self._values[section] = {}

            self._values[
                section
            ].update(
                section_values
            )

    def reset(
        self,
    ) -> None:
        # Resets all configuration values to their defaults

        self._values = (
            self._copy_defaults()
        )

    def reset_section(
        self,
        section: str,
    ) -> None:
        # Resets a single section to its default values

        self._validate_section(
            section
        )

        if section not in DEFAULT_CONFIG:
            raise KeyError(
                f"Unknown configuration section: {section}"
            )

        self._values[
            section
        ] = (
            DEFAULT_CONFIG[
                section
            ].copy()
        )

    # Conversion

    def to_dict(
        self,
    ) -> dict[str, Any]:
        # Returns the complete configuration as a dictionary

        return {
            section: values.copy()
            if isinstance(values, dict)
            else values
            for section, values
            in self._values.items()
        }

    def keys(
        self,
    ) -> list[str]:
        # Returns all configuration section names

        return list(
            self._values.keys()
        )

    def values(
        self,
    ) -> list[dict[str, Any]]:
        # Returns all configuration sections

        return list(
            self._values.values()
        )

    def items(
        self,
    ) -> list[
        tuple[
            str,
            dict[str, Any],
        ]
    ]:
        # Returns configuration sections and their values

        return list(
            self._values.items()
        )

    # Representation

    def __contains__(
        self,
        section: str,
    ) -> bool:
        # Supports membership testing for configuration sections

        return section in self._values

    def __repr__(
        self,
    ) -> str:
        # Returns a developer-friendly configuration representation

        return (
            f"Config({self._values!r})"
        )


# Configuration Helpers


def get_default_config() -> dict[str, Any]:
    # Returns a fresh copy of the default configuration

    return {
        section: values.copy()
        if isinstance(values, dict)
        else values
        for section, values
        in DEFAULT_CONFIG.items()
    }


def create_config(
    values: dict[str, Any] | None = None,
) -> Config:
    # Creates a new configuration object

    return Config(
        values
    )


def get_config_value(
    config: Config,
    section: str,
    key: str,
    default: Any = None,
) -> Any:
    # Retrieves a value from a configuration object

    if not isinstance(
        config,
        Config,
    ):
        raise TypeError(
            "config must be a Config instance."
        )

    return config.get(
        section,
        key,
        default,
    )


def set_config_value(
    config: Config,
    section: str,
    key: str,
    value: Any,
) -> None:
    # Sets a value in a configuration object

    if not isinstance(
        config,
        Config,
    ):
        raise TypeError(
            "config must be a Config instance."
        )

    config.set(
        section,
        key,
        value,
    )


# Path Helpers


def get_project_root() -> Path:
    # Returns the root directory of the project

    return Path(
        __file__
    ).resolve().parent.parent


def get_data_directory() -> Path:
    # Returns the project's data directory

    return (
        get_project_root()
        / "data"
    )


def get_reports_directory() -> Path:
    # Returns the project's reports directory

    return (
        get_project_root()
        / "reports"
    )


def get_history_directory() -> Path:
    # Returns the project's history directory

    return (
        get_project_root()
        / "history"
    )


def get_docs_directory() -> Path:
    # Returns the project's documentation directory

    return (
        get_project_root()
        / "docs"
    )


def get_examples_directory() -> Path:
    # Returns the project's examples directory

    return (
        get_project_root()
        / "examples"
    )


def get_tests_directory() -> Path:
    # Returns the project's tests directory

    return (
        get_project_root()
        / "tests"
    )


def get_log_directory(
    config: Config | None = None,
) -> Path:
    # Returns the configured logging directory

    if config is None:
        directory = DEFAULT_LOG_DIRECTORY
    else:
        directory = config.get(
            "logging",
            "directory",
            DEFAULT_LOG_DIRECTORY,
        )

    path = Path(
        directory
    )

    if not path.is_absolute():
        path = (
            get_project_root()
            / path
        )

    return path


# Configuration Validation


def validate_config(
    config: Config,
) -> bool:
    # Validates the structure and values of a configuration object

    if not isinstance(
        config,
        Config,
    ):
        return False

    encoding = config.get(
        "encoding",
        "default",
    )

    if not isinstance(
        encoding,
        str,
    ) or not encoding:
        return False

    language = config.get(
        "application",
        "language",
    )

    if not isinstance(
        language,
        str,
    ) or not language:
        return False

    theme = config.get(
        "application",
        "theme",
    )

    if not isinstance(
        theme,
        str,
    ) or not theme:
        return False

    chunk_size = config.get(
        "streaming",
        "chunk_size",
    )

    if not isinstance(
        chunk_size,
        int,
    ):
        return False

    if not (
        MIN_CHUNK_SIZE
        <= chunk_size
        <= MAX_CHUNK_SIZE
    ):
        return False

    timeout = config.get(
        "application_limits",
        "timeout",
    )

    if not isinstance(
        timeout,
        (int, float),
    ):
        return False

    if timeout < 0:
        return False

    top_candidates = config.get(
        "analysis",
        "top_candidates",
    )

    if not isinstance(
        top_candidates,
        int,
    ):
        return False

    if top_candidates < 1:
        return False

    return True


# Configuration Loading


def load_config(
    values: dict[str, Any] | None = None,
) -> Config:
    # Creates and validates a configuration object

    config = create_config(
        values
    )

    if not validate_config(
        config
    ):
        raise ValueError(
            "Invalid configuration."
        )

    return config


# Configuration Export


def export_config(
    config: Config,
) -> dict[str, Any]:
    # Exports a configuration object as a dictionary

    if not isinstance(
        config,
        Config,
    ):
        raise TypeError(
            "config must be a Config instance."
        )

    return config.to_dict()


# Self Test


def self_test() -> bool:
    # Runs a quick internal test of the configuration module

    config = create_config()

    if not validate_config(
        config
    ):
        return False

    if config.get(
        "application",
        "name",
    ) != PROJECT_NAME:
        return False

    if config.get(
        "encoding",
        "default",
    ) != DEFAULT_ENCODING:
        return False

    config.set(
        "application",
        "theme",
        "dark",
    )

    if config.get(
        "application",
        "theme",
    ) != "dark":
        return False

    if not config.has(
        "application",
        "theme",
    ):
        return False

    config.reset_section(
        "application"
    )

    if config.get(
        "application",
        "theme",
    ) != DEFAULT_THEME:
        return False

    config.set(
        "test",
        "value",
        123,
    )

    if config.get(
        "test",
        "value",
    ) != 123:
        return False

    if not config.remove(
        "test",
        "value",
    ):
        return False

    if config.has(
        "test",
        "value",
    ):
        return False

    config.reset()

    if not validate_config(
        config
    ):
        return False

    copied = config.to_dict()

    if not isinstance(
        copied,
        dict,
    ):
        return False

    if get_project_root().exists() is False:
        return False

    if not get_data_directory().name == "data":
        return False

    if not get_reports_directory().name == "reports":
        return False

    if not get_history_directory().name == "history":
        return False

    if not get_docs_directory().name == "docs":
        return False

    if not get_examples_directory().name == "examples":
        return False

    if not get_tests_directory().name == "tests":
        return False

    return True


# Module Exports

__all__ = [

    # Configuration
    "DEFAULT_CONFIG",
    "Config",

    # Configuration Helpers
    "get_default_config",
    "create_config",
    "get_config_value",
    "set_config_value",
    "validate_config",
    "load_config",
    "export_config",

    # Path Helpers
    "get_project_root",
    "get_data_directory",
    "get_reports_directory",
    "get_history_directory",
    "get_docs_directory",
    "get_examples_directory",
    "get_tests_directory",
    "get_log_directory",

    # Testing
    "self_test",
]

