# brute_force.py
# Brute-force cryptanalysis utilities for the Cryptography Toolkit

# Contains functions for generating possible Caesar cipher
# decryptions, evaluating candidates, and identifying the
# most likely plaintext


from __future__ import annotations
from .scorer import (
    english_score,
    rank_candidates,
)
from cipher.caesar import (
    decrypt,
)

# Candidate Generation

def generate_candidates(
    text: str,
    *,
    minimum_shift: int = 0,
    maximum_shift: int = 25,
) -> list[dict]:
    # Generates every Caesar-shift candidate within a supplied range

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    if not isinstance(
        minimum_shift,
        int,
    ):
        raise TypeError(
            "Minimum shift must be an integer."
        )

    if not isinstance(
        maximum_shift,
        int,
    ):
        raise TypeError(
            "Maximum shift must be an integer."
        )

    if minimum_shift < 0:
        raise ValueError(
            "Minimum shift cannot be negative."
        )

    if maximum_shift > 25:
        raise ValueError(
            "Maximum shift cannot be greater than 25."
        )

    if minimum_shift > maximum_shift:
        raise ValueError(
            "Minimum shift cannot be greater than maximum shift."
        )

    candidates = []

    for shift in range(
        minimum_shift,
        maximum_shift + 1,
    ):

        plaintext = decrypt(
            text,
            shift=shift,
        )

        candidates.append(
            {
                "shift": shift,
                "text": plaintext,
                "score": english_score(
                    plaintext
                ),
            }
        )

    return candidates


def generate_all_candidates(
    text: str,
) -> list[dict]:
    # Generates all 26 possible Caesar decryptions

    return generate_candidates(
        text,
        minimum_shift=0,
        maximum_shift=25,
    )


# Candidate Ranking


def rank_brute_force_candidates(
    text: str,
) -> list[dict]:
    # Generates and ranks every Caesar candidate by English score

    candidates = generate_all_candidates(
        text
    )

    return sorted(
        candidates,
        key=lambda candidate: candidate["score"],
        reverse=True,
    )


def best_brute_force_candidate(
    text: str,
) -> dict | None:
    # Returns the highest-scoring Caesar decryption candidate

    candidates = rank_brute_force_candidates(
        text
    )

    if not candidates:
        return None

    return candidates[0]


# Shift Testing


def test_shift(
    text: str,
    shift: int,
) -> dict:
    # Decrypts text using one shift and evaluates the result

    if not isinstance(
        shift,
        int,
    ):
        raise TypeError(
            "Shift must be an integer."
        )

    if not 0 <= shift <= 25:
        raise ValueError(
            "Shift must be between 0 and 25."
        )

    plaintext = decrypt(
        text,
        shift=shift,
    )

    return {
        "shift": shift,
        "text": plaintext,
        "score": english_score(
            plaintext
        ),
    }


def score_shift(
    text: str,
    shift: int,
) -> float:
    # Returns only the English score for a supplied shift

    result = test_shift(
        text,
        shift,
    )

    return result["score"] 

# Candidate Filtering


def filter_candidates(
    candidates: list[dict],
    minimum_score: float = 0.0,
) -> list[dict]:
    # Filters candidates using a minimum English score

    if not isinstance(
        candidates,
        list,
    ):
        raise TypeError(
            "Candidates must be a list."
        )

    if not isinstance(
        minimum_score,
        (int, float),
    ):
        raise TypeError(
            "Minimum score must be numeric."
        )

    return [
        candidate
        for candidate in candidates
        if candidate["score"] >= minimum_score
    ]


def top_candidates(
    text: str,
    count: int = 5,
) -> list[dict]:
    # Returns the strongest brute-force candidates

    if not isinstance(
        count,
        int,
    ):
        raise TypeError(
            "Count must be an integer."
        )

    if count <= 0:
        return []

    candidates = rank_brute_force_candidates(
        text
    )

    return candidates[
        :count
    ]


def candidate_at_rank(
    text: str,
    rank: int,
) -> dict | None:
    # Returns a brute-force candidate at a specific rank

    if not isinstance(
        rank,
        int,
    ):
        raise TypeError(
            "Rank must be an integer."
        )

    if rank <= 0:
        raise ValueError(
            "Rank must be greater than zero."
        )

    candidates = rank_brute_force_candidates(
        text
    )

    index = rank - 1

    if index >= len(
        candidates
    ):
        return None

    return candidates[
        index
    ]


# Batch Analysis


def brute_force(
    text: str,
) -> list[dict]:
    # Performs a complete brute-force Caesar analysis

    return rank_brute_force_candidates(
        text
    )


def brute_force_best(
    text: str,
) -> str | None:
    # Returns only the most likely plaintext

    candidate = best_brute_force_candidate(
        text
    )

    if candidate is None:
        return None

    return candidate["text"]


def brute_force_shift(
    text: str,
) -> int | None:
    # Returns the most likely Caesar shift

    candidate = best_brute_force_candidate(
        text
    )

    if candidate is None:
        return None

    return candidate["shift"]


def analyze_shifts(
    text: str,
) -> dict[int, float]:
    # Returns the English score for every possible Caesar shift

    candidates = generate_all_candidates(
        text
    )

    return {
        candidate["shift"]: candidate["score"]
        for candidate in candidates
    }


