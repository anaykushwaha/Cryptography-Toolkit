````markdown
# Analysis Package Documentation

## Overview

The `analysis/` package contains the cryptanalysis and statistical analysis tools used throughout the Cryptography Toolkit.

It is responsible for analyzing encrypted and plaintext messages, measuring their statistical properties, generating possible decryptions, identifying likely plaintext candidates, and evaluating how closely text resembles natural English.

The package works primarily with the cipher implementations provided by the `cipher/` package.

```text
analysis/
│
├── __init__.py
├── brute_force.py
├── english_data.py
├── entropy.py
├── frequency.py
├── ioc.py
├── ngrams.py
├── scorer.py
└── statistics.py
````

---

# Package Responsibilities

The `analysis/` package is responsible for:

* Frequency analysis.
* Statistical analysis.
* Shannon entropy calculations.
* Index of Coincidence calculations.
* Bigram and trigram analysis.
* English-language scoring.
* Brute-force Caesar Cipher analysis.
* Candidate generation and ranking.
* Plaintext likelihood estimation.
* English-language reference data.
* Cryptanalysis-related measurements.

The package does **not** primarily handle:

* Encryption algorithms.
* Decryption algorithms.
* User interaction.
* GUI rendering.
* Command-line menus.
* File management.
* Application configuration.
* Visual presentation.

Those responsibilities belong to other packages within the Cryptography Toolkit.

---

# Role Within the Project

The `analysis/` package sits above the core cipher implementations and uses them to perform cryptanalysis.

```text
                    Cryptography Toolkit
                            │
                            ▼
                         cipher/
                            │
                    Encryption / Decryption
                            │
                            ▼
                       Encrypted Text
                            │
                            ▼
                        analysis/
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
   Frequency            Statistics          Scoring
        │                   │                   │
        ├──────────────┬────┴────┬──────────────┤
        │              │         │              │
        ▼              ▼         ▼              ▼
      IOC           Entropy    N-Grams     Brute Force
        │              │         │              │
        └──────────────┴─────────┴──────────────┘
                            │
                            ▼
                     Likely Plaintext
```

The analysis system therefore acts as the toolkit's primary **cryptanalysis layer**.

---

# Module Structure

## `__init__.py`

The package initializer provides access to the analysis functionality.

It serves as the central entry point for the cryptanalysis package.

The package contains functionality from:

* `frequency`
* `statistics`
* `entropy`
* `ioc`
* `ngrams`
* `brute_force`
* `scorer`
* `english_data`

### Purpose

The initializer allows higher-level components to access analysis functionality without needing to understand the complete internal structure of the package.

---

# `english_data.py`

`english_data.py` contains reference information about the English language.

This data is used by the analysis system to determine whether a piece of text resembles normal English.

### Responsibilities

The module provides reference information such as:

* Expected English letter frequencies.
* Common English bigrams.
* Common English trigrams.
* English-language patterns.
* Other reference values used by cryptanalysis.

### Purpose

Cryptanalysis often requires a way to distinguish plausible plaintext from random or incorrectly decrypted text.

For example:

```text
"THE QUICK BROWN FOX"
```

should generally receive a stronger English-likeness score than:

```text
"XQZJ KQPW VNMZ"
```

The reference data allows the analysis package to make this distinction.

### Design Goal

English-language reference data is kept separate from the analysis algorithms so that:

* Algorithms remain easier to maintain.
* Reference data can be updated independently.
* Multiple analysis modules can reuse the same data.
* Scoring systems do not need to duplicate constants.

---

# `frequency.py`

`frequency.py` provides letter and character frequency analysis.

Frequency analysis measures how often characters occur within a text.

This is one of the oldest and most fundamental techniques in classical cryptanalysis.

### Basic Concept

For a piece of text:

```text
HELLO WORLD
```

the module can count how often each character appears.

The resulting distribution can then be compared against expected English frequencies.

### Responsibilities

The module handles tasks such as:

* Counting character occurrences.
* Calculating frequency percentages.
* Identifying common characters.
* Comparing observed and expected frequencies.
* Measuring frequency differences.
* Producing frequency summaries.

### Importance in Cryptanalysis

Simple substitution and Caesar-style ciphers preserve certain statistical characteristics of the plaintext.

Frequency analysis can therefore provide useful information about the underlying message.

### Relationship With Other Modules

`frequency.py` works closely with:

* `english_data.py`
* `statistics.py`
* `scorer.py`
* `brute_force.py`

---

# `statistics.py`

`statistics.py` contains general statistical utilities used throughout the analysis package.

It provides measurements that help describe the structure and distribution of text.

### Responsibilities

The module can provide calculations related to:

* Character counts.
* Percentages.
* Distribution measurements.
* Minimum and maximum values.
* Averages.
* Statistical summaries.
* Comparison between observed and expected values.

### Purpose

Rather than implementing statistical calculations repeatedly in individual cryptanalysis modules, shared statistical operations are centralized here.

This keeps the rest of the analysis package more modular.

### Design Goal

`statistics.py` should remain focused on reusable statistical calculations rather than cipher-specific logic.

---

# `entropy.py`

`entropy.py` provides Shannon entropy calculations.

Entropy measures the uncertainty or information density of a distribution.

For text analysis, entropy can provide an indication of how predictable or random a message is.

### Concept

A highly repetitive message generally has lower entropy.

A message containing a more evenly distributed collection of symbols generally has higher entropy.

Conceptually:

```text
Low Entropy
    │
    ▼
