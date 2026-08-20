# prompts.py

# Interactive prompt utilities for the
# Cryptography Toolkit

# Provides reusable functions for collecting,
# validating, and formatting user input through
# the command-line interface


from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)

from typing import (
    Any,
    Callable,
    Iterable,
    Sequence,
)


# Prompt Exceptions


class PromptError(Exception):
    # Base exception for prompt-related errors

    pass


class PromptCancelledError(PromptError):
    # Raised when the user cancels a prompt

    pass


class InvalidPromptInputError(PromptError):
    # Raised when prompt input is invalid

    pass


class PromptValidationError(PromptError):
    # Raised when prompt validation fails

    pass


# Prompt Result


@dataclass
class PromptResult:
    # Stores the result of a prompt

    value: Any
    cancelled: bool = False
    raw_value: str = ""
    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def is_valid(
        self,
    ) -> bool:
        # Returns whether the prompt produced
        # a usable value

        return (
            not self.cancelled
            and self.value is not None
        )

    def to_dict(
        self,
    ) -> dict[str, Any]:
        # Converts the result into a dictionary

        return {
            "value": self.value,
            "cancelled": self.cancelled,
            "raw_value": self.raw_value,
            "metadata": dict(
                self.metadata
            ),
        }


# Prompt Configuration


@dataclass
class PromptConfig:
    # Stores configuration for an individual prompt

    message: str
    default: Any = None
    required: bool = True
    allow_cancel: bool = True
    choices: Sequence[Any] | None = None
    validator: Callable[[Any], bool] | None = None
    converter: Callable[[str], Any] | None = None

    def __post_init__(
        self,
    ) -> None:
        # Validates prompt configuration

        if not isinstance(
            self.message,
            str,
        ):
            raise TypeError(
                "Prompt message must be a string."
            )

        if not self.message.strip():
            raise ValueError(
                "Prompt message cannot be empty."
            )

        if (
            self.choices is not None
            and not isinstance(
                self.choices,
                Sequence,
            )
        ):
            raise TypeError(
                "choices must be a sequence."
            )

    def has_choices(
        self,
    ) -> bool:
        # Returns whether the prompt has choices

        return (
            self.choices is not None
            and len(
                self.choices
            ) > 0
        )


# Input Utilities


CANCEL_VALUES = (
    "q",
    "quit",
    "cancel",
    "exit",
)


YES_VALUES = (
    "y",
    "yes",
)


NO_VALUES = (
    "n",
    "no",
)


def normalize_input(
    value: str,
) -> str:
    # Normalizes user input

    if not isinstance(
        value,
        str,
    ):
        raise InvalidPromptInputError(
            "Prompt input must be a string."
        )

    return value.strip()


def is_cancelled(
    value: str,
) -> bool:
    # Checks whether the user entered a
    # cancellation value

    normalized = normalize_input(
        value
    ).lower()

    return normalized in CANCEL_VALUES


def is_yes(
    value: str,
) -> bool:
    # Checks whether the user entered yes

    normalized = normalize_input(
        value
    ).lower()

    return normalized in YES_VALUES


def is_no(
    value: str,
) -> bool:
    # Checks whether the user entered no

    normalized = normalize_input(
        value
    ).lower()

    return normalized in NO_VALUES


# Prompt Manager


