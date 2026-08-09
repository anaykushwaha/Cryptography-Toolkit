# entropy.py
# Entropy analysis utilities for the Cryptography Toolkit

# Contains functions for calculating Shannon entropy,
# measuring randomness, and analyzing character distributions


from __future__ import annotations

from collections import Counter

from math import log2


# Basic Entropy


def calculate_entropy(
    text: str,
) -> float:
    # Calculates the Shannon entropy of a text

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    if not text:
        return 0.0

    frequencies = Counter(
        text
    )

    total = len(
        text
    )

    entropy = 0.0

    for count in frequencies.values():

        probability = (
            count
            / total
        )

        entropy -= (
            probability
            * log2(
                probability
            )
        )

    return entropy


def calculate_letter_entropy(
    text: str,
) -> float:
    # Calculates Shannon entropy using alphabetic characters only

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    letters = "".join(
        character.upper()
        for character in text
        if character.isalpha()
    )

    if not letters:
        return 0.0

    return calculate_entropy(
        letters
    )


def calculate_digit_entropy(
    text: str,
) -> float:
    # Calculates Shannon entropy using digits only

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    digits = "".join(
        character
        for character in text
        if character.isdigit()
    )

    if not digits:
        return 0.0

    return calculate_entropy(
        digits
    )


# Maximum Entropy


def maximum_entropy(
    alphabet_size: int,
) -> float:
    # Calculates the theoretical maximum entropy for an alphabet

    if not isinstance(
        alphabet_size,
        int,
    ):
        raise TypeError(
            "Alphabet size must be an integer."
        )

    if alphabet_size <= 0:
        raise ValueError(
            "Alphabet size must be greater than zero."
        )

    return log2(
        alphabet_size
    )


def normalized_entropy(
    text: str,
    *,
    alphabet_size: int | None = None,
) -> float:
    # Calculates entropy normalized against the maximum possible entropy

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    if not text:
        return 0.0

    if alphabet_size is None:
        alphabet_size = len(
            set(
                text
            )
        )

    if alphabet_size <= 1:
        return 0.0

    maximum = maximum_entropy(
        alphabet_size
    )

    if maximum == 0:
        return 0.0

    return calculate_entropy(
        text
    ) / maximum


# Character Entropy


def character_probabilities(
    text: str,
) -> dict[str, float]:
    # Returns the probability of every character in a text

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    if not text:
        return {}

    frequencies = Counter(
        text
    )

    total = len(
        text
    )

    return {
        character: (
            count
            / total
        )
        for character, count
        in frequencies.items()
    }


def character_entropy(
    text: str,
    character: str,
) -> float:
    # Returns the entropy contribution of a single character

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    if not isinstance(
        character,
        str,
    ):
        raise TypeError(
            "Character must be a string."
        )

    if len(
        character
    ) != 1:
        raise ValueError(
            "Character must contain exactly one character."
        )

    probabilities = character_probabilities(
        text
    )

    probability = probabilities.get(
        character,
        0.0,
    )

    if probability <= 0:
        return 0.0

    return -(
        probability
        * log2(
            probability
        )
    ) 

# Entropy Comparison


def entropy_difference(
    text: str,
    reference_entropy: float,
) -> float:
    # Calculates the absolute difference between text entropy
    # and a supplied reference entropy

    if not isinstance(
        reference_entropy,
        (int, float),
    ):
        raise TypeError(
            "Reference entropy must be numeric."
        )

    return abs(
        calculate_entropy(
            text
        )
        - reference_entropy
    )


def entropy_similarity(
    text: str,
    reference_entropy: float,
) -> float:
    # Converts entropy difference into a normalized similarity score

    difference = entropy_difference(
        text,
        reference_entropy,
    )

    maximum = max(
        reference_entropy,
        maximum_entropy(
            max(
                len(
                    set(
                        text
                    )
                ),
                1,
            )
        ),
    )

    if maximum == 0:
        return 1.0

    similarity = (
        1.0
        - (
            difference
            / maximum
        )
    )

    return max(
        0.0,
        min(
            1.0,
            similarity,
        ),
    )


# Randomness Estimation


def randomness_score(
    text: str,
) -> float:
    # Estimates how uniformly distributed the characters are
    # using normalized Shannon entropy

    if not text:
        return 0.0

    return normalized_entropy(
        text
    )


def is_high_entropy(
    text: str,
    threshold: float = 0.80,
) -> bool:
    # Determines whether a text has relatively high entropy

    if not 0.0 <= threshold <= 1.0:
        raise ValueError(
            "Threshold must be between 0 and 1."
        )

    return (
        randomness_score(
            text
        )
        >= threshold
    )


def is_low_entropy(
    text: str,
    threshold: float = 0.50,
) -> bool:
    # Determines whether a text has relatively low entropy

    if not 0.0 <= threshold <= 1.0:
        raise ValueError(
            "Threshold must be between 0 and 1."
        )

    return (
        randomness_score(
            text
        )
        <= threshold
    )


# Alphabet Analysis


def unique_character_count(
    text: str,
) -> int:
    # Returns the number of unique characters in a text

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    return len(
        set(
            text
        )
    )


def alphabet_utilization(
    text: str,
    alphabet_size: int,
) -> float:
    # Measures how much of a theoretical alphabet is represented

    if not isinstance(
        alphabet_size,
        int,
    ):
        raise TypeError(
            "Alphabet size must be an integer."
        )

    if alphabet_size <= 0:
        raise ValueError(
            "Alphabet size must be greater than zero."
        )

    if not text:
        return 0.0

    unique = unique_character_count(
        text
    )

    return min(
        1.0,
        unique
        / alphabet_size,
    )


def character_distribution(
    text: str,
) -> dict[str, float]:
    # Returns the probability distribution of characters

    return character_probabilities(
        text
    )


