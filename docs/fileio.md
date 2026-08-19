# FileIO Package Documentation

## Overview

The `fileio` package provides file-handling functionality for the entire Cryptography Toolkit.

It is responsible for managing files and directories, maintaining operation history, exporting results, and creating and restoring backups.

The package is designed to keep file-related operations separate from the cryptographic algorithms and analysis systems.

---

## Package Structure

```text
fileio/
│
├── __init__.py
├── file_manager.py
├── history.py
├── exporters.py
└── backups.py
````

---

# Responsibilities

The `fileio` package is responsible for:

* Reading text files
* Writing text files
* Reading and writing raw bytes
* Appending to files
* Copying files
* Moving files
* Deleting files
* Creating directories
* Searching for files
* Managing encryption and operation history
* Exporting analysis and cracking results
* Exporting history data
* Creating backups
* Restoring backups
* Deleting backups
* Maintaining backup metadata
* Verifying files, directories, exports, history entries, and backups

The package does **not** contain the actual encryption algorithms or cryptanalysis algorithms.

Those responsibilities belong to the `cipher` and `analysis` packages respectively.

---

# Modules

## `file_manager.py`

The `file_manager.py` module provides the core file-management system for the toolkit.

It acts as the primary interface between the rest of the application and the filesystem.

### Main Responsibilities

* Path resolution
* File validation
* Directory validation
* Reading files
* Writing files
* Appending content
* Reading raw bytes
* Writing raw bytes
* Copying files
* Moving files
* Deleting files
* Renaming files
* Listing files
* Listing directories
* Searching for files
* Retrieving file metadata

### Main Class

```python
FileManager
```

The `FileManager` class provides the main object-oriented interface for filesystem operations.

### Important Operations

```python
read_text()
read_lines()
iter_lines()
read_bytes()

write_text()
write_lines()
write_bytes()
append_text()

copy_file()
move_file()
delete_file()
rename_file()

list_files()
list_directories()

