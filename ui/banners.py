# banners.py
# Banner and header utilities for the
# entire Cryptography Toolkit
#
# Provides reusable functions for displaying
# application titles, section headers,
# separators, status banners, and formatted
# terminal output.


from __future__ import annotations

from typing import Iterable


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


APPLICATION_NAME = "CRYPTography Toolkit"

APPLICATION_SUBTITLE = (
    "Classical Cryptography & Cryptanalysis"
)

APPLICATION_VERSION = "1.0.0"

DEFAULT_WIDTH = 70

MIN_WIDTH = 20

MAX_WIDTH = 160

DEFAULT_BORDER = "="

SECONDARY_BORDER = "-"

ACCENT_BORDER = "*"

DEFAULT_PADDING = 2


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class BannerError(Exception):
    """Base exception for banner-related errors."""

    pass


class BannerConfigurationError(
    BannerError
):
    """Raised when banner configuration is invalid."""

    pass


# ---------------------------------------------------------------------------
# Banner Configuration
# ---------------------------------------------------------------------------


class BannerConfig:
    """
    Configuration object for banner generation.

    Parameters
    ----------
    width:
        Width of the generated banner.

    border:
        Character used for the primary border.

    padding:
        Number of spaces placed around banner text.

    centered:
        Whether banner text should be centered.

    uppercase:
        Whether banner text should be converted to
        uppercase before rendering.
    """

    def __init__(
        self,
        width: int = DEFAULT_WIDTH,
        border: str = DEFAULT_BORDER,
        padding: int = DEFAULT_PADDING,
        centered: bool = True,
        uppercase: bool = False,
    ) -> None:
        self.width = width

        self.border = border

        self.padding = padding

        self.centered = centered

        self.uppercase = uppercase

        self.validate()

    def validate(self) -> None:
        """Validate banner configuration."""

        if not isinstance(
            self.width,
            int,
        ):
            raise BannerConfigurationError(
                "Banner width must be an integer."
            )

        if not (
            MIN_WIDTH
            <= self.width
            <= MAX_WIDTH
        ):
            raise BannerConfigurationError(
                f"Banner width must be between "
                f"{MIN_WIDTH} and {MAX_WIDTH}."
            )

        if not isinstance(
            self.border,
            str,
        ):
            raise BannerConfigurationError(
                "Banner border must be a string."
            )

        if len(self.border) != 1:
            raise BannerConfigurationError(
                "Banner border must contain "
                "exactly one character."
            )

        if not isinstance(
            self.padding,
            int,
        ):
            raise BannerConfigurationError(
                "Banner padding must be an integer."
            )

        if self.padding < 0:
            raise BannerConfigurationError(
                "Banner padding cannot be negative."
            )

        if (
            self.padding * 2
            >= self.width
        ):
            raise BannerConfigurationError(
                "Banner padding is too large "
                "for the configured width."
            )

    def copy(
        self,
        **changes: object,
    ) -> "BannerConfig":
        """
        Create a copy of this configuration.

        Keyword arguments can be used to override
        individual configuration values.
        """

        values = {
            "width": self.width,
            "border": self.border,
            "padding": self.padding,
            "centered": self.centered,
            "uppercase": self.uppercase,
        }

        values.update(changes)

        return BannerConfig(
            **values,
        )

    def __repr__(self) -> str:
        """Return a developer-friendly representation."""

        return (
            "BannerConfig("
            f"width={self.width!r}, "
            f"border={self.border!r}, "
            f"padding={self.padding!r}, "
            f"centered={self.centered!r}, "
            f"uppercase={self.uppercase!r}"
            ")"
        )


# ---------------------------------------------------------------------------
# Text Utilities
# ---------------------------------------------------------------------------


