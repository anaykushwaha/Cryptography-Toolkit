# history.py

# Operation history management for the entire
# Cryptography Toolkit

# Provides functionality for recording,
# retrieving, filtering, and managing
# cryptographic operation history


from __future__ import annotations

from dataclasses import (
    asdict,
    dataclass,
    field,
)
from datetime import (
    datetime,
    timezone,
)
from pathlib import Path
from typing import (
    Any,
    Iterable,
)

from .file_manager import (
    FileManager,
    FileManagerError,
)


# History Exceptions


class HistoryError(Exception):
    # Base exception for history-related errors

    pass


class InvalidHistoryEntryError(HistoryError):
    # Raised when a history entry is invalid

    pass


class HistoryStorageError(HistoryError):
    # Raised when history cannot be stored or loaded

    pass


# History Entry


@dataclass
class HistoryEntry:
    # Represents a single cryptographic operation

    operation: str
    cipher: str = ""
    input_file: str | None = None
    output_file: str | None = None
    key: str | int | None = None
    success: bool = True
    timestamp: str = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        ).isoformat()
    )
    details: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        # Validates and normalizes a history entry

        if not isinstance(
            self.operation,
            str,
        ):
            raise InvalidHistoryEntryError(
                "operation must be a string."
            )

        if not self.operation.strip():
            raise InvalidHistoryEntryError(
                "operation cannot be empty."
            )

        if not isinstance(
            self.cipher,
            str,
        ):
            raise InvalidHistoryEntryError(
                "cipher must be a string."
            )

        if not isinstance(
            self.success,
            bool,
        ):
            raise InvalidHistoryEntryError(
                "success must be a boolean."
            )

        if not isinstance(
            self.details,
            dict,
        ):
            raise InvalidHistoryEntryError(
                "details must be a dictionary."
            )

    def to_dict(self) -> dict[str, Any]:
        # Converts the history entry into a dictionary

        return asdict(
            self
        )

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "HistoryEntry":
        # Creates a history entry from a dictionary

        if not isinstance(
            data,
            dict,
        ):
            raise InvalidHistoryEntryError(
                "History entry data must be a dictionary."
            )

        try:
            return cls(
                operation=data.get(
                    "operation",
                    "",
                ),
                cipher=data.get(
                    "cipher",
                    "",
                ),
                input_file=data.get(
                    "input_file"
                ),
                output_file=data.get(
                    "output_file"
                ),
                key=data.get(
                    "key"
                ),
                success=data.get(
                    "success",
                    True,
                ),
                timestamp=data.get(
                    "timestamp",
                    datetime.now(
                        timezone.utc
                    ).isoformat(),
                ),
                details=data.get(
                    "details",
                    {},
                ),
            )
        except (
            TypeError,
            ValueError,
            InvalidHistoryEntryError,
        ) as error:
            raise InvalidHistoryEntryError(
                "Unable to create history entry."
            ) from error


# History Manager


