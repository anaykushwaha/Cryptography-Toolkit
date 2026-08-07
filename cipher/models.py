# models.py
# Data models used throughout the Cryptography Toolkit

# Contains structured dataclasses for cipher results,
# character transformations, and encryption traces


from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime


# Cipher Result

@dataclass(slots=True)
class CipherResult:
    # Stores the result and basic information about a cipher operation

    original: str
    transformed: str
    algorithm: str
    shift: int | None = None
    alphabet_size: int | None = None
    letters: int = 0
    digits: int = 0
    symbols: int = 0
    timestamp: datetime = field(
        default_factory=datetime.now
    )


    @property
    def length(self) -> int:
        # Returns the length of the original text

        return len(
            self.original
        )


    @property
    def changed(self) -> bool:
        # Determines whether the transformation changed the text

        return self.original != self.transformed


    def as_dict(self) -> dict:
        # Converts the result into a dictionary

        return {
            "original": self.original,
            "transformed": self.transformed,
            "algorithm": self.algorithm,
            "shift": self.shift,
            "alphabet_size": self.alphabet_size,
            "letters": self.letters,
            "digits": self.digits,
            "symbols": self.symbols,
            "length": self.length,
            "changed": self.changed,
            "timestamp": self.timestamp.isoformat(),
        }


# Character Transformation

@dataclass(slots=True)
class CharacterTransform:
    # Stores information about a single character transformation

    original: str
    transformed: str
    original_index: int | None = None
    transformed_index: int | None = None


    @property
    def changed(self) -> bool:
        # Determines whether the character was changed

        return self.original != self.transformed


# Encryption Trace

@dataclass(slots=True)
class EncryptionTrace:
    # Stores the complete character-by-character transformation process

    original: str
    transformed: str
    algorithm: str
    steps: list[CharacterTransform] = field(
        default_factory=list
    )


    @property
    def total_steps(self) -> int:
        # Returns the number of transformation steps

        return len(
            self.steps
        )


    @property
    def changed_steps(self) -> int:
        # Returns the number of characters that were changed

        return sum(
            step.changed
            for step in self.steps
        )


    def as_dict(self) -> dict:
        # Converts the trace into a dictionary

        return {
            "original": self.original,
            "transformed": self.transformed,
            "algorithm": self.algorithm,
            "total_steps": self.total_steps,
            "changed_steps": self.changed_steps,
            "steps": [
                {
                    "original": step.original,
                    "transformed": step.transformed,
                    "original_index": step.original_index,
                    "transformed_index": step.transformed_index,
                }
                for step in self.steps
            ],
        } 

    # Benchmark Result

@dataclass(slots=True)
class BenchmarkResult:
    # Stores performance information about a cipher operation

    algorithm: str
    iterations: int
    total_seconds: float
    text_length: int


    @property
    def average_seconds(self) -> float:
        # Returns the average time required for one operation

        if self.iterations <= 0:
            return 0.0

        return (
            self.total_seconds
            / self.iterations
        )


    @property
    def operations_per_second(self) -> float:
        # Returns the number of operations completed per second

        if self.total_seconds <= 0:
            return 0.0

        return (
            self.iterations
            / self.total_seconds
        )


    def as_dict(self) -> dict:
        # Converts the benchmark result into a dictionary

        return {
            "algorithm": self.algorithm,
            "iterations": self.iterations,
            "total_seconds": self.total_seconds,
            "average_seconds": self.average_seconds,
            "operations_per_second": self.operations_per_second,
            "text_length": self.text_length,
        }


# Analysis Result

@dataclass(slots=True)
class AnalysisResult:
    # Stores general results produced by cryptanalysis tools

    algorithm: str
    text: str
    score: float | None = None
    confidence: float | None = None
    details: dict = field(
        default_factory=dict
    )


    @property
    def length(self) -> int:
        # Returns the length of the analyzed text

        return len(
            self.text
        )


    def as_dict(self) -> dict:
        # Converts the analysis result into a dictionary

        return {
            "algorithm": self.algorithm,
            "text": self.text,
            "length": self.length,
            "score": self.score,
            "confidence": self.confidence,
            "details": self.details.copy(),
        }


# Frequency Result

