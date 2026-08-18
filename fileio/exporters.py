# exporters.py

# Export utilities for the entire
# Cryptography Toolkit

# Provides reusable functionality for exporting
# encryption results, analysis results,
# history records, and other project data
# into common file formats


from __future__ import annotations

import csv
import json

from pathlib import Path
from typing import (
    Any,
    Iterable,
    Mapping,
    Sequence,
)

from .file_manager import (
    FileManager,
    FileManagerError,
)


# Export Exceptions


class ExportError(Exception):
    # Base exception for export-related errors

    pass


class UnsupportedFormatError(ExportError):
    # Raised when an unsupported export format
    # is requested

    pass


class InvalidExportDataError(ExportError):
    # Raised when supplied export data is invalid

    pass


class ExportOperationError(ExportError):
    # Raised when an export operation fails

    pass


# Export Manager


class ExportManager:
    # Manages exporting data into supported formats

    SUPPORTED_FORMATS = (
        "txt",
        "json",
        "csv",
    )

    def __init__(
        self,
        *,
        file_manager: FileManager | None = None,
    ) -> None:
        # Initializes the export manager

        self.file_manager = (
            file_manager
            if file_manager is not None
            else FileManager()
        )

    # Format Handling

    @classmethod
    def normalize_format(
        cls,
        format_name: str,
    ) -> str:
        # Normalizes and validates an export format

        if not isinstance(
            format_name,
            str,
        ):
            raise UnsupportedFormatError(
                "Export format must be a string."
            )

        normalized = (
            format_name
            .strip()
            .lower()
            .lstrip(".")
        )

        if normalized not in cls.SUPPORTED_FORMATS:
            raise UnsupportedFormatError(
                f"Unsupported export format: "
                f"{format_name}"
            )

        return normalized

    @classmethod
    def format_from_path(
        cls,
        path: str | Path,
    ) -> str:
        # Determines the export format from a file extension

        extension = Path(
            path
        ).suffix.lstrip(
            "."
        ).lower()

        if not extension:
            raise UnsupportedFormatError(
                "Unable to determine export format "
                "from path."
            )

        return cls.normalize_format(
            extension
        )

    @classmethod
    def supported_formats(
        cls,
    ) -> tuple[str, ...]:
        # Returns all supported export formats

        return cls.SUPPORTED_FORMATS

    # Data Validation

    @staticmethod
    def validate_data(
        data: Any,
    ) -> Any:
        # Validates that export data is not None

        if data is None:
            raise InvalidExportDataError(
                "Export data cannot be None."
            )

        return data

    @staticmethod
    def normalize_records(
        records: Iterable[Mapping[str, Any]],
    ) -> list[dict[str, Any]]:
        # Converts a collection of mappings into
        # serializable dictionaries

        if isinstance(
            records,
            (str, bytes),
        ):
            raise InvalidExportDataError(
                "Records must be an iterable of mappings."
            )

        normalized = []

        try:
            for record in records:
                if not isinstance(
                    record,
                    Mapping,
                ):
                    raise InvalidExportDataError(
                        "Every record must be a mapping."
                    )

                normalized.append(
                    dict(record)
                )

        except TypeError as error:
            raise InvalidExportDataError(
                "Records must be iterable."
            ) from error

        return normalized

    # Text Export

    def export_text(
        self,
        path: str | Path,
        content: str,
        *,
        encoding: str = "utf-8",
        overwrite: bool = True,
    ) -> Path:
        # Exports plain text content

        if not isinstance(
            content,
            str,
        ):
            raise InvalidExportDataError(
                "Text export content must be a string."
            )

        destination = self.file_manager.resolve_path(
            path
        )

        try:
            return self.file_manager.write_text(
                destination,
                content,
                encoding=encoding,
                overwrite=overwrite,
            )

        except FileManagerError as error:
            raise ExportOperationError(
                f"Unable to export text to: "
                f"{destination}"
            ) from error

    # JSON Export

    def export_json(
        self,
        path: str | Path,
        data: Any,
        *,
        indent: int = 4,
        encoding: str = "utf-8",
        overwrite: bool = True,
    ) -> Path:
        # Exports data as JSON

        self.validate_data(
            data
        )

        destination = self.file_manager.resolve_path(
            path
        )

        try:
            content = json.dumps(
                data,
                indent=indent,
                ensure_ascii=False,
            )

        except (
            TypeError,
            ValueError,
        ) as error:
            raise InvalidExportDataError(
                "Data cannot be serialized as JSON."
            ) from error

        try:
            return self.file_manager.write_text(
                destination,
                content,
                encoding=encoding,
                overwrite=overwrite,
            )

        except FileManagerError as error:
            raise ExportOperationError(
                f"Unable to export JSON to: "
                f"{destination}"
            ) from error

    # CSV Export

    def export_csv(
        self,
        path: str | Path,
        records: Iterable[Mapping[str, Any]],
        *,
        fieldnames: Sequence[str] | None = None,
        encoding: str = "utf-8",
        overwrite: bool = True,
    ) -> Path:
        # Exports a collection of records as CSV

        normalized_records = (
            self.normalize_records(
                records
            )
        )

        if fieldnames is None:
            if not normalized_records:
                raise InvalidExportDataError(
                    "Field names are required when "
                    "exporting empty records."
                )

            fieldnames = list(
                normalized_records[0].keys()
            )
        else:
            fieldnames = list(
                fieldnames
            )

        if not fieldnames:
            raise InvalidExportDataError(
                "CSV field names cannot be empty."
            )

        destination = self.file_manager.resolve_path(
            path
        )

        try:
            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            with destination.open(
                "w",
                newline="",
                encoding=encoding,
            ) as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=fieldnames,
                    extrasaction="ignore",
                )

                writer.writeheader()

                for record in normalized_records:
                    writer.writerow(
                        record
                    )

        except (
            OSError,
            UnicodeError,
            csv.Error,
        ) as error:
            raise ExportOperationError(
                f"Unable to export CSV to: "
                f"{destination}"
            ) from error

        return destination 

    # Specialized Exports


