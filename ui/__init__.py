# __init__.py
"""
User Interface utilities package for the Cryptography Toolkit.

This package contains reusable components for building a consistent,
readable, and user-friendly command-line interface throughout the
Cryptography Toolkit.

The UI package provides utilities for:

- ASCII banners and application headers
- Terminal colors and ANSI styling
- Text formatting and display helpers
- Progress bars, spinners, counters, and timing displays
- Console tables and structured data presentation

Modules
-------
banners
    ASCII banners, application titles, section headers, and
    decorative console elements.

colors
    Terminal color definitions, ANSI escape sequences, color
    helpers, and text styling utilities.

formatting
    Text formatting, indentation, wrapping, alignment, spacing,
    and console display helpers.

progress
    Progress bars, spinners, counters, timing utilities,
    batch progress tracking, and progress messages.

tables
    Terminal-friendly tables, table styles, column configuration,
    sorting, filtering, statistics tables, and cryptanalysis
    result displays.

The package re-exports the public utilities from each module so that
commonly used UI functionality can be imported directly from
``cryptography_toolkit.ui``.

Examples
--------
Import the complete UI package::

    from cryptography_toolkit import ui

Import commonly used utilities directly::

    from cryptography_toolkit.ui import (
        ProgressBar,
        TableBuilder,
        ColumnAlignment,
        BorderStyle,
    )

Create and display a table::

    table = TableBuilder(
        headers=["Algorithm", "Status"]
    )

    table.add_row(
        ["AES-256", "Available"]
    )

    print(table)

Display progress::

    progress = ProgressBar(total=100)
    progress.start()

    for _ in range(100):
        progress.increment()

    progress.complete()

Notes
-----
The UI package is intentionally independent from the core
cryptographic algorithms. Its purpose is presentation and user
interaction rather than cryptographic processing.

Keeping presentation utilities inside this package allows the
command-line interface, GUI components, reports, and other parts
of the toolkit to share a consistent visual language.
"""


# ---------------------------------------------------------------------------
# Package Metadata
# ---------------------------------------------------------------------------

__title__ = "Cryptography Toolkit UI"

__description__ = (
    "User interface, terminal formatting, progress, "
    "color, banner, and table utilities for the "
    "Cryptography Toolkit."
)

__version__ = "1.0.0"


# ---------------------------------------------------------------------------
# Package Modules
# ---------------------------------------------------------------------------

from . import banners
from . import colors
from . import formatting
from . import progress
from . import tables


# ---------------------------------------------------------------------------
# Public Utility Re-Exports
# ---------------------------------------------------------------------------

from .banners import *
from .colors import *
from .formatting import *
from .progress import *
from .tables import *


# ---------------------------------------------------------------------------
# Package Public API
# ---------------------------------------------------------------------------

__all__ = [
    # Package modules
    "banners",
    "colors",
    "formatting",
    "progress",
    "tables",

    # Package metadata
    "__title__",
    "__description__",
    "__version__",
]


# ---------------------------------------------------------------------------
# Extend Public API With Module Exports
# ---------------------------------------------------------------------------
#
# Each UI module maintains its own __all__ list.
# Merge those exports here so that:
#
#     from cryptography_toolkit.ui import *
#
# exposes the public utilities of the entire UI package.
#
# Duplicate names are removed while preserving order.

for _module in (
    banners,
    colors,
    formatting,
    progress,
    tables,
):
    for _name in getattr(
        _module,
        "__all__",
        [],
    ):
        if _name not in __all__:
            __all__.append(
                _name
            )


# ---------------------------------------------------------------------------
# Internal Cleanup
# ---------------------------------------------------------------------------
#
# These variables are implementation details used only while constructing
# the package-level __all__ list and should not remain exposed as part of
# the package namespace.

del _module
del _name