find_files()
find_by_extension()
find_by_name()
```

### File Metadata

The module also provides functionality for retrieving:

* File size
* Creation time
* Modification time
* Absolute paths

### Verification

```python
verify_file()
verify_directory()
```

These functions allow the application to safely verify filesystem paths before performing operations.

### Convenience Interface

A default `FileManager` instance is available through:

```python
get_file_manager()
```

Module-level functions provide access to common operations without requiring the caller to manually create a `FileManager`.

---

# `history.py`

The `history.py` module manages the history of cryptographic operations performed by the toolkit.

It provides a structured way to record operations such as encryption, decryption, analysis, and cracking attempts.

## Main Data Model

```python
HistoryEntry
```

A `HistoryEntry` represents one operation performed by the toolkit.

Each entry can contain:

* Operation name
* Cipher name
* Input file
* Output file
* Key
* Success status
* Timestamp
* Additional details

Example structure:

```python
HistoryEntry(
    operation="encrypt",
    cipher="Caesar",
    input_file="input.txt",
    output_file="encrypted.txt",
    key=3,
)
```

---

## `HistoryManager`

```python
HistoryManager
```

The `HistoryManager` maintains the collection of history entries.

### Entry Management

```python
add()
record()
remove()
clear()
get()
all()
latest()
```

### Searching

The manager can search history by:

```python
find_by_operation()
find_by_cipher()
search()
```

It also provides:

```python
successful_entries()
failed_entries()
```

for separating successful and unsuccessful operations.

---

## Persistence

History can be stored and restored using JSON.

```python
save()
load()
save_entry()
record_and_save()
```

The manager can also convert history entries into serializable dictionaries.

```python
to_list()
from_list()
```

---

## Statistics

History statistics are available through:

```python
count_operations()
count_ciphers()
summary()
```

The summary can provide information such as:

* Total entries
* Successful operations
* Failed operations
* Operation counts
* Cipher counts

---

## Exporting History

History can be exported using:

```python
export()
import_history()
```

The history system can therefore work together with the `exporters.py` module when producing reports or external records.

---

# `exporters.py`

The `exporters.py` module provides utilities for exporting toolkit data into common formats.

The currently supported formats are:

```text
TXT
JSON
CSV
```

---

## Main Class

```python
ExportManager
```

The `ExportManager` handles the conversion and writing of data into supported formats.

### Supported Formats

```python
ExportManager.SUPPORTED_FORMATS
```

The manager can also determine a format from a file extension.

```python
format_from_path()
```

---

## Text Export

Plain text can be exported using:

```python
export_text()
```

This is useful for:

* Human-readable reports
* Analysis summaries
* Candidate lists
* Logs
* General textual output

---

## JSON Export

Structured data can be exported using:

```python
export_json()
```

JSON is particularly useful for:

* Analysis results
* History
* Structured statistics
* Configuration-like output
* Machine-readable data

---

## CSV Export

Tabular records can be exported using:

```python
export_csv()
```

CSV is useful for:

* Frequency results
* Candidate rankings
* Statistical results
* Operation records
* Other tabular analysis data

---

# Specialized Export Functions

The exporter provides specialized functions for common toolkit data.

### History

```python
export_history()
```

Exports operation history.

### Analysis

```python
export_analysis()
```

Exports cryptanalysis and statistical results.

### Candidates

```python
export_candidates()
```

Exports brute-force or cracking candidates.

---

# Generic Export

The following function provides a format-independent interface:

```python
export()
```

The format can either be explicitly specified or inferred from the destination file extension.

Example:

```python
export(
    "results.json",
    analysis_results,
)
```

The exporter will determine that JSON should be used from the `.json` extension.

---

# Export Verification

Supported formats can be checked using:

```python
verify_export_format()
```

Output paths can be checked using:

```python
verify_output_path()
```

---

# `backups.py`

The `backups.py` module provides backup functionality for toolkit files.

It allows important files to be copied into a dedicated backup location and later restored.

---

## Main Data Model

```python
BackupMetadata
```

`BackupMetadata` stores information about an individual backup.

It contains:

* Backup name
* Source path
* Destination path
* Creation timestamp
* File size
* Description
* Additional metadata

Example:

```python
BackupMetadata(
    name="encrypted_backup.txt",
    source="encrypted.txt",
    destination="history/backups/encrypted_backup.txt",
)
```

---

# `BackupManager`

```python
BackupManager
```

The `BackupManager` handles the complete backup lifecycle.

### Directory Management

```python
ensure_directory()
```

Ensures that the configured backup directory exists.

### Backup Registration

```python
register_backup()
```

Registers backup metadata with the manager.

### Backup Creation

```python
create_backup()
```

Creates a physical copy of a file and registers its metadata.

Backups can include:

* Custom names
* Descriptions
* Additional metadata
* Overwrite behavior

---

# Backup Restoration

Backups can be restored using:

```python
restore_backup()
```

A backup can also be restored to its original source location using:

```python
restore_to_original()
```

---

# Backup Deletion

Individual backups can be deleted using:

```python
delete_backup()
```

All registered backups can be removed using:

```python
clear_backups()
```

---

# Backup Searching

The backup manager provides:

```python
find_backups()
latest_backups()
```

These functions allow the application to search backup metadata and retrieve recently created backups.

---

# Backup Statistics

The manager provides:

```python
backup_count()
total_size()
summary()
```

These can be used to determine:

* Number of backups
* Total storage used
* Backup directory
* Most recent backup

---

# Backup Persistence

Backup metadata can be serialized using:

```python
to_list()
from_list()
```

It can also be saved and loaded from JSON:

```python
save_metadata()
load_metadata()
```

This allows backup information to persist between application sessions.

---

# Convenience Interfaces

Each major component provides module-level convenience functions.

For example:

```python
from fileio import (
    create_backup,
    restore_backup,
    export_json,
    record_operation,
)
```

This allows other parts of the toolkit to use the file-management systems without directly managing the underlying classes.

---

# Exception Handling

The `fileio` package defines specialized exceptions so that filesystem-related failures can be handled independently from the rest of the application.

## File Manager Exceptions

```python
FileManagerError
FileNotFoundError
FileAlreadyExistsError
InvalidPathError
FileOperationError
```

These handle errors involving filesystem operations.

---

## History Exceptions

```python
HistoryError
InvalidHistoryEntryError
HistoryStorageError
```

These handle invalid history entries and history persistence failures.

---

## Export Exceptions

```python
ExportError
UnsupportedFormatError
InvalidExportDataError
ExportOperationError
```

These handle invalid export data, unsupported formats, and export failures.

---

## Backup Exceptions

```python
BackupError
BackupNotFoundError
BackupAlreadyExistsError
InvalidBackupError
BackupOperationError
```

These handle backup creation, restoration, deletion, and metadata errors.

---

# Package Interface

The `fileio/__init__.py` file exposes the public interfaces of all four modules.

The package can therefore be accessed directly through:

```python
from fileio import *
```

The preferred approach for normal application code is to import only the required components:

```python
from fileio import FileManager
```

or:

```python
from fileio import (
    HistoryManager,
    ExportManager,
    BackupManager,
)
```

---

# Relationship With Other Packages

The `fileio` package acts as a supporting layer for the rest of the Cryptography Toolkit.

```text
                ┌───────────────┐
                │      CLI      │
                └───────┬───────┘
                        │
                ┌───────▼───────┐
                │      GUI      │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │    FileIO     │
                └───────┬───────┘
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
     File Manager    History      Exporters
          │                           │
          └───────────┬───────────────┘
                      ▼
                   Backups
