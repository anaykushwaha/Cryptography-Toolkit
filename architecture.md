````markdown
# Cryptography Toolkit — Architecture

## Overview

The **Cryptography Toolkit** is a modular Python application designed for implementing, analyzing, and experimenting with classical cryptographic algorithms and cryptanalysis techniques.

The project is organized into separate packages based on responsibility.

The architecture follows a layered approach:

- Cryptographic algorithms are contained in `cipher/`
- Cryptanalysis functionality is contained in `analysis/`
- File operations are contained in `fileio/`
- Command-line functionality is contained in `cli/`
- Graphical functionality is contained in `gui/`
- Presentation utilities are contained in `ui/`
- Shared functionality is contained in `utils/`
- Static datasets are contained in `data/`
- Automated tests are contained in `tests/`
- Project documentation is contained in `docs/`
- Example files are contained in `examples/`

The architecture is designed to keep individual responsibilities separated while allowing the different components to work together as a single application.

---

# Project Structure

```text
Cryptography-Toolkit/
│
├── README.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── architecture.md
├── main.py
│
├── cipher/
│   ├── __init__.py
│   ├── alphabets.py
│   ├── atbash.py
│   ├── base.py
│   ├── caesar.py
│   ├── chain.py
│   ├── exceptions.py
│   ├── keygen.py
│   ├── models.py
│   ├── rot.py
│   └── streaming.py
│
├── analysis/
│   ├── __init__.py
│   ├── brute_force.py
│   ├── english_data.py
│   ├── entropy.py
│   ├── frequency.py
│   ├── ioc.py
│   ├── ngrams.py
│   ├── scorer.py
│   └── statistics.py
│
├── fileio/
│   ├── __init__.py
│   ├── backups.py
│   ├── exporters.py
│   ├── file_manager.py
│   └── history.py
│
├── cli/
│   ├── __init__.py
│   ├── commands.py
│   ├── help.py
│   ├── menu.py
│   ├── parser.py
│   └── prompts.py
│
├── gui/
│   ├── __init__.py
│   ├── app.py
│   ├── dialogs.py
│   ├── themes.py
│   ├── widgets.py
│   └── windows.py
│
├── ui/
│   ├── __init__.py
│   ├── banners.py
│   ├── colors.py
│   ├── formatting.py
│   ├── progress.py
│   └── tables.py
│
├── utils/
│   ├── __init__.py
│   ├── config.py
│   ├── constants.py
│   ├── decorators.py
│   ├── helpers.py
│   ├── logger.py
│   ├── timer.py
│   └── validator.py
│
├── data/
│   ├── common_bigrams.txt
│   ├── common_trigrams.txt
│   ├── english_frequency.json
│   ├── english_words.txt
│   ├── sample_messages.txt
│   └── stopwords.txt
│
├── reports/
│   └── .gitkeep
│
├── history/
│   └── .gitkeep
│
├── tests/
│   ├── __init__.py
│   ├── test_caesar.py
│   ├── test_atbash.py
│   ├── test_rot.py
│   ├── test_chain.py
│   ├── test_models.py
│   ├── test_keygen.py
│   ├── test_streaming.py
│   ├── test_frequency.py
│   ├── test_statistics.py
│   ├── test_entropy.py
│   ├── test_ioc.py
│   ├── test_ngrams.py
│   ├── test_scorer.py
│   ├── test_brute_force.py
│   ├── test_fileio.py
│   ├── test_cli.py
│   ├── test_gui.py
│   ├── test_ui.py
│   └── test_utils.py
│
├── docs/
│   ├── project_structure.md
│   ├── algorithms.md
│   ├── cryptanalysis.md
│   ├── api_reference.md
│   ├── main.md
│   ├── cipher.md
│   ├── analysis.md
│   ├── fileio.md
│   ├── cli.md
│   ├── gui.md
│   ├── ui.md
│   ├── utils.md
│   ├── data.md
│   ├── tests.md
│   └── screenshots/
│
└── examples/
    ├── encrypted.txt
    ├── hello_world.txt
    ├── lorem_ipsum.txt
    └── sample_messages.txt
````

---

# Architectural Layers

The project can be viewed as several logical layers.

```text
                         Cryptography Toolkit
                                  │
                                  ▼
                              main.py
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
           cipher/             analysis/            fileio/
              │                   │                   │
              └───────────────────┼───────────────────┘
                                  │
                                  ▼
                               utils/
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                    ▼             ▼             ▼
                   cli/          gui/           ui/
                    │             │             │
                    └─────────────┼─────────────┘
                                  │
                                  ▼
                             User Interface

                 Supporting Resources
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
           data/       tests/     examples/
