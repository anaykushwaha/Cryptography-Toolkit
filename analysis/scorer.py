# scorer.py
# Text scoring utilities for the Cryptography Toolkit

# Contains functions for scoring plaintext candidates,
# comparing text against English-language characteristics,
# and combining multiple cryptanalysis measurements


from __future__ import annotations

from .english_data import (
    ENGLISH_LETTER_FREQUENCIES,
)

from .frequency import (
    frequency_distance,
)

from .ngrams import (
    ngram_score,
)


# Basic Text Scoring


def letter_score(
    text: str,
) -> float:
    # Scores a text according to how closely its letter distribution
    # resembles the expected English letter distribution

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

    if not letters:
        return 0.0

    total = len(
        letters
    )

    frequencies = {}

    for letter in ENGLISH_LETTER_FREQUENCIES:
        frequencies[
            letter
        ] = 0

    for letter in letters:

        if letter in frequencies:
            frequencies[
                letter
            ] += 1

    score = 0.0

    for letter, expected in (
        ENGLISH_LETTER_FREQUENCIES.items()
    ):

        observed = (
            frequencies[
                letter
            ]
            / total
            * 100
        )

        difference = abs(
            observed
            - expected
        )

        score += difference

    return max(
        0.0,
        100.0
        - score,
    )


def frequency_score(
    text: str,
) -> float:
    # Converts frequency distance into a higher-is-better score

    distance = frequency_distance(
        text
    )

    return 1.0 / (
        1.0 + distance
    )


# Character Composition


def alphabetic_ratio(
    text: str,
) -> float:
    # Calculates the percentage of characters that are alphabetic

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    if not text:
        return 0.0

    alphabetic = sum(
        character.isalpha()
        for character in text
    )

    return (
        alphabetic
        / len(text)
    )


def space_ratio(
    text: str,
) -> float:
    # Calculates the percentage of characters that are whitespace

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    if not text:
        return 0.0

    spaces = sum(
        character.isspace()
        for character in text
    )

    return (
        spaces
        / len(text)
    )


def digit_ratio(
    text: str,
) -> float:
    # Calculates the percentage of characters that are digits

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    if not text:
        return 0.0

    digits = sum(
        character.isdigit()
        for character in text
    )

    return (
        digits
        / len(text)
    )


def symbol_ratio(
    text: str,
) -> float:
    # Calculates the percentage of characters that are symbols

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    if not text:
        return 0.0

    symbols = sum(
        not character.isalnum()
        and not character.isspace()
        for character in text
    )

    return (
        symbols
        / len(text)
    )


# N-Gram Scoring


def bigram_score(
    text: str,
    bigram: str,
) -> float:
    # Scores a text based on the frequency of a supplied bigram

    if len(
        bigram
    ) != 2:
        raise ValueError(
            "Bigram must contain exactly two characters."
        )

    return ngram_score(
        text,
        bigram,
    )


def trigram_score(
    text: str,
    trigram: str,
) -> float:
    # Scores a text based on the frequency of a supplied trigram

    if len(
        trigram
    ) != 3:
        raise ValueError(
            "Trigram must contain exactly three characters."
        )

    return ngram_score(
        text,
        trigram,
    ) 

# Combined Scoring


def composition_score(
    text: str,
) -> float:
    # Scores a text according to its character composition

    if not text:
        return 0.0

    alphabetic = alphabetic_ratio(
        text
    )

    spaces = space_ratio(
        text
    )

    digits = digit_ratio(
        text
    )

    symbols = symbol_ratio(
        text
    )

    score = (
        alphabetic * 0.70
        + spaces * 0.20
        + (
            1.0
            - digits
        ) * 0.05
        + (
            1.0
            - symbols
        ) * 0.05
    )

    return max(
        0.0,
        min(
            1.0,
            score,
        ),
    )


def english_score(
    text: str,
) -> float:
    # Produces a combined English-likeness score

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    if not text:
        return 0.0

    letter = letter_score(
        text
    ) / 100.0

    frequency = frequency_score(
        text
    )

    composition = composition_score(
        text
    )

    return (
        letter * 0.45
        + frequency * 0.35
        + composition * 0.20
    )


def weighted_score(
    text: str,
    *,
    letter_weight: float = 0.45,
    frequency_weight: float = 0.35,
    composition_weight: float = 0.20,
) -> float:
    # Calculates a customizable weighted plaintext score

    weights = (
        letter_weight,
        frequency_weight,
        composition_weight,
    )

    if any(
        weight < 0
        for weight in weights
    ):
        raise ValueError(
            "Weights cannot be negative."
        )

    total_weight = sum(
        weights
    )

    if total_weight == 0:
        raise ValueError(
            "At least one weight must be greater than zero."
        )

    return (
        (
            letter_score(
                text
            )
            / 100.0
            * letter_weight
        )
        + (
            frequency_score(
                text
            )
            * frequency_weight
        )
        + (
            composition_score(
                text
            )
            * composition_weight
        )
    ) / total_weight


# Candidate Comparison


def compare_texts(
    first: str,
    second: str,
) -> dict[str, float]:
    # Compares two plaintext candidates using the English score

    first_score = english_score(
        first
    )

    second_score = english_score(
        second
    )

    return {
        "first": first_score,
        "second": second_score,
        "difference": abs(
            first_score
            - second_score
        ),
    }


def better_candidate(
    first: str,
    second: str,
) -> str:
    # Returns the candidate with the stronger English score

    first_score = english_score(
        first
    )

    second_score = english_score(
        second
    )

    if first_score >= second_score:
        return first

    return second