def export_history(
    self,
    path: str | Path,
    entries: Iterable[Mapping[str, Any]],
    *,
    format_name: str | None = None,
    encoding: str = "utf-8",
    overwrite: bool = True,
) -> Path:
    # Exports operation history in the requested format

    records = self.normalize_records(
        entries
    )

    if format_name is None:
        format_name = self.format_from_path(
            path
        )
    else:
        format_name = self.normalize_format(
            format_name
        )

    if format_name == "json":
        return self.export_json(
            path,
            records,
            encoding=encoding,
            overwrite=overwrite,
        )

    if format_name == "csv":
        return self.export_csv(
            path,
            records,
            encoding=encoding,
            overwrite=overwrite,
        )

    if format_name == "txt":
        lines = []

        for index, record in enumerate(
            records,
            start=1,
        ):
            lines.append(
                f"Entry {index}"
            )

            for key, value in record.items():
                lines.append(
                    f"{key}: {value}"
                )

            lines.append("")

        return self.export_text(
            path,
            "\n".join(
                lines
            ),
            encoding=encoding,
            overwrite=overwrite,
        )

    raise UnsupportedFormatError(
        f"Unsupported history export format: "
        f"{format_name}"
    )


def export_analysis(
    self,
    path: str | Path,
    analysis: Mapping[str, Any],
    *,
    format_name: str | None = None,
    encoding: str = "utf-8",
    overwrite: bool = True,
) -> Path:
    # Exports cryptanalysis results

    if not isinstance(
        analysis,
        Mapping,
    ):
        raise InvalidExportDataError(
            "Analysis data must be a mapping."
        )

    if format_name is None:
        format_name = self.format_from_path(
            path
        )
    else:
        format_name = self.normalize_format(
            format_name
        )

    data = dict(
        analysis
    )

    if format_name == "json":
        return self.export_json(
            path,
            data,
            encoding=encoding,
            overwrite=overwrite,
        )

    if format_name == "csv":
        records = [
            {
                "metric": key,
                "value": value,
            }
            for key, value in data.items()
        ]

        return self.export_csv(
            path,
            records,
            fieldnames=[
                "metric",
                "value",
            ],
            encoding=encoding,
            overwrite=overwrite,
        )

    if format_name == "txt":
        lines = [
            f"{key}: {value}"
            for key, value in data.items()
        ]

        return self.export_text(
            path,
            "\n".join(
                lines
            ),
            encoding=encoding,
            overwrite=overwrite,
        )

    raise UnsupportedFormatError(
        f"Unsupported analysis export format: "
        f"{format_name}"
    )