# Candidate Comparison


def compare_shifts(
    text: str,
    first_shift: int,
    second_shift: int,
) -> dict:
    # Compares two Caesar shift candidates

    first = test_shift(
        text,
        first_shift,
    )

    second = test_shift(
        text,
        second_shift,
    )

    return {
        "first": first,
        "second": second,
        "difference": abs(
            first["score"]
            - second["score"]
        ),
        "better_shift": (
            first["shift"]
            if first["score"] >= second["score"]
            else second["shift"]
        ),
    }


def confidence_score(
    text: str,
) -> float:
    # Estimates confidence in the strongest brute-force candidate
    # based on the separation between the top two candidates

    candidates = rank_brute_force_candidates(
        text
    )

    if not candidates:
        return 0.0

    if len(
        candidates
    ) == 1:
        return 1.0

    best = candidates[0]["score"]
    second = candidates[1]["score"]

    difference = max(
        0.0,
        best - second,
    )

    return min(
        1.0,
        difference,
    )

# Analysis Summary


def brute_force_summary(
    text: str,
) -> dict:
    # Returns a complete summary of the brute-force analysis

    candidates = rank_brute_force_candidates(
        text
    )

    best = (
        candidates[0]
        if candidates
        else None
    )

    return {
        "input": text,
        "candidate_count": len(
            candidates
        ),
        "best_shift": (
            best["shift"]
            if best is not None
            else None
        ),
        "best_plaintext": (
            best["text"]
            if best is not None
            else None
        ),
        "best_score": (
            best["score"]
            if best is not None
            else 0.0
        ),
        "confidence": confidence_score(
            text
        ),
        "candidates": candidates,
    }


def analyze_candidate(
    candidate: dict,
) -> dict:
    # Returns a normalized analysis of a single candidate

    if not isinstance(
        candidate,
        dict,
    ):
        raise TypeError(
            "Candidate must be a dictionary."
        )

    required = {
        "shift",
        "text",
        "score",
    }

    if not required.issubset(
        candidate
    ):
        raise ValueError(
            "Candidate is missing required fields."
        )

    return {
        "shift": candidate["shift"],
        "text": candidate["text"],
        "score": candidate["score"],
        "is_valid": validate_candidate(
            candidate
        ),
    }


# Validation


def validate_candidate(
    candidate: dict,
) -> bool:
    # Determines whether a brute-force candidate has a valid structure

    if not isinstance(
        candidate,
        dict,
    ):
        return False

    required = {
        "shift",
        "text",
        "score",
    }

    if not required.issubset(
        candidate
    ):
        return False

    if not isinstance(
        candidate["shift"],
        int,
    ):
        return False

    if not 0 <= candidate["shift"] <= 25:
        return False

    if not isinstance(
        candidate["text"],
        str,
    ):
        return False

    if not isinstance(
        candidate["score"],
        (int, float),
    ):
        return False

    return True


def validate_shift(
    shift: int,
) -> bool:
    # Determines whether a Caesar shift is valid

    return (
        isinstance(
            shift,
            int,
        )
        and 0 <= shift <= 25
    )


# Self Test


def self_test() -> bool:
    # Runs a quick internal test of the brute-force utilities

    encrypted = (
        "KHOOR ZRUOG"
    )

    if not validate_shift(
        3
    ):
        return False

    if validate_shift(
        26
    ):
        return False

    candidates = generate_all_candidates(
        encrypted
    )

    if len(
        candidates
    ) != 26:
        return False

    for candidate in candidates:

        if not validate_candidate(
            candidate
        ):
            return False

    result = test_shift(
        encrypted,
        3,
    )

    if result["text"] != "HELLO WORLD":
        return False

    score = score_shift(
        encrypted,
        3,
    )

    if score < 0:
        return False

    ranked = rank_brute_force_candidates(
        encrypted
    )

    if len(
        ranked
    ) != 26:
        return False

    best = best_brute_force_candidate(
        encrypted
    )

    if best is None:
        return False

    top = top_candidates(
        encrypted,
        5,
    )

    if len(
        top
    ) != 5:
        return False

    filtered = filter_candidates(
        candidates,
        minimum_score=0.0,
    )

    if len(
        filtered
    ) != 26:
        return False

    analysis = analyze_shifts(
        encrypted
    )

    if len(
        analysis
    ) != 26:
        return False

    summary = brute_force_summary(
        encrypted
    )

    if "best_shift" not in summary:
        return False

    candidate_analysis = analyze_candidate(
        best
    )

    if not candidate_analysis["is_valid"]:
        return False

    return True


# Module Exports

__all__ = [
    "generate_candidates",
    "generate_all_candidates",
    "rank_brute_force_candidates",
    "best_brute_force_candidate",
    "test_shift",
    "score_shift",
    "filter_candidates",
    "top_candidates",
    "candidate_at_rank",
    "brute_force",
    "brute_force_best",
    "brute_force_shift",
    "analyze_shifts",
    "compare_shifts",
    "confidence_score",
    "brute_force_summary",
    "analyze_candidate",
    "validate_candidate",
    "validate_shift",
    "self_test",
] 