class HistoryManager:
    # Manages cryptographic operation history

    def __init__(
        self,
        history_file: str | Path | None = None,
        *,
        file_manager: FileManager | None = None,
        max_entries: int | None = None,
    ) -> None:
        # Initializes the history manager

        self.file_manager = (
            file_manager
            if file_manager is not None
            else FileManager()
        )

        if history_file is None:
            history_file = (
                self.file_manager.base_directory
                / "history"
                / "history.json"
            )

        self.history_file = (
            self.file_manager.resolve_path(
                history_file
            )
        )

        if (
            max_entries is not None
            and max_entries < 1
        ):
            raise ValueError(
                "max_entries must be greater than zero."
            )

        self.max_entries = max_entries

        self._entries: list[HistoryEntry] = []

    # Entry Validation

    @staticmethod
    def _validate_entry(
        entry: HistoryEntry,
    ) -> HistoryEntry:
        # Validates a history entry before storage

        if not isinstance(
            entry,
            HistoryEntry,
        ):
            raise InvalidHistoryEntryError(
                "entry must be a HistoryEntry object."
            )

        return entry

    # Entry Management

    def add(
        self,
        entry: HistoryEntry,
    ) -> HistoryEntry:
        # Adds a history entry to the manager

        validated = self._validate_entry(
            entry
        )

        self._entries.append(
            validated
        )

        if (
            self.max_entries is not None
            and len(self._entries)
            > self.max_entries
        ):
            excess = (
                len(self._entries)
                - self.max_entries
            )

            del self._entries[
                :excess
            ]

        return validated

    def record(
        self,
        operation: str,
        *,
        cipher: str = "",
        input_file: str | None = None,
        output_file: str | None = None,
        key: str | int | None = None,
        success: bool = True,
        details: dict[str, Any] | None = None,
    ) -> HistoryEntry:
        # Creates and records a history entry

        entry = HistoryEntry(
            operation=operation,
            cipher=cipher,
            input_file=input_file,
            output_file=output_file,
            key=key,
            success=success,
            details=(
                details
                if details is not None
                else {}
            ),
        )

        return self.add(
            entry
        )

    def remove(
        self,
        index: int,
    ) -> HistoryEntry:
        # Removes and returns a history entry

        if not isinstance(
            index,
            int,
        ):
            raise TypeError(
                "index must be an integer."
            )

        try:
            return self._entries.pop(
                index
            )
        except IndexError as error:
            raise IndexError(
                "History entry index is out of range."
            ) from error

    def clear(self) -> None:
        # Removes all history entries

        self._entries.clear()

    # Entry Access

    def get(
        self,
        index: int,
    ) -> HistoryEntry:
        # Returns a history entry by index

        if not isinstance(
            index,
            int,
        ):
            raise TypeError(
                "index must be an integer."
            )

        try:
            return self._entries[
                index
            ]
        except IndexError as error:
            raise IndexError(
                "History entry index is out of range."
            ) from error

    def all(
        self,
    ) -> list[HistoryEntry]:
        # Returns all history entries

        return list(
            self._entries
        )

    def latest(
        self,
        count: int = 1,
    ) -> list[HistoryEntry]:
        # Returns the most recent history entries

        if not isinstance(
            count,
            int,
        ):
            raise TypeError(
                "count must be an integer."
            )

        if count < 1:
            raise ValueError(
                "count must be greater than zero."
            )

        return list(
            self._entries[
                -count:
            ]
        )

    def __len__(
        self,
    ) -> int:
        # Returns the number of stored entries

        return len(
            self._entries
        )

    def __iter__(
        self,
    ) -> Iterable[HistoryEntry]:
        # Iterates through history entries

        return iter(
            self._entries
        )

    # Searching and Filtering


def find_by_operation(
    self,
    operation: str,
) -> list[HistoryEntry]:
    # Returns entries matching an operation

    if not isinstance(
        operation,
        str,
    ):
        raise TypeError(
            "operation must be a string."
        )

    return [
        entry
        for entry in self._entries
        if entry.operation.lower()
        == operation.lower()
    ]


def find_by_cipher(
    self,
    cipher: str,
) -> list[HistoryEntry]:
    # Returns entries matching a cipher

    if not isinstance(
        cipher,
        str,
    ):
        raise TypeError(
            "cipher must be a string."
        )

    return [
        entry
        for entry in self._entries
        if entry.cipher.lower()
        == cipher.lower()
    ]


def successful_entries(
    self,
) -> list[HistoryEntry]:
    # Returns entries representing successful operations

    return [
        entry
        for entry in self._entries
        if entry.success
    ]


def failed_entries(
    self,
) -> list[HistoryEntry]:
    # Returns entries representing failed operations

    return [
        entry
        for entry in self._entries
        if not entry.success
    ]


def search(
    self,
    query: str,
) -> list[HistoryEntry]:
    # Searches history entries for matching text

    if not isinstance(
        query,
        str,
    ):
        raise TypeError(
            "query must be a string."
        )

    normalized_query = (
        query.strip().lower()
    )

    if not normalized_query:
        return []

    results = []

    for entry in self._entries:
        searchable = " ".join(
            [
                entry.operation,
                entry.cipher,
                entry.input_file or "",
                entry.output_file or "",
                str(entry.key)
                if entry.key is not None
                else "",
                str(entry.details),
            ]
        ).lower()

        if normalized_query in searchable:
            results.append(
                entry
            )

    return results


