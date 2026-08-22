# `ui.md`

````markdown
# User Interface Package Documentation

## Overview

The `ui` package contains the presentation and terminal-interface utilities used throughout the Cryptography Toolkit.

Its purpose is to provide a consistent, reusable, and professional visual interface for the toolkit without mixing presentation logic into the cryptographic or application logic.

The package handles:

- ASCII banners
- Terminal colors
- Text formatting
- Progress indicators
- Console tables
- Analysis result displays
- Cryptanalysis output formatting
- Terminal-friendly status messages
- User-facing command-line presentation

The package is designed to be reusable across the CLI, analysis tools, file-processing utilities, and other components of the Cryptography Toolkit.

---

# Package Structure

```text
ui/
│
├── __init__.py
├── banners.py
├── colors.py
├── formatting.py
├── progress.py
├── tables.py
└── ui.md
````

---

# Module Overview

| Module          | Purpose                                                                              |
| --------------- | ------------------------------------------------------------------------------------ |
| `__init__.py`   | Initializes the UI package and exposes its public API                                |
| `banners.py`    | Provides ASCII banners, titles, headers, and decorative console elements             |
| `colors.py`     | Provides terminal colors, ANSI styles, and colored text utilities                    |
| `formatting.py` | Provides text formatting, spacing, indentation, wrapping, and display helpers        |
| `progress.py`   | Provides progress bars, spinners, counters, timers, and progress tracking            |
| `tables.py`     | Provides terminal tables, column formatting, sorting, filtering, and analysis tables |
| `ui.md`         | Documentation for the complete UI package                                            |

---

# 1. `__init__.py`

## Purpose

The `__init__.py` file initializes the `ui` package and provides a centralized public interface for all UI utilities.

It imports the package modules and re-exports their public functionality.

This allows other parts of the project to use:

```python
from cryptography_toolkit.ui import *
```

or import specific utilities directly:

```python
from cryptography_toolkit.ui import ProgressBar
```

## Responsibilities

* Initialize the UI package
* Import all UI modules
* Re-export public utilities
* Maintain package metadata
* Maintain the package-level `__all__`
* Provide package documentation

## Package Modules

```python
from . import banners
from . import colors
from . import formatting
from . import progress
from . import tables
```

The package also imports the public APIs from each module.

## Metadata

The package defines:

```python
__title__
__description__
__version__
```

These provide basic information about the UI package.

---

# 2. `banners.py`

## Purpose

The `banners.py` module contains ASCII-based visual elements used throughout the toolkit.

It provides a consistent visual identity for the application and its command-line interface.

## Responsibilities

The module handles:

* Application banners
* Section headers
* Subsection headers
* Decorative separators
* CLI titles
* Startup displays
* Exit messages
* Status headers
* ASCII artwork

## Typical Usage

```python
from cryptography_toolkit.ui.banners import banner

print(banner("Cryptography Toolkit"))
```

## Design Goals

Banners should:

* Remain readable in standard terminals
* Avoid excessive decoration
* Work with different terminal widths
* Provide consistent formatting
* Be reusable throughout the application

---

# 3. `colors.py`

## Purpose

The `colors.py` module provides terminal color and ANSI styling functionality.

It allows the toolkit to display different types of information using visual distinctions.

For example:

* Success messages
* Error messages
* Warnings
* Informational messages
* Important values
* Headers
* Debug information

## Responsibilities

The module handles:

* ANSI color codes
* Text colors
* Background colors
* Bright colors
* Text styles
* Reset codes
* Colored strings
* Style combinations
* Terminal color support

## Example

```python
from cryptography_toolkit.ui.colors import color_text

print(
    color_text(
        "Encryption successful!",
        "green",
    )
)
```

## Recommended Color Semantics

The toolkit should use colors consistently.

| Color   | Meaning                            |
| ------- | ---------------------------------- |
| Green   | Success / completed operation      |
| Red     | Error / failure                    |
| Yellow  | Warning / caution                  |
| Blue    | Information                        |
| Cyan    | Secondary information              |
| Magenta | Special or highlighted information |
| White   | Normal output                      |
| Gray    | Less-important information         |

Color should enhance readability rather than replace text.

---

# 4. `formatting.py`

## Purpose

The `formatting.py` module provides reusable text-formatting utilities.

Instead of manually constructing spaces, separators, indentation, and text blocks throughout the project, other modules can use the formatting utilities.

## Responsibilities

The module handles:

* Text alignment
* Indentation
* Padding
* Wrapping
* Spacing
* Separators
* Titles
* Section formatting
* Multiline formatting
* Console-friendly text layouts

## Typical Formatting Operations

Examples include:

```text
Left aligned
Centered text
                         Right aligned