class PromptManager:
    # Manages interactive CLI prompts

    def __init__(
        self,
        *,
        input_function: Callable[
            [str],
            str,
        ] = input,
        output_function: Callable[
            [str],
            Any,
        ] = print,
    ) -> None:
        # Initializes the prompt manager

        if not callable(
            input_function
        ):
            raise TypeError(
                "input_function must be callable."
            )

        if not callable(
            output_function
        ):
            raise TypeError(
                "output_function must be callable."
            )

        self.input_function = (
            input_function
        )

        self.output_function = (
            output_function
        )

    # Basic Input


    def ask(
        self,
        message: str,
        *,
        default: str | None = None,
        required: bool = True,
        allow_cancel: bool = True,
    ) -> PromptResult:
        # Prompts the user for text input

        if not isinstance(
            message,
            str,
        ):
            raise TypeError(
                "message must be a string."
            )

        if not message.strip():
            raise ValueError(
                "message cannot be empty."
            )

        prompt_message = message

        if default is not None:
            prompt_message += (
                f" [{default}]"
            )

        prompt_message += ": "

        while True:
            try:
                raw_value = (
                    self.input_function(
                        prompt_message
                    )
                )

            except (
                EOFError,
                KeyboardInterrupt,
            ) as error:
                if allow_cancel:
                    return PromptResult(
                        value=None,
                        cancelled=True,
                        metadata={
                            "reason": (
                                "interrupt"
                            )
                        },
                    )

                raise PromptCancelledError(
                    "Prompt interrupted."
                ) from error

            if not isinstance(
                raw_value,
                str,
            ):
                raise InvalidPromptInputError(
                    "Input function must return a string."
                )

            normalized = normalize_input(
                raw_value
            )

            if (
                allow_cancel
                and is_cancelled(
                    normalized
                )
            ):
                return PromptResult(
                    value=None,
                    cancelled=True,
                    raw_value=raw_value,
                    metadata={
                        "reason": (
                            "user_cancelled"
                        )
                    },
                )

            if not normalized:
                if default is not None:
                    return PromptResult(
                        value=default,
                        raw_value=raw_value,
                        metadata={
                            "used_default": True
                        },
                    )

                if not required:
                    return PromptResult(
                        value="",
                        raw_value=raw_value,
                    )

                self.output_function(
                    "Input is required."
                )
                continue

            return PromptResult(
                value=normalized,
                raw_value=raw_value,
            )

    # Choice Input


    def choose(
        self,
        message: str,
        choices: Sequence[Any],
        *,
        default: Any = None,
        allow_cancel: bool = True,
    ) -> PromptResult:
        # Prompts the user to select from choices

        if not choices:
            raise ValueError(
                "choices cannot be empty."
            )

        choices = list(
            choices
        )

        self.output_function(
            message
        )

        for index, choice in enumerate(
            choices,
            start=1,
        ):
            self.output_function(
                f"  {index}. {choice}"
            )

        if default is not None:
            self.output_function(
                f"Default: {default}"
            )

        while True:
            result = self.ask(
                "Select an option",
                default=(
                    str(default)
                    if default is not None
                    else None
                ),
                required=True,
                allow_cancel=allow_cancel,
            )

            if result.cancelled:
                return result

            value = result.value

            try:
                index = int(
                    value
                )

            except ValueError:
                # Also allow the user to enter
                # the actual choice value

                for choice in choices:
                    if str(
                        choice
                    ).lower() == str(
                        value
                    ).lower():
                        return PromptResult(
                            value=choice,
                            raw_value=result.raw_value,
                        )

                self.output_function(
                    "Please select a valid option."
                )
                continue

            if (
                1 <= index <= len(
                    choices
                )
            ):
                return PromptResult(
                    value=choices[
                        index - 1
                    ],
                    raw_value=result.raw_value,
                )

            self.output_function(
                "Please select a valid option."
            )

    # Yes / No Input


    def confirm(
        self,
        message: str,
        *,
        default: bool | None = None,
        allow_cancel: bool = True,
    ) -> PromptResult:
        # Prompts the user for a yes/no response

        suffix = ""

        if default is True:
            suffix = " [Y/n]"
        elif default is False:
            suffix = " [y/N]"
        else:
            suffix = " [y/n]"

        while True:
            result = self.ask(
                f"{message}{suffix}",
                required=True,
                allow_cancel=allow_cancel,
            )

            if result.cancelled:
                return result

            value = result.value.lower()

            if is_yes(
                value
            ):
                return PromptResult(
                    value=True,
                    raw_value=result.raw_value,
                )

            if is_no(
                value
            ):
                return PromptResult(
                    value=False,
                    raw_value=result.raw_value,
                )

            if (
                default is not None
                and not value
            ):
                return PromptResult(
                    value=default,
                    raw_value=result.raw_value,
                )

            self.output_function(
                "Please answer yes or no."
            )

    # Integer Input


    def integer(
        self,
        message: str,
        *,
        default: int | None = None,
        minimum: int | None = None,
        maximum: int | None = None,
        allow_cancel: bool = True,
    ) -> PromptResult:
        # Prompts the user for an integer

        while True:
            result = self.ask(
                message,
                default=(
                    str(default)
                    if default is not None
                    else None
                ),
                required=True,
                allow_cancel=allow_cancel,
            )

            if result.cancelled:
                return result

            try:
                value = int(
                    result.value
                )

            except ValueError:
                self.output_function(
                    "Please enter a valid integer."
                )
                continue

            if (
                minimum is not None
                and value < minimum
            ):
                self.output_function(
                    f"Value must be at least "
                    f"{minimum}."
                )
                continue

            if (
                maximum is not None
                and value > maximum
            ):
                self.output_function(
                    f"Value must be at most "
                    f"{maximum}."
                )
                continue

            return PromptResult(
                value=value,
                raw_value=result.raw_value,
            )

            # Float Input

    def floating_point(
        self,
        message: str,
        *,
        default: float | None = None,
        minimum: float | None = None,
        maximum: float | None = None,
        allow_cancel: bool = True,
    ) -> PromptResult:
        # Prompts the user for a floating-point number

        while True:
            result = self.ask(
                message,
                default=(
                    str(default)
                    if default is not None
                    else None
                ),
                required=True,
                allow_cancel=allow_cancel,
            )

            if result.cancelled:
                return result

            try:
                value = float(
                    result.value
                )

            except ValueError:
                self.output_function(
                    "Please enter a valid number."
                )
                continue

            if (
                minimum is not None
                and value < minimum
            ):
                self.output_function(
                    f"Value must be at least "
                    f"{minimum}."
                )
                continue

            if (
                maximum is not None
                and value > maximum
            ):
                self.output_function(
                    f"Value must be at most "
                    f"{maximum}."
                )
                continue

            return PromptResult(
                value=value,
                raw_value=result.raw_value,
            )

    # Text Input With Validation

    def validated(
        self,
        message: str,
        validator: Callable[
            [str],
            bool,
        ],
        *,
        default: str | None = None,
        required: bool = True,
        allow_cancel: bool = True,
        error_message: str = (
            "Invalid input."
        ),
    ) -> PromptResult:
        # Prompts for text and applies a custom validator

        if not callable(
            validator
        ):
            raise TypeError(
                "validator must be callable."
            )

        while True:
            result = self.ask(
                message,
                default=default,
                required=required,
                allow_cancel=allow_cancel,
            )

            if result.cancelled:
                return result

            try:
                valid = validator(
                    result.value
                )

            except Exception as error:
                raise PromptValidationError(
                    "Prompt validator failed."
                ) from error

            if valid:
                return result

            self.output_function(
                error_message
            )

    # Converted Input

    def converted(
        self,
        message: str,
        converter: Callable[
            [str],
            Any,
        ],
        *,
        default: Any = None,
        required: bool = True,
        allow_cancel: bool = True,
        error_message: str = (
            "Invalid input."
        ),
    ) -> PromptResult:
        # Prompts for input and converts it using
        # a supplied conversion function

        if not callable(
            converter
        ):
            raise TypeError(
                "converter must be callable."
            )

        while True:
            result = self.ask(
                message,
                default=(
                    str(default)
                    if default is not None
                    else None
                ),
                required=required,
                allow_cancel=allow_cancel,
            )

            if result.cancelled:
                return result

            try:
                value = converter(
                    result.value
                )

            except (
                ValueError,
                TypeError,
            ):
                self.output_function(
                    error_message
                )
                continue

            return PromptResult(
                value=value,
                raw_value=result.raw_value,
            )

    # Password-Style Input

    def secret(
        self,
        message: str,
        *,
        allow_cancel: bool = True,
    ) -> PromptResult:
        # Prompts for sensitive text.
        #
        # Uses getpass when available so the entered
        # value is not displayed on screen.

        try:
            from getpass import getpass

        except ImportError:
            getpass = None

        if getpass is None:
            return self.ask(
                message,
                required=True,
                allow_cancel=allow_cancel,
            )

        prompt_message = (
            f"{message}: "
        )

        try:
            raw_value = getpass(
                prompt_message
            )

        except (
            EOFError,
            KeyboardInterrupt,
        ) as error:
            if allow_cancel:
                return PromptResult(
                    value=None,
                    cancelled=True,
                    metadata={
                        "reason": "interrupt"
                    },
                )

            raise PromptCancelledError(
                "Secret prompt interrupted."
            ) from error

        normalized = normalize_input(
            raw_value
        )

        if (
            allow_cancel
            and is_cancelled(
                normalized
            )
        ):
            return PromptResult(
                value=None,
                cancelled=True,
                raw_value=raw_value,
                metadata={
                    "reason": "user_cancelled"
                },
            )

        return PromptResult(
            value=normalized,
            raw_value=raw_value,
        )

    # Multi-Value Input

    def multiple(
        self,
        message: str,
        *,
        separator: str = ",",
        default: Sequence[str] | None = None,
        required: bool = True,
        allow_cancel: bool = True,
    ) -> PromptResult:
        # Prompts for multiple values separated by
        # a configurable delimiter

        if not isinstance(
            separator,
            str,
        ):
            raise TypeError(
                "separator must be a string."
            )

        if not separator:
            raise ValueError(
                "separator cannot be empty."
            )

        default_value = None

        if default is not None:
            default_value = separator.join(
                str(
                    item
                )
                for item in default
            )

        while True:
            result = self.ask(
                message,
                default=default_value,
                required=required,
                allow_cancel=allow_cancel,
            )

            if result.cancelled:
                return result

            values = [
                item.strip()
                for item in result.value.split(
                    separator
                )
                if item.strip()
            ]

            if values:
                return PromptResult(
                    value=values,
                    raw_value=result.raw_value,
                )

            if not required:
                return PromptResult(
                    value=[],
                    raw_value=result.raw_value,
                )

            self.output_function(
                "Please enter at least one value."
            )

    # Caesar Key Prompt

    def cipher_key(
        self,
        message: str = "Enter cipher key",
        *,
        default: int | None = None,
        minimum: int = -25,
        maximum: int = 25,
        allow_cancel: bool = True,
    ) -> PromptResult:
        # Prompts for a Caesar cipher key

        return self.integer(
            message,
            default=default,
            minimum=minimum,
            maximum=maximum,
            allow_cancel=allow_cancel,
        )

    # File Path Prompt

    def file_path(
        self,
        message: str = "Enter file path",
        *,
        default: str | None = None,
        must_exist: bool = False,
        allow_cancel: bool = True,
    ) -> PromptResult:
        # Prompts for a file path

        from pathlib import Path

        while True:
            result = self.ask(
                message,
                default=default,
                required=True,
                allow_cancel=allow_cancel,
            )

            if result.cancelled:
                return result

            path = Path(
                result.value
            ).expanduser()

            if must_exist and not path.exists():
                self.output_function(
                    "The specified file does not exist."
                )
                continue

            return PromptResult(
                value=path,
                raw_value=result.raw_value,
            )

    # Directory Path Prompt

    def directory_path(
        self,
        message: str = "Enter directory path",
        *,
        default: str | None = None,
        must_exist: bool = False,
        allow_cancel: bool = True,
    ) -> PromptResult:
        # Prompts for a directory path

        from pathlib import Path

        while True:
            result = self.ask(
                message,
                default=default,
                required=True,
                allow_cancel=allow_cancel,
            )

            if result.cancelled:
                return result

            path = Path(
                result.value
            ).expanduser()

            if must_exist:
                if not path.exists():
                    self.output_function(
                        "The directory does not exist."
                    )
                    continue

                if not path.is_dir():
                    self.output_function(
                        "The specified path is not a directory."
                    )
                    continue

            return PromptResult(
                value=path,
                raw_value=result.raw_value,
            )

    # Password Confirmation

    def confirm_secret(
        self,
        message: str = "Enter value",
        confirmation_message: str = (
            "Confirm value"
        ),
        *,
        allow_cancel: bool = True,
    ) -> PromptResult:
        # Prompts for a secret twice and ensures
        # both values match

        while True:
            first = self.secret(
                message,
                allow_cancel=allow_cancel,
            )

            if first.cancelled:
                return first

            second = self.secret(
                confirmation_message,
                allow_cancel=allow_cancel,
            )

            if second.cancelled:
                return second

            if first.value == second.value:
                return PromptResult(
                    value=first.value,
                    raw_value=first.raw_value,
                    metadata={
                        "confirmed": True
                    },
                )

            self.output_function(
                "Values do not match. "
                "Please try again."
            )