def rank_candidates(
    candidates: list[str],
) -> list[tuple[str, float]]:
    # Ranks plaintext candidates from strongest to weakest

    if not isinstance(
        candidates,
        list,
    ):
        raise TypeError(
            "Candidates must be a list."
        )

    scored = [
        (
            candidate,
            english_score(
                candidate
            ),
        )
        for candidate in candidates
    ]

    return sorted(
        scored,
        key=lambda item: item[1],
        reverse=True,
    )


def best_candidate(
    candidates: list[str],
) -> str | None:
    # Returns the highest-scoring plaintext candidate

    ranked = rank_candidates(
        candidates
    )

    if not ranked:
        return None

    return ranked[0][0] 

# Scoring Summary


def scoring_summary(
    text: str,
) -> dict[str, float]:
    # Returns a complete breakdown of the text scoring metrics

    return {
        "letter_score": letter_score(
            text
        ),
        "frequency_score": frequency_score(
            text
        ),
        "composition_score": composition_score(
            text
        ),
        "english_score": english_score(
            text
        ),
        "alphabetic_ratio": alphabetic_ratio(
            text
        ),
        "space_ratio": space_ratio(
            text
        ),
        "digit_ratio": digit_ratio(
            text
        ),
        "symbol_ratio": symbol_ratio(
            text
        ),
    }


def score_candidate(
    text: str,
    *,
    letter_weight: float = 0.45,
    frequency_weight: float = 0.35,
    composition_weight: float = 0.20,
) -> dict[str, float]:
    # Scores a candidate and returns its individual
    # components alongside the final weighted score

    return {
        "letter_score": letter_score(
            text
        ),
        "frequency_score": frequency_score(
            text
        ),
        "composition_score": composition_score(
            text
        ),
        "weighted_score": weighted_score(
            text,
            letter_weight=letter_weight,
            frequency_weight=frequency_weight,
            composition_weight=composition_weight,
        ),
    }


# Batch Scoring


def score_candidates(
    candidates: list[str],
) -> list[dict[str, float | str]]:
    # Scores multiple plaintext candidates

    if not isinstance(
        candidates,
        list,
    ):
        raise TypeError(
            "Candidates must be a list."
        )

    return [
        {
            "text": candidate,
            "score": english_score(
                candidate
            ),
        }
        for candidate in candidates
    ]


def top_candidates(
    candidates: list[str],
    count: int = 5,
) -> list[tuple[str, float]]:
    # Returns the strongest plaintext candidates

    if not isinstance(
        count,
        int,
    ):
        raise TypeError(
            "Count must be an integer."
        )

    if count <= 0:
        return []

    return rank_candidates(
        candidates
    )[:count]


# Validation


def validate_weights(
    letter_weight: float,
    frequency_weight: float,
    composition_weight: float,
) -> bool:
    # Validates a set of scoring weights

    weights = (
        letter_weight,
        frequency_weight,
        composition_weight,
    )

    if any(
        not isinstance(
            weight,
            (int, float),
        )
        for weight
        in weights
    ):
        return False

    if any(
        weight < 0
        for weight
        in weights
    ):
        return False

    return sum(
        weights
    ) > 0


def validate_candidate(
    candidate: str,
) -> bool:
    # Determines whether a value can be scored as a candidate

    return isinstance(
        candidate,
        str,
    )


# Self Test


def self_test() -> bool:
    # Runs a quick internal test of the scoring utilities

    text = (
        "THE QUICK BROWN FOX "
        "JUMPS OVER THE LAZY DOG"
    )

    if not validate_candidate(
        text
    ):
        return False

    if not validate_weights(
        0.45,
        0.35,
        0.20,
    ):
        return False

    if validate_weights(
        -1.0,
        0.5,
        0.5,
    ):
        return False

    letter = letter_score(
        text
    )

    if letter < 0:
        return False

    frequency = frequency_score(
        text
    )

    if frequency < 0:
        return False

    composition = composition_score(
        text
    )

    if not 0.0 <= composition <= 1.0:
        return False

    english = english_score(
        text
    )

    if english < 0:
        return False

    weighted = weighted_score(
        text
    )

    if weighted < 0:
        return False

    summary = scoring_summary(
        text
    )

    if "english_score" not in summary:
        return False

    candidate_scores = score_candidates(
        [
            text,
            "ZZZZZZZZZZZZ",
        ]
    )

    if len(
        candidate_scores
    ) != 2:
        return False

    ranked = rank_candidates(
        [
            text,
            "ZZZZZZZZZZZZ",
        ]
    )

    if len(
        ranked
    ) != 2:
        return False

    best = best_candidate(
        [
            text,
            "ZZZZZZZZZZZZ",
        ]
    )

    if best is None:
        return False

    top = top_candidates(
        [
            text,
            "ZZZZZZZZZZZZ",
        ],
        1,
    )

    if len(
        top
    ) != 1:
        return False

    return True


# Module Exports

__all__ = [
    "letter_score",
    "frequency_score",
    "alphabetic_ratio",
    "space_ratio",
    "digit_ratio",
    "symbol_ratio",
    "bigram_score",
    "trigram_score",
    "composition_score",
    "english_score",
    "weighted_score",
    "compare_texts",
    "better_candidate",
    "rank_candidates",
    "best_candidate",
    "scoring_summary",
    "score_candidate",
    "score_candidates",
    "top_candidates",
    "validate_weights",
    "validate_candidate",
    "self_test",
] 

