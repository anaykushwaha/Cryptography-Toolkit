# english_data.py
# English language reference data for the Cryptography Toolkit

# Contains English letter frequencies, common letters,
# and reference values used by cryptanalysis modules


from __future__ import annotations


# English Letter Frequencies

ENGLISH_LETTER_FREQUENCIES = {
    "E": 12.70,
    "T": 9.06,
    "A": 8.17,
    "O": 7.51,
    "I": 6.97,
    "N": 6.75,
    "S": 6.33,
    "H": 6.09,
    "R": 5.99,
    "D": 4.25,
    "L": 4.03,
    "C": 2.78,
    "U": 2.76,
    "M": 2.41,
    "W": 2.36,
    "F": 2.23,
    "G": 2.02,
    "Y": 1.97,
    "P": 1.93,
    "B": 1.49,
    "V": 0.98,
    "K": 0.77,
    "J": 0.15,
    "X": 0.15,
    "Q": 0.10,
    "Z": 0.07,
}


# English Letter Probabilities

ENGLISH_LETTER_PROBABILITIES = {
    letter: frequency / 100
    for letter, frequency
    in ENGLISH_LETTER_FREQUENCIES.items()
}


# Common Letter Order

COMMON_LETTERS = (
    "ETAOINSHRDLCUMWFGYPBVKJXQZ"
)


RARE_LETTERS = (
    "QZXJ"
)


# Reference Values

EXPECTED_ENGLISH_IOC = 0.0667

RANDOM_IOC = 1 / 26

ENGLISH_ALPHABET_SIZE = 26


# Common English Patterns

COMMON_BIGRAMS = (
    "TH",
    "HE",
    "IN",
    "ER",
    "AN",
    "RE",
    "ON",
    "AT",
    "EN",
    "ND",
    "TI",
    "ES",
    "OR",
    "TE",
    "OF",
    "ED",
    "IS",
    "IT",
    "AL",
    "AR",
)


COMMON_TRIGRAMS = (
    "THE",
    "AND",
    "ING",
    "HER",
    "ERE",
    "ENT",
    "THA",
    "NTH",
    "WAS",
    "ETH",
    "FOR",
    "DTH",
    "HES",
    "VER",
    "HIS",
    "OFT",
    "STH",
    "OTH",
    "RES",
    "EST",
)


# Common English Words

COMMON_WORDS = (
    "THE",
    "BE",
    "TO",
    "OF",
    "AND",
    "A",
    "IN",
    "THAT",
    "HAVE",
    "I",
    "IT",
    "FOR",
    "NOT",
    "ON",
    "WITH",
    "HE",
    "AS",
    "YOU",
    "DO",
    "AT",
    "THIS",
    "BUT",
    "HIS",
    "BY",
    "FROM",
    "THEY",
    "WE",
    "SAY",
    "HER",
    "SHE",
    "OR",
    "AN",
    "WILL",
    "MY",
    "ONE",
    "ALL",
    "WOULD",
    "THERE",
    "THEIR",
)


# Module Information

DATA_SOURCE = (
    "Standard English language frequency references"
)

LANGUAGE = "English"

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 



# Data Lookup

def get_letter_frequency(
    letter: str,
) -> float:
    # Returns the expected English frequency of a letter

    if not isinstance(
        letter,
        str,
    ):
        raise TypeError(
            "Letter must be a string."
        )

    if len(letter) != 1:
        raise ValueError(
            "Letter must contain exactly one character."
        )

    return ENGLISH_LETTER_FREQUENCIES.get(
        letter.upper(),
        0.0,
    )


def get_letter_probability(
    letter: str,
) -> float:
    # Returns the expected English probability of a letter

    if not isinstance(
        letter,
        str,
    ):
        raise TypeError(
            "Letter must be a string."
        )

    if len(letter) != 1:
        raise ValueError(
            "Letter must contain exactly one character."
        )

    return ENGLISH_LETTER_PROBABILITIES.get(
        letter.upper(),
        0.0,
    )


def get_frequency_table() -> dict[str, float]:
    # Returns a copy of the English frequency table

    return ENGLISH_LETTER_FREQUENCIES.copy()


def get_probability_table() -> dict[str, float]:
    # Returns a copy of the English probability table

    return ENGLISH_LETTER_PROBABILITIES.copy()


# Pattern Lookup


def is_common_bigram(
    value: str,
) -> bool:
    # Determines whether a value is a common English bigram

    if not isinstance(
        value,
        str,
    ):
        return False

    return value.upper() in COMMON_BIGRAMS


def is_common_trigram(
    value: str,
) -> bool:
    # Determines whether a value is a common English trigram

    if not isinstance(
        value,
        str,
    ):
        return False

    return value.upper() in COMMON_TRIGRAMS


def is_common_word(
    word: str,
) -> bool:
    # Determines whether a word appears in the built-in common word list

    if not isinstance(
        word,
        str,
    ):
        return False

    return word.upper() in COMMON_WORDS


# Pattern Scores


def bigram_score(
    value: str,
) -> float:
    # Returns a simple score based on common English bigrams

    if not isinstance(
        value,
        str,
    ):
        raise TypeError(
            "Value must be a string."
        )

    normalized = value.upper()

    if len(normalized) != 2:
        raise ValueError(
            "Value must contain exactly two characters."
        )

    return (
        1.0
        if normalized in COMMON_BIGRAMS
        else 0.0
    )


def trigram_score(
    value: str,
) -> float:
    # Returns a simple score based on common English trigrams

    if not isinstance(
        value,
        str,
    ):
        raise TypeError(
            "Value must be a string."
        )

    normalized = value.upper()

    if len(normalized) != 3:
        raise ValueError(
            "Value must contain exactly three characters."
        )

    return (
        1.0
        if normalized in COMMON_TRIGRAMS
        else 0.0
    )


