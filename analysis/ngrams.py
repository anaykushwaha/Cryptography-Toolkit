# ngrams.py
# N-gram analysis utilities for the Cryptography Toolkit

# Contains functions for generating, counting, ranking,
# and analyzing character n-grams for cryptanalysis


from __future__ import annotations

from collections import Counter


# N-Gram Generation


def generate_ngrams(
    text: str,
    n: int,
) -> list[str]:
    # Generates consecutive n-character sequences from text

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    if not isinstance(
        n,
        int,
    ):
        raise TypeError(
            "N must be an integer."
        )

    if n <= 0:
        raise ValueError(
            "N must be greater than zero."
        )

    if len(text) < n:
        return []

    return [
        text[index:index + n]
        for index in range(
            len(text) - n + 1
        )
    ]


def generate_bigrams(
    text: str,
) -> list[str]:
    # Generates two-character sequences from text

    return generate_ngrams(
        text,
        2,
    )


def generate_trigrams(
    text: str,
) -> list[str]:
    # Generates three-character sequences from text

    return generate_ngrams(
        text,
        3,
    )


def generate_quadgrams(
    text: str,
) -> list[str]:
    # Generates four-character sequences from text

    return generate_ngrams(
        text,
        4,
    )


# N-Gram Counting


def count_ngrams(
    text: str,
    n: int,
) -> dict[str, int]:
    # Counts occurrences of every n-gram in a text

    ngrams = generate_ngrams(
        text,
        n,
    )

    return dict(
        Counter(
            ngrams
        )
    )


def count_bigrams(
    text: str,
) -> dict[str, int]:
    # Counts occurrences of every bigram

    return count_ngrams(
        text,
        2,
    )


def count_trigrams(
    text: str,
) -> dict[str, int]:
    # Counts occurrences of every trigram

    return count_ngrams(
        text,
        3,
    )


def count_quadgrams(
    text: str,
) -> dict[str, int]:
    # Counts occurrences of every quadgram

    return count_ngrams(
        text,
        4,
    )


# N-Gram Percentages


def ngram_percentages(
    text: str,
    n: int,
) -> dict[str, float]:
    # Calculates the percentage of each n-gram in a text

    frequencies = count_ngrams(
        text,
        n,
    )

    total = sum(
        frequencies.values()
    )

    if total == 0:
        return {}

    return {
        ngram: (
            count / total
        ) * 100
        for ngram, count
        in frequencies.items()
    }


def bigram_percentages(
    text: str,
) -> dict[str, float]:
    # Calculates bigram percentages

    return ngram_percentages(
        text,
        2,
    )


def trigram_percentages(
    text: str,
) -> dict[str, float]:
    # Calculates trigram percentages

    return ngram_percentages(
        text,
        3,
    )


def quadgram_percentages(
    text: str,
) -> dict[str, float]:
    # Calculates quadgram percentages

    return ngram_percentages(
        text,
        4,
    )


# N-Gram Ranking


def rank_ngrams(
    text: str,
    n: int,
) -> list[tuple[str, int]]:
    # Returns n-grams ordered from most frequent to least frequent

    frequencies = count_ngrams(
        text,
        n,
    )

    return sorted(
        frequencies.items(),
        key=lambda item: item[1],
        reverse=True,
    )


def rank_bigrams(
    text: str,
) -> list[tuple[str, int]]:
    # Returns bigrams ordered by frequency

    return rank_ngrams(
        text,
        2,
    )


def rank_trigrams(
    text: str,
) -> list[tuple[str, int]]:
    # Returns trigrams ordered by frequency

    return rank_ngrams(
        text,
        3,
    )


def rank_quadgrams(
    text: str,
) -> list[tuple[str, int]]:
    # Returns quadgrams ordered by frequency

    return rank_ngrams(
        text,
        4,
    ) 

# English N-Gram Comparison


def common_ngrams(
    text: str,
    n: int,
    minimum_count: int = 2,
) -> list[tuple[str, int]]:
    # Returns n-grams that occur at least the requested number of times

    if not isinstance(
        minimum_count,
        int,
    ):
        raise TypeError(
            "Minimum count must be an integer."
        )

    if minimum_count <= 0:
        raise ValueError(
            "Minimum count must be greater than zero."
        )

    ranked = rank_ngrams(
        text,
        n,
    )

    return [
        (
            ngram,
            count,
        )
        for ngram, count
        in ranked
        if count >= minimum_count
    ]


