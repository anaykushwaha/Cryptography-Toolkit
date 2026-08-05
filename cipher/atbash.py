# atbash.py 
# Implementation of the Atbash Cipher 

# The Atbash Cipher is a monoalphabetic substitution cipher where the alphabet is reversed 

from __future__ import annotations
from .alphabets import DEFAULT_ALPHABET


# Internal Helper 

def _reverse_alphabet(
    alphabet: str = DEFAULT_ALPHABET,
) -> dict[str, str]: 
    # Creates a lookup table mapping every character to its reversed equivalent 

    reversed_alphabet = alphabet[::-1]
    table = {}

    for original, reversed_character in zip(
        alphabet,
        reversed_alphabet,
    ):
        table[original] = reversed_character
    return table


# Core Cipher 

def atbash(
    text: str,
    *,
    alphabet: str = DEFAULT_ALPHABET,
    preserve_case: bool = True,
) -> str: 
    # Applies the Atbash Cipher 
    # Since Atbash is symmetrical, the same function encrypts and decrypts 

    table = _reverse_alphabet(
        alphabet.upper()
    )
    result = []
    for character in text:
        upper = character.upper()
        if upper in table:
            transformed = table[upper]
            if preserve_case and character.islower():
                transformed = transformed.lower()
            result.append(
                transformed
            )
        else:
            result.append(
                character
            )
    return "".join(result)


# Convenience Wrappers 

def encrypt(
    text: str,
    *,
    alphabet: str = DEFAULT_ALPHABET,
    preserve_case: bool = True,
) -> str: 
    # Encrypts using Atbash 

    return atbash(
        text,
        alphabet=alphabet,
        preserve_case=preserve_case,
    )


def decrypt(
    text: str,
    *,
    alphabet: str = DEFAULT_ALPHABET,
    preserve_case: bool = True,
) -> str: 
    # Decrypts using Atbash 
    # Since Atbash is symmetrical, this simply calls atbash()  

    return atbash(
        text,
        alphabet=alphabet,
        preserve_case=preserve_case,
    )


# Verification 

def verify(text: str) -> bool: 
    # Verifies that applying Atbash twice restores the original text 

    return atbash(
        atbash(text)
    ) == text


# Statistics 

def summary(text: str) -> dict: 
    # Returns information about an Atbash transformation 

    transformed = atbash(text)
    return {
        "original": text,
        "transformed": transformed,
        "length": len(text),
        "letters": sum(
            c.isalpha()
            for c in text
        ),
        "digits": sum(
            c.isdigit()
            for c in text
        ),
        "symbols": sum(
            not c.isalnum()
            for c in text
        ),
    }


# Self Test 

def self_test() -> bool: 
    # Run a quick internal test 

    tests = [
        atbash("ABC") == "ZYX",
        atbash("XYZ") == "CBA",
        atbash("Hello") == "Svool",
        verify("Python"),
        verify("HELLO WORLD"),
        verify("123456"),
    ]
    return all(tests)


# Module Exports 

__all__ = [
    "atbash",
    "encrypt",
    "decrypt",
    "verify",
    "summary",
    "self_test",
] 

