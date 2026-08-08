# frequency.py
# Frequency analysis utilities for the Cryptography Toolkit

# Contains functions for measuring character and letter frequencies,
# calculating frequency percentages, and preparing data for cryptanalysis


from __future__ import annotations

from collections import Counter

from .english_data import (
    ENGLISH_LETTER_FREQUENCIES,
    get_frequency_table,
)
from .statistics import (
    frequency_percentages,
    sorted_frequencies,
)


# Character Frequency


def count_characters(
    text: str,
) -> dict[str, int]:
    # Counts every character appearing in a text

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    return dict(
        Counter(
            text
        )
    )


def count_letters(
    text: str,
    *,
    case_sensitive: bool = False,
) -> dict[str, int]:
    # Counts alphabetic characters while ignoring non-letter characters

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    if not case_sensitive:
        text = text.upper()

    frequencies = Counter(
        character
        for character in text
        if character.isalpha()
    )

    return dict(
        frequencies
    )


def count_digits(
    text: str,
) -> dict[str, int]:
    # Counts numeric characters appearing in a text

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    return dict(
        Counter(
            character
            for character in text
            if character.isdigit()
        )
    )


def count_symbols(
    text: str,
) -> dict[str, int]:
    # Counts non-alphanumeric characters appearing in a text

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    return dict(
        Counter(
            character
            for character in text
            if not character.isalnum()
        )
    )


# Frequency Percentages


def character_percentages(
    text: str,
) -> dict[str, float]:
    # Calculates the percentage of each character in a text

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    if not text:
        return {}

    frequencies = count_characters(
        text
    )

    return frequency_percentages(
        frequencies
    )


def letter_percentages(
    text: str,
) -> dict[str, float]:
    # Calculates the percentage of each letter among all letters

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    letters = count_letters(
        text
    )

    return frequency_percentages(
        letters
    )


# Frequency Ranking


def rank_characters(
    text: str,
) -> list[tuple[str, int]]:
    # Returns characters ordered from most frequent to least frequent

    frequencies = count_characters(
        text
    )

    return sorted_frequencies(
        frequencies
    )


def rank_letters(
    text: str,
) -> list[tuple[str, int]]:
    # Returns letters ordered from most frequent to least frequent

    frequencies = count_letters(
        text
    )

    return sorted_frequencies(
        frequencies
    )


def most_common_letters(
    text: str,
    count: int = 5,
) -> list[tuple[str, int]]:
    # Returns the most frequently occurring letters

    if count <= 0:
        return []

    return rank_letters(
        text
    )[:count]


def least_common_letters(
    text: str,
    count: int = 5,
) -> list[tuple[str, int]]:
    # Returns the least frequently occurring letters

    if count <= 0:
        return []

    ranked = rank_letters(
        text
    )

    return ranked[
        -count:
    ] 

# English Frequency Comparison


def expected_frequencies(
    *,
    include_zero: bool = True,
) -> dict[str, float]:
    # Returns the expected English letter frequencies

    frequencies = get_frequency_table()

    if include_zero:
        return frequencies

    return {
        letter: frequency
        for letter, frequency
        in frequencies.items()
        if frequency > 0
    }


def observed_letter_percentages(
    text: str,
) -> dict[str, float]:
    # Returns observed letter percentages for a text
    # Includes all letters of the English alphabet

    percentages = letter_percentages(
        text
    )

    return {
        letter: percentages.get(
            letter,
            0.0,
        )
        for letter in ENGLISH_LETTER_FREQUENCIES
    }


def frequency_difference(
    text: str,
) -> dict[str, float]:
    # Calculates observed minus expected frequency for every letter

    observed = observed_letter_percentages(
        text
    )

    expected = expected_frequencies()

    return {
        letter: (
            observed[letter]
            - expected[letter]
        )
        for letter in expected
    }


def absolute_frequency_difference(
    text: str,
) -> dict[str, float]:
    # Calculates the absolute difference between observed
    # and expected English frequencies

    differences = frequency_difference(
        text
    )

    return {
        letter: abs(
            difference
        )
        for letter, difference
        in differences.items()
    }


