# validator.py

# Validation Utilities for the Entire Cryptography Toolkit

# Contains reusable validation functions for text, keys, alphabets,
# cipher parameters, configuration values, and other inputs used
# throughout the project.


from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from .constants import (
    LOWERCASE_ALPHABET,
    UPPERCASE_ALPHABET,
    DIGITS,
    ALPHANUMERIC,
    MIN_TEXT_LENGTH,
    MAX_TEXT_LENGTH,
    MIN_KEY_LENGTH,
    MAX_KEY_LENGTH,
    MIN_ALPHABET_LENGTH,
    MAX_ALPHABET_LENGTH,
    MIN_CAESAR_SHIFT,
    MAX_CAESAR_SHIFT,
    MIN_CHUNK_SIZE,
    MAX_CHUNK_SIZE,
)


# Internal Helpers


def _raise_type_error(
    name: str,
    expected: str,
) -> None:
    # Raises a consistent type validation error

    raise TypeError(
        f"{name} must be {expected}."
    )


def _raise_value_error(
    name: str,
    message: str,
) -> None:
    # Raises a consistent value validation error

    raise ValueError(
        f"{name} {message}."
    )


def _validate_name(
    name: str,
) -> None:
    # Validates a parameter name

    if not isinstance(
        name,
        str,
    ):
        _raise_type_error(
            "name",
            "a string",
        )

    if not name.strip():
        _raise_value_error(
            "name",
            "cannot be empty",
        )


# Basic Type Validation


def is_string(
    value: Any,
) -> bool:
    # Determines whether a value is a string

    return isinstance(
        value,
        str,
    )


def is_integer(
    value: Any,
) -> bool:
    # Determines whether a value is an integer

    return (
        isinstance(
            value,
            int,
        )
        and not isinstance(
            value,
            bool,
        )
    )


def is_number(
    value: Any,
) -> bool:
    # Determines whether a value is a numeric value

    return (
        isinstance(
            value,
            (int, float),
        )
        and not isinstance(
            value,
            bool,
        )
    )


def is_boolean(
    value: Any,
) -> bool:
    # Determines whether a value is a boolean

    return isinstance(
        value,
        bool,
    )


def is_sequence(
    value: Any,
) -> bool:
    # Determines whether a value is a sequence-like object

    if isinstance(
        value,
        (str, bytes, bytearray),
    ):
        return True

    try:
        len(value)
        value[0]
    except (
        TypeError,
        IndexError,
        KeyError,
    ):
        return False

    return True


def is_iterable(
    value: Any,
) -> bool:
    # Determines whether a value is iterable

    if isinstance(
        value,
        (str, bytes),
    ):
        return True

    try:
        iter(value)
    except TypeError:
        return False

    return True


def is_mapping(
    value: Any,
) -> bool:
    # Determines whether a value behaves like a mapping

    return hasattr(
        value,
        "keys",
    ) and hasattr(
        value,
        "items",
    )


# Required Value Validation


def require_string(
    value: Any,
    *,
    name: str = "value",
    allow_empty: bool = False,
) -> str:
    # Validates and returns a string value

    if not isinstance(
        value,
        str,
    ):
        _raise_type_error(
            name,
            "a string",
        )

    if not allow_empty and not value:
        _raise_value_error(
            name,
            "cannot be empty",
        )

    return value


def require_integer(
    value: Any,
    *,
    name: str = "value",
) -> int:
    # Validates and returns an integer value

    if not is_integer(
        value
    ):
        _raise_type_error(
            name,
            "an integer",
        )

    return value


def require_number(
    value: Any,
    *,
    name: str = "value",
) -> int | float:
    # Validates and returns a numeric value

    if not is_number(
        value
    ):
        _raise_type_error(
            name,
            "a number",
        )

    return value


def require_boolean(
    value: Any,
    *,
    name: str = "value",
) -> bool:
    # Validates and returns a boolean value

    if not isinstance(
        value,
        bool,
    ):
        _raise_type_error(
            name,
            "a boolean",
        )

    return value


# Text Validation


