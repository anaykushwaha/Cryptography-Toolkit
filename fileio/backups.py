# backups.py

# Backup management utilities for the entire
# Cryptography Toolkit

# Provides functionality for creating,
# restoring, listing, and deleting backups
# of project files and data


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
)


from .file_manager import (
    FileManager,
    FileManagerError,
)


# Backup Exceptions


class BackupError(Exception):
    # Base exception for backup-related errors

    pass


class BackupNotFoundError(BackupError):
    # Raised when a requested backup does not exist

    pass


class BackupAlreadyExistsError(BackupError):
    # Raised when a backup already exists

    pass


class InvalidBackupError(BackupError):
    # Raised when backup information is invalid

    pass


class BackupOperationError(BackupError):
    # Raised when a backup operation fails

    pass


# Backup Metadata


@dataclass
class BackupMetadata:
    # Stores information about a backup

    name: str
    source: str
    destination: str
    created_at: str = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        ).isoformat()
    )
    size: int = 0
    description: str = ""
    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(
        self,
    ) -> None:
        # Validates backup metadata

        if not isinstance(
            self.name,
            str,
        ):
            raise InvalidBackupError(
                "Backup name must be a string."
            )

        if not self.name.strip():
            raise InvalidBackupError(
                "Backup name cannot be empty."
            )

        if not isinstance(
            self.source,
            str,
        ):
            raise InvalidBackupError(
                "Backup source must be a string."
            )

        if not isinstance(
            self.destination,
            str,
        ):
            raise InvalidBackupError(
                "Backup destination must be a string."
            )

        if not isinstance(
            self.size,
            int,
        ):
            raise InvalidBackupError(
                "Backup size must be an integer."
            )

        if self.size < 0:
            raise InvalidBackupError(
                "Backup size cannot be negative."
            )

        if not isinstance(
            self.description,
            str,
        ):
            raise InvalidBackupError(
                "Backup description must be a string."
            )

        if not isinstance(
            self.metadata,
            dict,
        ):
            raise InvalidBackupError(
                "Backup metadata must be a dictionary."
            )

    def to_dict(
        self,
    ) -> dict[str, Any]:
        # Converts backup metadata into a dictionary

        return asdict(
            self
        )

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "BackupMetadata":
        # Creates backup metadata from a dictionary

        if not isinstance(
            data,
            dict,
        ):
            raise InvalidBackupError(
                "Backup metadata must be a dictionary."
            )

        try:
            return cls(
                name=data.get(
                    "name",
                    "",
                ),
                source=data.get(
                    "source",
                    "",
                ),
                destination=data.get(
                    "destination",
                    "",
                ),
                created_at=data.get(
                    "created_at",
                    datetime.now(
                        timezone.utc
                    ).isoformat(),
                ),
                size=data.get(
                    "size",
                    0,
                ),
                description=data.get(
                    "description",
                    "",
                ),
                metadata=data.get(
                    "metadata",
                    {},
                ),
            )

        except (
            TypeError,
            ValueError,
            InvalidBackupError,
        ) as error:
            raise InvalidBackupError(
                "Unable to create backup metadata."
            ) from error


# Backup Manager