# Standalone Prompt Functions


_default_prompt_manager = PromptManager()


def prompt(
    message: str,
    *,
    default: str | None = None,
    required: bool = True,
    allow_cancel: bool = True,
) -> PromptResult:
    # Convenience wrapper for a basic prompt

    return _default_prompt_manager.ask(
        message,
        default=default,
        required=required,
        allow_cancel=allow_cancel,
    )


def prompt_choice(
    message: str,
    choices: Sequence[Any],
    *,
    default: Any = None,
    allow_cancel: bool = True,
) -> PromptResult:
    # Convenience wrapper for a choice prompt

    return _default_prompt_manager.choose(
        message,
        choices,
        default=default,
        allow_cancel=allow_cancel,
    )


def prompt_confirm(
    message: str,
    *,
    default: bool | None = None,
    allow_cancel: bool = True,
) -> PromptResult:
    # Convenience wrapper for a confirmation prompt

    return _default_prompt_manager.confirm(
        message,
        default=default,
        allow_cancel=allow_cancel,
    )


def prompt_integer(
    message: str,
    *,
    default: int | None = None,
    minimum: int | None = None,
    maximum: int | None = None,
    allow_cancel: bool = True,
) -> PromptResult:
    # Convenience wrapper for integer input

    return _default_prompt_manager.integer(
        message,
        default=default,
        minimum=minimum,
        maximum=maximum,
        allow_cancel=allow_cancel,
    )


