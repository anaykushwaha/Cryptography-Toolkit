# ioc.py
# Index of Coincidence analysis for the Cryptography Toolkit

# Contains functions for calculating the Index of Coincidence,
# comparing text against language expectations, and supporting
# classical cipher analysis


from __future__ import annotations

from collections import Counter

from .english_data import (
    EXPECTED_ENGLISH_IOC,
    RANDOM_IOC,
    ENGLISH_ALPHABET_SIZE,
)


# Basic Index of Coincidence


def calculate_ioc(
    text: str,
) -> float:
    # Calculates the Index of Coincidence for alphabetic characters

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    letters = [
        character.upper()
        for character in text
        if character.isalpha()
    ]

    total = len(
        letters
    )

    if total <= 1:
        return 0.0

    frequencies = Counter(
        letters
    )

    numerator = sum(
        count * (
            count - 1
        )
        for count
        in frequencies.values()
    )

    denominator = (
        total
        * (
            total - 1
        )
    )

    return numerator / denominator


def calculate_ioc_from_counts(
    frequencies: dict[str, int],
) -> float:
    # Calculates the Index of Coincidence from frequency counts

    if not isinstance(
        frequencies,
        dict,
    ):
        raise TypeError(
            "Frequencies must be a dictionary."
        )

    total = sum(
        frequencies.values()
    )

    if total <= 1:
        return 0.0

    numerator = sum(
        count * (
            count - 1
        )
        for count
        in frequencies.values()
    )

    denominator = (
        total
        * (
            total - 1
        )
    )

    return numerator / denominator


# IOC Comparison


def ioc_difference(
    text: str,
) -> float:
    # Calculates the absolute difference between the text IOC
    # and the expected English IOC

    value = calculate_ioc(
        text
    )

    return abs(
        value
        - EXPECTED_ENGLISH_IOC
    )


def random_ioc_difference(
    text: str,
) -> float:
    # Calculates the absolute difference between the text IOC
    # and the expected random-text IOC

    value = calculate_ioc(
        text
    )

    return abs(
        value
        - RANDOM_IOC
    )


def english_ioc_similarity(
    text: str,
) -> float:
    # Calculates how closely a text IOC resembles English text

    difference = ioc_difference(
        text
    )

    maximum_difference = max(
        EXPECTED_ENGLISH_IOC,
        1.0 - EXPECTED_ENGLISH_IOC,
    )

    if maximum_difference == 0:
        return 1.0

    similarity = (
        1.0
        - (
            difference
            / maximum_difference
        )
    )

    return max(
        0.0,
        min(
            1.0,
            similarity,
        ),
    )


# IOC Classification


def classify_ioc(
    text: str,
) -> str:
    # Provides a broad classification based on the IOC value

    value = calculate_ioc(
        text
    )

    if value == 0.0:
        return "insufficient_data"

    if value >= 0.060:
        return "english_like"

    if value >= 0.045:
        return "mixed_or_polyalphabetic"

    return "random_like"


def is_english_like(
    text: str,
    tolerance: float = 0.010,
) -> bool:
    # Determines whether a text IOC falls near the expected English IOC

    if tolerance < 0:
        raise ValueError(
            "Tolerance cannot be negative."
        )

    value = calculate_ioc(
        text
    )

    return abs(
        value
        - EXPECTED_ENGLISH_IOC
    ) <= tolerance


def is_random_like(
    text: str,
    tolerance: float = 0.010,
) -> bool:
    # Determines whether a text IOC falls near the random-text IOC

    if tolerance < 0:
        raise ValueError(
            "Tolerance cannot be negative."
        )

    value = calculate_ioc(
        text
    )

    return abs(
        value
        - RANDOM_IOC
    ) <= tolerance


# IOC Statistics

def ioc_range(
    text: str,
) -> dict[str, float]:
    # Returns the IOC and its distance from major reference values

    value = calculate_ioc(
        text
    )

    return {
        "ioc": value,
        "english": EXPECTED_ENGLISH_IOC,
        "random": RANDOM_IOC,
        "english_difference": abs(
            value
            - EXPECTED_ENGLISH_IOC
        ),
        "random_difference": abs(
            value
            - RANDOM_IOC
        ),
    } 

