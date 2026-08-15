# Cipher Package Documentation

## Overview

The `cipher/` package contains the core encryption and transformation algorithms used throughout the Cryptography Toolkit.

It provides the toolkit's primary classical cipher implementations, alphabet utilities, key-generation functionality, streaming support, data models, and custom exceptions.

The package is designed to keep cryptographic operations separated from the user interface, command-line interface, file handling, analysis tools, and other application-level components.

```text
cipher/
│
├── __init__.py
├── alphabets.py
├── atbash.py
├── base.py
├── caesar.py
├── chain.py
├── exceptions.py
├── keygen.py
├── models.py
├── rot.py
└── streaming.py
```

---

# Package Responsibilities

The `cipher/` package is responsible for:

* Implementing classical encryption and decryption algorithms.
* Providing reusable cipher functions.
* Managing supported alphabets.
* Preserving or transforming character case.
* Handling cipher configuration and results.
* Generating encryption keys and related values.
* Supporting chained or multi-stage transformations.
* Supporting streaming and chunk-based processing.
* Providing common cipher abstractions.
* Providing custom exceptions for invalid cipher operations.
* Exposing the core cipher API to the rest of the project.

The package does **not** handle:

* User interaction.
* Command-line menus.
* GUI rendering.
* File management.
* Cryptanalysis.
* Reports.
* Logging.
* Application configuration.

Those responsibilities belong to other packages in the project.

---

# Module Structure

## `__init__.py`

The package initializer exposes the public cipher functionality to the rest of the Cryptography Toolkit.

It provides a centralized interface for importing commonly used cipher functions and alphabet utilities.

The initializer includes functionality from:

* `caesar`
* `rot`
* `chain`
* `alphabets`

Additional internal modules can still be imported directly when their specialized functionality is required.

### Purpose

The initializer allows code elsewhere in the project to use the cipher package without needing to know the internal organization of every module.

---

# `alphabets.py`

`alphabets.py` contains alphabet definitions and utilities used by the cipher implementations.

It provides the standard character sets used throughout the toolkit and functions for validating custom alphabets.

### Main Components

#### `DEFAULT_ALPHABET`

The primary alphabet used by the classical alphabet-based ciphers.

#### `LOWERCASE_ALPHABET`

Contains the lowercase English alphabet.

#### `UPPERCASE_ALPHABET`

Contains the uppercase English alphabet.

#### `DIGITS`

Contains the numerical digit characters.

#### `ALPHANUMERIC`

Combines alphabetic characters and digits.

#### `printable_ascii()`

Provides printable ASCII characters for ciphers that need to operate over a wider character range.

#### `validate_alphabet()`

Validates whether an alphabet is suitable for use by a cipher.

### Design Goal

Keeping alphabet definitions in one module prevents individual cipher implementations from duplicating alphabet constants and validation logic.

---

# `base.py`

`base.py` provides common abstractions and functionality shared by cipher implementations.

It acts as the foundation for more specialized cipher components.

The purpose of this module is to reduce duplicated logic between cipher implementations and provide a consistent interface for cipher operations.

### Responsibilities

The base layer is responsible for concepts such as:

* Common cipher behavior.
* Encryption/decryption interfaces.
* Cipher configuration.
* Shared transformation logic.
* Common validation behavior.
* Consistent handling of cipher results.

### Design Goal

Individual algorithms should focus on their actual transformation rules while reusable behavior remains centralized in the base layer.

---

# `caesar.py`

`caesar.py` contains the core Caesar Cipher implementation.

The Caesar Cipher shifts characters through an alphabet by a specified numerical offset.

For example:

```text
ABC
```

with a shift of `3` becomes:

```text
DEF
```

### Core Functions

#### `caesar()`

Performs a Caesar transformation using a supplied shift.

#### `encrypt()`

Encrypts text using a Caesar shift.

#### `decrypt()`

Decrypts text using a Caesar shift.

#### `shift_character()`

Applies a shift to an individual character.

### Additional Behavior

The implementation supports functionality such as:

* Uppercase characters.
* Lowercase characters.
* Alphabet-based transformations.
* Preservation of unsupported characters.
* Custom alphabets.
* Positive and negative shifts.

### Example

```python
from cipher.caesar import encrypt, decrypt

encrypted = encrypt(
    "Hello World",
    shift=3,
)

decrypted = decrypt(
    encrypted,
    shift=3,
)
```