def export_candidates(
    self,
    path: str | Path,
    candidates: Iterable[Mapping[str, Any]],
    *,
    format_name: str | None = None,
    encoding: str = "utf-8",
    overwrite: bool = True,
) -> Path:
    # Exports cipher cracking candidates

    records = self.normalize_records(
        candidates
    )

    if format_name is None:
        format_name = self.format_from_path(
            path
        )
    else:
        format_name = self.normalize_format(
            format_name
        )

    if format_name == "json":
        return self.export_json(
            path,
            records,
            encoding=encoding,
            overwrite=overwrite,
        )

    if format_name == "csv":
        return self.export_csv(
            path,
            records,
            encoding=encoding,
            overwrite=overwrite,
        )

    if format_name == "txt":
        lines = []

        for index, candidate in enumerate(
            records,
            start=1,
        ):
            values = [
                f"{key}={value}"
                for key, value
                in candidate.items()
            ]

            lines.append(
                f"{index}. "
                + ", ".join(
                    values
                )
            )

        return self.export_text(
            path,
            "\n".join(
                lines
            ),
            encoding=encoding,
            overwrite=overwrite,
        )

    raise UnsupportedFormatError(
        f"Unsupported candidate export format: "
        f"{format_name}"
    )


# Generic Export


def export(
    self,
    path: str | Path,
    data: Any,
    *,
    format_name: str | None = None,
    encoding: str = "utf-8",
    overwrite: bool = True,
) -> Path:
    # Automatically exports data using the
    # requested or detected format

    if format_name is None:
        format_name = self.format_from_path(
            path
        )
    else:
        format_name = self.normalize_format(
            format_name
        )

    if format_name == "json":
        return self.export_json(
            path,
            data,
            encoding=encoding,
            overwrite=overwrite,
        )

    if format_name == "txt":
        if isinstance(
            data,
            str,
        ):
            content = data
        elif isinstance(
            data,
            Mapping,
        ):
            content = "\n".join(
                f"{key}: {value}"
                for key, value
                in data.items()
            )
        elif isinstance(
            data,
            Iterable,
        ):
            content = "\n".join(
                str(item)
                for item in data
            )
        else:
            content = str(
                data
            )

        return self.export_text(
            path,
            content,
            encoding=encoding,
            overwrite=overwrite,
        )

    if format_name == "csv":
        if isinstance(
            data,
            Mapping,
        ):
            data = [
                data
            ]

        return self.export_csv(
            path,
            data,
            encoding=encoding,
            overwrite=overwrite,
        )

    raise UnsupportedFormatError(
        f"Unsupported export format: "
        f"{format_name}"
    )


# Export Verification


def can_export(
    self,
    format_name: str,
) -> bool:
    # Checks whether an export format is supported

    try:
        self.normalize_format(
            format_name
        )
        return True
    except UnsupportedFormatError:
        return False


def verify_output_path(
    self,
    path: str | Path,
) -> bool:
    # Verifies that an output path can be resolved

    try:
        self.file_manager.resolve_path(
            path
        )
        return True
    except FileManagerError:
        return False


# Module-Level Export Manager


_default_manager = ExportManager()


def get_export_manager() -> ExportManager:
    # Returns the default export manager

    return _default_manager

# Convenience Functions


def export_text(
    path: str | Path,
    content: str,
    *,
    encoding: str = "utf-8",
    overwrite: bool = True,
) -> Path:
    # Exports text using the default export manager

    return _default_manager.export_text(
        path,
        content,
        encoding=encoding,
        overwrite=overwrite,
    )


def export_json(
    path: str | Path,
    data: Any,
    *,
    indent: int = 4,
    encoding: str = "utf-8",
    overwrite: bool = True,
) -> Path:
    # Exports JSON using the default export manager

    return _default_manager.export_json(
        path,
        data,
        indent=indent,
        encoding=encoding,
        overwrite=overwrite,
    )