# Frequency Ranking


def ranked_letters() -> list[tuple[str, float]]:
    # Returns English letters ordered by expected frequency

    return sorted(
        ENGLISH_LETTER_FREQUENCIES.items(),
        key=lambda item: item[1],
        reverse=True,
    )


def most_common_letters(
    count: int = 5,
) -> tuple[str, ...]:
    # Returns the most common English letters

    if not isinstance(
        count,
        int,
    ):
        raise TypeError(
            "Count must be an integer."
        )

    if count <= 0:
        return ()

    return tuple(
        letter
        for letter, _ in ranked_letters()[:count]
    )


def least_common_letters(
    count: int = 5,
) -> tuple[str, ...]:
    # Returns the least common English letters

    if not isinstance(
        count,
        int,
    ):
        raise TypeError(
            "Count must be an integer."
        )

    if count <= 0:
        return ()

    return tuple(
        letter
        for letter, _ in ranked_letters()[-count:]
    )


# Word Extraction

def extract_words(
    text: str,
) -> list[str]:
    # Extracts alphabetic words from a text string

    if not isinstance(
        text,
        str,
    ):
        raise TypeError(
            "Text must be a string."
        )

    words = []
    current = []

    for character in text:

        if character.isalpha():
            current.append(
                character.upper()
            )

        elif current:
            words.append(
                "".join(current)
            )
            current = []

    if current:
        words.append(
            "".join(current)
        )

    return words


# Common Word Analysis


def count_common_words(
    text: str,
) -> int:
    # Counts how many words in a text are common English words

    words = extract_words(
        text
    )

    return sum(
        is_common_word(word)
        for word in words
    )


def common_word_ratio(
    text: str,
) -> float:
    # Calculates the proportion of words that are common English words

    words = extract_words(
        text
    )

    if not words:
        return 0.0

    return (
        count_common_words(text)
        / len(words)
    )


# Data Validation


def validate_frequency_data() -> bool:
    # Verifies that the English frequency data is internally consistent

    if len(
        ENGLISH_LETTER_FREQUENCIES
    ) != ENGLISH_ALPHABET_SIZE:
        return False

    if set(
        ENGLISH_LETTER_FREQUENCIES
    ) != set(
        ALPHABET
    ):
        return False

    total = sum(
        ENGLISH_LETTER_FREQUENCIES.values()
    )

    if not 99.0 <= total <= 101.0:
        return False

    for frequency in ENGLISH_LETTER_FREQUENCIES.values():

        if frequency < 0:
            return False

    return True


def validate_probability_data() -> bool:
    # Verifies that the English probability data is internally consistent

    if len(
        ENGLISH_LETTER_PROBABILITIES
    ) != ENGLISH_ALPHABET_SIZE:
        return False

    total = sum(
        ENGLISH_LETTER_PROBABILITIES.values()
    )

    if not 0.99 <= total <= 1.01:
        return False

    for probability in ENGLISH_LETTER_PROBABILITIES.values():

        if probability < 0:
            return False

    return True


# Data Summary


def data_summary() -> dict:
    # Returns information about the built-in English reference data

    return {
        "language": LANGUAGE,
        "alphabet": ALPHABET,
        "alphabet_size": ENGLISH_ALPHABET_SIZE,
        "frequency_entries": len(
            ENGLISH_LETTER_FREQUENCIES
        ),
        "common_bigrams": len(
            COMMON_BIGRAMS
        ),
        "common_trigrams": len(
            COMMON_TRIGRAMS
        ),
        "common_words": len(
            COMMON_WORDS
        ),
        "expected_ioc": EXPECTED_ENGLISH_IOC,
        "random_ioc": RANDOM_IOC,
        "data_source": DATA_SOURCE,
    }


# Self Test


def self_test() -> bool:
    # Runs a quick internal test of the English reference data

    if not validate_frequency_data():
        return False

    if not validate_probability_data():
        return False

    if get_letter_frequency(
        "E"
    ) != 12.70:
        return False

    if not is_common_bigram(
        "TH"
    ):
        return False

    if not is_common_trigram(
        "THE"
    ):
        return False

    if not is_common_word(
        "the"
    ):
        return False

    if extract_words(
        "The quick brown fox!"
    ) != [
        "THE",
        "QUICK",
        "BROWN",
        "FOX",
    ]:
        return False

    if count_common_words(
        "the cat is here"
    ) != 4:
        return False

    return True


# Module Exports

__all__ = [
    "ENGLISH_LETTER_FREQUENCIES",
    "ENGLISH_LETTER_PROBABILITIES",
    "COMMON_LETTERS",
    "RARE_LETTERS",
    "EXPECTED_ENGLISH_IOC",
    "RANDOM_IOC",
    "ENGLISH_ALPHABET_SIZE",
    "COMMON_BIGRAMS",
    "COMMON_TRIGRAMS",
    "COMMON_WORDS",
    "DATA_SOURCE",
    "LANGUAGE",
    "ALPHABET",
    "get_letter_frequency",
    "get_letter_probability",
    "get_frequency_table",
    "get_probability_table",
    "is_common_bigram",
    "is_common_trigram",
    "is_common_word",
    "bigram_score",
    "trigram_score",
    "ranked_letters",
    "most_common_letters",
    "least_common_letters",
    "extract_words",
    "count_common_words",
    "common_word_ratio",
    "validate_frequency_data",
    "validate_probability_data",
    "data_summary",
    "self_test",
] 