```

and:

```text
----------------------------------------
             SECTION TITLE
----------------------------------------
```

## Design Goals

Formatting functions should:

* Be predictable
* Be reusable
* Avoid duplicated formatting code
* Work correctly with terminal output
* Keep CLI output consistent

---

# 5. `progress.py`

## Purpose

The `progress.py` module provides progress-tracking and progress-display utilities.

It is particularly useful for operations that may take noticeable amounts of time, such as:

* File encryption
* File decryption
* Batch processing
* Cryptanalysis
* Key searching
* Large data processing
* Backup operations
* Export operations

## Main Components

### Progress Bars

Progress bars visually represent completion.

Example:

```text
Encrypting [██████████████░░░░░░] 70% 70/100
```

### Spinners

Spinners are useful when the total amount of work is unknown.

Example:

```text
Processing /
Processing -
Processing \
Processing |
```

### Progress Counters

Counters provide simple operation tracking.

```text
Processed: 125
```

### Timing

The module can track:

* Start time
* End time
* Elapsed time
* Processing rate
* Estimated time remaining

### Batch Progress

`BatchProgress` allows multiple operations to be tracked.

It can distinguish between:

* Completed operations
* Failed operations
* Skipped operations
* Remaining operations

## Important Classes

The module contains utilities such as:

```python
ProgressBar
Spinner
ProgressCounter
TimedProgress
BatchProgress
```

## Example

```python
progress = ProgressBar(
    total=100
)

progress.start()

for _ in range(100):
    progress.increment()

progress.complete()
```

## Iterable Progress

The module also supports progress-aware iteration:

```python
for item in iter_progress(items):
    process(item)
```

This keeps progress tracking separate from the underlying operation.

---

# 6. `tables.py`

## Purpose

The `tables.py` module provides structured terminal-table functionality.

Tables are especially useful for presenting cryptographic analysis results in a readable format.

Examples include:

* Frequency analysis
* Key candidates
* Cryptanalysis scores
* File information
* Configuration information
* Statistics
* Operation results

---

# Table Features

The table system supports:

* Headers
* Rows
* Columns
* Alignment
* Padding
* Borders
* Multiple border styles
* Automatic column sizing
* Text truncation
* ANSI-aware width calculations
* Sorting
* Filtering
* Column selection
* Table transposition
* Table summaries

---

# Border Styles

The module provides several built-in styles.

### Rounded

```text
╭──────────┬──────────╮
│ Key      │ Score    │
├──────────┼──────────┤
│ A        │ 98.4     │
╰──────────┴──────────╯
```

### Square

```text
┌──────────┬──────────┐
│ Key      │ Score    │
├──────────┼──────────┤
│ A        │ 98.4     │
└──────────┴──────────┘
```

### Double

```text
╔══════════╦══════════╗
║ Key      ║ Score    ║
╠══════════╬══════════╣
║ A        ║ 98.4     ║
╚══════════╩══════════╝
```

### Minimal

Uses fewer visual borders while maintaining alignment.

### None

Provides a borderless table layout.

---

# Table Configuration

`TableConfig` controls the overall appearance and behavior of a table.

Important settings include:

```python
show_header
show_border
header_alignment
default_alignment
padding
min_column_width
max_column_width
truncate_long_values
wrap_long_values
empty_value
```

Example:

```python
config = TableConfig(
    show_header=True,
    show_border=True,
    padding=1,
)
```

---

# Column Configuration

Individual columns can be configured using `ColumnConfig`.

A column can specify:

* Name
* Alignment
* Width
* Minimum width
* Maximum width
* Truncation
* Wrapping

Example:

```python
ColumnConfig(
    name="Score",
    alignment=ColumnAlignment.RIGHT,
)
```

---

# TableBuilder

`TableBuilder` is the main table-construction class.

Example:

```python
table = TableBuilder(
    headers=[
        "Algorithm",
        "Status",
    ]
)