def export_csv(
    path: str | Path,
    records: Iterable[Mapping[str, Any]],
    *,
    fieldnames: Sequence[str] | None = None,
    encoding: str = "utf-8",
    overwrite: bool = True,
) -> Path:
    # Exports CSV using the default export manager

    return _default_manager.export_csv(
        path,
        records,
        fieldnames=fieldnames,
        encoding=encoding,
        overwrite=overwrite,
    )


def export_history(
    path: str | Path,
    entries: Iterable[Mapping[str, Any]],
    *,
    format_name: str | None = None,
    encoding: str = "utf-8",
    overwrite: bool = True,
) -> Path:
    # Exports history using the default export manager

    return _default_manager.export_history(
        path,
        entries,
        format_name=format_name,
        encoding=encoding,
        overwrite=overwrite,
    )


def export_analysis(
    path: str | Path,
    analysis: Mapping[str, Any],
    *,
    format_name: str | None = None,
    encoding: str = "utf-8",
    overwrite: bool = True,
) -> Path:
    # Exports analysis results using
    # the default export manager

    return _default_manager.export_analysis(
        path,
        analysis,
        format_name=format_name,
        encoding=encoding,
        overwrite=overwrite,
    )


def export_candidates(
    path: str | Path,
    candidates: Iterable[Mapping[str, Any]],
    *,
    format_name: str | None = None,
    encoding: str = "utf-8",
    overwrite: bool = True,
) -> Path:
    # Exports cracking candidates using
    # the default export manager

    return _default_manager.export_candidates(
        path,
        candidates,
        format_name=format_name,
        encoding=encoding,
        overwrite=overwrite,
    )


def export(
    path: str | Path,
    data: Any,
    *,
    format_name: str | None = None,
    encoding: str = "utf-8",
    overwrite: bool = True,
) -> Path:
    # Automatically exports data using
    # the default export manager

    return _default_manager.export(
        path,
        data,
        format_name=format_name,
        encoding=encoding,
        overwrite=overwrite,
    )


# Verification


def verify_export_format(
    format_name: str,
) -> bool:
    # Verifies that an export format is supported

    return _default_manager.can_export(
        format_name
    )


def verify_output_path(
    path: str | Path,
) -> bool:
    # Verifies that an output path can be resolved

    return _default_manager.verify_output_path(
        path
    )


# Self Test


def self_test() -> bool:
    # Runs a basic internal verification
    # of the export system

    test_directory = (
        Path.cwd()
        / ".exporter_test"
    )

    text_file = (
        test_directory
        / "test.txt"
    )

    json_file = (
        test_directory
        / "test.json"
    )

    csv_file = (
        test_directory
        / "test.csv"
    )

    try:
        manager = ExportManager()

        manager.export_text(
            text_file,
            "Cryptography Toolkit",
        )

        if not text_file.exists():
            return False

        manager.export_json(
            json_file,
            {
                "cipher": "Caesar",
                "key": 3,
            },
        )

        if not json_file.exists():
            return False

        manager.export_csv(
            csv_file,
            [
                {
                    "cipher": "Caesar",
                    "key": 3,
                },
                {
                    "cipher": "ROT13",
                    "key": 13,
                },
            ],
        )

        if not csv_file.exists():
            return False

        if not manager.can_export(
            "json"
        ):
            return False

        if manager.can_export(
            "pdf"
        ):
            return False

        return True

    except ExportError:
        return False

    finally:
        try:
            if text_file.exists():
                text_file.unlink()

            if json_file.exists():
                json_file.unlink()

            if csv_file.exists():
                csv_file.unlink()

            if test_directory.exists():
                test_directory.rmdir()

        except OSError:
            pass


# Module Exports


__all__ = [
    # Exceptions
    "ExportError",
    "UnsupportedFormatError",
    "InvalidExportDataError",
    "ExportOperationError",

    # Main Class
    "ExportManager",

    # Manager
    "get_export_manager",

    # Export Functions
    "export_text",
    "export_json",
    "export_csv",
    "export_history",
    "export_analysis",
    "export_candidates",
    "export",

    # Verification
    "verify_export_format",
    "verify_output_path",

    # Testing
    "self_test",
]

