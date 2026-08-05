# caesar.py 
# Core Caesar Cipher Implementation 

# This module provides the primary encryption and decryption algorithms used 
# throughout the tooklikt 

# Features: 
# 1. Caesar Encryption & Decryption 
# 2. Custom alphabets 
# 3. Preserve case 
# 4. Strip non-alphabetic characters 
# 5. Shift normalization 
# 6. Full type hints 
# 7. Extensive Validation 

from __future__ import annotations
from typing import Iterable
from .alphabets import (
    DEFAULT_ALPHABET,
    validate_alphabet,
)

# Validation


def _validate_shift(shift: int) -> int: 
    # Validates and normalizes a shift 

    if not isinstance(shift, int):
        raise TypeError("Shift must be an integer.")
    return shift


def _validate_text(text: str) -> None: 
    # Validates text input 

    if not isinstance(text, str):
        raise TypeError("Text must be a string.")


def _validate_alphabet(alphabet: str) -> None: 
    # Validates alphabet 
    # Raises ValueError if alphabet contains duplicates / is empty 

    if not isinstance(alphabet, str):
        raise TypeError("Alphabet must be a string.")

    if not validate_alphabet(alphabet):
        raise ValueError(
            "Alphabet must contain unique characters."
        )


# Helper Functions

def normalize_shift(
    shift: int,
    alphabet: str = DEFAULT_ALPHABET,
) -> int: 
    # Normalizes a shift to the alphabet size 

    shift = _validate_shift(shift)
    return shift % len(alphabet)


def character_exists(
    character: str,
    alphabet: str = DEFAULT_ALPHABET,
) -> bool: 
    # Determines whether a character exists inside the chosen alphabet 

    return character.upper() in alphabet.upper()


def get_character_index(
    character: str,
    alphabet: str = DEFAULT_ALPHABET,
) -> int: 
    # Returns the index of a character inside the alphabet 

    return alphabet.upper().index(character.upper())


# Character Shifting

def shift_character(
    character: str,
    shift: int,
    alphabet: str = DEFAULT_ALPHABET,
    preserve_case: bool = True,
) -> str: 
    # Shifts a single character \

    if len(character) != 1:
        raise ValueError(
            "shift_character() expects exactly one character."
        )

    shift = normalize_shift(
        shift,
        alphabet,
    )

    alphabet_upper = alphabet.upper()
    upper = character.upper()

    if upper not in alphabet_upper:
        return character
    old_index = alphabet_upper.index(upper)

    new_index = (
        old_index + shift
    ) % len(alphabet_upper)

    new_character = alphabet_upper[new_index]

    if preserve_case:
        if character.islower():
            return new_character.lower()
    return new_character


# Core Caesar Engine


def caesar(
    text: str,
    shift: int,
    *,
    alphabet: str = DEFAULT_ALPHABET,
    preserve_case: bool = True,
    strip_non_alpha: bool = False,
) -> str: 
    # Applies a Caesar shift 
    # It is the master function used by encrypt() and decrypt() 

    _validate_text(text)

    _validate_alphabet(alphabet)

    shift = normalize_shift(
        shift,
        alphabet,
    )

    transformed: list[str] = []

    for character in text:
        if character_exists(
            character,
            alphabet,
        ):
            transformed.append(
                shift_character(
                    character,
                    shift,
                    alphabet,
                    preserve_case,
                )
            )
        else:
            if not strip_non_alpha:
                transformed.append(character)
    return "".join(transformed)


# Convenience Functions

def encrypt(
    text: str,
    shift: int,
    *,
    alphabet: str = DEFAULT_ALPHABET,
    preserve_case: bool = True,
    strip_non_alpha: bool = False,
) -> str: 
    # Encrypts plaintext using the Caesar Cipher 

    return caesar(
        text=text,
        shift=shift,
        alphabet=alphabet,
        preserve_case=preserve_case,
        strip_non_alpha=strip_non_alpha,
    )


def decrypt(
    text: str,
    shift: int,
    *,
    alphabet: str = DEFAULT_ALPHABET,
    preserve_case: bool = True,
    strip_non_alpha: bool = False,
) -> str: 
    # Decrypts Caesar Cipher text 

    return caesar(
        text=text,
        shift=-shift,
        alphabet=alphabet,
        preserve_case=preserve_case,
        strip_non_alpha=strip_non_alpha,
    )