def prompt_float(
    message: str,
    *,
    default: float | None = None,
    minimum: float | None = None,
    maximum: float | None = None,
    allow_cancel: bool = True,
) -> PromptResult:
    # Convenience wrapper for floating-point input

    return _default_prompt_manager.floating_point(
        message,
        default=default,
        minimum=minimum,
        maximum=maximum,
        allow_cancel=allow_cancel,
    )

def prompt_secret(
    message: str,
    *,
    allow_cancel: bool = True,
) -> PromptResult:
    # Convenience wrapper for secret input

    return _default_prompt_manager.secret(
        message,
        allow_cancel=allow_cancel,
    )


def prompt_multiple(
    message: str,
    *,
    separator: str = ",",
    default: Sequence[str] | None = None,
    required: bool = True,
    allow_cancel: bool = True,
) -> PromptResult:
    # Convenience wrapper for multiple-value input

    return _default_prompt_manager.multiple(
        message,
        separator=separator,
        default=default,
        required=required,
        allow_cancel=allow_cancel,
    )


def prompt_cipher_key(
    message: str = "Enter cipher key",
    *,
    default: int | None = None,
    minimum: int = -25,
    maximum: int = 25,
    allow_cancel: bool = True,
) -> PromptResult:
    # Convenience wrapper for cipher key input

    return _default_prompt_manager.cipher_key(
        message,
        default=default,
        minimum=minimum,
        maximum=maximum,
        allow_cancel=allow_cancel,
    )