# Persistence


def to_list(
    self,
) -> list[dict[str, Any]]:
    # Converts all history entries into
    # serializable dictionaries

    return [
        entry.to_dict()
        for entry in self._entries
    ]


def from_list(
    self,
    data: list[dict[str, Any]],
) -> None:
    # Loads history entries from a list of dictionaries

    if not isinstance(
        data,
        list,
    ):
        raise HistoryStorageError(
            "History data must be a list."
        )

    entries = []

    for item in data:
        try:
            entries.append(
                HistoryEntry.from_dict(
                    item
                )
            )
        except InvalidHistoryEntryError as error:
            raise HistoryStorageError(
                "Unable to load a history entry."
            ) from error

    self._entries = entries

    if (
        self.max_entries is not None
        and len(self._entries)
        > self.max_entries
    ):
        self._entries = self._entries[
            -self.max_entries:
        ]


def save(
    self,
) -> Path:
    # Saves history entries to the configured
    # history file

    import json

    data = self.to_list()

    try:
        content = json.dumps(
            data,
            indent=4,
            ensure_ascii=False,
        )

        return self.file_manager.write_text(
            self.history_file,
            content,
            encoding="utf-8",
        )

    except (
        OSError,
        TypeError,
        ValueError,
        FileManagerError,
    ) as error:
        raise HistoryStorageError(
            f"Unable to save history to: "
            f"{self.history_file}"
        ) from error


def load(
    self,
) -> list[HistoryEntry]:
    # Loads history entries from the configured
    # history file

    import json

    if not self.file_manager.exists(
        self.history_file
    ):
        self._entries = []
        return []

    try:
        content = self.file_manager.read_text(
            self.history_file,
            encoding="utf-8",
        )

        if not content.strip():
            self._entries = []
            return []

        data = json.loads(
            content
        )

        self.from_list(
            data
        )

        return self.all()

    except (
        OSError,
        ValueError,
        TypeError,
        FileManagerError,
        HistoryStorageError,
    ) as error:
        raise HistoryStorageError(
            f"Unable to load history from: "
            f"{self.history_file}"
        ) from error


def save_entry(
    self,
    entry: HistoryEntry,
) -> Path:
    # Adds an entry and immediately saves history

    self.add(
        entry
    )

    return self.save()


def record_and_save(
    self,
    operation: str,
    *,
    cipher: str = "",
    input_file: str | None = None,
    output_file: str | None = None,
    key: str | int | None = None,
    success: bool = True,
    details: dict[str, Any] | None = None,
) -> Path:
    # Records an operation and immediately saves history

    self.record(
        operation,
        cipher=cipher,
        input_file=input_file,
        output_file=output_file,
        key=key,
        success=success,
        details=details,
    )

    return self.save()


# Statistics


def count_operations(
    self,
) -> dict[str, int]:
    # Returns the number of entries for each operation

    counts: dict[str, int] = {}

    for entry in self._entries:
        operation = entry.operation

        counts[operation] = (
            counts.get(
                operation,
                0,
            )
            + 1
        )

    return counts


def count_ciphers(
    self,
) -> dict[str, int]:
    # Returns the number of entries for each cipher

    counts: dict[str, int] = {}

    for entry in self._entries:
        if not entry.cipher:
            continue

        cipher = entry.cipher

        counts[cipher] = (
            counts.get(
                cipher,
                0,
            )
            + 1
        )

    return counts


def summary(
    self,
) -> dict[str, Any]:
    # Returns summary information about
    # stored history

    total = len(
        self._entries
    )

    successful = len(
        self.successful_entries()
    )

    failed = len(
        self.failed_entries()
    )

    return {
        "total_entries": total,
        "successful": successful,
        "failed": failed,
        "operations": self.count_operations(),
        "ciphers": self.count_ciphers(),
    }

# History Management


def export(
    self,
    path: str | Path,
) -> Path:
    # Exports the current history to a JSON file

    import json

    destination = self.file_manager.resolve_path(
        path
    )

    try:
        content = json.dumps(
            self.to_list(),
            indent=4,
            ensure_ascii=False,
        )

        return self.file_manager.write_text(
            destination,
            content,
            encoding="utf-8",
        )

    except (
        OSError,
        TypeError,
        ValueError,
        FileManagerError,
    ) as error:
        raise HistoryStorageError(
            f"Unable to export history to: "
            f"{destination}"
        ) from error


