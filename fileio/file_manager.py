# file_manager.py

# File management utilities for the entire
# Cryptography Toolkit

# Provides safe and reusable functionality
# for reading, writing, copying, moving,
# deleting, and inspecting project files


from __future__ import annotations

from pathlib import Path
from typing import (
    Iterable,
    Iterator,
)


# File Manager Exceptions


class FileManagerError(Exception):
    # Base exception for file management errors

    pass


class FileNotFoundError(FileManagerError):
    # Raised when a requested file does not exist

    pass


class FileAlreadyExistsError(FileManagerError):
    # Raised when a file already exists and
    # overwriting is not permitted

    pass


class InvalidPathError(FileManagerError):
    # Raised when a supplied path is invalid

    pass


class FileOperationError(FileManagerError):
    # Raised when a file operation cannot be completed

    pass


# File Manager


class FileManager:
    # Provides centralized file management functionality

    def __init__(
        self,
        base_directory: str | Path | None = None,
    ) -> None:
        # Initializes the file manager

        if base_directory is None:
            self.base_directory = Path.cwd()
        else:
            self.base_directory = Path(
                base_directory
            ).expanduser()

        self.base_directory = (
            self.base_directory.resolve()
        )

    # Path Handling

    def resolve_path(
        self,
        path: str | Path,
    ) -> Path:
        # Resolves a path relative to the
        # configured base directory

        if not isinstance(
            path,
            (str, Path),
        ):
            raise InvalidPathError(
                "Path must be a string or Path object."
            )

        candidate = Path(
            path
        ).expanduser()

        if not candidate.is_absolute():
            candidate = (
                self.base_directory / candidate
            )

        try:
            return candidate.resolve()
        except (
            OSError,
            RuntimeError,
        ) as error:
            raise InvalidPathError(
                f"Unable to resolve path: {path}"
            ) from error

    def exists(
        self,
        path: str | Path,
    ) -> bool:
        # Checks whether a path exists

        resolved = self.resolve_path(
            path
        )

        return resolved.exists()

    def is_file(
        self,
        path: str | Path,
    ) -> bool:
        # Checks whether a path points to a file

        resolved = self.resolve_path(
            path
        )

        return resolved.is_file()

    def is_directory(
        self,
        path: str | Path,
    ) -> bool:
        # Checks whether a path points to a directory

        resolved = self.resolve_path(
            path
        )

        return resolved.is_dir()

    # Directory Handling

    def create_directory(
        self,
        path: str | Path,
    ) -> Path:
        # Creates a directory if it does not already exist

        resolved = self.resolve_path(
            path
        )

        try:
            resolved.mkdir(
                parents=True,
                exist_ok=True,
            )
        except OSError as error:
            raise FileOperationError(
                f"Unable to create directory: {resolved}"
            ) from error

        return resolved

    def ensure_parent_directory(
        self,
        path: str | Path,
    ) -> Path:
        # Ensures that the parent directory
        # of a file exists

        resolved = self.resolve_path(
            path
        )

        try:
            resolved.parent.mkdir(
                parents=True,
                exist_ok=True,
            )
        except OSError as error:
            raise FileOperationError(
                f"Unable to create parent directory: "
                f"{resolved.parent}"
            ) from error

        return resolved

    # File Information

    def get_size(
        self,
        path: str | Path,
    ) -> int:
        # Returns the size of a file in bytes

        resolved = self.resolve_path(
            path
        )

        if not resolved.exists():
            raise FileNotFoundError(
                f"File does not exist: {resolved}"
            )

        if not resolved.is_file():
            raise InvalidPathError(
                f"Path is not a file: {resolved}"
            )

        try:
            return resolved.stat().st_size
        except OSError as error:
            raise FileOperationError(
                f"Unable to determine file size: "
                f"{resolved}"
            ) from error

    def get_extension(
        self,
        path: str | Path,
    ) -> str:
        # Returns the file extension without the dot

        resolved = self.resolve_path(
            path
        )

        return resolved.suffix.lstrip(
            "."
        )

    def get_name(
        self,
        path: str | Path,
    ) -> str:
        # Returns the file name

        resolved = self.resolve_path(
            path
        )

        return resolved.name

    def get_parent(
        self,
        path: str | Path,
    ) -> Path:
        # Returns the parent directory of a path

        resolved = self.resolve_path(
            path
        )

        return resolved.parent

    # File Validation

    def require_file(
        self,
        path: str | Path,
    ) -> Path:
        # Ensures that a path exists and is a file

        resolved = self.resolve_path(
            path
        )

        if not resolved.exists():
            raise FileNotFoundError(
                f"File does not exist: {resolved}"
            )

        if not resolved.is_file():
            raise InvalidPathError(
                f"Path is not a file: {resolved}"
            )

        return resolved

    def require_directory(
        self,
        path: str | Path,
    ) -> Path:
        # Ensures that a path exists and is a directory

        resolved = self.resolve_path(
            path
        )

        if not resolved.exists():
            raise FileNotFoundError(
                f"Directory does not exist: {resolved}"
            )

        if not resolved.is_dir():
            raise InvalidPathError(
                f"Path is not a directory: {resolved}"
            )

        return resolved 

    # Reading Files