def prompt_file_path(
    message: str = "Enter file path",
    *,
    default: str | None = None,
    must_exist: bool = False,
    allow_cancel: bool = True,
) -> PromptResult:
    # Convenience wrapper for file path input

    return _default_prompt_manager.file_path(
        message,
        default=default,
        must_exist=must_exist,
        allow_cancel=allow_cancel,
    )


def prompt_directory_path(
    message: str = "Enter directory path",
    *,
    default: str | None = None,
    must_exist: bool = False,
    allow_cancel: bool = True,
) -> PromptResult:
    # Convenience wrapper for directory path input

    return _default_prompt_manager.directory_path(
        message,
        default=default,
        must_exist=must_exist,
        allow_cancel=allow_cancel,
    )


def prompt_confirm_secret(
    message: str = "Enter value",
    confirmation_message: str = "Confirm value",
    *,
    allow_cancel: bool = True,
) -> PromptResult:
    # Convenience wrapper for confirmed secret input

    return _default_prompt_manager.confirm_secret(
        message,
        confirmation_message,
        allow_cancel=allow_cancel,
    )


# Prompt Manager Access


def get_prompt_manager() -> PromptManager:
    # Returns the default prompt manager

    return _default_prompt_manager


def set_prompt_manager(
    manager: PromptManager,
) -> None:
    # Replaces the default prompt manager

    global _default_prompt_manager

    if not isinstance(
        manager,
        PromptManager,
    ):
        raise TypeError(
            "manager must be a PromptManager."
        )

    _default_prompt_manager = manager