table.add_row(
    [
        "AES-256",
        "Available",
    ]
)

print(table)
```

The builder automatically handles:

* Column sizing
* Alignment
* Headers
* Separators
* Borders
* Row formatting

---

# Key-Value Tables

The package provides convenient key-value tables.

Example:

```python
values = {
    "Algorithm": "AES",
    "Key Size": "256-bit",
    "Mode": "CBC",
}

print(
    key_value_table(values)
)
```

This is useful for:

* Configuration
* File metadata
* Encryption parameters
* Operation summaries
* System information

---

# Statistics Tables

`statistics_table()` is designed for numerical analysis results.

Example:

```python
statistics = {
    "Entropy": 7.82,
    "Index of Coincidence": 0.065,
    "Length": 5000,
}

print(
    statistics_table(statistics)
)
```

This is particularly useful for cryptanalysis.

---

# Frequency Tables

The `frequency_table()` helper provides a formatted frequency-analysis table.

Example output:

```text
┌────────┬───────────┬────────────┐
│ Symbol │ Frequency │ Percentage │
├────────┼───────────┼────────────┤
│ E      │ 127       │ 12.70%     │
│ T      │ 91        │ 9.10%      │
│ A      │ 82        │ 8.20%      │
└────────┴───────────┴────────────┘
```

Frequencies are automatically sorted from highest to lowest.

---

# Score Tables

`score_table()` can display cryptanalysis candidate scores.

Example:

```text
┌─────┬────────┐
│ Key │ Score  │
├─────┼────────┤
│ 12  │ 98.42  │
│ 7   │ 91.27  │
│ 19  │ 87.53  │
└─────┴────────┘
```

This is useful for:

* Caesar cracking
* Substitution analysis
* Vigenère analysis
* Brute-force searches
* Scoring candidate plaintexts

---

# Candidate Tables

`candidates_table()` displays possible cryptanalysis results.

Example:

```text
┌─────┬──────────────────────┐
│ Key │ Plaintext            │
├─────┼──────────────────────┤
│ 3   │ HELLO WORLD          │
│ 7   │ IFMMP XPSME          │
└─────┴──────────────────────┘
```

---

# Table Operations

The table module also provides utilities for manipulating table data.

## Sorting

```python
sort_rows(
    rows,
    column=1,
    reverse=True,
)
```

## Filtering

```python
filter_rows(
    rows,
    predicate,
)
```

## Column Filtering

```python
filter_column(
    rows,
    column=1,
    predicate=lambda value: value > 50,
)
```

## Selecting Columns

```python
select_columns(
    rows,
    [0, 2],
)
```

## Transposing

```python
transpose_rows(
    rows
)
```

---

# Table Summaries

`TableSummary` provides structural information about a table.

It tracks:

* Number of rows
* Number of columns
* Total cells
* Empty cells
* Whether headers exist
* Populated cells

Example:

```python
summary = summarize_table(
    rows,
    headers,
)
```

---

# Configuration Presets

The table module provides several ready-to-use configurations.

## Default

```python
default_table_config()
```

Designed for standard toolkit output.

## Compact

```python
compact_table_config()
```

Designed for dense terminal displays.

## Borderless

```python
borderless_table_config()
```

Designed for simple text-based layouts.

---

# UI Package Design

The UI package follows a separation-of-concerns approach.

```text
                    ┌────────────────────┐
                    │    Application     │
                    │      / CLI         │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │        UI          │
                    │      Package       │
                    └─────────┬──────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
      Formatting           Progress            Tables
          │                   │                   │
          ▼                   ▼                   ▼
       Colors             Banners             Results
```

The cryptographic modules should not need to know how their results are visually presented.

For example:

```text
Cryptography Logic
        │
        ▼
     Result
        │
        ▼
     UI Layer
        │
        ├── Color
        ├── Formatting
        ├── Table
        └── Progress
        │
        ▼
   Terminal Output
