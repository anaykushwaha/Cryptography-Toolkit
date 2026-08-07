# keygen.py
# Secure key generation utilities for the Cryptography Toolkit

# Contains utilities for generating random Caesar keys,
# keywords, alphabets, and other cryptographic key material


from __future__ import annotations

import secrets
import string


# Constants

DEFAULT_KEY_LENGTH = 16
MIN_KEY_LENGTH = 4
MAX_KEY_LENGTH = 256

LOWERCASE_ALPHABET = string.ascii_lowercase
UPPERCASE_ALPHABET = string.ascii_uppercase
DIGITS = string.digits
ALPHANUMERIC = (
    UPPERCASE_ALPHABET
    + LOWERCASE_ALPHABET
    + DIGITS
)


# Key Validation

def validate_key_length(
    length: int,
    *,
    minimum: int = MIN_KEY_LENGTH,
    maximum: int = MAX_KEY_LENGTH,
) -> None:
    # Validates that a requested key length is within the allowed range

    if not isinstance(
        length,
        int,
    ):
        raise TypeError(
            "Key length must be an integer."
        )

    if length < minimum:
        raise ValueError(
            f"Key length must be at least {minimum}."
        )

    if length > maximum:
        raise ValueError(
            f"Key length cannot exceed {maximum}."
        )


# Caesar Key Generation

def generate_caesar_key(
    alphabet_size: int = 26,
) -> int:
    # Generates a cryptographically secure Caesar shift

    if not isinstance(
        alphabet_size,
        int,
    ):
        raise TypeError(
            "Alphabet size must be an integer."
        )

    if alphabet_size <= 1:
        raise ValueError(
            "Alphabet size must be greater than 1."
        )

    return secrets.randbelow(
        alphabet_size
    )


def generate_nonzero_caesar_key(
    alphabet_size: int = 26,
) -> int:
    # Generates a Caesar shift that is guaranteed to change the alphabet

    if not isinstance(
        alphabet_size,
        int,
    ):
        raise TypeError(
            "Alphabet size must be an integer."
        )

    if alphabet_size <= 1:
        raise ValueError(
            "Alphabet size must be greater than 1."
        )

    return secrets.randbelow(
        alphabet_size - 1
    ) + 1


# Random Character Generation

def generate_random_character(
    *,
    alphabet: str = ALPHANUMERIC,
) -> str:
    # Generates one cryptographically secure random character

    if not alphabet:
        raise ValueError(
            "Alphabet cannot be empty."
        )

    return secrets.choice(
        alphabet
    )


def generate_random_string(
    length: int = DEFAULT_KEY_LENGTH,
    *,
    alphabet: str = ALPHANUMERIC,
) -> str:
    # Generates a cryptographically secure random string

    validate_key_length(
        length
    )

    if not alphabet:
        raise ValueError(
            "Alphabet cannot be empty."
        )

    return "".join(
        secrets.choice(alphabet)
        for _ in range(length)
    )


# Random Keyword Generation

def generate_keyword(
    length: int = DEFAULT_KEY_LENGTH,
    *,
    alphabet: str = UPPERCASE_ALPHABET,
) -> str:
    # Generates a random keyword suitable for classical ciphers

    validate_key_length(
        length
    )

    if not alphabet:
        raise ValueError(
            "Alphabet cannot be empty."
        )

    return "".join(
        secrets.choice(alphabet)
        for _ in range(length)
    ) 

# Random Alphabet Generation

def generate_random_alphabet(
    *,
    alphabet: str = UPPERCASE_ALPHABET,
) -> str:
    # Generates a cryptographically secure randomized alphabet

    if not alphabet:
        raise ValueError(
            "Alphabet cannot be empty."
        )

    characters = list(
        alphabet
    )

    secrets.SystemRandom().shuffle(
        characters
    )

    return "".join(
        characters
    )


# Unique Keyword Generation