class BackupManager:
    # Manages project file backups

    def __init__(
        self,
        backup_directory: str | Path | None = None,
        *,
        file_manager: FileManager | None = None,
        max_backups: int | None = None,
    ) -> None:
        # Initializes the backup manager

        self.file_manager = (
            file_manager
            if file_manager is not None
            else FileManager()
        )

        if backup_directory is None:
            backup_directory = (
                self.file_manager.base_directory
                / "history"
                / "backups"
            )

        self.backup_directory = (
            self.file_manager.resolve_path(
                backup_directory
            )
        )

        if (
            max_backups is not None
            and max_backups < 1
        ):
            raise ValueError(
                "max_backups must be greater than zero."
            )

        self.max_backups = max_backups

        self._backups: list[
            BackupMetadata
        ] = []

    # Backup Validation

    @staticmethod
    def _validate_metadata(
        metadata: BackupMetadata,
    ) -> BackupMetadata:
        # Validates backup metadata

        if not isinstance(
            metadata,
            BackupMetadata,
        ):
            raise InvalidBackupError(
                "metadata must be a BackupMetadata object."
            )

        return metadata

    # Backup Information

    def ensure_directory(
        self,
    ) -> Path:
        # Ensures that the backup directory exists

        try:
            return self.file_manager.create_directory(
                self.backup_directory
            )

        except FileManagerError as error:
            raise BackupOperationError(
                f"Unable to create backup directory: "
                f"{self.backup_directory}"
            ) from error

    def backup_count(
        self,
    ) -> int:
        # Returns the number of registered backups

        return len(
            self._backups
        )

    def all_backups(
        self,
    ) -> list[BackupMetadata]:
        # Returns all registered backup metadata

        return list(
            self._backups
        )

    def get_backup(
        self,
        name: str,
    ) -> BackupMetadata:
        # Returns backup metadata by name

        if not isinstance(
            name,
            str,
        ):
            raise TypeError(
                "name must be a string."
            )

        for backup in self._backups:
            if backup.name == name:
                return backup

        raise BackupNotFoundError(
            f"Backup not found: {name}"
        )

    def register_backup(
        self,
        metadata: BackupMetadata,
    ) -> BackupMetadata:
        # Registers backup metadata

        validated = self._validate_metadata(
            metadata
        )

        for backup in self._backups:
            if backup.name == validated.name:
                raise BackupAlreadyExistsError(
                    f"Backup already exists: "
                    f"{validated.name}"
                )

        self._backups.append(
            validated
        )

        if (
            self.max_backups is not None
            and len(self._backups)
            > self.max_backups
        ):
            excess = (
                len(self._backups)
                - self.max_backups
            )

            del self._backups[
                :excess
            ]

        return validated

    # Backup Creation


def create_backup(
    self,
    source: str | Path,
    *,
    name: str | None = None,
    description: str = "",
    overwrite: bool = False,
    metadata: dict[str, Any] | None = None,
) -> BackupMetadata:
    # Creates a backup of a file

    source_path = self.file_manager.require_file(
        source
    )

    if name is None:
        timestamp = datetime.now(
            timezone.utc
        ).strftime(
            "%Y%m%d_%H%M%S"
        )

        name = (
            f"{source_path.stem}_"
            f"{timestamp}"
        )

    if not isinstance(
        name,
        str,
    ):
        raise TypeError(
            "name must be a string."
        )

    if not name.strip():
        raise InvalidBackupError(
            "Backup name cannot be empty."
        )

    self.ensure_directory()

    destination = (
        self.backup_directory
        / name
    )

    if not destination.suffix:
        destination = destination.with_suffix(
            source_path.suffix
        )

    if (
        destination.exists()
        and not overwrite
    ):
        raise BackupAlreadyExistsError(
            f"Backup already exists: "
            f"{destination}"
        )

    try:
        copied = self.file_manager.copy_file(
            source_path,
            destination,
            overwrite=overwrite,
        )

        size = self.file_manager.get_size(
            copied
        )

    except FileManagerError as error:
        raise BackupOperationError(
            f"Unable to create backup from "
            f"{source_path}"
        ) from error

    backup_metadata = BackupMetadata(
        name=copied.name,
        source=str(
            source_path
        ),
        destination=str(
            copied
        ),
        size=size,
        description=description,
        metadata=(
            metadata
            if metadata is not None
            else {}
        ),
    )

    try:
        self.register_backup(
            backup_metadata
        )
    except BackupAlreadyExistsError:
        if not overwrite:
            raise

        self._backups = [
            backup
            for backup in self._backups
            if backup.name
            != backup_metadata.name
        ]

        self.register_backup(
            backup_metadata
        )

    return backup_metadata


# Backup Restoration


def restore_backup(
    self,
    name: str,
    destination: str | Path,
    *,
    overwrite: bool = False,
) -> Path:
    # Restores a backup to a specified location

    backup = self.get_backup(
        name
    )

    backup_path = self.file_manager.resolve_path(
        backup.destination
    )

    if not backup_path.exists():
        raise BackupNotFoundError(
            f"Backup file does not exist: "
            f"{backup_path}"
        )

    if not backup_path.is_file():
        raise InvalidBackupError(
            f"Backup path is not a file: "
            f"{backup_path}"
        )

    destination_path = (
        self.file_manager.resolve_path(
            destination
        )
    )

    try:
        return self.file_manager.copy_file(
            backup_path,
            destination_path,
            overwrite=overwrite,
        )

    except FileManagerError as error:
        raise BackupOperationError(
            f"Unable to restore backup: "
            f"{name}"
        ) from error