def validate_text(
    text: str,
    *,
    min_length: int = MIN_TEXT_LENGTH,
    max_length: int = MAX_TEXT_LENGTH,
    allow_empty: bool = True,
    strip: bool = False,
) -> bool:
    # Validates text against length and content requirements

    if not isinstance(
        text,
        str,
    ):
        return False

    if strip:
        text = text.strip()

    if not allow_empty and not text:
        return False

    if len(text) < min_length:
        return False

    if len(text) > max_length:
        return False

    return True


def require_text(
    text: str,
    *,
    name: str = "text",
    min_length: int = MIN_TEXT_LENGTH,
    max_length: int = MAX_TEXT_LENGTH,
    allow_empty: bool = True,
) -> str:
    # Validates text and raises an exception if invalid

    require_string(
        text,
        name=name,
        allow_empty=allow_empty,
    )

    if len(text) < min_length:
        _raise_value_error(
            name,
            f"must contain at least {min_length} characters",
        )

    if len(text) > max_length:
        _raise_value_error(
            name,
            f"cannot contain more than {max_length} characters",
        )

    return text


def validate_nonempty_text(
    text: str,
) -> bool:
    # Determines whether text contains at least one character

    return (
        isinstance(
            text,
            str,
        )
        and bool(text)
    )


def validate_printable_text(
    text: str,
) -> bool:
    # Determines whether all characters in text are printable

    if not isinstance(
        text,
        str,
    ):
        return False

    return all(
        character.isprintable()
        or character in "\n\r\t"
        for character in text
    )


def validate_ascii_text(
    text: str,
) -> bool:
    # Determines whether text contains only ASCII characters

    if not isinstance(
        text,
        str,
    ):
        return False

    return all(
        ord(character) < 128
        for character in text
    )


# Key Validation


def validate_key(
    key: Any,
    *,
    min_length: int = MIN_KEY_LENGTH,
    max_length: int = MAX_KEY_LENGTH,
    allow_empty: bool = False,
) -> bool:
    # Validates a cipher key

    if not isinstance(
        key,
        str,
    ):
        return False

    if not allow_empty and not key:
        return False

    if len(key) < min_length:
        return False

    if len(key) > max_length:
        return False

    return True


def require_key(
    key: Any,
    *,
    name: str = "key",
    min_length: int = MIN_KEY_LENGTH,
    max_length: int = MAX_KEY_LENGTH,
) -> str:
    # Validates a cipher key and raises an exception if invalid

    require_string(
        key,
        name=name,
        allow_empty=False,
    )

    if len(key) < min_length:
        _raise_value_error(
            name,
            f"must contain at least {min_length} characters",
        )

    if len(key) > max_length:
        _raise_value_error(
            name,
            f"cannot contain more than {max_length} characters",
        )

    return key


def validate_numeric_key(
    key: Any,
) -> bool:
    # Determines whether a key can be interpreted as an integer

    if is_integer(
        key
    ):
        return True

    if isinstance(
        key,
        str,
    ):
        try:
            int(key)
        except ValueError:
            return False

        return True

    return False


# Alphabet Validation


def validate_alphabet(
    alphabet: Any,
    *,
    min_length: int = MIN_ALPHABET_LENGTH,
    max_length: int = MAX_ALPHABET_LENGTH,
    require_unique: bool = True,
) -> bool:
    # Validates an alphabet used by a cipher

    if not isinstance(
        alphabet,
        str,
    ):
        return False

    if len(alphabet) < min_length:
        return False

    if len(alphabet) > max_length:
        return False

    if require_unique and len(
        set(alphabet)
    ) != len(alphabet):
        return False

    return True


def require_alphabet(
    alphabet: Any,
    *,
    name: str = "alphabet",
    min_length: int = MIN_ALPHABET_LENGTH,
    max_length: int = MAX_ALPHABET_LENGTH,
    require_unique: bool = True,
) -> str:
    # Validates an alphabet and raises an exception if invalid

    require_string(
        alphabet,
        name=name,
        allow_empty=False,
    )

    if len(alphabet) < min_length:
        _raise_value_error(
            name,
            f"must contain at least {min_length} characters",
        )

    if len(alphabet) > max_length:
        _raise_value_error(
            name,
            f"cannot contain more than {max_length} characters",
        )

    if (
        require_unique
        and len(set(alphabet))
        != len(alphabet)
    ):
        _raise_value_error(
            name,
            "must contain unique characters",
        )

    return alphabet