def read_text(
    self,
    path: str | Path,
    *,
    encoding: str = "utf-8",
) -> str:
    # Reads a text file and returns its contents

    resolved = self.require_file(
        path
    )

    try:
        return resolved.read_text(
            encoding=encoding
        )
    except (
        OSError,
        UnicodeError,
    ) as error:
        raise FileOperationError(
            f"Unable to read file: {resolved}"
        ) from error


def read_lines(
    self,
    path: str | Path,
    *,
    encoding: str = "utf-8",
    keepends: bool = False,
) -> list[str]:
    # Reads a text file and returns its contents
    # as a list of lines

    resolved = self.require_file(
        path
    )

    try:
        with resolved.open(
            "r",
            encoding=encoding,
        ) as file:
            return file.readlines(
                keepends=keepends
            )
    except (
        OSError,
        UnicodeError,
    ) as error:
        raise FileOperationError(
            f"Unable to read lines from file: "
            f"{resolved}"
        ) from error


def iter_lines(
    self,
    path: str | Path,
    *,
    encoding: str = "utf-8",
) -> Iterator[str]:
    # Iterates over a text file one line at a time

    resolved = self.require_file(
        path
    )

    try:
        with resolved.open(
            "r",
            encoding=encoding,
        ) as file:
            for line in file:
                yield line
    except (
        OSError,
        UnicodeError,
    ) as error:
        raise FileOperationError(
            f"Unable to iterate through file: "
            f"{resolved}"
        ) from error


def read_bytes(
    self,
    path: str | Path,
) -> bytes:
    # Reads a file as raw bytes

    resolved = self.require_file(
        path
    )

    try:
        return resolved.read_bytes()
    except OSError as error:
        raise FileOperationError(
            f"Unable to read bytes from file: "
            f"{resolved}"
        ) from error


# Writing Files


def write_text(
    self,
    path: str | Path,
    content: str,
    *,
    encoding: str = "utf-8",
    overwrite: bool = True,
) -> Path:
    # Writes text content to a file

    if not isinstance(
        content,
        str,
    ):
        raise TypeError(
            "content must be a string."
        )

    resolved = self.resolve_path(
        path
    )

    if (
        resolved.exists()
        and not overwrite
    ):
        raise FileAlreadyExistsError(
            f"File already exists: {resolved}"
        )

    self.ensure_parent_directory(
        resolved
    )

    try:
        resolved.write_text(
            content,
            encoding=encoding,
        )
    except (
        OSError,
        UnicodeError,
    ) as error:
        raise FileOperationError(
            f"Unable to write file: "
            f"{resolved}"
        ) from error

    return resolved


def write_lines(
    self,
    path: str | Path,
    lines: Iterable[str],
    *,
    encoding: str = "utf-8",
    overwrite: bool = True,
) -> Path:
    # Writes an iterable of strings to a text file

    resolved = self.resolve_path(
        path
    )

    if (
        resolved.exists()
        and not overwrite
    ):
        raise FileAlreadyExistsError(
            f"File already exists: {resolved}"
        )

    self.ensure_parent_directory(
        resolved
    )

    try:
        with resolved.open(
            "w",
            encoding=encoding,
        ) as file:
            for line in lines:
                if not isinstance(
                    line,
                    str,
                ):
                    raise TypeError(
                        "Every line must be a string."
                    )

                file.write(
                    line
                )

    except (
        OSError,
        UnicodeError,
    ) as error:
        raise FileOperationError(
            f"Unable to write lines to file: "
            f"{resolved}"
        ) from error

    return resolved