def restore_to_original(
    self,
    name: str,
    *,
    overwrite: bool = False,
) -> Path:
    # Restores a backup to its original source location

    backup = self.get_backup(
        name
    )

    return self.restore_backup(
        name,
        backup.source,
        overwrite=overwrite,
    )


# Backup Deletion


def delete_backup(
    self,
    name: str,
    *,
    missing_ok: bool = False,
) -> bool:
    # Deletes a registered backup

    backup = None

    for item in self._backups:
        if item.name == name:
            backup = item
            break

    if backup is None:
        if missing_ok:
            return False

        raise BackupNotFoundError(
            f"Backup not found: {name}"
        )

    backup_path = self.file_manager.resolve_path(
        backup.destination
    )

    try:
        if backup_path.exists():
            self.file_manager.delete_file(
                backup_path
            )

        self._backups.remove(
            backup
        )

        return True

    except FileManagerError as error:
        raise BackupOperationError(
            f"Unable to delete backup: "
            f"{name}"
        ) from error


def clear_backups(
    self,
) -> int:
    # Deletes all registered backups

    deleted = 0

    for backup in list(
        self._backups
    ):
        try:
            if self.delete_backup(
                backup.name
            ):
                deleted += 1
        except BackupError:
            continue

    return deleted


# Backup Searching


def find_backups(
    self,
    query: str,
) -> list[BackupMetadata]:
    # Searches backups by name, source,
    # or description

    if not isinstance(
        query,
        str,
    ):
        raise TypeError(
            "query must be a string."
        )

    normalized = (
        query.strip().lower()
    )

    if not normalized:
        return []

    results = []

    for backup in self._backups:
        searchable = " ".join(
            [
                backup.name,
                backup.source,
                backup.destination,
                backup.description,
                str(
                    backup.metadata
                ),
            ]
        ).lower()

        if normalized in searchable:
            results.append(
                backup
            )

    return results


def latest_backups(
    self,
    count: int = 1,
) -> list[BackupMetadata]:
    # Returns the most recently registered backups

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
        self._backups[
            -count:
        ]
    )


# Backup Statistics


def total_size(
    self,
) -> int:
    # Returns the combined size of all backups

    return sum(
        backup.size
        for backup in self._backups
    )


def summary(
    self,
) -> dict[str, Any]:
    # Returns summary information about backups

    return {
        "total_backups": len(
            self._backups
        ),
        "total_size": self.total_size(),
        "backup_directory": str(
            self.backup_directory
        ),
        "latest": (
            self._backups[-1].name
            if self._backups
            else None
        ),
    }


# Backup Persistence


def to_list(
    self,
) -> list[dict[str, Any]]:
    # Converts backup metadata into
    # serializable dictionaries

    return [
        backup.to_dict()
        for backup in self._backups
    ]


def from_list(
    self,
    data: list[dict[str, Any]],
) -> None:
    # Loads backup metadata from a list

    if not isinstance(
        data,
        list,
    ):
        raise InvalidBackupError(
            "Backup data must be a list."
        )

    backups = []

    for item in data:
        try:
            backups.append(
                BackupMetadata.from_dict(
                    item
                )
            )
        except InvalidBackupError as error:
            raise InvalidBackupError(
                "Unable to load backup metadata."
            ) from error

    self._backups = backups

    if (
        self.max_backups is not None
        and len(self._backups)
        > self.max_backups
    ):
        self._backups = self._backups[
            -self.max_backups:
        ]

        # Backup Persistence


def save_metadata(
    self,
    path: str | Path | None = None,
) -> Path:
    # Saves registered backup metadata as JSON

    import json

    if path is None:
        path = (
            self.backup_directory
            / "backups.json"
        )

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
        raise BackupOperationError(
            f"Unable to save backup metadata to: "
            f"{destination}"
        ) from error


def load_metadata(
    self,
    path: str | Path | None = None,
) -> list[BackupMetadata]:
    # Loads registered backup metadata from JSON

    import json

    if path is None:
        path = (
            self.backup_directory
            / "backups.json"
        )

    source = self.file_manager.resolve_path(
        path
    )

    if not source.exists():
        self._backups = []
        return []

    try:
        content = self.file_manager.read_text(
            source,
            encoding="utf-8",
        )

        if not content.strip():
            self._backups = []
            return []

        data = json.loads(
            content
        )

        self.from_list(
            data
        )

        return self.all_backups()

    except (
        OSError,
        ValueError,
        TypeError,
        FileManagerError,
        InvalidBackupError,
    ) as error:
        raise BackupOperationError(
            f"Unable to load backup metadata from: "
            f"{source}"
        ) from error