Highly Repetitive / Predictable Text

High Entropy
    │
    ▼
More Random / Less Predictable Text
```

### Responsibilities

The module handles:

* Shannon entropy.
* Character-based entropy.
* Entropy-related summaries.
* Entropy comparisons.

### Cryptanalysis Usage

Entropy can help provide additional information about a ciphertext.

It should not normally be treated as a standalone method for identifying a specific cipher or plaintext.

Instead, it works alongside:

* Frequency analysis.
* Index of Coincidence.
* N-gram analysis.
* Statistical scoring.

---

# `ioc.py`

`ioc.py` implements Index of Coincidence calculations.

The Index of Coincidence (IOC) measures the probability that two randomly selected characters from a text are the same.

### Purpose

IOC is useful in classical cryptanalysis because different types of text and cipher systems can produce different statistical distributions.

For example:

```text
Natural English
       │
       ▼
Higher structural regularity

Randomized text
       │
       ▼
More uniform distribution
```

### Responsibilities

The module provides functionality for:

* Calculating IOC.
* Calculating IOC for selected character sets.
* Comparing IOC values.
* Producing IOC-related summaries.

### Cryptanalysis Usage

IOC can help investigate:

* Whether text resembles natural language.
* Whether a ciphertext has a relatively uniform distribution.
* Possible properties of a classical cipher.
* Statistical differences between candidate plaintexts.

IOC should be treated as an analytical measurement rather than a definitive cipher detector.

---

# `ngrams.py`

`ngrams.py` provides n-gram analysis functionality.

An n-gram is a sequence of `n` consecutive characters.

The toolkit focuses particularly on:

* Bigrams.
* Trigrams.

### Bigram

A bigram contains two characters.

Example:

```text
TH
HE
EL
LL
LO
```

### Trigram

A trigram contains three characters.

Example:

```text
THE
HEL
ELL
LLO
```

### Responsibilities

The module provides functionality for:

* Generating n-grams.
* Counting n-grams.
* Measuring n-gram frequencies.
* Looking up common patterns.
* Scoring text using n-gram information.

### Cryptanalysis Usage

Natural English contains many recurring patterns.

For example:

```text
TH
HE
IN
ER
AN
```

are common English patterns.

Incorrectly decrypted text is generally less likely to contain natural English n-gram patterns.

Therefore, n-gram analysis provides a useful signal for plaintext scoring.

### Relationship With `english_data.py`

`ngrams.py` uses English-language reference information to evaluate whether n-grams in a candidate plaintext resemble expected English patterns.

---

# `scorer.py`

`scorer.py` provides candidate scoring utilities.

It combines several statistical measurements to estimate how closely text resembles English.

### Responsibilities

The module can evaluate:

* Letter distribution.
* Character frequency.
* Character composition.
* Alphabetic ratios.
* Space ratios.
* Digit ratios.
* Symbol ratios.
* N-gram characteristics.
* Overall English-likeness.
* Candidate rankings.

### Scoring Concept

Rather than relying on a single measurement, the scorer combines multiple signals.

Conceptually:

```text
                 Candidate Text
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
 Letter Frequency   Composition    N-Grams
        │              │              │
        └──────────────┼──────────────┘
                       │
                       ▼
                Combined Score
                       │
                       ▼
              English-Likeness