```

---

# UI and Cryptography Separation

The UI package should not contain cryptographic algorithms.

For example, encryption logic belongs in the appropriate cryptography package:

```text
crypto/
```

while displaying the result belongs here:

```text
ui/
```

This separation makes the project easier to maintain.

---

# Typical Usage Across the Project

A command might combine several UI utilities:

```python
from cryptography_toolkit.ui import (
    banner,
    color_text,
    TableBuilder,
    ProgressBar,
)
```

Then:

```python
print(
    banner(
        "Encryption"
    )
)

progress = ProgressBar(
    total=100
)

progress.start()

# Encryption work...

progress.complete()

table = TableBuilder(
    headers=[
        "Property",
        "Value",
    ]
)

table.add_row(
    [
        "Algorithm",
        "AES-256",
    ]
)

table.add_row(
    [
        "Status",
        color_text(
            "Success",
            "green",
        ),
    ]
)

print(table)
```

---

# Public API

The package exposes the public functionality of all UI modules.

The package-level API includes functionality from:

```text
banners
colors
formatting
progress
tables
```

Each module maintains its own `__all__` declaration.

The package initializer combines these exports into the package-level `__all__`.

This allows:

```python
from cryptography_toolkit.ui import *
```

while still keeping internal implementation details private.

---

# Error Handling

The UI package defines its own exceptions where appropriate.

For example, the table system provides:

```python
TableError
TableConfigurationError
TableDataError
```

These allow callers to distinguish UI-related errors from errors originating in the cryptography or application layers.

---

# Design Principles

The UI package follows several design principles.

## 1. Reusability

UI functionality should be reusable across multiple commands and applications.

## 2. Consistency

The same colors, formatting conventions, tables, and progress indicators should be used throughout the toolkit.

## 3. Separation of Concerns

Presentation logic should remain separate from cryptographic logic.

## 4. Readability

Terminal output should be easy to understand at a glance.

## 5. Configurability

Users and other modules should be able to customize presentation where necessary.

## 6. Minimal Duplication

Common formatting logic should exist in one location rather than being rewritten throughout the project.

## 7. Terminal Compatibility

The UI should work correctly in standard command-line environments and avoid unnecessary dependencies.

---

# Dependencies

The UI package primarily relies on Python's standard library.

Typical dependencies include:

```python
dataclasses
enum
typing
sys
re
time
```

No external UI framework is required for the terminal utilities.

---

# Integration With Other Packages

The UI package is primarily a presentation layer and can be used by several other packages.

Potential consumers include:

```text
cli/
fileio/
analysis/
crypto/
core/
```

For example:

```text
┌───────────────┐
│ Cryptography  │
│ Algorithms    │
└───────┬───────┘
        │
        │ results
        ▼
┌───────────────┐
│ Analysis      │
└───────┬───────┘
        │
        │ formatted data
        ▼
┌───────────────┐
│      UI       │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│   Terminal    │
└───────────────┘
```

---

# Testing Recommendations

The UI package should be tested for:

* Correct string formatting
* Correct alignment
* Correct table borders
* Empty data handling
* Long values
* Unicode characters
* ANSI-colored text
* Different terminal widths
* Progress completion
* Progress failure
* Spinner behavior
* Invalid configurations
* Invalid table data
* Sorting
* Filtering
* Column selection
* Table transposition

Special attention should be given to terminal-width calculations when ANSI escape sequences are present.

---

# Future Improvements

Possible future additions include:

* Automatic terminal-width detection
* Richer Unicode table styles
* Optional ANSI color integration
* Multi-line cell wrapping
* Nested tables
* CSV-style output
* Markdown table output
* JSON table output
* Exportable formatted reports
* Dynamic terminal resizing
* Improved Unicode width handling
* More advanced progress rendering
* Concurrent progress indicators
* GUI-compatible formatting adapters

---

# Summary

The `ui` package provides the presentation layer for the Cryptography Toolkit.

Its five primary modules have distinct responsibilities:

```text
banners.py
    ↓
Application identity and visual headers

colors.py
    ↓
Terminal colors and styling

formatting.py
    ↓
Text layout and formatting

progress.py
    ↓
Progress, timing, and operation status

tables.py
    ↓
Structured data and cryptanalysis results
```

Together, these modules provide a consistent interface for presenting information throughout the toolkit while keeping presentation logic separate from the underlying cryptographic implementation.

The package therefore acts as the central **presentation utility layer** of the Cryptography Toolkit.

```
```