def is_standard_alphabet(
    alphabet: str,
) -> bool:
    # Determines whether an alphabet is one of the toolkit's standard alphabets

    return alphabet in (
        LOWERCASE_ALPHABET,
        UPPERCASE_ALPHABET,
        DIGITS,
        ALPHANUMERIC,
    )


# Numeric Range Validation


def validate_range(
    value: Any,
    minimum: float,
    maximum: float,
) -> bool:
    # Determines whether a numeric value falls within a range

    if not is_number(
        value
    ):
        return False

    if minimum > maximum:
        return False

    return (
        minimum
        <= value
        <= maximum
    )


def require_range(
    value: Any,
    minimum: float,
    maximum: float,
    *,
    name: str = "value",
) -> int | float:
    # Validates that a value falls within a specified range

    require_number(
        value,
        name=name,
    )

    if minimum > maximum:
        raise ValueError(
            "minimum cannot be greater than maximum."
        )

    if not (
        minimum
        <= value
        <= maximum
    ):
        _raise_value_error(
            name,
            f"must be between {minimum} and {maximum}",
        )

    return value


def validate_positive(
    value: Any,
) -> bool:
    # Determines whether a numeric value is positive

    return (
        is_number(value)
        and value > 0
    )


def validate_nonnegative(
    value: Any,
) -> bool:
    # Determines whether a numeric value is zero or positive

    return (
        is_number(value)
        and value >= 0
    )


# Cipher Parameter Validation


def validate_shift(
    shift: Any,
) -> bool:
    # Validates a standard Caesar Cipher shift

    return validate_range(
        shift,
        MIN_CAESAR_SHIFT,
        MAX_CAESAR_SHIFT,
    )


def require_shift(
    shift: Any,
    *,
    name: str = "shift",
) -> int:
    # Validates and returns a standard Caesar Cipher shift

    require_integer(
        shift,
        name=name,
    )

    if not validate_shift(
        shift
    ):
        _raise_value_error(
            name,
            f"must be between {MIN_CAESAR_SHIFT} and {MAX_CAESAR_SHIFT}",
        )

    return shift 


# Chunk Size Validation


def validate_chunk_size(
    chunk_size: Any,
) -> bool:
    # Determines whether a streaming chunk size is valid

    return (
        is_integer(chunk_size)
        and MIN_CHUNK_SIZE
        <= chunk_size
        <= MAX_CHUNK_SIZE
    )


def require_chunk_size(
    chunk_size: Any,
    *,
    name: str = "chunk_size",
) -> int:
    # Validates and returns a streaming chunk size

    require_integer(
        chunk_size,
        name=name,
    )

    if not validate_chunk_size(
        chunk_size
    ):
        _raise_value_error(
            name,
            f"must be between {MIN_CHUNK_SIZE} and {MAX_CHUNK_SIZE}",
        )

    return chunk_size


# N-gram Parameter Validation


def validate_ngram_size(
    size: Any,
    *,
    minimum: int = 1,
    maximum: int = 100,
) -> bool:
    # Determines whether an n-gram size is valid

    if not is_integer(
        size
    ):
        return False

    if minimum > maximum:
        return False

    return (
        minimum
        <= size
        <= maximum
    )


def require_ngram_size(
    size: Any,
    *,
    name: str = "size",
    minimum: int = 1,
    maximum: int = 100,
) -> int:
    # Validates and returns an n-gram size

    require_integer(
        size,
        name=name,
    )

    if minimum > maximum:
        raise ValueError(
            "minimum cannot be greater than maximum."
        )

    if not validate_ngram_size(
        size,
        minimum=minimum,
        maximum=maximum,
    ):
        _raise_value_error(
            name,
            f"must be between {minimum} and {maximum}",
        )

    return size


# Probability Validation


def validate_probability(
    value: Any,
) -> bool:
    # Determines whether a value is a valid probability

    return validate_range(
        value,
        0.0,
        1.0,
    )