# Validation Helpers


def validate_non_empty(
    value: str,
) -> bool:
    # Checks whether a value contains text

    if not isinstance(
        value,
        str,
    ):
        return False

    return bool(
        value.strip()
    )


def validate_integer(
    value: str,
) -> bool:
    # Checks whether a value is an integer

    if not isinstance(
        value,
        str,
    ):
        return False

    try:
        int(
            value.strip()
        )
        return True

    except ValueError:
        return False


def validate_float(
    value: str,
) -> bool:
    # Checks whether a value is a floating-point number

    if not isinstance(
        value,
        str,
    ):
        return False

    try:
        float(
            value.strip()
        )
        return True

    except ValueError:
        return False


def validate_choice(
    value: str,
    choices: Sequence[Any],
) -> bool:
    # Checks whether a value matches one of
    # the available choices

    if not isinstance(
        value,
        str,
    ):
        return False

    normalized = value.strip().lower()

    for choice in choices:
        if normalized == str(
            choice
        ).strip().lower():
            return True

    try:
        index = int(
            normalized
        )

    except ValueError:
        return False

    return (
        1 <= index <= len(
            choices
        )
    )


def validate_key(
    value: str,
    *,
    minimum: int = -25,
    maximum: int = 25,
) -> bool:
    # Checks whether a value is a valid
    # Caesar cipher key

    if not validate_integer(
        value
    ):
        return False

    number = int(
        value.strip()
    )

    return (
        minimum
        <= number
        <= maximum
    )


# Conversion Helpers


def convert_to_integer(
    value: str,
) -> int:
    # Converts prompt input into an integer

    try:
        return int(
            value.strip()
        )

    except (
        AttributeError,
        ValueError,
    ) as error:
        raise InvalidPromptInputError(
            f"Invalid integer: {value}"
        ) from error


def convert_to_float(
    value: str,
) -> float:
    # Converts prompt input into a float

    try:
        return float(
            value.strip()
        )

    except (
        AttributeError,
        ValueError,
    ) as error:
        raise InvalidPromptInputError(
            f"Invalid number: {value}"
        ) from error


def convert_to_boolean(
    value: str,
) -> bool:
    # Converts common yes/no values into bool

    if not isinstance(
        value,
        str,
    ):
        raise InvalidPromptInputError(
            "Boolean input must be a string."
        )

    normalized = value.strip().lower()

    if normalized in YES_VALUES:
        return True

    if normalized in NO_VALUES:
        return False

    raise InvalidPromptInputError(
        "Expected yes or no."
    )


# Prompt Formatting


def format_choices(
    choices: Sequence[Any],
) -> str:
    # Formats choices into a numbered list

    if not choices:
        return ""

    lines = []

    for index, choice in enumerate(
        choices,
        start=1,
    ):
        lines.append(
            f"{index}. {choice}"
        )

    return "\n".join(
        lines
    )


def format_prompt(
    message: str,
    *,
    default: Any = None,
    choices: Sequence[Any] | None = None,
) -> str:
    # Builds a formatted prompt message

    if not isinstance(
        message,
        str,
    ):
        raise TypeError(
            "message must be a string."
        )

    result = message.strip()

    if choices:
        result += (
            "\n"
            + format_choices(
                choices
            )
        )

    if default is not None:
        result += (
            f" [{default}]"
        )

    return result + ": "


# Batch Prompts