The Caesar implementation is one of the primary algorithms used by the toolkit and is also used by the cryptanalysis package for brute-force Caesar cracking.

---

# `rot.py`

`rot.py` contains fixed-rotation cipher implementations.

ROT ciphers are specialized forms of character rotation where the rotation amount is predetermined.

### Supported Transformations

The toolkit provides:

* `rot13`
* `rot5`
* `rot18`
* `rot47`

### ROT13

ROT13 rotates alphabetic characters by 13 positions.

Because the alphabet contains 26 letters, applying ROT13 twice returns the original text.

```text
HELLO
```

becomes:

```text
URYYB
```

### ROT5

ROT5 rotates decimal digits by five positions.

### ROT18

ROT18 combines:

* ROT13 for letters.
* ROT5 for digits.

### ROT47

ROT47 operates across a wider range of printable ASCII characters.

### Design Goal

The module provides convenient wrappers for common fixed-rotation transformations without requiring callers to manually specify shift values.

---

# `atbash.py`

`atbash.py` implements the Atbash Cipher.

Atbash is a monoalphabetic substitution cipher where characters are mapped to their corresponding positions in a reversed alphabet.

For example:

```text
ABCDEFGHIJKLMNOPQRSTUVWXYZ
ZYXWVUTSRQPONMLKJIHGFEDCBA
```

Therefore:

```text
ABC
```

becomes:

```text
ZYX
```

### Main Functions

#### `atbash()`

Performs the Atbash transformation.

#### `encrypt()`

Convenience wrapper for encryption.

#### `decrypt()`

Convenience wrapper for decryption.

Because Atbash is symmetrical, encryption and decryption use the same transformation.

#### `verify()`

Checks whether applying Atbash twice restores the original text.

#### `summary()`

Returns information about an Atbash transformation.

#### `self_test()`

Runs internal verification tests.

---

# `chain.py`

`chain.py` provides multi-stage cipher transformations.

Instead of applying one cipher operation to a message, a chain allows multiple transformations to be performed sequentially.

Conceptually:

```text
Plaintext
   │
   ▼
Cipher 1
   │
   ▼
Cipher 2
   │
   ▼
Cipher 3
   │
   ▼
Ciphertext
```

### Main Functions

#### `chain_encrypt()`

Applies a sequence of cipher transformations in order.

#### `chain_decrypt()`

Reverses the sequence and applies the inverse transformations.

### Example Concept

A chain could conceptually perform:

```text
Caesar → ROT13 → Atbash
```

during encryption.

Decryption would reverse the process:

```text
Atbash → ROT13 → Caesar
```

### Design Goal

The chain system allows the toolkit to experiment with multi-layer classical encryption while keeping individual cipher implementations independent.

---

# `exceptions.py`

`exceptions.py` contains custom exceptions used by the cipher package.

Centralizing exceptions makes error handling more predictable across the toolkit.

### Responsibilities

Exceptions can represent situations such as:

* Invalid cipher configuration.
* Invalid alphabet definitions.
* Invalid keys.
* Invalid shifts.
* Unsupported operations.
* Invalid cipher parameters.

### Design Goal

Cipher-specific errors should be distinguishable from generic Python exceptions so higher-level components can handle them appropriately.

---

# `models.py`

`models.py` contains structured data models used by the cipher package.

Instead of passing loosely structured collections of values throughout the toolkit, models provide consistent representations of cipher-related data.

### Potential Model Responsibilities

Models can represent information such as:

* Cipher configuration.
* Encryption results.
* Decryption results.
* Cipher operations.
* Transformation metadata.
* Key information.
* Chain configuration.

### Design Goal

Models provide a clean boundary between the low-level cipher implementations and higher-level systems such as:

* CLI.
* GUI.
* File I/O.
* Analysis.
* History.
* Reporting.

This makes the toolkit easier to extend without changing the fundamental cipher algorithms.

---

# `keygen.py`

`keygen.py` provides key and shift generation utilities.

The module is intended to centralize the creation and validation of values used by cipher operations.

### Responsibilities

Depending on the cipher being used, key-generation functionality can include:

* Random Caesar shifts.
* Random numerical keys.
* Random alphabet selections.
* Random strings.
* Key validation.
* Key normalization.

### Design Goal