# Entropy Classification


def classify_entropy(
    text: str,
) -> str:
    # Classifies text according to its normalized entropy

    score = randomness_score(
        text
    )

    if not text:
        return "insufficient_data"

    if score >= 0.80:
        return "high_entropy"

    if score >= 0.50:
        return "moderate_entropy"

    return "low_entropy"


def entropy_range(
    text: str,
) -> dict[str, float]:
    # Returns the entropy and normalized entropy of a text

    entropy = calculate_entropy(
        text
    )

    normalized = normalized_entropy(
        text
    )

    return {
        "entropy": entropy,
        "normalized_entropy": normalized,
        "randomness_score": normalized,
    } 

# Block Entropy Analysis


def block_entropy(
    text: str,
    block_size: int,
) -> list[float]:
    # Calculates entropy for consecutive blocks of text

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    if not isinstance(
        block_size,
        int,
    ):
        raise TypeError(
            "Block size must be an integer."
        )

    if block_size <= 0:
        raise ValueError(
            "Block size must be greater than zero."
        )

    if not text:
        return []

    return [
        calculate_entropy(
            text[index:index + block_size]
        )
        for index in range(
            0,
            len(text),
            block_size,
        )
    ]


def sliding_entropy(
    text: str,
    window_size: int,
) -> list[float]:
    # Calculates entropy across overlapping sliding windows

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    if not isinstance(
        window_size,
        int,
    ):
        raise TypeError(
            "Window size must be an integer."
        )

    if window_size <= 0:
        raise ValueError(
            "Window size must be greater than zero."
        )

    if len(text) < window_size:
        return []

    return [
        calculate_entropy(
            text[index:index + window_size]
        )
        for index in range(
            len(text) - window_size + 1
        )
    ]


def average_entropy(
    text: str,
    block_size: int,
) -> float:
    # Calculates the average entropy across text blocks

    values = block_entropy(
        text,
        block_size,
    )

    if not values:
        return 0.0

    return sum(
        values
    ) / len(
        values
    )


# Entropy Summary


def entropy_summary(
    text: str,
) -> dict:
    # Returns a complete entropy analysis summary

    return {
        "length": len(text),
        "unique_characters": unique_character_count(
            text
        ),
        "entropy": calculate_entropy(
            text
        ),
        "normalized_entropy": normalized_entropy(
            text
        ),
        "randomness_score": randomness_score(
            text
        ),
        "classification": classify_entropy(
            text
        ),
        "alphabet_utilization": alphabet_utilization(
            text,
            max(
                len(
                    set(
                        text
                    )
                ),
                1,
            ),
        ),
    }


def compare_entropy(
    first: str,
    second: str,
) -> dict[str, float]:
    # Compares entropy measurements between two texts

    first_entropy = calculate_entropy(
        first
    )

    second_entropy = calculate_entropy(
        second
    )

    return {
        "first": first_entropy,
        "second": second_entropy,
        "difference": abs(
            first_entropy
            - second_entropy
        ),
        "first_normalized": normalized_entropy(
            first
        ),
        "second_normalized": normalized_entropy(
            second
        ),
    }


# Validation


def validate_entropy_input(
    text: str,
) -> bool:
    # Determines whether a value can be analyzed for entropy

    return isinstance(
        text,
        str,
    )


def validate_window_size(
    size: int,
) -> bool:
    # Validates a block or window size

    return (
        isinstance(
            size,
            int,
        )
        and size > 0
    )


# Self Test


def self_test() -> bool:
    # Runs a quick internal test of the entropy utilities

    text = (
        "THE QUICK BROWN FOX "
        "JUMPS OVER THE LAZY DOG"
    )

    if not validate_entropy_input(
        text
    ):
        return False

    if not validate_window_size(
        5
    ):
        return False

    if validate_window_size(
        0
    ):
        return False

    entropy = calculate_entropy(
        text
    )

    if entropy <= 0:
        return False

    letter_entropy = calculate_letter_entropy(
        text
    )

    if letter_entropy <= 0:
        return False

    digit_entropy = calculate_digit_entropy(
        "112233445566"
    )

    if digit_entropy <= 0:
        return False

    maximum = maximum_entropy(
        26
    )

    if maximum <= 0:
        return False

    normalized = normalized_entropy(
        text
    )

    if not 0.0 <= normalized <= 1.0:
        return False

    probabilities = character_probabilities(
        text
    )

    if not probabilities:
        return False

    contribution = character_entropy(
        text,
        "T",
    )

    if contribution < 0:
        return False

    blocks = block_entropy(
        text,
        5,
    )

    if not blocks:
        return False

    sliding = sliding_entropy(
        text,
        5,
    )

    if not sliding:
        return False

    average = average_entropy(
        text,
        5,
    )

    if average <= 0:
        return False

    summary = entropy_summary(
        text
    )

    if "entropy" not in summary:
        return False

    comparison = compare_entropy(
        text,
        "AAAAAAAAAAAA",
    )

    if "difference" not in comparison:
        return False

    return True


# Module Exports

__all__ = [
    "calculate_entropy",
    "calculate_letter_entropy",
    "calculate_digit_entropy",
    "maximum_entropy",
    "normalized_entropy",
    "character_probabilities",
    "character_entropy",
    "entropy_difference",
    "entropy_similarity",
    "randomness_score",
    "is_high_entropy",
    "is_low_entropy",
    "unique_character_count",
    "alphabet_utilization",
    "character_distribution",
    "classify_entropy",
    "entropy_range",
    "block_entropy",
    "sliding_entropy",
    "average_entropy",
    "entropy_summary",
    "compare_entropy",
    "validate_entropy_input",
    "validate_window_size",
    "self_test",
] 