# IOC Column Analysis


def split_into_columns(
    text: str,
    column: int,
    key_length: int,
) -> str:
    # Extracts every character belonging to one key position

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    if not isinstance(
        column,
        int,
    ):
        raise TypeError(
            "Column must be an integer."
        )

    if not isinstance(
        key_length,
        int,
    ):
        raise TypeError(
            "Key length must be an integer."
        )

    if key_length <= 0:
        raise ValueError(
            "Key length must be greater than zero."
        )

    if column < 0 or column >= key_length:
        raise ValueError(
            "Column must be within the key length."
        )

    letters = [
        character
        for character in text
        if character.isalpha()
    ]

    return "".join(
        letters[column::key_length]
    )


def column_iocs(
    text: str,
    key_length: int,
) -> list[float]:
    # Calculates the IOC of every column for a proposed key length

    if not isinstance(
        key_length,
        int,
    ):
        raise TypeError(
            "Key length must be an integer."
        )

    if key_length <= 0:
        raise ValueError(
            "Key length must be greater than zero."
        )

    return [
        calculate_ioc(
            split_into_columns(
                text,
                column,
                key_length,
            )
        )
        for column
        in range(
            key_length
        )
    ]


def average_column_ioc(
    text: str,
    key_length: int,
) -> float:
    # Calculates the average IOC across all columns

    values = column_iocs(
        text,
        key_length,
    )

    if not values:
        return 0.0

    return sum(
        values
    ) / len(
        values
    )


def column_ioc_summary(
    text: str,
    key_length: int,
) -> dict:
    # Returns detailed IOC information for every column

    values = column_iocs(
        text,
        key_length,
    )

    return {
        "key_length": key_length,
        "columns": values,
        "average": (
            sum(values)
            / len(values)
            if values
            else 0.0
        ),
        "minimum": (
            min(values)
            if values
            else 0.0
        ),
        "maximum": (
            max(values)
            if values
            else 0.0
        ),
    }


# Key Length Analysis


def key_length_scores(
    text: str,
    maximum_length: int = 20,
) -> dict[int, float]:
    # Calculates average column IOC for every possible key length

    if not isinstance(
        maximum_length,
        int,
    ):
        raise TypeError(
            "Maximum length must be an integer."
        )

    if maximum_length <= 0:
        raise ValueError(
            "Maximum length must be greater than zero."
        )

    return {
        length: average_column_ioc(
            text,
            length,
        )
        for length
        in range(
            1,
            maximum_length + 1,
        )
    }


def rank_key_lengths(
    text: str,
    maximum_length: int = 20,
) -> list[tuple[int, float]]:
    # Ranks possible key lengths by their average column IOC

    scores = key_length_scores(
        text,
        maximum_length,
    )

    return sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True,
    )


def probable_key_lengths(
    text: str,
    maximum_length: int = 20,
    count: int = 5,
) -> list[int]:
    # Returns the strongest candidate key lengths

    if not isinstance(
        count,
        int,
    ):
        raise TypeError(
            "Count must be an integer."
        )

    if count <= 0:
        return []

    ranked = rank_key_lengths(
        text,
        maximum_length,
    )

    return [
        length
        for length, _
        in ranked[:count]
    ] 

# Repeated Pattern Analysis


def repeated_patterns(
    text: str,
    minimum_length: int = 3,
    maximum_length: int = 5,
) -> dict[str, list[int]]:
    # Finds repeated alphabetic patterns and their positions

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    if minimum_length <= 0:
        raise ValueError(
            "Minimum length must be greater than zero."
        )

    if maximum_length < minimum_length:
        raise ValueError(
            "Maximum length must be greater than or equal "
            "to minimum length."
        )

    letters = "".join(
        character.upper()
        for character in text
        if character.isalpha()
    )

    patterns = {}

    for length in range(
        minimum_length,
        maximum_length + 1,
    ):

        for index in range(
            len(letters) - length + 1
        ):

            pattern = letters[
                index:index + length
            ]

            positions = []

            for position in range(
                index + 1,
                len(letters) - length + 1,
            ):

                if letters[
                    position:position + length
                ] == pattern:
                    positions.append(
                        position
                    )

            if positions:
                patterns.setdefault(
                    pattern,
                    [index],
                )

                patterns[pattern].extend(
                    position
                    for position in positions
                    if position
                    not in patterns[pattern]
                )

    return patterns


