# __init__.py
# Graphical User Interface package
# for the entire Cryptography Toolkit
#
# Provides the complete graphical interface
# for encryption, decryption, cryptanalysis,
# file operations, application settings,
# and toolkit navigation.
#
# Contains application management, windows,
# custom widgets, themes, and dialogs.
#
# Modules
# app      - Main GUI application and controller
# windows  - Application windows and window management
# widgets  - Custom GUI widgets
# themes   - GUI themes and styling
# dialogs  - Dialog windows and user interactions


# ---------------------------------------------------------------------------
# Package Metadata
# ---------------------------------------------------------------------------

__package_name__ = "gui"

__description__ = (
    "Graphical user interface package "
    "for the Cryptography Toolkit."
)

__version__ = "1.0.0"


# ---------------------------------------------------------------------------
# Module Imports
# ---------------------------------------------------------------------------

from .app import *
from .windows import *
from .widgets import *
from .themes import *
from .dialogs import *


# ---------------------------------------------------------------------------
# Public Package API
# ---------------------------------------------------------------------------

__all__ = [
    # Package metadata
    "__package_name__",
    "__description__",
    "__version__",

    # GUI modules
    "app",
    "windows",
    "widgets",
    "themes",
    "dialogs",
]