def require_probability(
    value: Any,
    *,
    name: str = "probability",
) -> int | float:
    # Validates and returns a probability

    require_number(
        value,
        name=name,
    )

    if not validate_probability(
        value
    ):
        _raise_value_error(
            name,
            "must be between 0 and 1",
        )

    return value


def validate_percentage(
    value: Any,
) -> bool:
    # Determines whether a value is a valid percentage

    return validate_range(
        value,
        0.0,
        100.0,
    )


def require_percentage(
    value: Any,
    *,
    name: str = "percentage",
) -> int | float:
    # Validates and returns a percentage

    require_number(
        value,
        name=name,
    )

    if not validate_percentage(
        value
    ):
        _raise_value_error(
            name,
            "must be between 0 and 100",
        )

    return value


# Encoding Validation


def validate_encoding(
    encoding: Any,
) -> bool:
    # Determines whether an encoding name is valid

    if not isinstance(
        encoding,
        str,
    ):
        return False

    if not encoding.strip():
        return False

    try:
        "".encode(
            encoding
        )
    except (
        LookupError,
        TypeError,
    ):
        return False

    return True


def require_encoding(
    encoding: Any,
    *,
    name: str = "encoding",
) -> str:
    # Validates and returns an encoding name

    require_string(
        encoding,
        name=name,
        allow_empty=False,
    )

    if not validate_encoding(
        encoding
    ):
        _raise_value_error(
            name,
            "must be a valid text encoding",
        )

    return encoding


# File Path Validation


def validate_path(
    path: Any,
    *,
    must_exist: bool = False,
    must_be_file: bool = False,
    must_be_directory: bool = False,
) -> bool:
    # Validates a filesystem path

    from pathlib import Path

    if not isinstance(
        path,
        (str, Path),
    ):
        return False

    if isinstance(
        path,
        str,
    ) and not path.strip():
        return False

    try:
        resolved = Path(
            path
        )
    except (
        TypeError,
        ValueError,
    ):
        return False

    if must_exist and not resolved.exists():
        return False

    if must_be_file and not resolved.is_file():
        return False

    if must_be_directory and not resolved.is_dir():
        return False

    return True


def require_path(
    path: Any,
    *,
    name: str = "path",
    must_exist: bool = False,
    must_be_file: bool = False,
    must_be_directory: bool = False,
):
    # Validates and returns a filesystem path

    from pathlib import Path

    if not validate_path(
        path,
        must_exist=must_exist,
        must_be_file=must_be_file,
        must_be_directory=must_be_directory,
    ):
        _raise_value_error(
            name,
            "must be a valid filesystem path",
        )

    return Path(
        path
    )


# Collection Validation


def validate_collection(
    value: Any,
    *,
    allow_empty: bool = True,
) -> bool:
    # Determines whether a value is a valid collection

    if isinstance(
        value,
        (str, bytes),
    ):
        return False

    if not is_iterable(
        value
    ):
        return False

    if not allow_empty:
        try:
            return len(value) > 0
        except TypeError:
            return True

    return True


def require_collection(
    value: Any,
    *,
    name: str = "value",
    allow_empty: bool = True,
):
    # Validates and returns a collection

    if not validate_collection(
        value,
        allow_empty=allow_empty,
    ):
        _raise_value_error(
            name,
            "must be a valid collection",
        )

    return value


def validate_unique_collection(
    values: Iterable[Any],
) -> bool:
    # Determines whether every item in an iterable is unique

    try:
        items = list(
            values
        )
    except TypeError:
        return False

    return len(
        items
    ) == len(
        set(items)
    )


# Callable Validation


def validate_callable(
    value: Any,
) -> bool:
    # Determines whether a value is callable

    return callable(
        value
    )


def require_callable(
    value: Any,
    *,
    name: str = "value",
):
    # Validates and returns a callable

    if not callable(
        value
    ):
        _raise_type_error(
            name,
            "callable",
        )

    return value


# Generic Parameter Validation


def validate_choice(
    value: Any,
    choices: Iterable[Any],
) -> bool:
    # Determines whether a value exists within an allowed collection

    try:
        return value in choices
    except TypeError:
        return False


