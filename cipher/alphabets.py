# alphabets.py 
# Defines built-in alphabets used throughout the toolkit 

# This module allows users to work with different alphabets 
# instead of being limited to A-Z 

# Examples 
# ABCDEFGHIJKLNOPQRSTUVWXYZ 
# abcdefghijklmnopqrstuvwxyz 
# 0123456789 
# ABCDEFGHIJKLMNOPRSTUVWXYZ0123456789 
# Printable ASCII characters 


from __future__ import annotations
import string

# Built-in Alphabets

UPPERCASE_ALPHABET: str = string.ascii_uppercase

LOWERCASE_ALPHABET: str = string.ascii_lowercase

DEFAULT_ALPHABET: str = UPPERCASE_ALPHABET

DIGITS: str = string.digits

HEX_ALPHABET: str = "0123456789ABCDEF"

BINARY_ALPHABET: str = "01"

OCTAL_ALPHABET: str = "01234567"

ALPHANUMERIC: str = string.ascii_uppercase + string.digits

LOWERCASE_ALPHANUMERIC: str = (
    string.ascii_lowercase +
    string.digits
)

ASCII_LETTERS: str = string.ascii_letters

PRINTABLE_ASCII: str = "".join(
    chr(i)
    for i in range(32, 127)
)

SYMBOLS: str = (
    "!@#$%^&*()"
    "-_=+[]{}"
    ";:'\",.<>/?\\|`~"
)

# Helper Functions

def printable_ascii() -> str:
    # Returns every printable ASCII character 
    # Returns string 
    
    # Includes: 
    # 1. Letters 
    # 2. Numbers 
    # 3. Punctuation 
    # 4. Symbols 
    # 5. Space 

    return PRINTABLE_ASCII


def validate_alphabet(alphabet: str) -> bool:
    # Validates an alphabet 
    # Returns boolean 

    # Conditions: 
    # 1. Must not be empty 
    # 2. Every character must be unique 
    
    if not alphabet:
        return False

    return len(set(alphabet)) == len(alphabet)


def alphabet_size(alphabet: str = DEFAULT_ALPHABET) -> int:
    # Returns the size of an alphabet 

    return len(alphabet)


def contains(character: str, alphabet: str = DEFAULT_ALPHABET) -> bool:
    # Checks whether a character exists in an alphabet 

    return character in alphabet


def normalize_alphabet(alphabet: str) -> str:
    # Removes duplicate characters while preserving order 
    
    seen = set()
    result = []

    for character in alphabet:

        if character not in seen:

            seen.add(character)

            result.append(character)

    return "".join(result)


def reverse_alphabet(alphabet: str = DEFAULT_ALPHABET) -> str:
    # Returns a reverse alphabet 
    
    return alphabet[::-1]


def rotate_alphabet(
    shift: int,
    alphabet: str = DEFAULT_ALPHABET,
) -> str:
    # Rotates an alphabet by a given shift 

    if not alphabet:
        return alphabet

    shift %= len(alphabet)

    return alphabet[shift:] + alphabet[:shift]


def generate_custom_alphabet(
    *,
    include_uppercase: bool = True,
    include_lowercase: bool = False,
    include_digits: bool = False,
    include_symbols: bool = False,
) -> str:
    # Generates a custom alphabet 
    # Returns string 

    alphabet = ""

    if include_uppercase:
        alphabet += UPPERCASE_ALPHABET

    if include_lowercase:
        alphabet += LOWERCASE_ALPHABET

    if include_digits:
        alphabet += DIGITS

    if include_symbols:
        alphabet += SYMBOLS

    return alphabet

 
AVAILABLE_ALPHABETS = {

    "default": DEFAULT_ALPHABET,

    "uppercase": UPPERCASE_ALPHABET,

    "lowercase": LOWERCASE_ALPHABET,

    "digits": DIGITS,

    "hex": HEX_ALPHABET,

    "binary": BINARY_ALPHABET,

    "octal": OCTAL_ALPHABET,

    "alphanumeric": ALPHANUMERIC,

    "lowercase_alphanumeric": LOWERCASE_ALPHANUMERIC,

    "ascii_letters": ASCII_LETTERS,

    "printable_ascii": PRINTABLE_ASCII,

    "symbols": SYMBOLS,
}


def get_alphabet(name: str) -> str:
    # Retrieves an alphabet by name 
    # Raises KeyError if the alphabet doesn't exist 

    key = name.lower()

    if key not in AVAILABLE_ALPHABETS:

        raise KeyError(
            f"Unknown alphabet '{name}'. "
            f"Available: {', '.join(AVAILABLE_ALPHABETS.keys())}"
        )

    return AVAILABLE_ALPHABETS[key]