def append_text(
    self,
    path: str | Path,
    content: str,
    *,
    encoding: str = "utf-8",
) -> Path:
    # Appends text content to a file

    if not isinstance(
        content,
        str,
    ):
        raise TypeError(
            "content must be a string."
        )

    resolved = self.resolve_path(
        path
    )

    self.ensure_parent_directory(
        resolved
    )

    try:
        with resolved.open(
            "a",
            encoding=encoding,
        ) as file:
            file.write(
                content
            )
    except (
        OSError,
        UnicodeError,
    ) as error:
        raise FileOperationError(
            f"Unable to append to file: "
            f"{resolved}"
        ) from error

    return resolved


def write_bytes(
    self,
    path: str | Path,
    content: bytes,
    *,
    overwrite: bool = True,
) -> Path:
    # Writes raw bytes to a file

    if not isinstance(
        content,
        bytes,
    ):
        raise TypeError(
            "content must be bytes."
        )

    resolved = self.resolve_path(
        path
    )

    if (
        resolved.exists()
        and not overwrite
    ):
        raise FileAlreadyExistsError(
            f"File already exists: {resolved}"
        )

    self.ensure_parent_directory(
        resolved
    )

    try:
        resolved.write_bytes(
            content
        )
    except OSError as error:
        raise FileOperationError(
            f"Unable to write bytes to file: "
            f"{resolved}"
        ) from error

    return resolved


# File Management


def copy_file(
    self,
    source: str | Path,
    destination: str | Path,
    *,
    overwrite: bool = False,
) -> Path:
    # Copies a file to another location

    source_path = self.require_file(
        source
    )

    destination_path = self.resolve_path(
        destination
    )

    if (
        destination_path.exists()
        and not overwrite
    ):
        raise FileAlreadyExistsError(
            f"Destination already exists: "
            f"{destination_path}"
        )

    self.ensure_parent_directory(
        destination_path
    )

    try:
        import shutil

        shutil.copy2(
            source_path,
            destination_path,
        )
    except OSError as error:
        raise FileOperationError(
            f"Unable to copy file from "
            f"{source_path} to "
            f"{destination_path}"
        ) from error

    return destination_path 

# File Management


def move_file(
    self,
    source: str | Path,
    destination: str | Path,
    *,
    overwrite: bool = False,
) -> Path:
    # Moves a file to another location

    source_path = self.require_file(
        source
    )

    destination_path = self.resolve_path(
        destination
    )

    if (
        destination_path.exists()
        and not overwrite
    ):
        raise FileAlreadyExistsError(
            f"Destination already exists: "
            f"{destination_path}"
        )

    self.ensure_parent_directory(
        destination_path
    )

    try:
        import shutil

        if (
            destination_path.exists()
            and overwrite
        ):
            destination_path.unlink()

        shutil.move(
            str(source_path),
            str(destination_path),
        )
    except OSError as error:
        raise FileOperationError(
            f"Unable to move file from "
            f"{source_path} to "
            f"{destination_path}"
        ) from error

    return destination_path


def delete_file(
    self,
    path: str | Path,
    *,
    missing_ok: bool = False,
) -> bool:
    # Deletes a file

    resolved = self.resolve_path(
        path
    )

    if not resolved.exists():
        if missing_ok:
            return False

        raise FileNotFoundError(
            f"File does not exist: {resolved}"
        )

    if not resolved.is_file():
        raise InvalidPathError(
            f"Path is not a file: {resolved}"
        )

    try:
        resolved.unlink()
    except OSError as error:
        raise FileOperationError(
            f"Unable to delete file: "
            f"{resolved}"
        ) from error

    return True


def rename_file(
    self,
    path: str | Path,
    new_name: str,
    *,
    overwrite: bool = False,
) -> Path:
    # Renames a file without changing
    # its parent directory

    if not isinstance(
        new_name,
        str,
    ):
        raise TypeError(
            "new_name must be a string."
        )

    if not new_name.strip():
        raise InvalidPathError(
            "New file name cannot be empty."
        )

    source_path = self.require_file(
        path
    )

    destination_path = (
        source_path.parent / new_name
    )

    if (
        destination_path.exists()
        and not overwrite
    ):
        raise FileAlreadyExistsError(
            f"File already exists: "
            f"{destination_path}"
        )

    try:
        if (
            destination_path.exists()
            and overwrite
        ):
            destination_path.unlink()

        return source_path.rename(
            destination_path
        )
    except OSError as error:
        raise FileOperationError(
            f"Unable to rename file: "
            f"{source_path}"
        ) from error


# Directory Listing