# Batch Operations

def encrypt_many(
    texts: Iterable[str],
    shift: int,
    *,
    alphabet: str = DEFAULT_ALPHABET,
    preserve_case: bool = True,
) -> list[str]: 
    # Encrypts multiple strings 

    return [
        encrypt(
            text,
            shift,
            alphabet=alphabet,
            preserve_case=preserve_case,
        )
        for text in texts
    ]


def decrypt_many(
    texts: Iterable[str],
    shift: int,
    *,
    alphabet: str = DEFAULT_ALPHABET,
    preserve_case: bool = True,
) -> list[str]: 
    # Decrypts multiple strings 

    return [
        decrypt(
            text,
            shift,
            alphabet=alphabet,
            preserve_case=preserve_case,
        )
        for text in texts
    ]


# Generator Utilities

def caesar_generator(
    text: str,
    shift: int,
    *,
    alphabet: str = DEFAULT_ALPHABET,
    preserve_case: bool = True,
): 
    # Yields encrypted characters one at a time 
    # Useful for streaming very large files 

    _validate_text(text)
    _validate_alphabet(alphabet)
    shift = normalize_shift(
        shift,
        alphabet,
    )

    for character in text:
        if character_exists(
            character,
            alphabet,
        ):
            yield shift_character(
                character,
                shift,
                alphabet,
                preserve_case,
            )
        else:
            yield character


# Statistics

def count_shiftable_characters(
    text: str,
    alphabet: str = DEFAULT_ALPHABET,
) -> int: 
    # Counts how many characters belong to the selected alphabet 

    return sum(
        1
        for character in text
        if character_exists(
            character,
            alphabet,
        )
    )


def count_non_shiftable_characters(
    text: str,
    alphabet: str = DEFAULT_ALPHABET,
) -> int: 
    # Counts punctuation, spaces, digits and other characters 

    return len(text) - count_shiftable_characters(
        text,
        alphabet,
    )


# Information Utilities

def supported_alphabet(
    alphabet: str = DEFAULT_ALPHABET,
) -> bool: 
    # Determines whether an alphabet is valid 

    return validate_alphabet(alphabet)


def cipher_summary(
    text: str,
    shift: int,
    *,
    alphabet: str = DEFAULT_ALPHABET,
) -> dict: 
    # Returns information about an encryption operation 

    encrypted = encrypt(
        text,
        shift,
        alphabet=alphabet,
    )

    return {
        "original": text,
        "encrypted": encrypted,
        "shift": normalize_shift(
            shift,
            alphabet,
        ),
        "alphabet_size": len(alphabet),
        "letters": count_shiftable_characters(
            text,
            alphabet,
        ),
        "symbols": count_non_shiftable_characters(
            text,
            alphabet,
        ),
    }


# Comparison Utilities

def verify_decryption(
    plaintext: str,
    ciphertext: str,
    shift: int,
    *,
    alphabet: str = DEFAULT_ALPHABET,
) -> bool: 
    # Verifies that a ciphertext matches a plaintext using the supplied shift 

    return encrypt(
        plaintext,
        shift,
        alphabet=alphabet,
    ) == ciphertext


# Self-Test

def self_test() -> bool: 
    # Runs a quick internal correctness test 

    tests = [
        encrypt("ABC", 3) == "DEF",
        decrypt("DEF", 3) == "ABC",
        encrypt("XYZ", 3) == "ABC",
        decrypt("ABC", 3) == "XYZ",
        encrypt("Hello!", 5) == "Mjqqt!",
        decrypt("Mjqqt!", 5) == "Hello!",
        encrypt("Python 3.12", 7) == "Wfaovu 3.12",
        decrypt(
            encrypt("OpenAI", 19),
            19,
        ) == "OpenAI",
    ]
    return all(tests)


# Module Exports

__all__ = [
    "caesar",
    "encrypt",
    "decrypt", 
    "shift_character",
    "normalize_shift",
    "character_exists",
    "get_character_index",
    "encrypt_many",
    "decrypt_many",
    "caesar_generator",
    "count_shiftable_characters",
    "count_non_shiftable_characters",
    "supported_alphabet",
    "cipher_summary",
    "verify_decryption",
    "self_test",
] 