def prompt_many(
    prompts: Iterable[PromptConfig],
    *,
    manager: PromptManager | None = None,
) -> dict[str, Any]:
    # Executes multiple configured prompts

    prompt_manager = (
        manager
        if manager is not None
        else _default_prompt_manager
    )

    if not isinstance(
        prompt_manager,
        PromptManager,
    ):
        raise TypeError(
            "manager must be a PromptManager."
        )

    results: dict[str, Any] = {}

    for config in prompts:
        if not isinstance(
            config,
            PromptConfig,
        ):
            raise TypeError(
                "All prompts must be PromptConfig objects."
            )

        result = prompt_manager.ask(
            config.message,
            default=(
                str(config.default)
                if config.default is not None
                else None
            ),
            required=config.required,
            allow_cancel=config.allow_cancel,
        )

        if result.cancelled:
            raise PromptCancelledError(
                f"Prompt cancelled: "
                f"{config.message}"
            )

        value = result.value

        if config.converter is not None:
            try:
                value = config.converter(
                    value
                )

            except (
                ValueError,
                TypeError,
            ) as error:
                raise PromptValidationError(
                    f"Unable to convert prompt: "
                    f"{config.message}"
                ) from error

        if config.validator is not None:
            try:
                valid = config.validator(
                    value
                )

            except Exception as error:
                raise PromptValidationError(
                    f"Validator failed for prompt: "
                    f"{config.message}"
                ) from error

            if not valid:
                raise PromptValidationError(
                    f"Invalid value for prompt: "
                    f"{config.message}"
                )

        results[
            config.message
        ] = value

    return results


# Self-Test


def self_test() -> bool:
    # Runs basic prompt utility tests without
    # requiring interactive input

    try:
        if not normalize_input(
            "  hello  "
        ) == "hello":
            return False

        if not is_cancelled(
            "quit"
        ):
            return False

        if not is_yes(
            "YES"
        ):
            return False

        if not is_no(
            "no"
        ):
            return False

        if not validate_non_empty(
            "hello"
        ):
            return False

        if validate_non_empty(
            "   "
        ):
            return False

        if not validate_integer(
            "42"
        ):
            return False

        if validate_integer(
            "abc"
        ):
            return False

        if not validate_float(
            "3.14"
        ):
            return False

        if not validate_key(
            "5"
        ):
            return False

        if validate_key(
            "100"
        ):
            return False

        if convert_to_integer(
            "42"
        ) != 42:
            return False

        if convert_to_float(
            "3.5"
        ) != 3.5:
            return False

        if convert_to_boolean(
            "yes"
        ) is not True:
            return False

        if convert_to_boolean(
            "no"
        ) is not False:
            return False

        formatted = format_choices(
            [
                "Encrypt",
                "Decrypt",
            ]
        )

        if "1. Encrypt" not in formatted:
            return False

        if "2. Decrypt" not in formatted:
            return False

        return True

    except (
        PromptError,
        TypeError,
        ValueError,
    ):
        return False


# Module Exports


__all__ = [
    # Exceptions
    "PromptError",
    "PromptCancelledError",
    "InvalidPromptInputError",
    "PromptValidationError",

    # Data Models
    "PromptResult",
    "PromptConfig",

    # Constants
    "CANCEL_VALUES",
    "YES_VALUES",
    "NO_VALUES",

    # Input Utilities
    "normalize_input",
    "is_cancelled",
    "is_yes",
    "is_no",

    # Prompt Manager
    "PromptManager",

    # Standalone Prompts
    "prompt",
    "prompt_choice",
    "prompt_confirm",
    "prompt_integer",
    "prompt_float",
    "prompt_secret",
    "prompt_multiple",
    "prompt_cipher_key",
    "prompt_file_path",
    "prompt_directory_path",
    "prompt_confirm_secret",

    # Manager Access
    "get_prompt_manager",
    "set_prompt_manager",

    # Validation
    "validate_non_empty",
    "validate_integer",
    "validate_float",
    "validate_choice",
    "validate_key",

    # Conversion
    "convert_to_integer",
    "convert_to_float",
    "convert_to_boolean",

    # Formatting
    "format_choices",
    "format_prompt",

    # Batch Operations
    "prompt_many",

    # Testing
    "self_test",
]