def list_files(
    self,
    directory: str | Path = ".",
    *,
    recursive: bool = False,
    pattern: str = "*",
) -> list[Path]:
    # Returns files contained within a directory

    resolved = self.require_directory(
        directory
    )

    try:
        if recursive:
            paths = resolved.rglob(
                pattern
            )
        else:
            paths = resolved.glob(
                pattern
            )

        return sorted(
            path
            for path in paths
            if path.is_file()
        )

    except OSError as error:
        raise FileOperationError(
            f"Unable to list files in: "
            f"{resolved}"
        ) from error


def list_directories(
    self,
    directory: str | Path = ".",
    *,
    recursive: bool = False,
) -> list[Path]:
    # Returns directories contained within
    # another directory

    resolved = self.require_directory(
        directory
    )

    try:
        if recursive:
            paths = resolved.rglob(
                "*"
            )
        else:
            paths = resolved.iterdir()

        return sorted(
            path
            for path in paths
            if path.is_dir()
        )

    except OSError as error:
        raise FileOperationError(
            f"Unable to list directories in: "
            f"{resolved}"
        ) from error


# File Searching


def find_files(
    self,
    directory: str | Path = ".",
    *,
    pattern: str = "*",
    recursive: bool = True,
) -> list[Path]:
    # Finds files matching a specified pattern

    return self.list_files(
        directory,
        recursive=recursive,
        pattern=pattern,
    )


def find_by_extension(
    self,
    directory: str | Path = ".",
    extension: str = "",
    *,
    recursive: bool = True,
) -> list[Path]:
    # Finds files with a specific extension

    if not isinstance(
        extension,
        str,
    ):
        raise TypeError(
            "extension must be a string."
        )

    normalized = extension.lower()

    if normalized and not normalized.startswith(
        "."
    ):
        normalized = "." + normalized

    files = self.list_files(
        directory,
        recursive=recursive,
    )

    return [
        path
        for path in files
        if path.suffix.lower()
        == normalized
    ]


def find_by_name(
    self,
    directory: str | Path = ".",
    name: str = "",
    *,
    recursive: bool = True,
) -> list[Path]:
    # Finds files with an exact file name

    if not isinstance(
        name,
        str,
    ):
        raise TypeError(
            "name must be a string."
        )

    if not name:
        raise ValueError(
            "name cannot be empty."
        )

    files = self.list_files(
        directory,
        recursive=recursive,
    )

    return [
        path
        for path in files
        if path.name == name
    ]


# File Metadata


def get_modified_time(
    self,
    path: str | Path,
) -> float:
    # Returns the last modification time
    # as a Unix timestamp

    resolved = self.require_file(
        path
    )

    try:
        return resolved.stat().st_mtime
    except OSError as error:
        raise FileOperationError(
            f"Unable to determine modification "
            f"time: {resolved}"
        ) from error


def get_created_time(
    self,
    path: str | Path,
) -> float:
    # Returns the creation time
    # as a Unix timestamp

    resolved = self.require_file(
        path
    )

    try:
        return resolved.stat().st_ctime
    except OSError as error:
        raise FileOperationError(
            f"Unable to determine creation "
            f"time: {resolved}"
        ) from error


def get_absolute_path(
    self,
    path: str | Path,
) -> str:
    # Returns the absolute path as a string

    return str(
        self.resolve_path(
            path
        )
    )


# Module-Level File Manager


_default_manager = FileManager()


def get_file_manager() -> FileManager:
    # Returns the default FileManager instance

    return _default_manager

# Convenience Functions


def resolve_path(
    path: str | Path,
) -> Path:
    # Resolves a path using the default file manager

    return _default_manager.resolve_path(
        path
    )


def read_text(
    path: str | Path,
    *,
    encoding: str = "utf-8",
) -> str:
    # Reads a text file using the default file manager

    return _default_manager.read_text(
        path,
        encoding=encoding,
    )


def read_lines(
    path: str | Path,
    *,
    encoding: str = "utf-8",
    keepends: bool = False,
) -> list[str]:
    # Reads lines from a text file using
    # the default file manager

    return _default_manager.read_lines(
        path,
        encoding=encoding,
        keepends=keepends,
    )


def read_bytes(
    path: str | Path,
) -> bytes:
    # Reads raw bytes using the default file manager

    return _default_manager.read_bytes(
        path
    )


def write_text(
    path: str | Path,
    content: str,
    *,
    encoding: str = "utf-8",
    overwrite: bool = True,
) -> Path:
    # Writes text using the default file manager

    return _default_manager.write_text(
        path,
        content,
        encoding=encoding,
        overwrite=overwrite,
    )