```

The package can receive data from:

* `cipher`
* `analysis`
* `cli`
* `gui`
* `ui`

and handle the filesystem-related operations required by those components.

---

# Design Principles

The `fileio` package follows several design principles.

## Separation of Responsibilities

Each module has a specific purpose:

```text
file_manager.py → Filesystem operations
history.py      → Operation history
exporters.py    → Data exports
backups.py      → Backup management
```

This prevents one large file-handling module from becoming responsible for every type of persistent data.

---

## Reusability

The classes can be instantiated independently when custom configuration is required.

For example:

```python
manager = FileManager()
```

or:

```python
manager = BackupManager(
    backup_directory="history/backups"
)
```

---

## Error Isolation

Specialized exceptions allow higher-level packages to distinguish between different types of failures.

For example:

```python
try:
    export_json(
        "results.json",
        results,
    )

except ExportError:
    ...
```

This prevents filesystem errors from being mixed with cipher or analysis errors.

---

## Persistence

The package provides persistent storage for:

* Operation history
* Backup metadata
* Exported results

This allows information to survive between application sessions.

---

# Testing

Each major module contains a built-in:

```python
self_test()
```

function for basic internal verification.

The broader project test suite should also contain dedicated tests for the `fileio` package.

Recommended coverage includes:

* Reading files
* Writing files
* Copying and moving files
* File deletion
* History creation
* History persistence
* Export formats
* Invalid export data
* Backup creation
* Backup restoration
* Backup deletion
* Backup metadata persistence
* Exception handling

---

# Public API Summary

| Module            | Main Class       | Primary Purpose            |
| ----------------- | ---------------- | -------------------------- |
| `file_manager.py` | `FileManager`    | Core filesystem operations |
| `history.py`      | `HistoryManager` | Operation history          |
| `exporters.py`    | `ExportManager`  | Data and report exports    |
| `backups.py`      | `BackupManager`  | File backup management     |

---

# Usage Examples

## Reading a File

```python
from fileio import read_text

content = read_text(
    "examples/hello_world.txt"
)
```

---

## Writing a File

```python
from fileio import write_text

write_text(
    "output.txt",
    "Cryptography Toolkit",
)
```

---

## Recording an Operation

```python
from fileio import record_operation

record_operation(
    "encrypt",
    cipher="Caesar",
    input_file="input.txt",
    output_file="encrypted.txt",
    key=3,
)
```

---

## Exporting Results

```python
from fileio import export_json

export_json(
    "reports/results.json",
    results,
)
```

---

## Creating a Backup

```python
from fileio import create_backup

create_backup(
    "encrypted.txt",
    name="encrypted_backup.txt",
)
```

---

# Summary

The `fileio` package provides the Cryptography Toolkit with a centralized system for handling persistent files and application data.

Its four primary components are:

```text
file_manager.py
    ↓
Core filesystem operations

history.py
    ↓
Operation tracking and persistence

exporters.py
    ↓
Results and report generation

backups.py
    ↓
Backup creation and restoration
```

Together, these modules provide the storage and file-management layer required by the toolkit while keeping filesystem concerns separate from the encryption and cryptanalysis logic.

```
```