@dataclass(slots=True)
class FrequencyResult:
    # Stores letter frequency analysis results

    text_length: int
    frequencies: dict[str, int] = field(
        default_factory=dict
    )
    percentages: dict[str, float] = field(
        default_factory=dict
    )


    @property
    def unique_characters(self) -> int:
        # Returns the number of unique characters found

        return len(
            self.frequencies
        )


    @property
    def most_common(self) -> tuple[str, int] | None:
        # Returns the most frequent character

        if not self.frequencies:
            return None

        return max(
            self.frequencies.items(),
            key=lambda item: item[1],
        )


    def as_dict(self) -> dict:
        # Converts the frequency result into a dictionary

        return {
            "text_length": self.text_length,
            "unique_characters": self.unique_characters,
            "frequencies": self.frequencies.copy(),
            "percentages": self.percentages.copy(),
            "most_common": self.most_common,
        }


# Brute Force Candidate

@dataclass(slots=True)
class BruteForceCandidate:
    # Stores a single candidate produced by brute-force analysis

    shift: int
    plaintext: str
    score: float
    rank: int | None = None
    confidence: float | None = None


    def as_dict(self) -> dict:
        # Converts the candidate into a dictionary

        return {
            "shift": self.shift,
            "plaintext": self.plaintext,
            "score": self.score,
            "rank": self.rank,
            "confidence": self.confidence,
        }


# File Encryption Result

@dataclass(slots=True)
class FileEncryptionResult:
    # Stores information about a file encryption operation

    source: str
    destination: str
    algorithm: str
    input_size: int
    output_size: int
    success: bool
    error: str | None = None


    @property
    def size_difference(self) -> int:
        # Returns the difference between output and input size

        return (
            self.output_size
            - self.input_size
        )


    def as_dict(self) -> dict:
        # Converts the file result into a dictionary

        return {
            "source": self.source,
            "destination": self.destination,
            "algorithm": self.algorithm,
            "input_size": self.input_size,
            "output_size": self.output_size,
            "size_difference": self.size_difference,
            "success": self.success,
            "error": self.error,
        } 

    # History Entry

@dataclass(slots=True)
class HistoryEntry:
    # Stores information about a previous cipher operation

    operation: str
    algorithm: str
    original: str
    result: str
    timestamp: datetime = field(
        default_factory=datetime.now
    )
    metadata: dict = field(
        default_factory=dict
    )


    @property
    def length(self) -> int:
        # Returns the length of the original text

        return len(
            self.original
        )


    def as_dict(self) -> dict:
        # Converts the history entry into a dictionary

        return {
            "operation": self.operation,
            "algorithm": self.algorithm,
            "original": self.original,
            "result": self.result,
            "timestamp": self.timestamp.isoformat(),
            "length": self.length,
            "metadata": self.metadata.copy(),
        }


# Serialization Helpers

def serialize_model(
    model: object,
) -> dict:
    # Converts a supported data model into a dictionary

    if hasattr(model, "as_dict"):
        return model.as_dict()

    raise TypeError(
        f"Unsupported model type: {type(model).__name__}"
    )


def serialize_models(
    models: list[object],
) -> list[dict]:
    # Converts multiple data models into dictionaries

    return [
        serialize_model(model)
        for model in models
    ]


# Model Validation

def validate_result(
    result: CipherResult,
) -> bool:
    # Verifies that a CipherResult contains valid data

    if not isinstance(
        result,
        CipherResult,
    ):
        return False

    if not isinstance(
        result.original,
        str,
    ):
        return False

    if not isinstance(
        result.transformed,
        str,
    ):
        return False

    if not isinstance(
        result.algorithm,
        str,
    ):
        return False

    return True


def validate_history_entry(
    entry: HistoryEntry,
) -> bool:
    # Verifies that a HistoryEntry contains valid data

    if not isinstance(
        entry,
        HistoryEntry,
    ):
        return False

    if not entry.operation:
        return False

    if not entry.algorithm:
        return False

    return True


# Module Exports

__all__ = [
    "CipherResult",
    "CharacterTransform",
    "EncryptionTrace",
    "BenchmarkResult",
    "AnalysisResult",
    "FrequencyResult",
    "BruteForceCandidate",
    "FileEncryptionResult",
    "HistoryEntry",
    "serialize_model",
    "serialize_models",
    "validate_result",
    "validate_history_entry",
] 