def unique_ngrams(
    text: str,
    n: int,
) -> set[str]:
    # Returns every unique n-gram appearing in a text

    return set(
        generate_ngrams(
            text,
            n,
        )
    )


def ngram_diversity(
    text: str,
    n: int,
) -> float:
    # Calculates the ratio of unique n-grams to total n-grams

    generated = generate_ngrams(
        text,
        n,
    )

    if not generated:
        return 0.0

    return (
        len(
            set(generated)
        )
        / len(generated)
    )


# Pattern Detection


def contains_ngram(
    text: str,
    ngram: str,
) -> bool:
    # Determines whether a specific n-gram appears in a text

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    if not isinstance(
        ngram,
        str,
    ):
        raise TypeError(
            "N-gram must be a string."
        )

    if not ngram:
        return False

    return ngram in text


def count_ngram(
    text: str,
    ngram: str,
) -> int:
    # Counts occurrences of a specific n-gram

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    if not isinstance(
        ngram,
        str,
    ):
        raise TypeError(
            "N-gram must be a string."
        )

    if not ngram:
        return 0

    return text.count(
        ngram
    )


def ngram_positions(
    text: str,
    ngram: str,
) -> list[int]:
    # Returns starting positions of a specific n-gram

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    if not isinstance(
        ngram,
        str,
    ):
        raise TypeError(
            "N-gram must be a string."
        )

    if not ngram:
        return []

    positions = []
    start = 0

    while True:

        position = text.find(
            ngram,
            start,
        )

        if position == -1:
            break

        positions.append(
            position
        )

        start = position + 1

    return positions


# N-Gram Scoring


def ngram_score(
    text: str,
    ngram: str,
) -> float:
    # Calculates how frequently an n-gram appears in a text

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    if not isinstance(
        ngram,
        str,
    ):
        raise TypeError(
            "N-gram must be a string."
        )

    if not ngram:
        return 0.0

    total = len(
        generate_ngrams(
            text,
            len(ngram),
        )
    )

    if total == 0:
        return 0.0

    return (
        count_ngram(
            text,
            ngram,
        )
        / total
    )


def repeated_ngram_score(
    text: str,
    n: int,
) -> float:
    # Measures how frequently n-grams repeat in a text

    generated = generate_ngrams(
        text,
        n,
    )

    if not generated:
        return 0.0

    frequencies = Counter(
        generated
    )

    repeated = sum(
        count
        for count in frequencies.values()
        if count > 1
    )

    return (
        repeated
        / len(generated)
    )


def top_ngrams(
    text: str,
    n: int,
    count: int = 10,
) -> list[tuple[str, int]]:
    # Returns the top n-grams in a text

    if not isinstance(
        count,
        int,
    ):
        raise TypeError(
            "Count must be an integer."
        )

    if count <= 0:
        return []

    return rank_ngrams(
        text,
        n,
    )[:count] 

# N-Gram Summary


def ngram_summary(
    text: str,
    n: int,
    top_count: int = 10,
) -> dict:
    # Returns a complete statistical summary of n-grams in a text

    if not isinstance(
        top_count,
        int,
    ):
        raise TypeError(
            "Top count must be an integer."
        )

    if top_count <= 0:
        raise ValueError(
            "Top count must be greater than zero."
        )

    generated = generate_ngrams(
        text,
        n,
    )

    frequencies = count_ngrams(
        text,
        n,
    )

    return {
        "n": n,
        "total": len(
            generated
        ),
        "unique": len(
            frequencies
        ),
        "diversity": ngram_diversity(
            text,
            n,
        ),
        "repeated_score": repeated_ngram_score(
            text,
            n,
        ),
        "top": top_ngrams(
            text,
            n,
            top_count,
        ),
    }


def bigram_summary(
    text: str,
    top_count: int = 10,
) -> dict:
    # Returns a summary of bigrams in a text

    return ngram_summary(
        text,
        2,
        top_count,
    )