def require_choice(
    value: Any,
    choices: Iterable[Any],
    *,
    name: str = "value",
):
    # Validates that a value is one of the permitted choices

    try:
        valid = value in choices
    except TypeError:
        valid = False

    if not valid:
        _raise_value_error(
            name,
            "is not an allowed value",
        )

    return value


def validate_not_none(
    value: Any,
) -> bool:
    # Determines whether a value is not None

    return value is not None


def require_not_none(
    value: Any,
    *,
    name: str = "value",
):
    # Validates that a value is not None

    if value is None:
        _raise_value_error(
            name,
            "cannot be None",
        )

    return value


# Dictionary Validation


def validate_mapping_keys(
    mapping: Any,
    required_keys: Iterable[Any],
) -> bool:
    # Determines whether a mapping contains all required keys

    if not is_mapping(
        mapping
    ):
        return False

    try:
        return all(
            key in mapping
            for key in required_keys
        )
    except TypeError:
        return False


def require_mapping_keys(
    mapping: Any,
    required_keys: Iterable[Any],
    *,
    name: str = "mapping",
):
    # Validates that a mapping contains required keys

    if not validate_mapping_keys(
        mapping,
        required_keys,
    ):
        _raise_value_error(
            name,
            "does not contain all required keys",
        )

    return mapping


# Boolean Parameter Validation


def validate_flag(
    value: Any,
) -> bool:
    # Determines whether a value is a valid boolean flag

    return isinstance(
        value,
        bool,
    )


def require_flag(
    value: Any,
    *,
    name: str = "flag",
) -> bool:
    # Validates and returns a boolean flag

    if not isinstance(
        value,
        bool,
    ):
        _raise_type_error(
            name,
            "a boolean",
        )

    return value


# Validation Summary Helpers


def validation_errors(
    values: dict[str, Any],
    validators: dict[str, Any],
) -> dict[str, str]:
    # Returns validation errors for a collection of named values

    if not isinstance(
        values,
        dict,
    ):
        raise TypeError(
            "values must be a dictionary."
        )

    if not isinstance(
        validators,
        dict,
    ):
        raise TypeError(
            "validators must be a dictionary."
        )

    errors: dict[str, str] = {}

    for name, validator in validators.items():

        if not callable(
            validator
        ):
            errors[name] = (
                "validator is not callable"
            )
            continue

        value = values.get(
            name
        )

        try:
            valid = validator(
                value
            )
        except (
            TypeError,
            ValueError,
        ) as error:
            errors[name] = str(
                error
            )
            continue

        if not valid:
            errors[name] = (
                "invalid value"
            )

    return errors


def validate_all(
    values: Iterable[Any],
    validator: Any,
) -> bool:
    # Determines whether every value passes a validator

    if not callable(
        validator
    ):
        raise TypeError(
            "validator must be callable."
        )

    return all(
        validator(value)
        for value in values
    )


def validate_any(
    values: Iterable[Any],
    validator: Any,
) -> bool:
    # Determines whether at least one value passes a validator

    if not callable(
        validator
    ):
        raise TypeError(
            "validator must be callable."
        )

    return any(
        validator(value)
        for value in values
    )


# Self Test