```

### Main Scoring Concepts

#### Letter Score

Measures how closely the letter distribution resembles expected English frequencies.

#### Frequency Score

Converts frequency-distance measurements into a score where stronger matches receive stronger scores.

#### Composition Score

Examines the overall character composition of the text.

#### English Score

Combines multiple measurements into an overall English-likeness score.

#### Candidate Ranking

Multiple plaintext candidates can be scored and ranked from strongest to weakest.

### Purpose

The scorer is especially important for brute-force cryptanalysis.

When multiple possible decryptions exist, the scorer provides a mechanism for identifying the most plausible result.

---

# `brute_force.py`

`brute_force.py` provides automated brute-force Caesar Cipher analysis.

Instead of requiring the user to manually test every possible Caesar shift, the module generates all possible candidates and evaluates them.

### Basic Process

```text
Ciphertext
    │
    ▼
Generate Shift 0
    │
Generate Shift 1
    │
Generate Shift 2
    │
    ...
    │
Generate Shift 25
    │
    ▼
Score Candidates
    │
    ▼
Rank Candidates
    │
    ▼
Best Candidate
```

### Responsibilities

The module handles:

* Candidate generation.
* Caesar shift testing.
* Candidate scoring.
* Candidate ranking.
* Candidate filtering.
* Best-candidate selection.
* Shift comparison.
* Confidence estimation.
* Brute-force summaries.

### Candidate Generation

The module can generate the complete set of 26 possible Caesar decryptions.

Each candidate contains information such as:

```text
Shift
Plaintext
Score
```

### Candidate Ranking

Candidates can then be sorted according to their English-likeness score.

For example:

```text
Rank 1 → Shift 3 → "HELLO WORLD"
Rank 2 → Shift 10 → ...
Rank 3 → Shift 19 → ...
```

The strongest candidate is treated as the most likely plaintext.

### Confidence

The module can also estimate how strongly the best candidate separates itself from the other candidates.

This allows higher-level components to distinguish between:

```text
Very Clear Result
```

and:

```text
Ambiguous Result
```

### Relationship With `cipher/`

The brute-force system depends on the Caesar Cipher implementation from the `cipher/` package.

This separation is important:

```text
cipher.caesar
      │
      ▼
Performs Caesar transformations
      │
      ▼
analysis.brute_force
      │
      ▼
Tests and evaluates transformations
```

The cipher package performs the transformation.

The analysis package determines which transformation is most likely to be correct.

---

# Analysis Architecture

The `analysis/` package is organized into several layers.

```text
                         analysis/
                             │
                             ▼
                    Reference Information
                             │
                    ┌────────┴────────┐
                    ▼                 ▼
              english_data       Algorithms
                                      │
              ┌───────────────────────┼──────────────────────┐
              │                       │                      │
              ▼                       ▼                      ▼
          Frequency               Statistics             Entropy
              │                       │                      │
              └──────────────┬────────┴───────────┬──────────┘
                             │                    │
                             ▼                    ▼
                            IOC                N-Grams
                             │                    │
                             └──────────┬─────────┘
                                        │
                                        ▼
                                     Scorer
                                        │
                                        ▼
                                  Brute Force
                                        │
                                        ▼
                                  Best Candidate