def import_history(
    self,
    path: str | Path,
) -> list[HistoryEntry]:
    # Imports history entries from a JSON file

    import json

    source = self.file_manager.require_file(
        path
    )

    try:
        content = self.file_manager.read_text(
            source,
            encoding="utf-8",
        )

        data = json.loads(
            content
        )

        self.from_list(
            data
        )

        return self.all()

    except (
        OSError,
        ValueError,
        TypeError,
        FileManagerError,
        HistoryStorageError,
    ) as error:
        raise HistoryStorageError(
            f"Unable to import history from: "
            f"{source}"
        ) from error


def delete_history_file(
    self,
) -> bool:
    # Deletes the configured history file

    if not self.file_manager.exists(
        self.history_file
    ):
        return False

    try:
        return self.file_manager.delete_file(
            self.history_file
        )
    except FileManagerError as error:
        raise HistoryStorageError(
            f"Unable to delete history file: "
            f"{self.history_file}"
        ) from error


def reset(
    self,
) -> None:
    # Clears in-memory history and removes
    # the persisted history file

    self.clear()

    try:
        self.delete_history_file()
    except HistoryStorageError:
        raise


# Convenience Functions


_default_manager = HistoryManager()


def get_history_manager() -> HistoryManager:
    # Returns the default history manager

    return _default_manager


def record_operation(
    operation: str,
    *,
    cipher: str = "",
    input_file: str | None = None,
    output_file: str | None = None,
    key: str | int | None = None,
    success: bool = True,
    details: dict[str, Any] | None = None,
) -> HistoryEntry:
    # Records an operation using the default manager

    return _default_manager.record(
        operation,
        cipher=cipher,
        input_file=input_file,
        output_file=output_file,
        key=key,
        success=success,
        details=details,
    )


def save_history() -> Path:
    # Saves history using the default manager

    return _default_manager.save()


def load_history() -> list[HistoryEntry]:
    # Loads history using the default manager

    return _default_manager.load()


def get_history() -> list[HistoryEntry]:
    # Returns all history entries

    return _default_manager.all()


def clear_history() -> None:
    # Clears all in-memory history

    _default_manager.clear()


# Verification


def verify_entry(
    entry: HistoryEntry,
) -> bool:
    # Verifies that an object is a valid history entry

    try:
        HistoryManager._validate_entry(
            entry
        )
        return True
    except InvalidHistoryEntryError:
        return False


# Self Test


def self_test() -> bool:
    # Runs a basic internal verification
    # of the history system

    test_file = (
        Path.cwd()
        / ".history_test"
        / "history.json"
    )

    try:
        manager = HistoryManager(
            history_file=test_file
        )

        entry = manager.record(
            "encrypt",
            cipher="Caesar",
            input_file="input.txt",
            output_file="encrypted.txt",
            key=3,
            success=True,
        )

        if len(manager) != 1:
            return False

        if manager.get(0) != entry:
            return False

        if not manager.successful_entries():
            return False

        manager.save()

        loaded = HistoryManager(
            history_file=test_file
        )

        loaded.load()

        if len(loaded) != 1:
            return False

        if loaded.get(0).operation != "encrypt":
            return False

        if loaded.get(0).cipher != "Caesar":
            return False

        return True

    except (
        HistoryError,
        FileManagerError,
    ):
        return False

    finally:
        try:
            if test_file.exists():
                test_file.unlink()

            parent = test_file.parent

            if parent.exists():
                parent.rmdir()

        except OSError:
            pass


# Module Exports


__all__ = [
    # Exceptions
    "HistoryError",
    "InvalidHistoryEntryError",
    "HistoryStorageError",

    # Data Model
    "HistoryEntry",

    # Manager
    "HistoryManager",
    "get_history_manager",

    # Operations
    "record_operation",
    "save_history",
    "load_history",
    "get_history",
    "clear_history",

    # Verification
    "verify_entry",

    # Testing
    "self_test",
]