def normalize_text(
    text: object,
    *,
    uppercase: bool = False,
) -> str:
    """
    Normalize text before inserting it into a banner.

    Parameters
    ----------
    text:
        Value to convert into display text.

    uppercase:
        Whether the resulting text should be uppercase.

    Returns
    -------
    str
        Normalized display text.
    """

    if text is None:
        value = ""

    else:
        value = str(text)

    value = value.strip()

    if uppercase:
        value = value.upper()

    return value


def repeat_character(
    character: str,
    length: int,
) -> str:
    """
    Repeat a single character a specified number of times.
    """

    if not isinstance(
        character,
        str,
    ):
        raise TypeError(
            "character must be a string."
        )

    if len(character) != 1:
        raise ValueError(
            "character must contain "
            "exactly one character."
        )

    if not isinstance(
        length,
        int,
    ):
        raise TypeError(
            "length must be an integer."
        )

    if length < 0:
        raise ValueError(
            "length cannot be negative."
        )

    return character * length


def make_separator(
    width: int = DEFAULT_WIDTH,
    character: str = DEFAULT_BORDER,
) -> str:
    """
    Create a horizontal separator.

    Example
    -------

    ``make_separator(10, "-")``

    produces:

    ``----------``
    """

    if not isinstance(
        width,
        int,
    ):
        raise TypeError(
            "width must be an integer."
        )

    if width <= 0:
        raise ValueError(
            "width must be positive."
        )

    if len(character) != 1:
        raise ValueError(
            "character must contain "
            "exactly one character."
        )

    return character * width


# ---------------------------------------------------------------------------
# Line Formatting
# ---------------------------------------------------------------------------


def center_text(
    text: object,
    width: int = DEFAULT_WIDTH,
    *,
    fill: str = " ",
) -> str:
    """
    Center text within a specified width.
    """

    value = str(text)

    if width <= 0:
        raise ValueError(
            "width must be positive."
        )

    if len(fill) != 1:
        raise ValueError(
            "fill must contain exactly one character."
        )

    if len(value) >= width:
        return value[:width]

    return value.center(
        width,
        fill,
    )


def left_align_text(
    text: object,
    width: int = DEFAULT_WIDTH,
    *,
    fill: str = " ",
) -> str:
    """
    Left-align text within a specified width.
    """

    value = str(text)

    if width <= 0:
        raise ValueError(
            "width must be positive."
        )

    if len(fill) != 1:
        raise ValueError(
            "fill must contain exactly one character."
        )

    if len(value) >= width:
        return value[:width]

    return value.ljust(
        width,
        fill,
    )


def right_align_text(
    text: object,
    width: int = DEFAULT_WIDTH,
    *,
    fill: str = " ",
) -> str:
    """
    Right-align text within a specified width.
    """

    value = str(text)

    if width <= 0:
        raise ValueError(
            "width must be positive."
        )

    if len(fill) != 1:
        raise ValueError(
            "fill must contain exactly one character."
        )

    if len(value) >= width:
        return value[:width]

    return value.rjust(
        width,
        fill,
    )


def format_banner_line(
    text: object,
    config: BannerConfig | None = None,
) -> str:
    """
    Format a single line according to banner configuration.
    """

    if config is None:
        config = BannerConfig()

    value = normalize_text(
        text,
        uppercase=config.uppercase,
    )

    available_width = (
        config.width
        - (config.padding * 2)
    )

    if len(value) > available_width:
        value = value[
            :available_width
        ]

    padded = (
        " " * config.padding
        + value
        + " " * config.padding
    )

    if config.centered:
        return center_text(
            padded,
            config.width,
        )

    return left_align_text(
        padded,
        config.width,
    )


# ---------------------------------------------------------------------------
# Basic Banner Generation
# ---------------------------------------------------------------------------


