# chain.py 
# Multi-layer toolkit implementation 

# Module allows a message to be encrypted multiple times using different Casar shifts 

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from time import perf_counter
from typing import Iterable

from .caesar import encrypt
from .caesar import decrypt
from .caesar import normalize_shift
from .alphabets import DEFAULT_ALPHABET


# Dataclasses

@dataclass(slots=True)
class ChainStep: 
    # Represents one stage of a chained encryption 

    step: int
    shift: int
    input_text: str
    output_text: str

@dataclass(slots=True)
class ChainResult: 
    # Stores the complete encryption history 

    original: str
    result: str
    shifts: list[int]
    steps: list[ChainStep]
    elapsed: float
    timestamp: datetime = field(
        default_factory=datetime.now
    )

    @property
    def total_layers(self) -> int:
        return len(self.shifts)

    @property
    def net_shift(self) -> int:
        return sum(self.shifts) % 26

    def as_dict(self) -> dict:
        return {
            "original": self.original,
            "result": self.result,
            "layers": self.total_layers,
            "net_shift": self.net_shift,
            "elapsed": self.elapsed,
            "timestamp": self.timestamp.isoformat(),
        }


# Validation

def validate_shifts(
    shifts: Iterable[int],
    alphabet: str = DEFAULT_ALPHABET,
) -> list[int]: 
    # Validates a sequence of shifts 

    if shifts is None:
        raise TypeError(
            "Shift list cannot be None."
        )
    shifts = list(shifts)

    if len(shifts) == 0:
        raise ValueError(
            "At least one shift is required."
        )
    normalized = []

    for shift in shifts:
        if not isinstance(shift, int):
            raise TypeError(
                "Every shift must be an integer."
            )
        normalized.append(
            normalize_shift(
                shift,
                alphabet,
            )
        )
    return normalized


# Utilities

def calculate_net_shift(
    shifts: Iterable[int],
    alphabet: str = DEFAULT_ALPHABET,
) -> int: 
    # Returns the effective shift after all layers have been applied 

    shifts = validate_shifts(
        shifts,
        alphabet,
    )
    return sum(shifts) % len(alphabet)

def reverse_shifts(
    shifts: Iterable[int],
) -> list[int]: 
    # Reverses a shift sequence 

    return list(reversed(list(shifts)))

def total_layers(
    shifts: Iterable[int],
) -> int:
    return len(list(shifts))


# Core Encryption

def chain_encrypt(
    text: str,
    shifts: Iterable[int],
    *,
    alphabet: str = DEFAULT_ALPHABET,
    preserve_case: bool = True,
    strip_non_alpha: bool = False,
) -> str: 
    # Applies multiple Caesar encryptions 

    shifts = validate_shifts(
        shifts,
        alphabet,
    )
    result = text

    for shift in shifts:
        result = encrypt(
            result,
            shift,
            alphabet=alphabet,
            preserve_case=preserve_case,
            strip_non_alpha=strip_non_alpha,
        )
    return result

def chain_decrypt(
    text: str,
    shifts: Iterable[int],
    *,
    alphabet: str = DEFAULT_ALPHABET,
    preserve_case: bool = True,
    strip_non_alpha: bool = False,
) -> str: 
    # Reverses a chained encryption 
    # Shifts are automatically applied in reverse order 

    shifts = reverse_shifts(
        validate_shifts(
            shifts,
            alphabet,
        )
    )
    result = text

    for shift in shifts:
        result = decrypt(
            result,
            shift,
            alphabet=alphabet,
            preserve_case=preserve_case,
            strip_non_alpha=strip_non_alpha,
        )
    return result


# Rich Results

def chain_encrypt_result(
    text: str,
    shifts: Iterable[int],
    *,
    alphabet: str = DEFAULT_ALPHABET,
    preserve_case: bool = True,
    strip_non_alpha: bool = False,
) -> ChainResult: 
    # Encrypts while recording every layer 

    shifts = validate_shifts(
        shifts,
        alphabet,
    )

    start = perf_counter()
    current = text
    history: list[ChainStep] = []

    for number, shift in enumerate(
        shifts,
        start=1,
    ):
        encrypted = encrypt(
            current,
            shift,
            alphabet=alphabet,
            preserve_case=preserve_case,
            strip_non_alpha=strip_non_alpha,
        )
        history.append(
            ChainStep(
                step=number,
                shift=shift,
                input_text=current,
                output_text=encrypted,
            )
        )
        current = encrypted

    elapsed = perf_counter() - start
    return ChainResult(
        original=text,
        result=current,
        shifts=list(shifts),
        steps=history,
        elapsed=elapsed,
    )