```

This structure separates low-level measurements from higher-level cryptanalysis.

---

# Analysis Processing Flow

A typical cryptanalysis operation can follow this process:

```text
                     Ciphertext
                         │
                         ▼
                  Analysis Request
                         │
                         ▼
              ┌─────────────────────┐
              │ Statistical Analysis│
              └──────────┬──────────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
      Frequency         IOC          Entropy
          │              │              │
          └──────────────┼──────────────┘
                         │
                         ▼
                     N-Grams
                         │
                         ▼
                      Scorer
                         │
                         ▼
                 Candidate Ranking
                         │
                         ▼
                  Likely Plaintext
```

Different analysis operations may use different subsets of this pipeline.

---

# Relationship With the Cipher Package

The `analysis/` package depends heavily on the functionality provided by `cipher/`.

The relationship can be summarized as:

```text
cipher/
  │
  │ Performs transformations
  │
  ▼
analysis/
  │
  │ Evaluates transformations
  │
  ▼
Likely Result
```

For example, brute-force Caesar analysis uses the Caesar implementation to generate candidate plaintexts.

The analysis package should **not** duplicate the Caesar transformation logic.

Instead, it should call the existing implementation.

This keeps the project modular and prevents different parts of the toolkit from implementing conflicting versions of the same algorithm.

---

# Relationship With Other Packages

## `cipher/`

Provides the encryption and decryption algorithms that analysis tools evaluate.

---

## `fileio/`

Can provide encrypted or plaintext files for analysis.

For example:

```text
Encrypted File
      │
      ▼
   fileio/
      │
      ▼
  analysis/
      │
      ▼
Analysis Results
```

---

## `cli/`

Provides command-line access to cryptanalysis functions.

Potential CLI operations include:

* Frequency analysis.
* Entropy calculation.
* IOC calculation.
* N-gram analysis.
* Caesar brute force.
* Candidate ranking.

---

## `gui/`

Provides graphical interfaces for analysis functionality.

The GUI can display information such as:

* Frequency tables.
* Statistical measurements.
* Candidate lists.
* Scores.
* Cryptanalysis results.

---

## `tests/`

Contains automated tests for the analysis modules.

Testing should verify both individual calculations and interactions between analysis components.

---

# Design Principles

## Separation of Concerns

Each analysis module should have a focused responsibility.

```text
frequency.py     → Frequency analysis

statistics.py    → Statistical calculations

entropy.py       → Entropy calculations

ioc.py           → Index of Coincidence

ngrams.py        → N-gram analysis

scorer.py        → Candidate scoring

brute_force.py   → Automated Caesar analysis

english_data.py  → English reference data
```

This makes the system easier to maintain and expand.

---

# Reusability

Analysis functions should be reusable by multiple parts of the application.

The same frequency-analysis function may be used by:

* CLI commands.
* GUI windows.
* Brute-force analysis.
* Reports.
* Tests.
* Future cryptanalysis algorithms.

The analysis layer should therefore avoid making assumptions about how its results will be displayed.

---

# Composability

The analysis modules are designed to work together.

For example:

```text
Frequency
    │
    ▼
Statistics
    │
    ▼
N-Grams
    │
    ▼
Scorer
    │
    ▼
Candidate Ranking
```

This allows more advanced analysis systems to combine multiple measurements.

---

# Statistical Independence

Different measurements provide different information.

For example:

```text
Frequency
    → Character distribution

IOC
    → Character collision probability

Entropy
    → Information uncertainty

N-Grams
    → Sequential character patterns

Scorer
    → Combined English-likeness