def create_banner(
    title: object,
    *,
    subtitle: object | None = None,
    config: BannerConfig | None = None,
) -> str:
    """
    Create a standard bordered banner.

    Example
    -------

    ``create_banner("Hello")``

    produces a structure similar to:

    ==============================
                Hello
    ==============================
    """

    if config is None:
        config = BannerConfig()

    title_line = format_banner_line(
        title,
        config,
    )

    top_border = make_separator(
        config.width,
        config.border,
    )

    lines = [
        top_border,
        title_line,
    ]

    if subtitle is not None:
        subtitle_line = format_banner_line(
            subtitle,
            config.copy(
                uppercase=False,
            ),
        )

        lines.append(
            subtitle_line
        )

    lines.append(
        top_border
    )

    return "\n".join(
        lines
    )


def create_section_header(
    title: object,
    *,
    width: int = DEFAULT_WIDTH,
    border: str = SECONDARY_BORDER,
) -> str:
    """
    Create a compact section header.
    """

    value = normalize_text(
        title
    )

    if not value:
        raise ValueError(
            "Section title cannot be empty."
        )

    if width <= 0:
        raise ValueError(
            "width must be positive."
        )

    separator = make_separator(
        width,
        border,
    )

    line = center_text(
        value,
        width,
    )

    return "\n".join(
        [
            separator,
            line,
            separator,
        ]
    )


def create_title_line(
    title: object,
    *,
    width: int = DEFAULT_WIDTH,
    character: str = ACCENT_BORDER,
) -> str:
    """
    Create a single decorative title line.
    """

    value = normalize_text(
        title
    )

    if not value:
        return make_separator(
            width,
            character,
        )

    if len(value) >= width:
        return value[:width]

    remaining = (
        width - len(value)
    )

    left = remaining // 2

    right = (
        remaining - left
    )

    return (
        character * left
        + value
        + character * right
    )


# ---------------------------------------------------------------------------
# Multi-Line Banner Support
# ---------------------------------------------------------------------------


def create_multiline_banner(
    lines: Iterable[object],
    *,
    config: BannerConfig | None = None,
) -> str:
    """
    Create a banner containing multiple lines of text.
    """

    if config is None:
        config = BannerConfig()

    normalized_lines = [
        normalize_text(
            line,
            uppercase=config.uppercase,
        )
        for line in lines
    ]

    if not normalized_lines:
        raise ValueError(
            "At least one banner line is required."
        )

    available_width = (
        config.width
        - (config.padding * 2)
    )

    formatted_lines = []

    for line in normalized_lines:
        if len(line) > available_width:
            line = line[
                :available_width
            ]

        formatted_lines.append(
            format_banner_line(
                line,
                config,
            )
        )

    border = make_separator(
        config.width,
        config.border,
    )

    return "\n".join(
        [
            border,
            *formatted_lines,
            border,
        ]
    )


# ---------------------------------------------------------------------------
# Application Banner
# ---------------------------------------------------------------------------


def create_application_banner(
    *,
    width: int = DEFAULT_WIDTH,
    version: str = APPLICATION_VERSION,
) -> str:
    """
    Create the standard Cryptography Toolkit banner.
    """

    config = BannerConfig(
        width=width,
        border=DEFAULT_BORDER,
        padding=DEFAULT_PADDING,
        centered=True,
        uppercase=False,
    )

    return create_multiline_banner(
        [
            APPLICATION_NAME,
            APPLICATION_SUBTITLE,
            f"Version {version}",
        ],
        config=config,
    )

# ---------------------------------------------------------------------------
# Specialized Application Banners
# ---------------------------------------------------------------------------


def create_welcome_banner(
    *,
    width: int = DEFAULT_WIDTH,
) -> str:
    """
    Create the welcome banner displayed when the toolkit starts.
    """

    return create_multiline_banner(
        [
            APPLICATION_NAME,
            "Welcome!",
            APPLICATION_SUBTITLE,
        ],
        config=BannerConfig(
            width=width,
            border=DEFAULT_BORDER,
            padding=DEFAULT_PADDING,
            centered=True,
            uppercase=False,
        ),
    )