def chain_decrypt_result(
    text: str,
    shifts: Iterable[int],
    *,
    alphabet: str = DEFAULT_ALPHABET,
    preserve_case: bool = True,
    strip_non_alpha: bool = False,
) -> ChainResult: 
    # Decrypts while recording every layer 

    shifts = reverse_shifts(
        validate_shifts(
            shifts,
            alphabet,
        )
    )

    start = perf_counter()
    current = text
    history: list[ChainStep] = []

    for number, shift in enumerate(
        shifts,
        start=1,
    ):
        decrypted = decrypt(
            current,
            shift,
            alphabet=alphabet,
            preserve_case=preserve_case,
            strip_non_alpha=strip_non_alpha,
        )
        history.append(
            ChainStep(
                step=number,
                shift=shift,
                input_text=current,
                output_text=decrypted,
            )
        )
        current = decrypted
    elapsed = perf_counter() - start

    return ChainResult(
        original=text,
        result=current,
        shifts=list(shifts),
        steps=history,
        elapsed=elapsed,
    )


# Verification

def verify_chain(
    plaintext: str,
    ciphertext: str,
    shifts: Iterable[int],
    *,
    alphabet: str = DEFAULT_ALPHABET,
) -> bool: 
    # Verifies a chained encryption 

    return (
        chain_encrypt(
            plaintext,
            shifts,
            alphabet=alphabet,
        )
        == ciphertext
    )

def reversible(
    text: str,
    shifts: Iterable[int],
    *,
    alphabet: str = DEFAULT_ALPHABET,
) -> bool: 
    # Ensures the chain decrypts back to the original text 

    encrypted = chain_encrypt(
        text,
        shifts,
        alphabet=alphabet,
    )
    decrypted = chain_decrypt(
        encrypted,
        shifts,
        alphabet=alphabet,
    )
    return decrypted == text


# Statistics

def average_shift(
    shifts: Iterable[int],
) -> float:
    
    shifts = list(shifts)
    if not shifts:
        return 0.0
    return sum(shifts) / len(shifts)

def largest_shift(
    shifts: Iterable[int],
) -> int:

    shifts = list(shifts)
    if not shifts:
        return 0
    return max(shifts)

def smallest_shift(
    shifts: Iterable[int],
) -> int:
    
    shifts = list(shifts)
    if not shifts:
        return 0
    return min(shifts)

def shift_distribution(
    shifts: Iterable[int],
) -> dict[int, int]: 
    # Counts how many times each shift appears 

    distribution: dict[int, int] = {}
    for shift in shifts:
        distribution[shift] = (
            distribution.get(shift, 0) + 1
        )
    return distribution


# Pretty Printing 

def print_chain_steps(
    result: ChainResult,
) -> None: 
    # Displays every stage of a chained encryption 

    print()
    print("=" * 60)
    print("CHAIN ENCRYPTION")
    print("=" * 60)
    for step in result.steps:
        print()
        print(
            f"Layer {step.step} "
            f"(Shift {step.shift:+})"
        )
        print("-" * 40)
        print(step.input_text)
        print("↓")
        print(step.output_text)
    print()
    print("=" * 60)
    print("Final Result")
    print("=" * 60)
    print(result.result)
    print()


# Benchmark 

def benchmark_chain(
    text: str,
    shifts: Iterable[int],
    iterations: int = 1000,
) -> float: 
    # Benchmarks chained encryption 

    start = perf_counter()
    for _ in range(iterations):
        chain_encrypt(
            text,
            shifts,
        )
    end = perf_counter()
    return end - start


# Summary 

def chain_summary(
    result: ChainResult,
) -> dict: 
    # Produces a concise summary 

    return {
        "layers": result.total_layers,
        "net_shift": result.net_shift,
        "elapsed_seconds": result.elapsed,
        "characters": len(result.original),
        "changed": result.original != result.result,
    }


# Exports 

__all__ = [
    "ChainStep",
    "ChainResult",
    "validate_shifts",
    "calculate_net_shift",
    "reverse_shifts",
    "total_layers",
    "chain_encrypt",
    "chain_decrypt",
    "chain_encrypt_result",
    "chain_decrypt_result",
    "verify_chain",
    "reversible",
    "average_shift",
    "largest_shift",
    "smallest_shift",
    "shift_distribution",
    "print_chain_steps",
    "benchmark_chain",
    "chain_summary",
] 

