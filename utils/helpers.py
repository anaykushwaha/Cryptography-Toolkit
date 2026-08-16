# helpers.py

# General-Purpose Helper Utilities for the Cryptography Toolkit

# Contains reusable helper functions for text processing,
# collection handling, formatting, conversion, and common
# operations shared throughout the project.


from __future__ import annotations

import math
import string
from collections.abc import (
    Iterable,
    Sequence,
)
from typing import (
    Any,
    TypeVar,
)

from .constants import (
    LOWERCASE_ALPHABET,
    UPPERCASE_ALPHABET,
    DIGITS,
    ALPHANUMERIC,
    EMPTY_STRING,
    SPACE,
    DEFAULT_ENCODING,
)


# Type Variables

T = TypeVar("T")


# Text Helpers


def is_empty(
    value: Any,
) -> bool:
    # Determines whether a value is empty

    if value is None:
        return True

    if isinstance(
        value,
        str,
    ):
        return not value.strip()

    try:
        return len(value) == 0
    except TypeError:
        return False


def normalize_text(
    text: str,
    *,
    strip: bool = True,
    collapse_spaces: bool = False,
    lowercase: bool = False,
) -> str:
    # Normalizes text according to the supplied options

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "text must be a string."
        )

    result = text

    if strip:
        result = result.strip()

    if collapse_spaces:
        result = " ".join(
            result.split()
        )

    if lowercase:
        result = result.lower()

    return result


def clean_text(
    text: str,
    *,
    keep_spaces: bool = True,
    keep_digits: bool = True,
    keep_punctuation: bool = True,
) -> str:
    # Removes unwanted character categories from text

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "text must be a string."
        )

    allowed = set(
        LOWERCASE_ALPHABET
        + UPPERCASE_ALPHABET
    )

    if keep_spaces:
        allowed.update(
            string.whitespace
        )

    if keep_digits:
        allowed.update(
            DIGITS
        )

    if keep_punctuation:
        allowed.update(
            string.punctuation
        )

    return "".join(
        character
        for character in text
        if character in allowed
    )


def reverse_text(
    text: str,
) -> str:
    # Returns text in reverse order

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "text must be a string."
        )

    return text[::-1]


def count_characters(
    text: str,
    *,
    ignore_case: bool = False,
) -> dict[str, int]:
    # Counts the occurrences of every character in text

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "text must be a string."
        )

    if ignore_case:
        text = text.lower()

    counts: dict[str, int] = {}

    for character in text:
        counts[character] = (
            counts.get(
                character,
                0,
            )
            + 1
        )

    return counts


def count_words(
    text: str,
) -> int:
    # Returns the number of whitespace-separated words

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "text must be a string."
        )

    return len(
        text.split()
    )


def word_list(
    text: str,
) -> list[str]:
    # Returns a list of whitespace-separated words

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "text must be a string."
        )

    return text.split()


def character_ratio(
    text: str,
    character: str,
) -> float:
    # Returns the proportion of text occupied by a character

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "text must be a string."
        )

    if not isinstance(
        character,
        str,
    ):
        raise TypeError(
            "character must be a string."
        )

    if len(character) != 1:
        raise ValueError(
            "character must contain exactly one character."
        )

    if not text:
        return 0.0

    return (
        text.count(character)
        / len(text)
    )


def alphabetic_ratio(
    text: str,
) -> float:
    # Returns the proportion of alphabetic characters in text

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "text must be a string."
        )

    if not text:
        return 0.0

    return sum(
        character.isalpha()
        for character in text
    ) / len(text)


def digit_ratio(
    text: str,
) -> float:
    # Returns the proportion of digits in text

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "text must be a string."
        )

    if not text:
        return 0.0

    return sum(
        character.isdigit()
        for character in text
    ) / len(text)


def whitespace_ratio(
    text: str,
) -> float:
    # Returns the proportion of whitespace characters in text

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "text must be a string."
        )

    if not text:
        return 0.0

    return sum(
        character.isspace()
        for character in text
    ) / len(text)


# Character Helpers


def is_letter(
    character: str,
) -> bool:
    # Determines whether a value is a single alphabetic character

    return (
        isinstance(
            character,
            str,
        )
        and len(character) == 1
        and character.isalpha()
    )


def is_digit(
    character: str,
) -> bool:
    # Determines whether a value is a single digit

    return (
        isinstance(
            character,
            str,
        )
        and len(character) == 1
        and character.isdigit()
    )


def is_whitespace(
    character: str,
) -> bool:
    # Determines whether a value is a single whitespace character

    return (
        isinstance(
            character,
            str,
        )
        and len(character) == 1
        and character.isspace()
    )


def is_alphanumeric(
    character: str,
) -> bool:
    # Determines whether a value is a single alphanumeric character

    return (
        isinstance(
            character,
            str,
        )
        and len(character) == 1
        and character.isalnum()
    )


def is_printable(
    character: str,
) -> bool:
    # Determines whether a character is printable

    return (
        isinstance(
            character,
            str,
        )
        and len(character) == 1
        and character.isprintable()
    )