# Convenience Functions


_default_manager = BackupManager()


def get_backup_manager() -> BackupManager:
    # Returns the default backup manager

    return _default_manager


def create_backup(
    source: str | Path,
    *,
    name: str | None = None,
    description: str = "",
    overwrite: bool = False,
    metadata: dict[str, Any] | None = None,
) -> BackupMetadata:
    # Creates a backup using the default manager

    return _default_manager.create_backup(
        source,
        name=name,
        description=description,
        overwrite=overwrite,
        metadata=metadata,
    )


def restore_backup(
    name: str,
    destination: str | Path,
    *,
    overwrite: bool = False,
) -> Path:
    # Restores a backup using the default manager

    return _default_manager.restore_backup(
        name,
        destination,
        overwrite=overwrite,
    )


def delete_backup(
    name: str,
    *,
    missing_ok: bool = False,
) -> bool:
    # Deletes a backup using the default manager

    return _default_manager.delete_backup(
        name,
        missing_ok=missing_ok,
    )


def list_backups() -> list[BackupMetadata]:
    # Returns all backups using the default manager

    return _default_manager.all_backups()


def save_backups(
    path: str | Path | None = None,
) -> Path:
    # Saves backup metadata using the default manager

    return _default_manager.save_metadata(
        path
    )


def load_backups(
    path: str | Path | None = None,
) -> list[BackupMetadata]:
    # Loads backup metadata using the default manager

    return _default_manager.load_metadata(
        path
    )


# Verification


def verify_backup(
    name: str,
) -> bool:
    # Verifies that a registered backup exists

    try:
        backup = _default_manager.get_backup(
            name
        )

        path = _default_manager.file_manager.resolve_path(
            backup.destination
        )

        return path.exists() and path.is_file()

    except (
        BackupError,
        FileManagerError,
    ):
        return False


# Self Test


def self_test() -> bool:
    # Runs a basic internal verification
    # of the backup system

    test_directory = (
        Path.cwd()
        / ".backup_test"
    )

    source_file = (
        test_directory
        / "source.txt"
    )

    backup_directory = (
        test_directory
        / "backups"
    )

    restored_file = (
        test_directory
        / "restored.txt"
    )

    try:
        file_manager = FileManager()

        file_manager.create_directory(
            test_directory
        )

        file_manager.write_text(
            source_file,
            "Cryptography Toolkit",
        )

        manager = BackupManager(
            backup_directory=backup_directory,
            file_manager=file_manager,
        )

        backup = manager.create_backup(
            source_file,
            name="test_backup.txt",
        )

        if not manager.verify_backup(
            backup.name
        ) if hasattr(
            manager,
            "verify_backup",
        ) else False:
            return False

        if manager.backup_count() != 1:
            return False

        if manager.total_size() <= 0:
            return False

        manager.restore_backup(
            backup.name,
            restored_file,
        )

        if not restored_file.exists():
            return False

        restored_content = (
            file_manager.read_text(
                restored_file
            )
        )

        if restored_content != "Cryptography Toolkit":
            return False

        manager.save_metadata()

        manager.delete_backup(
            backup.name
        )

        return manager.backup_count() == 0

    except (
        BackupError,
        FileManagerError,
    ):
        return False

    finally:
        try:
            if restored_file.exists():
                restored_file.unlink()

            if source_file.exists():
                source_file.unlink()

            metadata_file = (
                backup_directory
                / "backups.json"
            )

            if metadata_file.exists():
                metadata_file.unlink()

            if backup_directory.exists():
                backup_directory.rmdir()

            if test_directory.exists():
                test_directory.rmdir()

        except OSError:
            pass


# Module Exports


__all__ = [
    # Exceptions
    "BackupError",
    "BackupNotFoundError",
    "BackupAlreadyExistsError",
    "InvalidBackupError",
    "BackupOperationError",

    # Data Model
    "BackupMetadata",

    # Manager
    "BackupManager",
    "get_backup_manager",

    # Operations
    "create_backup",
    "restore_backup",
    "delete_backup",
    "list_backups",

    # Persistence
    "save_backups",
    "load_backups",

    # Verification
    "verify_backup",

    # Testing
    "self_test",
]