def create_cli_banner(
    *,
    width: int = DEFAULT_WIDTH,
) -> str:
    """
    Create the banner used by the command-line interface.
    """

    return create_multiline_banner(
        [
            APPLICATION_NAME,
            "Command Line Interface",
            APPLICATION_SUBTITLE,
        ],
        config=BannerConfig(
            width=width,
            border=DEFAULT_BORDER,
            padding=DEFAULT_PADDING,
            centered=True,
            uppercase=False,
        ),
    )


def create_analysis_banner(
    *,
    width: int = DEFAULT_WIDTH,
) -> str:
    """
    Create a banner for cryptanalysis operations.
    """

    return create_banner(
        "CRYPTANALYSIS",
        subtitle="Frequency Analysis, Statistics & Cipher Analysis",
        config=BannerConfig(
            width=width,
            border=SECONDARY_BORDER,
            padding=DEFAULT_PADDING,
            centered=True,
            uppercase=False,
        ),
    )


def create_encryption_banner(
    *,
    width: int = DEFAULT_WIDTH,
) -> str:
    """
    Create a banner for encryption operations.
    """

    return create_banner(
        "ENCRYPTION",
        subtitle="Encrypt text using the Cryptography Toolkit",
        config=BannerConfig(
            width=width,
            border=SECONDARY_BORDER,
            padding=DEFAULT_PADDING,
            centered=True,
            uppercase=False,
        ),
    )


def create_decryption_banner(
    *,
    width: int = DEFAULT_WIDTH,
) -> str:
    """
    Create a banner for decryption operations.
    """

    return create_banner(
        "DECRYPTION",
        subtitle="Decrypt text using the Cryptography Toolkit",
        config=BannerConfig(
            width=width,
            border=SECONDARY_BORDER,
            padding=DEFAULT_PADDING,
            centered=True,
            uppercase=False,
        ),
    )


def create_file_banner(
    *,
    width: int = DEFAULT_WIDTH,
) -> str:
    """
    Create a banner for file operations.
    """

    return create_banner(
        "FILE OPERATIONS",
        subtitle="Read, Write, Encrypt & Manage Files",
        config=BannerConfig(
            width=width,
            border=SECONDARY_BORDER,
            padding=DEFAULT_PADDING,
            centered=True,
            uppercase=False,
        ),
    )


def create_history_banner(
    *,
    width: int = DEFAULT_WIDTH,
) -> str:
    """
    Create a banner for history information.
    """

    return create_banner(
        "HISTORY",
        subtitle="Cryptography Toolkit Operation History",
        config=BannerConfig(
            width=width,
            border=SECONDARY_BORDER,
            padding=DEFAULT_PADDING,
            centered=True,
            uppercase=False,
        ),
    )


def create_settings_banner(
    *,
    width: int = DEFAULT_WIDTH,
) -> str:
    """
    Create a banner for application settings.
    """

    return create_banner(
        "SETTINGS",
        subtitle="Cryptography Toolkit Configuration",
        config=BannerConfig(
            width=width,
            border=SECONDARY_BORDER,
            padding=DEFAULT_PADDING,
            centered=True,
            uppercase=False,
        ),
    )


def create_help_banner(
    *,
    width: int = DEFAULT_WIDTH,
) -> str:
    """
    Create a banner for help information.
    """

    return create_banner(
        "HELP",
        subtitle="Cryptography Toolkit Help & Documentation",
        config=BannerConfig(
            width=width,
            border=SECONDARY_BORDER,
            padding=DEFAULT_PADDING,
            centered=True,
            uppercase=False,
        ),
    )


def create_error_banner(
    message: object,
    *,
    width: int = DEFAULT_WIDTH,
) -> str:
    """
    Create a visually distinct error banner.
    """

    value = normalize_text(
        message
    )

    return create_multiline_banner(
        [
            "ERROR",
            value,
        ],
        config=BannerConfig(
            width=width,
            border="!",
            padding=DEFAULT_PADDING,
            centered=True,
            uppercase=False,
        ),
    )