def generate_unique_keyword(
    length: int = DEFAULT_KEY_LENGTH,
    *,
    alphabet: str = UPPERCASE_ALPHABET,
) -> str:
    # Generates a keyword containing no repeated characters

    validate_key_length(
        length,
        minimum=1,
        maximum=len(alphabet),
    )

    if not alphabet:
        raise ValueError(
            "Alphabet cannot be empty."
        )

    if length > len(
        set(alphabet)
    ):
        raise ValueError(
            "Keyword length cannot exceed "
            "the number of unique characters "
            "in the alphabet."
        )

    available = list(
        dict.fromkeys(alphabet)
    )

    result = []

    for _ in range(length):

        index = secrets.randbelow(
            len(available)
        )

        result.append(
            available.pop(index)
        )

    return "".join(
        result
    )


# Substitution Alphabet Generation

def generate_substitution_alphabet(
    *,
    alphabet: str = UPPERCASE_ALPHABET,
) -> str:
    # Generates a random substitution alphabet

    if not alphabet:
        raise ValueError(
            "Alphabet cannot be empty."
        )

    if len(alphabet) != len(
        set(alphabet)
    ):
        raise ValueError(
            "Alphabet must contain unique characters."
        )

    return generate_random_alphabet(
        alphabet=alphabet
    )


# Keyword Alphabet Generation

def generate_keyword_alphabet(
    keyword: str,
    *,
    alphabet: str = UPPERCASE_ALPHABET,
) -> str:
    # Creates a keyed alphabet by placing the keyword
    # before the remaining unused alphabet characters

    if not keyword:
        raise ValueError(
            "Keyword cannot be empty."
        )

    if not alphabet:
        raise ValueError(
            "Alphabet cannot be empty."
        )

    normalized_keyword = []

    for character in keyword:

        if character not in alphabet:
            raise ValueError(
                f"Character {character!r} "
                "is not present in the alphabet."
            )

        if character not in normalized_keyword:
            normalized_keyword.append(
                character
            )

    remaining = [
        character
        for character in alphabet
        if character not in normalized_keyword
    ]

    return "".join(
        normalized_keyword
        + remaining
    )


# Key Validation

def validate_caesar_key(
    key: int,
    alphabet_size: int = 26,
) -> bool:
    # Determines whether a Caesar key is valid

    if not isinstance(
        key,
        int,
    ):
        return False

    if not isinstance(
        alphabet_size,
        int,
    ):
        return False

    if alphabet_size <= 1:
        return False

    return 0 <= key < alphabet_size


def validate_keyword(
    keyword: str,
    *,
    alphabet: str = UPPERCASE_ALPHABET,
) -> bool:
    # Determines whether every keyword character
    # belongs to the supplied alphabet

    if not isinstance(
        keyword,
        str,
    ):
        return False

    if not keyword:
        return False

    return all(
        character in alphabet
        for character in keyword
    )


# Key Strength

def estimate_key_strength(
    key: str,
) -> str:
    # Provides a simple estimate of random key strength
    # This is not a formal cryptographic security measurement

    if not isinstance(
        key,
        str,
    ):
        raise TypeError(
            "Key must be a string."
        )

    if not key:
        return "Very Weak"

    length = len(
        key
    )

    character_sets = 0

    if any(
        character.islower()
        for character in key
    ):
        character_sets += 1

    if any(
        character.isupper()
        for character in key
    ):
        character_sets += 1

    if any(
        character.isdigit()
        for character in key
    ):
        character_sets += 1

    if any(
        not character.isalnum()
        for character in key
    ):
        character_sets += 1

    score = length + (
        character_sets * 5
    )

    if score < 10:
        return "Very Weak"

    if score < 18:
        return "Weak"

    if score < 28:
        return "Moderate"

    if score < 40:
        return "Strong"

    return "Very Strong" 

# Key Entropy

def estimate_key_entropy(
    key: str,
    *,
    alphabet_size: int | None = None,
) -> float:
    # Estimates the theoretical entropy of a uniformly random key

    if not isinstance(
        key,
        str,
    ):
        raise TypeError(
            "Key must be a string."
        )

    if not key:
        return 0.0

    if alphabet_size is None:
        alphabet_size = len(
            set(key)
        )

    if alphabet_size <= 1:
        return 0.0

    import math

    return len(key) * math.log2(
        alphabet_size
    )