def total_frequency_error(
    text: str,
) -> float:
    # Calculates the total absolute frequency error

    differences = absolute_frequency_difference(
        text
    )

    return sum(
        differences.values()
    )


# Frequency Distance


def frequency_distance(
    text: str,
) -> float:
    # Calculates the root mean squared frequency distance
    # between a text and the expected English distribution

    observed = observed_letter_percentages(
        text
    )

    expected = expected_frequencies()

    squared_differences = [
        (
            observed[letter]
            - expected[letter]
        ) ** 2
        for letter in expected
    ]

    if not squared_differences:
        return 0.0

    return (
        sum(
            squared_differences
        )
        / len(
            squared_differences
        )
    ) ** 0.5


def frequency_similarity(
    text: str,
) -> float:
    # Converts frequency distance into a simple similarity score

    distance = frequency_distance(
        text
    )

    return 1.0 / (
        1.0 + distance
    )


# Letter Mapping


def frequency_mapping(
    text: str,
) -> dict[str, str]:
    # Maps observed letters to English letters
    # according to their frequency rankings

    observed = rank_letters(
        text
    )

    expected = sorted(
        ENGLISH_LETTER_FREQUENCIES.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    mapping = {}

    for index, (
        observed_letter,
        _,
    ) in enumerate(
        observed
    ):

        if index >= len(
            expected
        ):
            break

        expected_letter = expected[
            index
        ][0]

        mapping[
            observed_letter
        ] = expected_letter

    return mapping


def apply_frequency_mapping(
    text: str,
    mapping: dict[str, str],
) -> str:
    # Applies a letter substitution mapping to a text

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    if not isinstance(
        mapping,
        dict,
    ):
        raise TypeError(
            "Mapping must be a dictionary."
        )

    result = []

    for character in text:

        upper = character.upper()

        if upper in mapping:

            transformed = mapping[
                upper
            ]

            if character.islower():
                transformed = transformed.lower()

            result.append(
                transformed
            )

        else:
            result.append(
                character
            )

    return "".join(
        result
    )


# Frequency Analysis


def analyze_letter(
    text: str,
    letter: str,
) -> dict[str, float]:
    # Returns observed and expected frequency information for one letter

    if not isinstance(
        letter,
        str,
    ):
        raise TypeError(
            "Letter must be a string."
        )

    if len(
        letter
    ) != 1:
        raise ValueError(
            "Letter must contain exactly one character."
        )

    normalized = letter.upper()

    if normalized not in ENGLISH_LETTER_FREQUENCIES:
        raise ValueError(
            "Letter must be an English alphabet character."
        )

    observed = observed_letter_percentages(
        text
    )

    expected = ENGLISH_LETTER_FREQUENCIES[
        normalized
    ]

    actual = observed.get(
        normalized,
        0.0,
    )

    return {
        "letter": normalized,
        "observed": actual,
        "expected": expected,
        "difference": actual - expected,
        "absolute_difference": abs(
            actual - expected
        ),
    } 

# Frequency Summary


def frequency_summary(
    text: str,
) -> dict:
    # Returns a complete frequency-analysis summary for a text

    letters = count_letters(
        text
    )

    percentages = observed_letter_percentages(
        text
    )

    ranked = rank_letters(
        text
    )

    return {
        "length": len(text),
        "letter_count": sum(
            letters.values()
        ),
        "unique_letters": len(
            letters
        ),
        "frequencies": letters,
        "percentages": percentages,
        "ranked": ranked,
        "most_common": most_common_letters(
            text
        ),
        "least_common": least_common_letters(
            text
        ),
        "frequency_distance": frequency_distance(
            text
        ),
        "frequency_similarity": frequency_similarity(
            text
        ),
        "total_frequency_error": total_frequency_error(
            text
        ),
    }


# Chi-Square Analysis


def chi_square_score(
    text: str,
) -> float:
    # Calculates a chi-square statistic comparing observed
    # letter frequencies against expected English frequencies

    observed = count_letters(
        text
    )

    total = sum(
        observed.values()
    )

    if total == 0:
        return 0.0

    score = 0.0

    for letter, expected_percentage in (
        ENGLISH_LETTER_FREQUENCIES.items()
    ):

        expected = (
            expected_percentage
            / 100
            * total
        )

        actual = observed.get(
            letter,
            0,
        )

        if expected > 0:
            score += (
                (
                    actual
                    - expected
                ) ** 2
            ) / expected

    return score


def chi_square_similarity(
    text: str,
) -> float:
    # Converts the chi-square score into a normalized similarity value

    score = chi_square_score(
        text
    )

    return 1.0 / (
        1.0 + score
    )


# Frequency Coincidence


def repeated_frequency_values(
    text: str,
) -> dict[int, list[str]]:
    # Groups letters that occur the same number of times

    frequencies = count_letters(
        text
    )

    groups = {}

    for letter, count in frequencies.items():

        groups.setdefault(
            count,
            [],
        ).append(
            letter
        )

    return {
        count: sorted(
            letters
        )
        for count, letters
        in groups.items()
    }


def frequency_concentration(
    text: str,
) -> float:
    # Measures how concentrated the letter distribution is

    frequencies = count_letters(
        text
    )

    total = sum(
        frequencies.values()
    )

    if total == 0:
        return 0.0

    squared = sum(
        (
            count / total
        ) ** 2
        for count
        in frequencies.values()
    )

    return squared


# Validation


def validate_frequency_input(
    text: str,
) -> bool:
    # Determines whether a value can be analyzed as text

    return isinstance(
        text,
        str,
    )


def validate_frequency_mapping(
    mapping: dict[str, str],
) -> bool:
    # Validates the basic structure of a frequency mapping

    if not isinstance(
        mapping,
        dict,
    ):
        return False

    for source, target in mapping.items():

        if not isinstance(
            source,
            str,
        ):
            return False

        if not isinstance(
            target,
            str,
        ):
            return False

        if len(source) != 1:
            return False

        if len(target) != 1:
            return False

    return True


# Self Test


def self_test() -> bool:
    # Runs a quick internal test of the frequency-analysis utilities

    text = (
        "THE QUICK BROWN FOX "
        "JUMPS OVER THE LAZY DOG"
    )

    if not validate_frequency_input(
        text
    ):
        return False

    letters = count_letters(
        text
    )

    if letters.get(
        "T",
        0,
    ) != 2:
        return False

    if sum(
        letters.values()
    ) != 35:
        return False

    percentages = letter_percentages(
        text
    )

    if round(
        sum(percentages.values()),
        5,
    ) != 100.0:
        return False

    ranked = rank_letters(
        text
    )

    if not ranked:
        return False

    mapping = frequency_mapping(
        text
    )

    if not validate_frequency_mapping(
        mapping
    ):
        return False

    mapped = apply_frequency_mapping(
        "ABC",
        {
            "A": "X",
            "B": "Y",
            "C": "Z",
        },
    )

    if mapped != "XYZ":
        return False

    analysis = analyze_letter(
        text,
        "E",
    )

    if "observed" not in analysis:
        return False

    summary = frequency_summary(
        text
    )

    if summary["letter_count"] != 35:
        return False

    if chi_square_score(
        text
    ) < 0:
        return False

    if not 0.0 <= frequency_concentration(
        text
    ) <= 1.0:
        return False

    return True


# Module Exports

__all__ = [
    "count_characters",
    "count_letters",
    "count_digits",
    "count_symbols",
    "character_percentages",
    "letter_percentages",
    "rank_characters",
    "rank_letters",
    "most_common_letters",
    "least_common_letters",
    "expected_frequencies",
    "observed_letter_percentages",
    "frequency_difference",
    "absolute_frequency_difference",
    "total_frequency_error",
    "frequency_distance",
    "frequency_similarity",
    "frequency_mapping",
    "apply_frequency_mapping",
    "analyze_letter",
    "frequency_summary",
    "chi_square_score",
    "chi_square_similarity",
    "repeated_frequency_values",
    "frequency_concentration",
    "validate_frequency_input",
    "validate_frequency_mapping",
    "self_test",
] 