```

No single measurement should automatically be treated as a definitive answer.

The toolkit is designed to combine multiple signals where appropriate.

---

# Extensibility

The analysis package is designed to support additional cryptanalysis techniques.

Potential future modules include:

```text
analysis/
│
├── substitution.py
├── vigenere.py
├── hill_climbing.py
├── simulated_annealing.py
├── language_detection.py
├── word_segmentation.py
└── pattern_matching.py
```

These should be added as independent modules rather than making existing modules unnecessarily complex.

---

# Candidate Evaluation

A major part of the analysis package is evaluating competing plaintext candidates.

The general process is:

```text
Candidate A
     │
     ▼
Score A

Candidate B
     │
     ▼
Score B

Candidate C
     │
     ▼
Score C

     │
     ▼
Compare Scores
     │
     ▼
Rank Candidates
     │
     ▼
Select Strongest Candidate
```

This architecture allows the same scoring system to be reused by multiple cryptanalysis algorithms.

---

# Example: Caesar Brute Force

Suppose the ciphertext is:

```text
KHOOR ZRUOG
```

The brute-force system can generate candidates:

```text
Shift 0
KHOOR ZRUOG

Shift 1
JGNNQ YQTNF

Shift 2
IFMMP XPSME

Shift 3
HELLO WORLD

...

Shift 25
LIPPS ASVPH
```

The scorer evaluates each candidate.

The candidate resembling natural English receives the strongest score.

The result can therefore identify:

```text
Shift: 3
Plaintext: HELLO WORLD
```

without requiring the user to manually test every shift.

---

# Example Usage

## Frequency Analysis

```python
from analysis.frequency import frequency_table

text = "HELLO WORLD"

result = frequency_table(
    text
)

print(result)
```

The exact functions available should be referenced from `frequency.py` and its public API.

---

## Entropy Analysis

```python
from analysis.entropy import entropy

text = "HELLO WORLD"

result = entropy(
    text
)

print(result)
```

---

## IOC Analysis

```python
from analysis.ioc import index_of_coincidence

text = "HELLO WORLD"

result = index_of_coincidence(
    text
)

print(result)
```

---

## N-Gram Analysis

```python
from analysis.ngrams import ngram_score

text = "HELLO WORLD"

result = ngram_score(
    text,
    "TH",
)

print(result)
```

---

## English Scoring

```python
from analysis.scorer import english_score

text = "HELLO WORLD"

score = english_score(
    text
)

print(score)
```

---

## Caesar Brute Force

```python
from analysis.brute_force import (
    brute_force_best,
    brute_force_shift,
)

ciphertext = "KHOOR ZRUOG"

plaintext = brute_force_best(
    ciphertext
)

shift = brute_force_shift(
    ciphertext
)

print(plaintext)
print(shift)
```

---

# Error Handling

Analysis functions should validate their input before performing calculations.

Typical validation includes:

* Confirming that text is a string.
* Confirming that numerical parameters are valid.
* Confirming that candidate collections have the expected structure.
* Confirming that shifts fall within supported ranges.
* Confirming that scoring weights are valid.
* Handling empty input appropriately.

Invalid inputs should raise appropriate Python exceptions or toolkit-specific exceptions where applicable.

---

# Internal Testing

Analysis modules can provide `self_test()` functions for lightweight internal verification.

For example:

```python
from analysis.scorer import self_test

if self_test():
    print("Scorer passed.")
```

These checks provide quick confirmation that core functionality is operating correctly.

They are not a replacement for the formal automated test suite.

The project's `tests/` directory should contain the comprehensive tests for the analysis package.

---

# Testing Strategy

The analysis package should be tested at multiple levels.

## Unit Testing

Individual calculations should be tested independently.

Examples:

```text
frequency calculation
entropy calculation
IOC calculation
n-gram generation
score calculation
```

---

## Integration Testing

Interactions between modules should also be tested.

Examples:

```text
English Data
     │
     ▼
Frequency
     │
     ▼
Scorer
```

and:

```text
Cipher
   │
   ▼
Brute Force
   │
   ▼