def write_bytes(
    path: str | Path,
    content: bytes,
    *,
    overwrite: bool = True,
) -> Path:
    # Writes raw bytes using the default file manager

    return _default_manager.write_bytes(
        path,
        content,
        overwrite=overwrite,
    )


def append_text(
    path: str | Path,
    content: str,
    *,
    encoding: str = "utf-8",
) -> Path:
    # Appends text using the default file manager

    return _default_manager.append_text(
        path,
        content,
        encoding=encoding,
    )


def copy_file(
    source: str | Path,
    destination: str | Path,
    *,
    overwrite: bool = False,
) -> Path:
    # Copies a file using the default file manager

    return _default_manager.copy_file(
        source,
        destination,
        overwrite=overwrite,
    )


def move_file(
    source: str | Path,
    destination: str | Path,
    *,
    overwrite: bool = False,
) -> Path:
    # Moves a file using the default file manager

    return _default_manager.move_file(
        source,
        destination,
        overwrite=overwrite,
    )


def delete_file(
    path: str | Path,
    *,
    missing_ok: bool = False,
) -> bool:
    # Deletes a file using the default file manager

    return _default_manager.delete_file(
        path,
        missing_ok=missing_ok,
    )


def create_directory(
    path: str | Path,
) -> Path:
    # Creates a directory using the default file manager

    return _default_manager.create_directory(
        path
    )


def list_files(
    directory: str | Path = ".",
    *,
    recursive: bool = False,
    pattern: str = "*",
) -> list[Path]:
    # Lists files using the default file manager

    return _default_manager.list_files(
        directory,
        recursive=recursive,
        pattern=pattern,
    )


def find_files(
    directory: str | Path = ".",
    *,
    pattern: str = "*",
    recursive: bool = True,
) -> list[Path]:
    # Finds files using the default file manager

    return _default_manager.find_files(
        directory,
        pattern=pattern,
        recursive=recursive,
    )


# Verification


def verify_file(
    path: str | Path,
) -> bool:
    # Verifies that a path exists and is a file

    try:
        _default_manager.require_file(
            path
        )
        return True
    except FileManagerError:
        return False


def verify_directory(
    path: str | Path,
) -> bool:
    # Verifies that a path exists and is a directory

    try:
        _default_manager.require_directory(
            path
        )
        return True
    except FileManagerError:
        return False


# Statistics


def file_summary(
    path: str | Path,
) -> dict:
    # Returns basic information about a file

    resolved = _default_manager.require_file(
        path
    )

    return {
        "name": resolved.name,
        "path": str(resolved),
        "extension": resolved.suffix.lstrip(
            "."
        ),
        "size": _default_manager.get_size(
            resolved
        ),
        "parent": str(
            resolved.parent
        ),
        "modified": _default_manager.get_modified_time(
            resolved
        ),
        "created": _default_manager.get_created_time(
            resolved
        ),
    }


# Self Test


def self_test() -> bool:
    # Runs a basic internal verification
    # of the file manager

    manager = FileManager()

    try:
        test_directory = (
            manager.base_directory
            / ".file_manager_test"
        )

        test_file = (
            test_directory
            / "test.txt"
        )

        manager.create_directory(
            test_directory
        )

        manager.write_text(
            test_file,
            "Cryptography Toolkit",
        )

        if not manager.exists(
            test_file
        ):
            return False

        if not manager.is_file(
            test_file
        ):
            return False

        content = manager.read_text(
            test_file
        )

        if content != "Cryptography Toolkit":
            return False

        if manager.get_size(
            test_file
        ) <= 0:
            return False

        manager.delete_file(
            test_file
        )

        return not manager.exists(
            test_file
        )

    except FileManagerError:
        return False

    finally:
        try:
            if test_directory.exists():
                test_directory.rmdir()
        except OSError:
            pass


# Module Exports


__all__ = [
    # Exceptions
    "FileManagerError",
    "FileNotFoundError",
    "FileAlreadyExistsError",
    "InvalidPathError",
    "FileOperationError",

    # Main Class
    "FileManager",

    # Manager
    "get_file_manager",

    # Path Handling
    "resolve_path",

    # Reading
    "read_text",
    "read_lines",
    "read_bytes",

    # Writing
    "write_text",
    "write_bytes",
    "append_text",

    # File Management
    "copy_file",
    "move_file",
    "delete_file",
    "create_directory",

    # Searching
    "list_files",
    "find_files",

    # Verification
    "verify_file",
    "verify_directory",

    # Statistics
    "file_summary",

    # Testing
    "self_test",
]