# Key Normalization

def normalize_key(
    key: str,
    *,
    alphabet: str = UPPERCASE_ALPHABET,
) -> str:
    # Normalizes a key by removing characters
    # that are not present in the supplied alphabet

    if not isinstance(
        key,
        str,
    ):
        raise TypeError(
            "Key must be a string."
        )

    if not alphabet:
        raise ValueError(
            "Alphabet cannot be empty."
        )

    normalized = []

    for character in key.upper():

        if character in alphabet:
            normalized.append(
                character
            )

    return "".join(
        normalized
    )


# Random Caesar Key

def generate_random_caesar_key(
    alphabet_size: int = 26,
) -> int:
    # Alias for generate_caesar_key()
    # Provides a descriptive name for external callers

    return generate_caesar_key(
        alphabet_size
    )


# Random Substitution Key

def generate_random_substitution_key(
    *,
    alphabet: str = UPPERCASE_ALPHABET,
) -> dict[str, str]:
    # Generates a random one-to-one substitution mapping

    if not alphabet:
        raise ValueError(
            "Alphabet cannot be empty."
        )

    if len(alphabet) != len(
        set(alphabet)
    ):
        raise ValueError(
            "Alphabet must contain unique characters."
        )

    shuffled = generate_random_alphabet(
        alphabet=alphabet
    )

    return dict(
        zip(
            alphabet,
            shuffled,
        )
    )


# Key Information

def key_information(
    key: str,
) -> dict:
    # Returns useful information about a generated key

    if not isinstance(
        key,
        str,
    ):
        raise TypeError(
            "Key must be a string."
        )

    return {
        "key": key,
        "length": len(key),
        "unique_characters": len(
            set(key)
        ),
        "strength": estimate_key_strength(
            key
        ),
        "entropy_bits": estimate_key_entropy(
            key
        ),
        "has_lowercase": any(
            character.islower()
            for character in key
        ),
        "has_uppercase": any(
            character.isupper()
            for character in key
        ),
        "has_digits": any(
            character.isdigit()
            for character in key
        ),
        "has_symbols": any(
            not character.isalnum()
            for character in key
        ),
    }


# Self Test

def self_test() -> bool:
    # Runs a quick internal test of the key generation utilities

    caesar_key = generate_caesar_key()

    if not validate_caesar_key(
        caesar_key
    ):
        return False

    keyword = generate_unique_keyword(
        8
    )

    if not validate_keyword(
        keyword
    ):
        return False

    random_string = generate_random_string(
        16
    )

    if len(random_string) != 16:
        return False

    substitution = generate_random_substitution_key()

    if len(substitution) != 26:
        return False

    if len(
        set(substitution.values())
    ) != 26:
        return False

    keyed_alphabet = generate_keyword_alphabet(
        "CRYPTO"
    )

    if len(keyed_alphabet) != 26:
        return False

    if len(
        set(keyed_alphabet)
    ) != 26:
        return False

    return True


# Module Exports

__all__ = [
    "DEFAULT_KEY_LENGTH",
    "MIN_KEY_LENGTH",
    "MAX_KEY_LENGTH",
    "LOWERCASE_ALPHABET",
    "UPPERCASE_ALPHABET",
    "DIGITS",
    "ALPHANUMERIC",
    "validate_key_length",
    "generate_caesar_key",
    "generate_nonzero_caesar_key",
    "generate_random_character",
    "generate_random_string",
    "generate_keyword",
    "generate_random_alphabet",
    "generate_unique_keyword",
    "generate_substitution_alphabet",
    "generate_keyword_alphabet",
    "validate_caesar_key",
    "validate_keyword",
    "estimate_key_strength",
    "estimate_key_entropy",
    "normalize_key",
    "generate_random_caesar_key",
    "generate_random_substitution_key",
    "key_information",
    "self_test",
] 