```

---

# Root Application

## `main.py`

`main.py` serves as the primary entry point for the application.

Its responsibility is to initialize and coordinate the application rather than contain the implementation of individual cryptographic algorithms.

The main application can eventually provide access to:

* Encryption
* Decryption
* Cryptanalysis
* File operations
* Command-line functionality
* Graphical functionality

The implementation details remain separated into their respective packages.

---

# Cipher Layer

## `cipher/`

The `cipher` package contains the core cryptographic functionality of the project.

It is responsible for implementing encryption and transformation algorithms and the supporting models and utilities required by those algorithms.

### Components

#### `alphabets.py`

Contains built-in alphabet definitions and alphabet-related helper functionality.

#### `atbash.py`

Contains the implementation of the Atbash cipher.

#### `base.py`

Contains base abstractions and shared functionality for cipher implementations.

#### `caesar.py`

Contains the core Caesar Cipher implementation.

#### `chain.py`

Provides functionality for chaining multiple Caesar-based transformations.

#### `exceptions.py`

Contains custom exceptions used by the cipher layer.

#### `keygen.py`

Provides key-generation functionality used by cryptographic operations.

#### `models.py`

Contains data models used by the cipher system.

#### `rot.py`

Contains ROT-based transformations such as ROT13, ROT5, ROT18, and ROT47.

#### `streaming.py`

Provides functionality for processing encryption and decryption operations as streams rather than requiring all data to be processed at once.

---

# Cryptanalysis Layer

## `analysis/`

The `analysis` package contains tools for examining ciphertext and plaintext characteristics.

It is responsible for statistical analysis, language analysis, scoring, and automated classical-cipher analysis.

### Components

#### `brute_force.py`

Provides automated brute-force functionality for supported classical ciphers.

#### `english_data.py`

Provides English-language reference data used by analysis and scoring systems.

#### `entropy.py`

Provides Shannon entropy calculations and related functionality.

#### `frequency.py`

Provides letter and character frequency analysis.

#### `ioc.py`

Provides Index of Coincidence calculations.

#### `ngrams.py`

Provides bigram, trigram, and general n-gram analysis.

#### `scorer.py`

Provides candidate scoring functionality for evaluating possible plaintext.

#### `statistics.py`

Provides statistical helper functionality used throughout cryptanalysis.

---

# File I/O Layer

## `fileio/`

The `fileio` package handles persistent data and file operations.

### Components

#### `file_manager.py`

Handles reading, writing, and general file management.

#### `exporters.py`

Handles exporting results and processed data.

#### `history.py`

Manages operation history.

#### `backups.py`

Provides backup functionality for project files and generated data.

---

# Command-Line Layer

## `cli/`

The `cli` package provides the command-line interface.

### Components

#### `commands.py`

Contains CLI command implementations.

#### `help.py`

Provides help information and command documentation.

#### `menu.py`

Provides menu-based CLI navigation.

#### `parser.py`

Handles command-line argument parsing.

#### `prompts.py`

Handles interactive user prompts.

---

# Graphical Interface Layer

## `gui/`

The `gui` package contains the graphical interface.

### Components

#### `app.py`

Provides the main GUI application setup.

#### `windows.py`

Contains application windows.

#### `widgets.py`

Contains reusable GUI widgets.

#### `themes.py`

Contains GUI theme definitions and styling.

#### `dialogs.py`

Contains dialog windows used for user interaction.

---

# User Interface Layer

## `ui/`

The `ui` package contains reusable presentation utilities.

### Components

#### `banners.py`

Provides application banners and headings.

#### `colors.py`

Provides color-related interface functionality.

#### `formatting.py`

Provides formatting utilities.

#### `progress.py`

Provides progress indicators.

#### `tables.py`

Provides table formatting and display functionality.

The `ui` package is separate from the `cli` and `gui` packages so that presentation-related functionality can be reused without mixing it with application logic.

---

# Utility Layer

## `utils/`

The `utils` package contains shared functionality used throughout the project.

### Components

#### `config.py`

Provides project configuration functionality.

#### `constants.py`

Contains shared constants.

#### `decorators.py`

Contains reusable decorators.

#### `helpers.py`

Contains general-purpose helper functions.

#### `logger.py`

Provides centralized logging functionality.

#### `timer.py`

Provides timing and benchmarking functionality.

#### `validator.py`

Provides validation functionality.

The utility layer is intended to support other packages without containing the primary implementation of cryptographic algorithms.

---

# Data Layer

## `data/`

The `data` directory contains static datasets and reference material used by the project.

Current resources include:

* `common_bigrams.txt`
* `common_trigrams.txt`
* `english_frequency.json`
* `english_words.txt`
* `sample_messages.txt`
* `stopwords.txt`

These files are project resources rather than Python modules and therefore do not require `__init__.py`.

---

# Testing Layer

## `tests/`

The `tests` package contains automated tests for the project's functionality.

Tests are organized according to the major components of the application.

The test suite covers:

* Cipher implementations
* Cryptanalysis
* File I/O
* CLI functionality
* GUI functionality
* UI functionality
* Utility functionality

The testing architecture is intended to make individual modules independently testable while also helping detect regressions between packages.

---

# Documentation Layer

## `docs/`

The `docs` directory contains project documentation.

It contains two major categories of documentation.

### General Documentation

```text
project_structure.md
algorithms.md
cryptanalysis.md
api_reference.md
```

These documents describe the project's overall structure, algorithms, cryptanalysis concepts, and API.

### Package Documentation

```text
main.md
cipher.md
analysis.md
fileio.md
cli.md
gui.md
ui.md
utils.md
data.md
tests.md
```

These documents provide package-specific documentation.

The `screenshots/` directory contains screenshots used by the documentation.

---

# Examples

## `examples/`

The `examples` directory contains sample text files used for demonstrations and testing.

Current examples include:

* `encrypted.txt`
* `hello_world.txt`
* `lorem_ipsum.txt`
* `sample_messages.txt`

These files provide convenient inputs for testing encryption, decryption, analysis, and file operations.

---

# Reports and History

## `reports/`

The `reports` directory is reserved for generated analysis reports and other output generated by the application.

A `.gitkeep` file is used to preserve the directory in version control when it is otherwise empty.

Generated report files should not be treated as source code.

---

## `history/`

The `history` directory is reserved for persisted operation history.

A `.gitkeep` file is used to preserve the directory in version control.

Generated history files may be ignored by Git depending on the project's `.gitignore` configuration.

---

# Dependency Direction

The project should generally follow a one-directional dependency structure.

The core cryptographic and analysis functionality should remain independent from the user interface.

A simplified dependency model is:

```text
                ┌─────────────┐
                │   main.py   │
                └──────┬──────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       cipher/      analysis/     fileio/
          │            │            │
          └────────────┼────────────┘
                       │
                       ▼
                    utils/
                       │
             ┌─────────┼─────────┐
             ▼         ▼         ▼
            cli/      gui/       ui/
