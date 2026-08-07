# __init__.py
# Core Encryption package for the entire Cryptography Toolkit

# Contains primary encryption algorithms, alphabet definitions,
# data models, key generation utilities, streaming utilities,
# and custom exceptions used throughout the project

# Modules

# caesar - Core Caesar Cipher implementation
# rot - ROT cipher implementations
# chain - Multi-layer Caesar Cipher implementation
# atbash - Atbash Cipher implementation
# alphabets - Built-in alphabets and helper functions
# base - Base interface for cipher implementations
# models - Shared data models and result objects
# keygen - Cryptographic key generation utilities
# streaming - Streaming encryption and decryption utilities
# exceptions - Custom exceptions


from .caesar import (
    caesar,
    encrypt,
    decrypt,
    shift_character,
)

from .rot import (
    rot13,
    rot5,
    rot18,
    rot47,
)

from .chain import (
    chain_encrypt,
    chain_decrypt,
)

from .atbash import (
    atbash,
)

from .alphabets import (
    DEFAULT_ALPHABET,
    LOWERCASE_ALPHABET,
    UPPERCASE_ALPHABET,
    DIGITS,
    ALPHANUMERIC,
    printable_ascii,
    validate_alphabet,
)

from .base import (
    Cipher,
)

from .models import (
    CipherResult,
    CharacterTransform,
    EncryptionTrace,
    BenchmarkResult,
    AnalysisResult,
    FrequencyResult,
    BruteForceCandidate,
    FileEncryptionResult,
    HistoryEntry,
    serialize_model,
    serialize_models,
    validate_result,
    validate_history_entry,
)

from .keygen import (
    generate_caesar_key,
    generate_nonzero_caesar_key,
    generate_random_character,
    generate_random_string,
    generate_keyword,
    generate_random_alphabet,
    generate_unique_keyword,
    generate_substitution_alphabet,
    generate_keyword_alphabet,
    validate_caesar_key,
    validate_keyword,
    estimate_key_strength,
    estimate_key_entropy,
    normalize_key,
    generate_random_caesar_key,
    generate_random_substitution_key,
    key_information,
)

from .streaming import (
    encrypt_chunks,
    decrypt_chunks,
    encrypt_generator,
    decrypt_generator,
    process_chunks,
    encrypt_file,
    decrypt_file,
    encrypt_lines,
    decrypt_lines,
    process_file_lines,
    validate_chunk_size,
    validate_encoding,
    count_chunks,
    count_lines,
)


__all__ = [

    # Caesar
    "caesar",
    "encrypt",
    "decrypt",
    "shift_character",

    # ROT
    "rot13",
    "rot5",
    "rot18",
    "rot47",

    # Chain
    "chain_encrypt",
    "chain_decrypt",

    # Atbash
    "atbash",

    # Alphabets
    "DEFAULT_ALPHABET",
    "LOWERCASE_ALPHABET",
    "UPPERCASE_ALPHABET",
    "DIGITS",
    "ALPHANUMERIC",
    "printable_ascii",
    "validate_alphabet",

    # Base
    "Cipher",

    # Models
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

    # Key Generation
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

    # Streaming
    "encrypt_chunks",
    "decrypt_chunks",
    "encrypt_generator",
    "decrypt_generator",
    "process_chunks",
    "encrypt_file",
    "decrypt_file",
    "encrypt_lines",
    "decrypt_lines",
    "process_file_lines",
    "validate_chunk_size",
    "validate_encoding",
    "count_chunks",
    "count_lines",
] 

