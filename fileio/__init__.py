# __init__.py

# File handling package for the entire
# Cryptography Toolkit

# Contains utilities for reading, writing,
# encrypting, decrypting, exporting,
# backing up, and tracking files


# Modules
# file_manager - Core file management,
#                reading, writing, copying,
#                deleting, and file operations
#
# history - Encryption and operation
#           history management
#
# exporters - Export utilities for analysis
#             results, history, and candidates
#
# backups - Backup creation, restoration,
#           deletion, and metadata management


# File Manager
from .file_manager import *


# History
from .history import *


# Exporters
from .exporters import *


# Backups
from .backups import *


__all__ = [
    # File Manager
    "FileManager",
    "FileManagerError",
    "FileNotFoundError",
    "FileAlreadyExistsError",
    "InvalidFileError",
    "FileOperationError",

    # History
    "HistoryError",
    "InvalidHistoryEntryError",
    "HistoryStorageError",
    "HistoryEntry",
    "HistoryManager",
    "get_history_manager",
    "record_operation",
    "save_history",
    "load_history",
    "get_history",
    "clear_history",
    "verify_entry",

    # Exporters
    "ExportError",
    "UnsupportedFormatError",
    "InvalidExportDataError",
    "ExportOperationError",
    "ExportManager",
    "get_export_manager",
    "export_text",
    "export_json",
    "export_csv",
    "export_history",
    "export_analysis",
    "export_candidates",
    "export",
    "verify_export_format",
    "verify_output_path",

    # Backups
    "BackupError",
    "BackupNotFoundError",
    "BackupAlreadyExistsError",
    "InvalidBackupError",
    "BackupOperationError",
    "BackupMetadata",
    "BackupManager",
    "get_backup_manager",
    "create_backup",
    "restore_backup",
    "delete_backup",
    "list_backups",
    "save_backups",
    "load_backups",
    "verify_backup",
]