def self_test() -> bool:
    # Runs a quick internal test of the validation module

    tests = [

        # Basic Types
        is_string("hello"),
        not is_string(123),

        is_integer(10),
        not is_integer(True),

        is_number(10),
        is_number(3.14),
        not is_number(False),

        is_boolean(True),
        not is_boolean(1),

        is_iterable("hello"),
        is_mapping({}),

        # Text
        validate_text(
            "Hello",
            min_length=1,
            max_length=10,
        ),

        not validate_text(
            "",
            allow_empty=False,
        ),

        validate_nonempty_text(
            "hello"
        ),

        validate_printable_text(
            "Hello World!"
        ),

        validate_ascii_text(
            "Hello World!"
        ),

        # Keys
        validate_key(
            "secret"
        ),

        not validate_key(
            ""
        ),

        validate_numeric_key(
            3
        ),

        validate_numeric_key(
            "13"
        ),

        # Alphabets
        validate_alphabet(
            LOWERCASE_ALPHABET
        ),

        validate_alphabet(
            UPPERCASE_ALPHABET
        ),

        not validate_alphabet(
            "aabc"
        ),

        is_standard_alphabet(
            LOWERCASE_ALPHABET
        ),

        # Numeric
        validate_range(
            5,
            0,
            10,
        ),

        not validate_range(
            15,
            0,
            10,
        ),

        validate_positive(
            5
        ),

        validate_nonnegative(
            0
        ),

        # Cipher
        validate_shift(
            3
        ),

        validate_shift(
            25
        ),

        not validate_shift(
            26
        ),

        # Chunking
        validate_chunk_size(
            4096
        ),

        not validate_chunk_size(
            0
        ),

        # N-grams
        validate_ngram_size(
            2
        ),

        not validate_ngram_size(
            0
        ),

        # Probability
        validate_probability(
            0.5
        ),

        validate_probability(
            1.0
        ),

        not validate_probability(
            1.5
        ),

        validate_percentage(
            50
        ),

        not validate_percentage(
            101
        ),

        # Encoding
        validate_encoding(
            "utf-8"
        ),

        not validate_encoding(
            "not-an-encoding"
        ),

        # Paths
        validate_path(
            "."
        ),

        validate_path(
            ".",
            must_exist=True,
            must_be_directory=True,
        ),

        # Collections
        validate_collection(
            [1, 2, 3]
        ),

        validate_unique_collection(
            [1, 2, 3]
        ),

        not validate_unique_collection(
            [1, 2, 2]
        ),

        # Callables
        validate_callable(
            self_test
        ),

        # Choices
        validate_choice(
            "caesar",
            [
                "caesar",
                "atbash",
            ],
        ),

        not validate_choice(
            "unknown",
            [
                "caesar",
                "atbash",
            ],
        ),

        # None
        validate_not_none(
            "value"
        ),

        not validate_not_none(
            None
        ),

        # Mappings
        validate_mapping_keys(
            {
                "name": "test",
                "value": 1,
            },
            [
                "name",
                "value",
            ],
        ),

        # Flags
        validate_flag(
            True
        ),

        not validate_flag(
            1
        ),

        # Validation Utilities
        validate_all(
            [1, 2, 3],
            lambda value: value > 0,
        ),

        validate_any(
            [0, 0, 1],
            lambda value: value > 0,
        ),
    ]

    return all(
        tests
    )


# Module Exports


__all__ = [

    # Basic Type Validation
    "is_string",
    "is_integer",
    "is_number",
    "is_boolean",
    "is_sequence",
    "is_iterable",
    "is_mapping",

    # Required Values
    "require_string",
    "require_integer",
    "require_number",
    "require_boolean",

    # Text Validation
    "validate_text",
    "require_text",
    "validate_nonempty_text",
    "validate_printable_text",
    "validate_ascii_text",

    # Key Validation
    "validate_key",
    "require_key",
    "validate_numeric_key",

    # Alphabet Validation
    "validate_alphabet",
    "require_alphabet",
    "is_standard_alphabet",

    # Numeric Validation
    "validate_range",
    "require_range",
    "validate_positive",
    "validate_nonnegative",

    # Cipher Validation
    "validate_shift",
    "require_shift",

    # Chunk Validation
    "validate_chunk_size",
    "require_chunk_size",

    # N-gram Validation
    "validate_ngram_size",
    "require_ngram_size",

    # Probability Validation
    "validate_probability",
    "require_probability",
    "validate_percentage",
    "require_percentage",

    # Encoding Validation
    "validate_encoding",
    "require_encoding",

    # Path Validation
    "validate_path",
    "require_path",

    # Collection Validation
    "validate_collection",
    "require_collection",
    "validate_unique_collection",

    # Callable Validation
    "validate_callable",
    "require_callable",

    # Generic Validation
    "validate_choice",
    "require_choice",
    "validate_not_none",
    "require_not_none",

    # Dictionary Validation
    "validate_mapping_keys",
    "require_mapping_keys",

    # Boolean Validation
    "validate_flag",
    "require_flag",

    # Validation Helpers
    "validation_errors",
    "validate_all",
    "validate_any",

    # Testing
    "self_test",
]