Key generation should remain separate from encryption algorithms.

For example:

```text
Key Generation
      │
      ▼
Cipher Configuration
      │
      ▼
Encryption
```

This allows the same key-generation functionality to be reused by multiple parts of the toolkit.

---

# `streaming.py`

`streaming.py` provides support for processing text incrementally.

Instead of requiring an entire message to be loaded and transformed at once, streaming functionality allows data to be processed in chunks.

### Concept

```text
Input
  │
  ├── Chunk 1 ──► Cipher ──► Output 1
  │
  ├── Chunk 2 ──► Cipher ──► Output 2
  │
  ├── Chunk 3 ──► Cipher ──► Output 3
  │
  └── Chunk N ──► Cipher ──► Output N
```

### Benefits

Streaming support can be useful for:

* Large text files.
* Memory-efficient processing.
* File encryption workflows.
* Continuous data processing.
* GUI applications handling large inputs.

### Design Goal

Streaming functionality should reuse the underlying cipher algorithms rather than implementing separate encryption logic.

---

# Cipher Architecture

The package follows a layered architecture.

```text
                    cipher/
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
    Alphabets       Base Layer     Exceptions
        │              │
        │              ▼
        │        Cipher Models
        │              │
        └───────┬──────┴────────┐
                │               │
                ▼               ▼
             Ciphers         Utilities
                │               │
       ┌────────┼────────┐      │
       │        │        │      │
       ▼        ▼        ▼      ▼
    Caesar     ROT    Atbash   Keygen
       │        │        │
       └────────┼────────┘
                │
                ▼
              Chain
                │
                ▼
            Streaming
```

The goal is to keep individual algorithms modular while allowing them to be composed into larger operations.

---

# Cipher Processing Flow

A typical encryption operation follows this general flow:

```text
User/Application
       │
       ▼
Cipher Configuration
       │
       ▼
Input Validation
       │
       ▼
Alphabet / Key Processing
       │
       ▼
Cipher Algorithm
       │
       ▼
Transformation
       │
       ▼
Cipher Result
       │
       ▼
Application Layer
```

The cipher package should not be responsible for deciding how the result is displayed to the user.

That responsibility belongs to the CLI, GUI, or other application layers.

---

# Relationship With Other Packages

The `cipher/` package is a foundational component of the Cryptography Toolkit.

Other packages depend on it rather than the cipher package depending on user-interface components.

```text
                    Cryptography Toolkit
                            │
              ┌─────────────┴─────────────┐
              │                           │
           cipher                      analysis
              │                           │
              └─────────────┬─────────────┘
                            │
                     Application
                    /     │      \
                  CLI     GUI    File I/O
```

### `analysis/`

Uses cipher implementations to:

* Generate Caesar candidates.
* Test shifts.
* Evaluate encrypted text.
* Perform cryptanalysis.

### `fileio/`

Uses cipher functionality when encrypted or decrypted files need to be processed.

### `cli/`

Provides command-line access to the cipher functionality.

### `gui/`

Provides graphical access to the cipher functionality.

### `tests/`

Tests the behavior of the cipher modules and their integration with the rest of the project.

---

# Design Principles

## Separation of Concerns

Each module has a focused responsibility.

For example:

```text
caesar.py      → Caesar Cipher
rot.py         → ROT transformations
atbash.py      → Atbash Cipher
alphabets.py   → Alphabet management
keygen.py      → Key generation
streaming.py   → Incremental processing
```

---

## Reusability

Cipher functions are designed to be usable by multiple interfaces.

The same Caesar encryption function can be called by:

* CLI commands.
* GUI controls.
* File-processing operations.
* Automated tests.
* Cryptanalysis utilities.
* Other cipher chains.

---

## Composability

Individual ciphers can be combined through the chain system.

This allows the toolkit to support increasingly complex classical transformations without modifying the underlying algorithms.

---

## Testability

Cipher functionality is kept separate from user interaction so that individual functions can be tested independently.

Each cipher should ideally provide predictable behavior for:

* Normal input.
* Empty input.
* Invalid parameters.
* Boundary values.
* Uppercase text.
* Lowercase text.
* Mixed text.
* Numbers.
* Symbols.
* Custom alphabets.

---

# Public API

The package initializer exposes commonly used functionality so that higher-level modules can access the cipher system through a consistent interface.

Commonly exposed functionality includes:

```python
caesar
encrypt
decrypt
shift_character

rot13
rot5
rot18
rot47

chain_encrypt
chain_decrypt

DEFAULT_ALPHABET
LOWERCASE_ALPHABET
UPPERCASE_ALPHABET
DIGITS
ALPHANUMERIC

printable_ascii
validate_alphabet
```

Specialized functionality can be imported directly from its corresponding module when necessary.

---

# Example Usage

## Caesar Cipher

```python
from cipher.caesar import encrypt, decrypt

message = "Hello World"

encrypted = encrypt(
    message,
    shift=3,
)

decrypted = decrypt(
    encrypted,
    shift=3,
)

print(encrypted)
print(decrypted)
```

---

## ROT13

```python
from cipher.rot import rot13

encrypted = rot13(
    "Hello World"
)

decrypted = rot13(
    encrypted
)
```

Because ROT13 is symmetrical, the same operation performs both encryption and decryption.

---

## Atbash

```python
from cipher.atbash import atbash

encrypted = atbash(
    "Hello World"
)

decrypted = atbash(
    encrypted
)
```

Atbash is also symmetrical.

---

# Module Dependency Guidelines

The cipher package should follow a mostly one-directional dependency structure.

Recommended relationship:

```text
alphabets
    │
    ▼
base
    │
    ├──────────► models
    │
    ▼
cipher implementations
    │
    ├──► caesar
    ├──► rot
    ├──► atbash
    └──► chain
            │
            ▼
        streaming
```

Shared utilities should remain at the lower levels of the dependency structure.

This minimizes circular dependencies and makes individual modules easier to test.

---

# Extending the Cipher Package

New cipher algorithms should be added as independent modules whenever possible.

For example, adding a Vigenère Cipher would ideally result in:

```text
cipher/
├── ...
├── vigenere.py
└── ...
```

The new module should:

1. Contain the cipher's transformation logic.
2. Reuse existing alphabet utilities where appropriate.
3. Follow the project's formatting conventions.
4. Validate its inputs.
5. Provide encryption and decryption operations.
6. Include a `self_test()` function where appropriate.
7. Define `__all__` for its public API.
8. Be covered by tests in `tests/`.
9. Be documented in the appropriate documentation files.
10. Be exposed through `cipher/__init__.py` if it is part of the public API.

---

# Error Handling

Cipher functions should validate inputs before performing transformations.

Typical validation includes:

* Confirming that text is a string.
* Confirming that shifts are integers.
* Confirming that shifts fall within valid ranges.
* Confirming that alphabets are valid.
* Confirming that keys are valid.
* Confirming that configuration values are supported.

Cipher-specific errors should use the custom exceptions defined in `exceptions.py` when appropriate.

---

# Internal Testing

Several cipher modules contain a `self_test()` function.

These functions provide a lightweight way to verify that core behavior remains functional.

For example:

```python
from cipher.atbash import self_test

if self_test():
    print("Atbash passed.")
```

The project's formal automated testing remains in the `tests/` package.

The `self_test()` functions are intended as quick internal checks rather than replacements for the full test suite.

---

# Future Expansion

The `cipher/` package is designed to support additional classical cryptographic algorithms in the future.

Potential additions include:

* Vigenère Cipher.
* Affine Cipher.
* Rail Fence Cipher.
* Substitution Cipher.
* Transposition Cipher.
* XOR-based transformations.
* Bacon's Cipher.
* Playfair Cipher.
* Hill Cipher.
* Beaufort Cipher.

Each new algorithm should remain modular and should integrate with the existing alphabet, model, exception, chain, and streaming systems where appropriate.

---

# Summary

The `cipher/` package forms the **core cryptographic engine** of the Cryptography Toolkit.

Its primary responsibility is to provide reliable, reusable, and composable encryption and decryption functionality while remaining independent from the project's user interfaces and application logic.

The package is structured around:

```text
Algorithms
    │
    ├── Caesar
    ├── ROT
    ├── Atbash
    └── Chain
          │
          ▼
Shared Infrastructure
    │
    ├── Alphabets
    ├── Base abstractions
    ├── Models
    ├── Key generation
    ├── Streaming
    └── Exceptions
```

This separation allows the rest of the Cryptography Toolkit to build on a stable cryptographic foundation while keeping the individual components maintainable, testable, and extensible.