def repeated_pattern_distances(
    text: str,
    minimum_length: int = 3,
    maximum_length: int = 5,
) -> dict[str, list[int]]:
    # Calculates distances between repeated pattern occurrences

    patterns = repeated_patterns(
        text,
        minimum_length,
        maximum_length,
    )

    distances = {}

    for pattern, positions in patterns.items():

        if len(
            positions
        ) < 2:
            continue

        distances[pattern] = [
            second - first
            for first, second
            in zip(
                positions,
                positions[1:],
            )
        ]

    return distances


# IOC Analysis


def analyze_ioc(
    text: str,
) -> dict:
    # Returns a complete Index of Coincidence analysis

    value = calculate_ioc(
        text
    )

    return {
        "ioc": value,
        "english_ioc": EXPECTED_ENGLISH_IOC,
        "random_ioc": RANDOM_IOC,
        "english_difference": ioc_difference(
            text
        ),
        "random_difference": random_ioc_difference(
            text
        ),
        "english_similarity": english_ioc_similarity(
            text
        ),
        "classification": classify_ioc(
            text
        ),
        "letter_count": sum(
            1
            for character in text
            if character.isalpha()
        ),
    }


def analyze_key_lengths(
    text: str,
    maximum_length: int = 20,
) -> dict:
    # Returns ranked key-length candidates with IOC scores

    ranked = rank_key_lengths(
        text,
        maximum_length,
    )

    return {
        "maximum_length": maximum_length,
        "candidates": ranked,
        "probable_lengths": probable_key_lengths(
            text,
            maximum_length,
        ),
    }


# Validation


def validate_ioc_input(
    text: str,
) -> bool:
    # Determines whether a value can be analyzed by the IOC module

    return isinstance(
        text,
        str,
    )


def validate_key_length(
    key_length: int,
) -> bool:
    # Validates a proposed key length

    return (
        isinstance(
            key_length,
            int,
        )
        and key_length > 0
    )


# Self Test


def self_test() -> bool:
    # Runs a quick internal test of the IOC utilities

    text = (
        "THIS IS A SAMPLE MESSAGE "
        "FOR INDEX OF COINCIDENCE ANALYSIS"
    )

    if not validate_ioc_input(
        text
    ):
        return False

    if not validate_key_length(
        3
    ):
        return False

    if validate_key_length(
        0
    ):
        return False

    value = calculate_ioc(
        text
    )

    if value < 0:
        return False

    column = split_into_columns(
        text,
        0,
        3,
    )

    if not isinstance(
        column,
        str,
    ):
        return False

    values = column_iocs(
        text,
        3,
    )

    if len(
        values
    ) != 3:
        return False

    average = average_column_ioc(
        text,
        3,
    )

    if average < 0:
        return False

    ranked = rank_key_lengths(
        text,
        5,
    )

    if len(
        ranked
    ) != 5:
        return False

    probable = probable_key_lengths(
        text,
        5,
        3,
    )

    if len(
        probable
    ) != 3:
        return False

    analysis = analyze_ioc(
        text
    )

    if "ioc" not in analysis:
        return False

    key_analysis = analyze_key_lengths(
        text,
        5,
    )

    if "candidates" not in key_analysis:
        return False

    return True


# Module Exports

__all__ = [
    "calculate_ioc",
    "calculate_ioc_from_counts",
    "ioc_difference",
    "random_ioc_difference",
    "english_ioc_similarity",
    "classify_ioc",
    "is_english_like",
    "is_random_like",
    "ioc_range",
    "split_into_columns",
    "column_iocs",
    "average_column_ioc",
    "column_ioc_summary",
    "key_length_scores",
    "rank_key_lengths",
    "probable_key_lengths",
    "repeated_patterns",
    "repeated_pattern_distances",
    "analyze_ioc",
    "analyze_key_lengths",
    "validate_ioc_input",
    "validate_key_length",
    "self_test",
] 