```

The exact implementation dependencies may evolve as the project is completed, but the architecture should preserve separation between core functionality and presentation layers.

---

# Separation of Concerns

Each package has a specific responsibility.

| Package     | Responsibility                               |
| ----------- | -------------------------------------------- |
| `cipher/`   | Encryption and cryptographic transformations |
| `analysis/` | Cryptanalysis and statistical analysis       |
| `fileio/`   | File and persistence operations              |
| `cli/`      | Command-line interaction                     |
| `gui/`      | Graphical interaction                        |
| `ui/`       | Reusable presentation utilities              |
| `utils/`    | Shared utilities and infrastructure          |
| `data/`     | Static datasets and reference material       |
| `tests/`    | Automated testing                            |
| `docs/`     | Documentation                                |
| `examples/` | Demonstration and sample files               |

This separation prevents unrelated responsibilities from being placed into the same module.

---

# Design Principles

The architecture follows several primary design principles.

## Modularity

Each major area of functionality is separated into its own package.

## Separation of Concerns

Cryptographic algorithms, cryptanalysis, interfaces, file handling, and utilities remain independently organized.

## Reusability

Shared functionality is placed into `utils/` and `ui/` where appropriate so that it can be reused throughout the application.

## Testability

Major components are designed to be independently testable.

## Maintainability

Files are kept relatively focused so that individual modules can be modified without requiring large changes throughout the project.

## Extensibility

The architecture allows additional ciphers, cryptanalysis techniques, interfaces, utilities, and datasets to be added without fundamentally restructuring the project.

---

# Data Flow

A typical encryption workflow can be represented as:

```text
User
 │
 ▼