def create_warning_banner(
    message: object,
    *,
    width: int = DEFAULT_WIDTH,
) -> str:
    """
    Create a warning banner.
    """

    value = normalize_text(
        message
    )

    return create_multiline_banner(
        [
            "WARNING",
            value,
        ],
        config=BannerConfig(
            width=width,
            border="!",
            padding=DEFAULT_PADDING,
            centered=True,
            uppercase=False,
        ),
    )


def create_success_banner(
    message: object,
    *,
    width: int = DEFAULT_WIDTH,
) -> str:
    """
    Create a success banner.
    """

    value = normalize_text(
        message
    )

    return create_multiline_banner(
        [
            "SUCCESS",
            value,
        ],
        config=BannerConfig(
            width=width,
            border="+",
            padding=DEFAULT_PADDING,
            centered=True,
            uppercase=False,
        ),
    )


# ---------------------------------------------------------------------------
# Status Banners
# ---------------------------------------------------------------------------


def create_status_banner(
    status: object,
    message: object | None = None,
    *,
    width: int = DEFAULT_WIDTH,
) -> str:
    """
    Create a generic status banner.

    Parameters
    ----------
    status:
        Status label such as ``READY``, ``RUNNING``,
        ``COMPLETE`` or ``FAILED``.

    message:
        Optional status description.
    """

    status_text = normalize_text(
        status
    )

    if not status_text:
        raise ValueError(
            "status cannot be empty."
        )

    lines = [
        status_text,
    ]

    if message is not None:
        lines.append(
            normalize_text(message)
        )

    return create_multiline_banner(
        lines,
        config=BannerConfig(
            width=width,
            border=ACCENT_BORDER,
            padding=DEFAULT_PADDING,
            centered=True,
            uppercase=False,
        ),
    )


def create_ready_banner(
    *,
    width: int = DEFAULT_WIDTH,
) -> str:
    """Create a standard ready-status banner."""

    return create_status_banner(
        "READY",
        "The Cryptography Toolkit is ready.",
        width=width,
    )


def create_running_banner(
    operation: object = "Operation",
    *,
    width: int = DEFAULT_WIDTH,
) -> str:
    """Create a standard running-status banner."""

    return create_status_banner(
        "RUNNING",
        f"{normalize_text(operation)} in progress...",
        width=width,
    )


def create_complete_banner(
    operation: object = "Operation",
    *,
    width: int = DEFAULT_WIDTH,
) -> str:
    """Create a standard completion banner."""

    return create_success_banner(
        f"{normalize_text(operation)} completed successfully.",
        width=width,
    )


# ---------------------------------------------------------------------------
# Menu Banners
# ---------------------------------------------------------------------------


def create_menu_banner(
    title: object,
    *,
    width: int = DEFAULT_WIDTH,
    border: str = DEFAULT_BORDER,
) -> str:
    """
    Create a banner suitable for an interactive menu.
    """

    return create_banner(
        title,
        config=BannerConfig(
            width=width,
            border=border,
            padding=DEFAULT_PADDING,
            centered=True,
            uppercase=False,
        ),
    )


def create_menu_option_header(
    title: object,
    *,
    width: int = DEFAULT_WIDTH,
) -> str:
    """
    Create a compact header for a group of menu options.
    """

    return create_title_line(
        title,
        width=width,
        character=SECONDARY_BORDER,
    )


# ---------------------------------------------------------------------------
# Decorative Banners
# ---------------------------------------------------------------------------


def create_double_line_banner(
    title: object,
    *,
    width: int = DEFAULT_WIDTH,
) -> str:
    """
    Create a banner using two horizontal border styles.
    """

    value = normalize_text(
        title
    )

    if not value:
        raise ValueError(
            "title cannot be empty."
        )

    if len(value) > width - 4:
        value = value[
            :width - 4
        ]

    top = make_separator(
        width,
        DEFAULT_BORDER,
    )

    bottom = make_separator(
        width,
        SECONDARY_BORDER,
    )

    line = center_text(
        value,
        width,
    )

    return "\n".join(
        [
            top,
            line,
            bottom,
        ]
    )