Scorer
   │
   ▼
Candidate
```

---

## Edge Cases

Tests should include:

* Empty strings.
* Single-character strings.
* Numbers.
* Symbols.
* Mixed-case text.
* Very short messages.
* Long messages.
* Invalid parameters.
* Invalid candidates.
* Boundary shifts.

---

# Performance Considerations

Most individual analysis calculations are lightweight for normal text sizes.

However, brute-force and candidate-ranking operations can become more computationally expensive as the number of candidates increases.

The general relationship is:

```text
More Candidates
      │
      ▼
More Transformations
      │
      ▼
More Scoring Operations
      │
      ▼
Higher Processing Cost
```

For classical Caesar brute force, the number of candidates is small because there are only 26 possible shifts.

Future cryptanalysis systems involving larger key spaces may require:

* Candidate pruning.
* Parallel processing.
* Efficient scoring.
* Caching.
* Incremental analysis.
* Search heuristics.

---

# Dependency Guidelines

The analysis package should generally follow this dependency direction:

```text
english_data
     │
     ▼
statistical modules
     │
     ├── frequency
     ├── entropy
     ├── ioc
     └── ngrams
            │
            ▼
          scorer
            │
            ▼
       brute_force
            │
            ▼
          Results
```

The analysis package can depend on the `cipher/` package when it needs to perform transformations.

The reverse relationship should generally be avoided.

For example:

```text
Good:

cipher → provides encryption
analysis → evaluates encryption
```

rather than:

```text
Bad:

cipher → depends on analysis
```

This keeps the cryptographic core independent from the cryptanalysis layer.

---

# Future Expansion

The analysis system can eventually support significantly more advanced cryptanalysis.

Potential additions include:

* Automated substitution-cipher solving.
* Vigenère Cipher analysis.
* Frequency-based substitution mapping.
* Dictionary-based plaintext detection.
* Word-pattern analysis.
* Hill-climbing attacks.
* Simulated annealing.
* Language detection.
* Machine-learning-based plaintext scoring.
* Larger n-gram models.
* Statistical cipher identification.
* Automated cipher classification.
* Multi-cipher analysis.
* Visualization of frequency distributions.
* Interactive cryptanalysis tools.

The current architecture provides a foundation for these additions without requiring the existing modules to be rewritten.

---

# Security Considerations

The analysis package is primarily designed for **educational and classical cryptography purposes**.

The algorithms included in this package should not be interpreted as providing modern secure encryption.

Classical ciphers such as:

* Caesar.
* ROT.
* Atbash.
* Classical substitution.
* Similar historical ciphers.

are cryptographically weak by modern standards.

The analysis functionality exists primarily to demonstrate:

* Cryptographic concepts.
* Statistical analysis.
* Classical cryptanalysis.
* Algorithmic reasoning.
* Candidate evaluation.
* Information theory.

The toolkit should not be used as a replacement for modern cryptographic libraries when real-world security is required.

---

# Summary

The `analysis/` package forms the **cryptanalysis and statistical analysis layer** of the Cryptography Toolkit.

Its primary responsibility is to examine text and ciphertext, calculate statistical properties, evaluate English-likeness, and identify likely plaintext candidates.

The package is structured around:

```text
Reference Data
      │
      ▼
Statistical Analysis
      │
      ├── Frequency
      ├── Statistics
      ├── Entropy
      ├── IOC
      └── N-Grams
              │
              ▼
           Scoring
              │
              ▼
        Candidate Ranking
              │
              ▼
         Brute Force
              │
              ▼
       Likely Plaintext
```

The separation between `cipher/` and `analysis/` is particularly important:

```text
cipher/
    │
    │ Performs transformations
    ▼
analysis/
    │
    │ Evaluates transformations
    ▼
Cryptanalysis Results
```

This architecture keeps the Cryptography Toolkit modular, extensible, testable, and suitable for adding more advanced classical cryptanalysis techniques in the future.

```
```