def is_ascii(
    character: str,
) -> bool:
    # Determines whether a character belongs to ASCII

    if not isinstance(
        character,
        str,
    ):
        return False

    return all(
        ord(char) < 128
        for char in character
    )


def safe_lower(
    value: str,
) -> str:
    # Safely converts a string to lowercase

    if not isinstance(
        value,
        str,
    ):
        raise TypeError(
            "value must be a string."
        )

    return value.lower()


def safe_upper(
    value: str,
) -> str:
    # Safely converts a string to uppercase

    if not isinstance(
        value,
        str,
    ):
        raise TypeError(
            "value must be a string."
        )

    return value.upper()


# Collection Helpers


def flatten(
    items: Iterable[Any],
) -> list[Any]:
    # Flattens nested iterables into a single list

    result: list[Any] = []

    for item in items:

        if isinstance(
            item,
            (str, bytes),
        ):
            result.append(
                item
            )
            continue

        if isinstance(
            item,
            Iterable,
        ):
            result.extend(
                flatten(item)
            )
        else:
            result.append(
                item
            )

    return result


def chunk(
    sequence: Sequence[T],
    size: int,
) -> list[list[T]]:
    # Splits a sequence into equally sized chunks

    if not isinstance(
        size,
        int,
    ):
        raise TypeError(
            "size must be an integer."
        )

    if size <= 0:
        raise ValueError(
            "size must be greater than zero."
        )

    return [
        list(
            sequence[index:index + size]
        )
        for index in range(
            0,
            len(sequence),
            size,
        )
    ]


def unique(
    items: Iterable[T],
) -> list[T]:
    # Returns items while preserving their original order

    result: list[T] = []

    for item in items:

        if item not in result:
            result.append(
                item
            )

    return result


def first(
    items: Sequence[T],
    default: T | None = None,
) -> T | None:
    # Returns the first item in a sequence

    if not items:
        return default

    return items[0]


def last(
    items: Sequence[T],
    default: T | None = None,
) -> T | None:
    # Returns the final item in a sequence

    if not items:
        return default

    return items[-1]


def clamp(
    value: float,
    minimum: float,
    maximum: float,
) -> float:
    # Restricts a value to a specified range

    if minimum > maximum:
        raise ValueError(
            "minimum cannot be greater than maximum."
        )

    return max(
        minimum,
        min(
            value,
            maximum,
        ),
    )


# Numeric Helpers


def safe_divide(
    numerator: float,
    denominator: float,
    default: float = 0.0,
) -> float:
    # Safely divides two numbers

    if denominator == 0:
        return default

    return numerator / denominator


def percentage(
    value: float,
    total: float,
) -> float:
    # Calculates a percentage

    return safe_divide(
        value * 100,
        total,
    )


def round_float(
    value: float,
    digits: int = 4,
) -> float:
    # Rounds a floating-point value

    if not isinstance(
        digits,
        int,
    ):
        raise TypeError(
            "digits must be an integer."
        )

    if digits < 0:
        raise ValueError(
            "digits cannot be negative."
        )

    return round(
        value,
        digits,
    )


def mean(
    values: Sequence[float],
) -> float:
    # Calculates the arithmetic mean of a sequence

    if not values:
        return 0.0

    return sum(
        values
    ) / len(
        values
    )


def median(
    values: Sequence[float],
) -> float:
    # Calculates the median of a sequence

    if not values:
        return 0.0

    ordered = sorted(
        values
    )

    middle = len(
        ordered
    ) // 2

    if len(
        ordered
    ) % 2 == 0:
        return (
            ordered[middle - 1]
            + ordered[middle]
        ) / 2

    return ordered[
        middle
    ]


def standard_deviation(
    values: Sequence[float],
) -> float:
    # Calculates the population standard deviation

    if not values:
        return 0.0

    average = mean(
        values
    )

    variance = mean(
        [
            (
                value
                - average
            ) ** 2
            for value in values
        ]
    )

    return math.sqrt(
        variance
    )


# Encoding Helpers


def encode_text(
    text: str,
    encoding: str = DEFAULT_ENCODING,
) -> bytes:
    # Encodes text into bytes

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "text must be a string."
        )

    return text.encode(
        encoding
    )


def decode_bytes(
    data: bytes,
    encoding: str = DEFAULT_ENCODING,
) -> str:
    # Decodes bytes into text

    if not isinstance(
        data,
        bytes,
    ):
        raise TypeError(
            "data must be bytes."
        )

    return data.decode(
        encoding
    )


# Module Exports

__all__ = [
    "is_empty",
    "normalize_text",
    "clean_text",
    "reverse_text",
    "count_characters",
    "count_words",
    "word_list",
    "character_ratio",
    "alphabetic_ratio",
    "digit_ratio",
    "whitespace_ratio",
    "is_letter",
    "is_digit",
    "is_whitespace",
    "is_alphanumeric",
    "is_printable",
    "is_ascii",
    "safe_lower",
    "safe_upper",
    "flatten",
    "chunk",
    "unique",
    "first",
    "last",
    "clamp",
    "safe_divide",
    "percentage",
    "round_float",
    "mean",
    "median",
    "standard_deviation",
    "encode_text",
    "decode_bytes",
]

