# rot.py 
# Implementation of the ROT family of ciphers 

# Supported ciphers: 
# 1. ROT5 
# 2. ROT13 
# 3. ROT18 
# 4. ROT47 

# They're implemented as wrappers around the core implementation wherever possible 

from __future__ import annotations
import string
from .caesar import encrypt
from .caesar import decrypt


# Constants

ROT47_ASCII = "".join(
    chr(i)
    for i in range(33, 127)
)
DIGITS = string.digits


# Internal Helpers

def _rotate_custom(
    text: str,
    shift: int,
    alphabet: str,
) -> str: 
    # Rotates text using an arbitrary alphabet 
    # Used for ROT5 & ROT47 

    shift %= len(alphabet)
    result = []

    for character in text:
        if character in alphabet:
            index = alphabet.index(character)
            new_index = (
                index + shift
            ) % len(alphabet)
            result.append(
                alphabet[new_index]
            )
        else:
            result.append(character)
    return "".join(result)


# ROT5

def rot5(
    text: str,
) -> str: 
    # Applies ROT5 
    # Rotates only digits 

    return _rotate_custom(
        text,
        5,
        DIGITS,
    )


# ROT13 

def rot13(
    text: str,
) -> str: 
    # Applies ROT13 
    # ROT13 is its own inverse 

    return encrypt(
        text,
        13,
    )


# ROT18 

def rot18(
    text: str,
) -> str: 
    # Applies ROT18 
    # ROT13 on letters 
    # ROT5 on digits 

    stage_one = rot13(text)
    return rot5(stage_one)


# ROT47 

def rot47(
    text: str,
) -> str: 
    # Applies ROT47 
    # Works on printable ASCII characters 

    return _rotate_custom(
        text,
        47,
        ROT47_ASCII,
    )


# Detection 

def detect_rot(
    text: str,
) -> list[str]: 
    # Returns every ROT alogirthm that could reasonably apply to the text 
    # Only heuristic 

    possible = []

    if any(c.isalpha() for c in text):
        possible.append("ROT13")

    if any(c.isdigit() for c in text):
        possible.append("ROT5")
        if "ROT13" in possible:
            possible.append("ROT18")

    if any(
        33 <= ord(c) <= 126
        for c in text
    ):
        possible.append("ROT47")
    return possible


# Generic Dispatcher 

def apply_rot(text: str, mode: str) -> str: 
    # Applies a chosen ROT cipher 

    mode = mode.upper()

    if mode == "ROT5":
        return rot5(text)

    if mode == "ROT13":
        return rot13(text)

    if mode == "ROT18":
        return rot18(text)

    if mode == "ROT47":
        return rot47(text)

    raise ValueError(
        f"Unsupported ROT mode: {mode}"
    )


# Validation 

SUPPORTED_ROT_MODES = (
    "ROT5",
    "ROT13",
    "ROT18",
    "ROT47",
)

def is_rot_mode(mode: str) -> bool: 
    # Determines whether a ROT mode is supported 

    return mode.upper() in SUPPORTED_ROT_MODES

def supported_rot_modes() -> tuple[str, ...]:
    # Returns every supported ROT algorithm 

    return SUPPORTED_ROT_MODES


# Statistics 

def rot_summary(text: str, mode: str) -> dict: 
    # Generates information about a ROT operation 

    transformed = apply_rot(
        text,
        mode,
    )

    return {
        "algorithm": mode.upper(),
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


# Verification 

def verify_rot(text: str, mode: str) -> bool: 
    # Verifies that applying the same ROT cipher twice restores the original text 
    # This property holds true for all standard ROT ciphers 

    transformed = apply_rot(
        text,
        mode,
    )
    restored = apply_rot(
        transformed,
        mode,
    )
    return restored == text

def verify_all_rot_modes(text: str) -> dict[str, bool]: 
    # Verifies every supported ROT algorithm 

    results = {}
    for mode in SUPPORTED_ROT_MODES:
        results[mode] = verify_rot(
            text,
            mode,
        )
    return results


# Benchmarking 

def benchmark_rot(
    text: str,
    mode: str,
    iterations: int = 10000,
) -> float: 
    # Benchmarks the selected ROT algorithm 

    from time import perf_counter
    start = perf_counter()

    for _ in range(iterations):
        apply_rot(
            text,
            mode,
        )
    end = perf_counter()
    return end - start


# Utility Functions 

def available_rot_functions() -> dict[str, callable]: 
    # Returns a mapping of supported ROT functions 

    return {
        "ROT5": rot5,
        "ROT13": rot13,
        "ROT18": rot18,
        "ROT47": rot47,
    }

def print_rot_summary(text: str) -> None: 
    # Displays the available ROT algorithms for the supplied text 

    print()
    print("=" * 50)
    print("ROT ANALYSIS")
    print("=" * 50)
    detected = detect_rot(text)

    for mode in detected:
        print()
        print(f"{mode}")
        print("-" * 25)
        print(apply_rot(text, mode))
    print()


# Self Test 

def self_test() -> bool: 
    # Executes a quick correctness test 

    tests = [
        rot13(
            rot13("HELLO")
        ) == "HELLO",
        rot5(
            rot5("12345")
        ) == "12345",
        rot18(
            rot18("HELLO123")
        ) == "HELLO123",
        rot47(
            rot47("Hello World!")
        ) == "Hello World!",
        verify_rot(
            "Python123",
            "ROT18",
        ),
        verify_rot(
            "HELLO",
            "ROT13",
        ),
    ]

    return all(tests)


# Module Exports 

__all__ = [
    "rot5",
    "rot13",
    "rot18",
    "rot47",
    "apply_rot",
    "detect_rot",
    "verify_rot",
    "verify_all_rot_modes",
    "supported_rot_modes",
    "is_rot_mode",
    "rot_summary",
    "benchmark_rot",
    "available_rot_functions",
    "print_rot_summary",
    "self_test",
] 