CLI / GUI
 │
 ▼
Input Processing
 │
 ▼
Validation
 │
 ▼
Cipher Layer
 │
 ▼
Encryption
 │
 ▼
Output / File I/O
 │
 ▼
User
```

A typical cryptanalysis workflow can be represented as:

```text
Ciphertext
 │
 ▼
Input Processing
 │
 ▼
Analysis
 │
 ├── Frequency Analysis
 ├── Statistics
 ├── Entropy
 ├── Index of Coincidence
 ├── N-Grams
 └── Candidate Scoring
 │
 ▼
Candidate Results
 │
 ▼
User / Report
```

---

# Current Development Status

The project is being developed incrementally.

The architecture is currently considered established, while individual implementations, interfaces, tests, and documentation continue to be completed.

The final implementation may refine individual modules internally without requiring changes to the overall project structure.

---

# Future Expansion

The architecture is designed to support future additions such as:

* Additional classical ciphers
* Additional cryptanalysis techniques
* More statistical models
* Additional datasets
* More file formats
* Improved CLI functionality
* Expanded GUI functionality
* Visualization tools
* Additional automated tests
* Expanded documentation
* Performance improvements

Future additions should follow the existing separation-of-concerns model whenever possible.

---

# Architecture Status

**Current Status: 🟢 Architecture Locked**

The directory structure described in this document represents the finalized architectural plan for the Cryptography Toolkit.

Individual files may be expanded, implemented, tested, or internally refactored during development, but the overall project architecture should remain stable.

````

## What we're working on next

With **`cipher/`**, **`analysis/`**, and **`utils/`** finished, I recommend we move to **`fileio/` next**.

That's the best next step because it sits between the core functionality and the eventual CLI/GUI layers. Once file handling is established, the interface layers can call into a much more complete backend.

### `fileio/` chronological order

I'd do the files in this order:

| # | File | Approx. size | Why |
|---:|---|---:|---|
| 1 | `file_manager.py` | ~150–180 lines | Core file reading/writing functionality |
| 2 | `history.py` | ~100–130 lines | Builds on file/persistence concepts |
| 3 | `exporters.py` | ~100–130 lines | Handles exporting results |
| 4 | `backups.py` | ~100–120 lines | Builds on file management and history |
| 5 | `__init__.py` | ~40–60 lines | Final package exports |
| 6 | `docs/fileio.md` | Documentation | Document the completed folder |

So the development order is:

```text
FILEIO
  │
  ├── 1. file_manager.py
  ├── 2. history.py
  ├── 3. exporters.py
  ├── 4. backups.py
  ├── 5. __init__.py
  └── 6. fileio.md
````