def create_compact_banner(
    title: object,
    *,
    width: int = DEFAULT_WIDTH,
) -> str:
    """
    Create a compact one-line banner.
    """

    value = normalize_text(
        title
    )

    if not value:
        raise ValueError(
            "title cannot be empty."
        )

    available = width - 4

    if len(value) > available:
        value = value[
            :available
        ]

    return (
        f"{DEFAULT_BORDER} "
        f"{value.center(available)}"
        f" {DEFAULT_BORDER}"
    )


# ---------------------------------------------------------------------------
# Banner Printing
# ---------------------------------------------------------------------------


def print_banner(
    banner: object,
) -> None:
    """
    Print a pre-generated banner to standard output.
    """

    print(
        str(banner)
    )


def print_application_banner(
    *,
    width: int = DEFAULT_WIDTH,
) -> None:
    """Print the standard application banner."""

    print_banner(
        create_application_banner(
            width=width,
        )
    )


def print_welcome_banner(
    *,
    width: int = DEFAULT_WIDTH,
) -> None:
    """Print the standard welcome banner."""

    print_banner(
        create_welcome_banner(
            width=width,
        )
    )


def print_section_header(
    title: object,
    *,
    width: int = DEFAULT_WIDTH,
) -> None:
    """Print a section header."""

    print_banner(
        create_section_header(
            title,
            width=width,
        )
    )


def print_success_banner(
    message: object,
    *,
    width: int = DEFAULT_WIDTH,
) -> None:
    """Print a success banner."""

    print_banner(
        create_success_banner(
            message,
            width=width,
        )
    )


def print_error_banner(
    message: object,
    *,
    width: int = DEFAULT_WIDTH,
) -> None:
    """Print an error banner."""

    print_banner(
        create_error_banner(
            message,
            width=width,
        )
    )


def print_warning_banner(
    message: object,
    *,
    width: int = DEFAULT_WIDTH,
) -> None:
    """Print a warning banner."""

    print_banner(
        create_warning_banner(
            message,
            width=width,
        )
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


__all__ = [
    # Constants
    "APPLICATION_NAME",
    "APPLICATION_SUBTITLE",
    "APPLICATION_VERSION",
    "DEFAULT_WIDTH",
    "MIN_WIDTH",
    "MAX_WIDTH",
    "DEFAULT_BORDER",
    "SECONDARY_BORDER",
    "ACCENT_BORDER",
    "DEFAULT_PADDING",

    # Exceptions
    "BannerError",
    "BannerConfigurationError",

    # Configuration
    "BannerConfig",

    # Text utilities
    "normalize_text",
    "repeat_character",
    "make_separator",

    # Alignment
    "center_text",
    "left_align_text",
    "right_align_text",

    # Basic banners
    "format_banner_line",
    "create_banner",
    "create_section_header",
    "create_title_line",
    "create_multiline_banner",
    "create_application_banner",

    # Application banners
    "create_welcome_banner",
    "create_cli_banner",
    "create_analysis_banner",
    "create_encryption_banner",
    "create_decryption_banner",
    "create_file_banner",
    "create_history_banner",
    "create_settings_banner",
    "create_help_banner",

    # Status banners
    "create_error_banner",
    "create_warning_banner",
    "create_success_banner",
    "create_status_banner",
    "create_ready_banner",
    "create_running_banner",
    "create_complete_banner",

    # Menu banners
    "create_menu_banner",
    "create_menu_option_header",

    # Decorative banners
    "create_double_line_banner",
    "create_compact_banner",

    # Printing
    "print_banner",
    "print_application_banner",
    "print_welcome_banner",
    "print_section_header",
    "print_success_banner",
    "print_error_banner",
    "print_warning_banner",
]