def trigram_summary(
    text: str,
    top_count: int = 10,
) -> dict:
    # Returns a summary of trigrams in a text

    return ngram_summary(
        text,
        3,
        top_count,
    )


def quadgram_summary(
    text: str,
    top_count: int = 10,
) -> dict:
    # Returns a summary of quadgrams in a text

    return ngram_summary(
        text,
        4,
        top_count,
    )


# Pattern Comparison


def compare_ngram_sets(
    first: str,
    second: str,
    n: int,
) -> dict[str, float]:
    # Compares the unique n-grams found in two texts

    first_set = unique_ngrams(
        first,
        n,
    )

    second_set = unique_ngrams(
        second,
        n,
    )

    union = first_set | second_set
    intersection = first_set & second_set

    if not union:
        similarity = 0.0
    else:
        similarity = (
            len(intersection)
            / len(union)
        )

    return {
        "first_unique": len(
            first_set
        ),
        "second_unique": len(
            second_set
        ),
        "shared": len(
            intersection
        ),
        "union": len(
            union
        ),
        "similarity": similarity,
    }


def shared_ngrams(
    first: str,
    second: str,
    n: int,
) -> set[str]:
    # Returns n-grams shared by two texts

    return (
        unique_ngrams(
            first,
            n,
        )
        & unique_ngrams(
            second,
            n,
        )
    )


# Validation


def validate_n(
    n: int,
) -> bool:
    # Validates an n-gram size

    return (
        isinstance(
            n,
            int,
        )
        and n > 0
    )


def validate_ngram(
    value: str,
    n: int,
) -> bool:
    # Validates that a value is a valid n-gram of the requested size

    if not isinstance(
        value,
        str,
    ):
        return False

    if not validate_n(
        n
    ):
        return False

    return len(
        value
    ) == n


# Self Test


def self_test() -> bool:
    # Runs a quick internal test of the n-gram analysis utilities

    text = (
        "THE THE QUICK BROWN FOX"
    )

    if not validate_n(
        2
    ):
        return False

    if validate_n(
        0
    ):
        return False

    bigrams = generate_bigrams(
        text
    )

    if not bigrams:
        return False

    trigrams = generate_trigrams(
        text
    )

    if not trigrams:
        return False

    quadgrams = generate_quadgrams(
        text
    )

    if not quadgrams:
        return False

    if count_ngram(
        text,
        "THE",
    ) != 2:
        return False

    if not contains_ngram(
        text,
        "QUICK",
    ):
        return False

    positions = ngram_positions(
        text,
        "THE",
    )

    if len(
        positions
    ) != 2:
        return False

    if not validate_ngram(
        "THE",
        3,
    ):
        return False

    if validate_ngram(
        "THE",
        2,
    ):
        return False

    summary = bigram_summary(
        text
    )

    if summary["total"] != len(
        bigrams
    ):
        return False

    comparison = compare_ngram_sets(
        "THE CAT",
        "THE DOG",
        3,
    )

    if comparison["shared"] <= 0:
        return False

    if not isinstance(
        ngram_score(
            text,
            "THE",
        ),
        float,
    ):
        return False

    return True


# Module Exports

__all__ = [
    "generate_ngrams",
    "generate_bigrams",
    "generate_trigrams",
    "generate_quadgrams",
    "count_ngrams",
    "count_bigrams",
    "count_trigrams",
    "count_quadgrams",
    "ngram_percentages",
    "bigram_percentages",
    "trigram_percentages",
    "quadgram_percentages",
    "rank_ngrams",
    "rank_bigrams",
    "rank_trigrams",
    "rank_quadgrams",
    "common_ngrams",
    "unique_ngrams",
    "ngram_diversity",
    "contains_ngram",
    "count_ngram",
    "ngram_positions",
    "ngram_score",
    "repeated_ngram_score",
    "top_ngrams",
    "ngram_summary",
    "bigram_summary",
    "trigram_summary",
    "quadgram_summary",
    "compare_ngram_sets",
    "shared_ngrams",
    "validate_n",
    "validate_ngram",
    "self_test",
] 

