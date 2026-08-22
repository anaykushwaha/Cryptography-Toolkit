# colors.py
# Color and terminal styling utilities for the
# entire Cryptography Toolkit
#
# Provides reusable ANSI color codes, text styling,
# color configuration, terminal capability detection,
# and helpers for applying and removing terminal colors.


from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from typing import Final


# ---------------------------------------------------------------------------
# ANSI Escape Sequences
# ---------------------------------------------------------------------------

ANSI_ESCAPE: Final[str] = "\033["

ANSI_RESET: Final[str] = "\033[0m"

# Text styles
STYLE_RESET: Final[str] = "\033[0m"
STYLE_BOLD: Final[str] = "\033[1m"
STYLE_DIM: Final[str] = "\033[2m"
STYLE_ITALIC: Final[str] = "\033[3m"
STYLE_UNDERLINE: Final[str] = "\033[4m"
STYLE_BLINK: Final[str] = "\033[5m"
STYLE_REVERSE: Final[str] = "\033[7m"
STYLE_HIDDEN: Final[str] = "\033[8m"
STYLE_STRIKETHROUGH: Final[str] = "\033[9m"

# Standard foreground colors
COLOR_BLACK: Final[str] = "\033[30m"
COLOR_RED: Final[str] = "\033[31m"
COLOR_GREEN: Final[str] = "\033[32m"
COLOR_YELLOW: Final[str] = "\033[33m"
COLOR_BLUE: Final[str] = "\033[34m"
COLOR_MAGENTA: Final[str] = "\033[35m"
COLOR_CYAN: Final[str] = "\033[36m"
COLOR_WHITE: Final[str] = "\033[37m"

# Bright foreground colors
COLOR_BRIGHT_BLACK: Final[str] = "\033[90m"
COLOR_BRIGHT_RED: Final[str] = "\033[91m"
COLOR_BRIGHT_GREEN: Final[str] = "\033[92m"
COLOR_BRIGHT_YELLOW: Final[str] = "\033[93m"
COLOR_BRIGHT_BLUE: Final[str] = "\033[94m"
COLOR_BRIGHT_MAGENTA: Final[str] = "\033[95m"
COLOR_BRIGHT_CYAN: Final[str] = "\033[96m"
COLOR_BRIGHT_WHITE: Final[str] = "\033[97m"

# Standard background colors
BG_BLACK: Final[str] = "\033[40m"
BG_RED: Final[str] = "\033[41m"
BG_GREEN: Final[str] = "\033[42m"
BG_YELLOW: Final[str] = "\033[43m"
BG_BLUE: Final[str] = "\033[44m"
BG_MAGENTA: Final[str] = "\033[45m"
BG_CYAN: Final[str] = "\033[46m"
BG_WHITE: Final[str] = "\033[47m"

# Bright background colors
BG_BRIGHT_BLACK: Final[str] = "\033[100m"
BG_BRIGHT_RED: Final[str] = "\033[101m"
BG_BRIGHT_GREEN: Final[str] = "\033[102m"
BG_BRIGHT_YELLOW: Final[str] = "\033[103m"
BG_BRIGHT_BLUE: Final[str] = "\033[104m"
BG_BRIGHT_MAGENTA: Final[str] = "\033[105m"
BG_BRIGHT_CYAN: Final[str] = "\033[106m"
BG_BRIGHT_WHITE: Final[str] = "\033[107m"


# ---------------------------------------------------------------------------
# Named Color Registry
# ---------------------------------------------------------------------------

FOREGROUND_COLORS: Final[dict[str, str]] = {
    "black": COLOR_BLACK,
    "red": COLOR_RED,
    "green": COLOR_GREEN,
    "yellow": COLOR_YELLOW,
    "blue": COLOR_BLUE,
    "magenta": COLOR_MAGENTA,
    "cyan": COLOR_CYAN,
    "white": COLOR_WHITE,
    "bright_black": COLOR_BRIGHT_BLACK,
    "bright_red": COLOR_BRIGHT_RED,
    "bright_green": COLOR_BRIGHT_GREEN,
    "bright_yellow": COLOR_BRIGHT_YELLOW,
    "bright_blue": COLOR_BRIGHT_BLUE,
    "bright_magenta": COLOR_BRIGHT_MAGENTA,
    "bright_cyan": COLOR_BRIGHT_CYAN,
    "bright_white": COLOR_BRIGHT_WHITE,
}

BACKGROUND_COLORS: Final[dict[str, str]] = {
    "black": BG_BLACK,
    "red": BG_RED,
    "green": BG_GREEN,
    "yellow": BG_YELLOW,
    "blue": BG_BLUE,
    "magenta": BG_MAGENTA,
    "cyan": BG_CYAN,
    "white": BG_WHITE,
    "bright_black": BG_BRIGHT_BLACK,
    "bright_red": BG_BRIGHT_RED,
    "bright_green": BG_BRIGHT_GREEN,
    "bright_yellow": BG_BRIGHT_YELLOW,
    "bright_blue": BG_BRIGHT_BLUE,
    "bright_magenta": BG_BRIGHT_MAGENTA,
    "bright_cyan": BG_BRIGHT_CYAN,
    "bright_white": BG_BRIGHT_WHITE,
}


# ---------------------------------------------------------------------------
# Semantic Toolkit Colors
# ---------------------------------------------------------------------------

COLOR_INFO: Final[str] = COLOR_CYAN
COLOR_SUCCESS: Final[str] = COLOR_GREEN
COLOR_WARNING: Final[str] = COLOR_YELLOW
COLOR_ERROR: Final[str] = COLOR_RED
COLOR_DEBUG: Final[str] = COLOR_BRIGHT_BLACK
COLOR_PRIMARY: Final[str] = COLOR_BLUE
COLOR_SECONDARY: Final[str] = COLOR_MAGENTA
COLOR_ACCENT: Final[str] = COLOR_BRIGHT_CYAN


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class ColorError(Exception):
    """Base exception for color-related errors."""

    pass


class ColorConfigurationError(ColorError):
    """Raised when color configuration is invalid."""

    pass


class ColorNameError(ColorError):
    """Raised when an unknown color name is requested."""

    pass


class ColorFormatError(ColorError):
    """Raised when a color or style format is invalid."""

    pass


# ---------------------------------------------------------------------------
# Color Configuration
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class ColorConfig:
    """
    Configuration for terminal color output.

    Parameters
    ----------
    enabled:
        Whether ANSI color output is enabled.

    use_bright:
        Whether semantic colors should prefer bright variants.

    reset:
        Whether styled output should automatically append
        an ANSI reset sequence.

    force:
        Force colors even when terminal detection indicates
        that color output may not be supported.
    """

    enabled: bool = True
    use_bright: bool = False
    reset: bool = True
    force: bool = False

    def validate(self) -> None:
        """Validate the color configuration."""

        if not isinstance(self.enabled, bool):
            raise ColorConfigurationError(
                "enabled must be a boolean."
            )

        if not isinstance(self.use_bright, bool):
            raise ColorConfigurationError(
                "use_bright must be a boolean."
            )

        if not isinstance(self.reset, bool):
            raise ColorConfigurationError(
                "reset must be a boolean."
            )

        if not isinstance(self.force, bool):
            raise ColorConfigurationError(
                "force must be a boolean."
            )

    def copy(
        self,
        **changes: object,
    ) -> "ColorConfig":
        """Return a copy with optional configuration changes."""

        values = {
            "enabled": self.enabled,
            "use_bright": self.use_bright,
            "reset": self.reset,
            "force": self.force,
        }

        values.update(changes)

        config = ColorConfig(**values)
        config.validate()

        return config


# ---------------------------------------------------------------------------
# Terminal Detection
# ---------------------------------------------------------------------------


def supports_color(
    stream: object | None = None,
) -> bool:
    """
    Determine whether the current output stream likely supports
    ANSI color sequences.
    """

    if stream is None:
        stream = sys.stdout

    if os.environ.get("NO_COLOR") is not None:
        return False

    if os.environ.get("TERM", "").lower() == "dumb":
        return False

    isatty = getattr(
        stream,
        "isatty",
        None,
    )

    if callable(isatty):
        try:
            if isatty():
                return True
        except OSError:
            return False

    if os.name == "nt":
        return (
            os.environ.get("ANSICON") is not None
            or os.environ.get("WT_SESSION") is not None
            or os.environ.get("TERM_PROGRAM") is not None
        )

    return False


def colors_enabled(
    config: ColorConfig | None = None,
    *,
    stream: object | None = None,
) -> bool:
    """
    Determine whether color output should currently be used.
    """

    if config is None:
        config = ColorConfig()

    config.validate()

    if not config.enabled:
        return False

    if config.force:
        return True

    return supports_color(stream)


# ---------------------------------------------------------------------------
# Color Lookup
# ---------------------------------------------------------------------------


def normalize_color_name(
    name: str,
) -> str:
    """
    Normalize a named color.

    Examples
    --------
    ``"Bright Red"`` becomes ``"bright_red"``.
    """

    if not isinstance(name, str):
        raise ColorNameError(
            "Color name must be a string."
        )

    normalized = (
        name.strip()
        .lower()
        .replace("-", "_")
        .replace(" ", "_")
    )

    if not normalized:
        raise ColorNameError(
            "Color name cannot be empty."
        )

    return normalized


def get_foreground_color(
    name: str,
) -> str:
    """
    Return an ANSI foreground sequence by name.
    """

    normalized = normalize_color_name(name)

    try:
        return FOREGROUND_COLORS[normalized]
    except KeyError as exc:
        raise ColorNameError(
            f"Unknown foreground color: {name!r}"
        ) from exc


def get_background_color(
    name: str,
) -> str:
    """
    Return an ANSI background sequence by name.
    """

    normalized = normalize_color_name(name)

    try:
        return BACKGROUND_COLORS[normalized]
    except KeyError as exc:
        raise ColorNameError(
            f"Unknown background color: {name!r}"
        ) from exc


def is_valid_foreground_color(
    name: str,
) -> bool:
    """Return whether a foreground color name is recognized."""

    try:
        normalized = normalize_color_name(name)
    except ColorNameError:
        return False

    return normalized in FOREGROUND_COLORS


def is_valid_background_color(
    name: str,
) -> bool:
    """Return whether a background color name is recognized."""

    try:
        normalized = normalize_color_name(name)
    except ColorNameError:
        return False

    return normalized in BACKGROUND_COLORS


# ---------------------------------------------------------------------------
# ANSI Sequence Utilities
# ---------------------------------------------------------------------------


def ansi_sequence(
    code: int | str,
) -> str:
    """
    Build an ANSI escape sequence from a numeric code.
    """

    if isinstance(code, bool):
        raise ColorFormatError(
            "ANSI code must be an integer or string."
        )

    if not isinstance(code, (int, str)):
        raise ColorFormatError(
            "ANSI code must be an integer or string."
        )

    value = str(code).strip()

    if not value:
        raise ColorFormatError(
            "ANSI code cannot be empty."
        )

    return f"{ANSI_ESCAPE}{value}m"


def combine_styles(
    *styles: str,
) -> str:
    """
    Combine multiple ANSI style sequences.
    """

    result: list[str] = []

    for style in styles:
        if not isinstance(style, str):
            raise ColorFormatError(
                "Styles must be strings."
            )

        if style:
            result.append(style)

    return "".join(result)


# ---------------------------------------------------------------------------
# ANSI Detection and Removal
# ---------------------------------------------------------------------------


ANSI_ESCAPE_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])"
)


def contains_ansi(
    text: object,
) -> bool:
    """
    Return whether text contains an ANSI escape sequence.
    """

    if not isinstance(text, str):
        text = str(text)

    return ANSI_ESCAPE_PATTERN.search(text) is not None


def strip_ansi(
    text: object,
) -> str:
    """
    Remove ANSI escape sequences from text.
    """

    if not isinstance(text, str):
        text = str(text)

    return ANSI_ESCAPE_PATTERN.sub(
        "",
        text,
    )


def visible_length(
    text: object,
) -> int:
    """
    Return the visible length of terminal text.

    ANSI escape sequences are excluded from the count.
    """

    return len(
        strip_ansi(text)
    )

# ---------------------------------------------------------------------------
# Text Styling
# ---------------------------------------------------------------------------


def apply_color(
    text: object,
    color: str,
    *,
    config: ColorConfig | None = None,
) -> str:
    """
    Apply a foreground color to text.

    Parameters
    ----------
    text:
        Text to color.

    color:
        Named foreground color.

    config:
        Optional color configuration.
    """

    if config is None:
        config = ColorConfig()

    config.validate()

    value = str(text)

    if not colors_enabled(config):
        return value

    sequence = get_foreground_color(color)

    suffix = (
        ANSI_RESET
        if config.reset
        else ""
    )

    return (
        f"{sequence}"
        f"{value}"
        f"{suffix}"
    )


def apply_background(
    text: object,
    color: str,
    *,
    config: ColorConfig | None = None,
) -> str:
    """
    Apply a background color to text.
    """

    if config is None:
        config = ColorConfig()

    config.validate()

    value = str(text)

    if not colors_enabled(config):
        return value

    sequence = get_background_color(color)

    suffix = (
        ANSI_RESET
        if config.reset
        else ""
    )

    return (
        f"{sequence}"
        f"{value}"
        f"{suffix}"
    )


def apply_style(
    text: object,
    style: str,
    *,
    config: ColorConfig | None = None,
) -> str:
    """
    Apply an ANSI text style.

    Parameters
    ----------
    text:
        Text to style.

    style:
        ANSI style sequence.
    """

    if config is None:
        config = ColorConfig()

    config.validate()

    if not isinstance(style, str):
        raise ColorFormatError(
            "style must be a string."
        )

    value = str(text)

    if not colors_enabled(config):
        return value

    suffix = (
        ANSI_RESET
        if config.reset
        else ""
    )

    return (
        f"{style}"
        f"{value}"
        f"{suffix}"
    )


def style_text(
    text: object,
    *,
    color: str | None = None,
    background: str | None = None,
    bold: bool = False,
    dim: bool = False,
    italic: bool = False,
    underline: bool = False,
    reverse: bool = False,
    strikethrough: bool = False,
    config: ColorConfig | None = None,
) -> str:
    """
    Apply multiple colors and styles to text.

    This is the primary high-level styling helper.
    """

    if config is None:
        config = ColorConfig()

    config.validate()

    value = str(text)

    if not colors_enabled(config):
        return value

    styles: list[str] = []

    if color is not None:
        styles.append(
            get_foreground_color(color)
        )

    if background is not None:
        styles.append(
            get_background_color(background)
        )

    if bold:
        styles.append(
            STYLE_BOLD
        )

    if dim:
        styles.append(
            STYLE_DIM
        )

    if italic:
        styles.append(
            STYLE_ITALIC
        )

    if underline:
        styles.append(
            STYLE_UNDERLINE
        )

    if reverse:
        styles.append(
            STYLE_REVERSE
        )

    if strikethrough:
        styles.append(
            STYLE_STRIKETHROUGH
        )

    if not styles:
        return value

    prefix = combine_styles(
        *styles
    )

    suffix = (
        ANSI_RESET
        if config.reset
        else ""
    )

    return (
        f"{prefix}"
        f"{value}"
        f"{suffix}"
    )


# ---------------------------------------------------------------------------
# Semantic Styling
# ---------------------------------------------------------------------------


def info(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """
    Format text as informational output.
    """

    return apply_color(
        text,
        "cyan",
        config=config,
    )


def success(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """
    Format text as successful output.
    """

    return apply_color(
        text,
        "green",
        config=config,
    )


def warning(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """
    Format text as warning output.
    """

    return apply_color(
        text,
        "yellow",
        config=config,
    )


def error(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """
    Format text as error output.
    """

    return apply_color(
        text,
        "red",
        config=config,
    )


def debug(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """
    Format text as debug output.
    """

    return apply_color(
        text,
        "bright_black",
        config=config,
    )


def primary(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """
    Format text using the primary toolkit color.
    """

    return apply_color(
        text,
        "blue",
        config=config,
    )


def secondary(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """
    Format text using the secondary toolkit color.
    """

    return apply_color(
        text,
        "magenta",
        config=config,
    )


def accent(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """
    Format text using the toolkit accent color.
    """

    return apply_color(
        text,
        "bright_cyan",
        config=config,
    )


# ---------------------------------------------------------------------------
# Common Text Styles
# ---------------------------------------------------------------------------


def bold(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Return bold text."""

    return apply_style(
        text,
        STYLE_BOLD,
        config=config,
    )


def dim(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Return dimmed text."""

    return apply_style(
        text,
        STYLE_DIM,
        config=config,
    )


def italic(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Return italic text."""

    return apply_style(
        text,
        STYLE_ITALIC,
        config=config,
    )


def underline(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Return underlined text."""

    return apply_style(
        text,
        STYLE_UNDERLINE,
        config=config,
    )


def reverse(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Return reversed-color text."""

    return apply_style(
        text,
        STYLE_REVERSE,
        config=config,
    )


def strike(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Return strikethrough text."""

    return apply_style(
        text,
        STYLE_STRIKETHROUGH,
        config=config,
    )


# ---------------------------------------------------------------------------
# Convenience Color Functions
# ---------------------------------------------------------------------------


def black(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply black foreground color."""

    return apply_color(
        text,
        "black",
        config=config,
    )


def red(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply red foreground color."""

    return apply_color(
        text,
        "red",
        config=config,
    )


def green(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply green foreground color."""

    return apply_color(
        text,
        "green",
        config=config,
    )


def yellow(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply yellow foreground color."""

    return apply_color(
        text,
        "yellow",
        config=config,
    )


def blue(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply blue foreground color."""

    return apply_color(
        text,
        "blue",
        config=config,
    )


def magenta(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply magenta foreground color."""

    return apply_color(
        text,
        "magenta",
        config=config,
    )


def cyan(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply cyan foreground color."""

    return apply_color(
        text,
        "cyan",
        config=config,
    )


def white(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply white foreground color."""

    return apply_color(
        text,
        "white",
        config=config,
    )


def bright_red(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply bright red foreground color."""

    return apply_color(
        text,
        "bright_red",
        config=config,
    )


def bright_green(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply bright green foreground color."""

    return apply_color(
        text,
        "bright_green",
        config=config,
    )


def bright_yellow(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply bright yellow foreground color."""

    return apply_color(
        text,
        "bright_yellow",
        config=config,
    )


def bright_blue(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply bright blue foreground color."""

    return apply_color(
        text,
        "bright_blue",
        config=config,
    )


def bright_magenta(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply bright magenta foreground color."""

    return apply_color(
        text,
        "bright_magenta",
        config=config,
    )


def bright_cyan(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply bright cyan foreground color."""

    return apply_color(
        text,
        "bright_cyan",
        config=config,
    )


def bright_white(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply bright white foreground color."""

    return apply_color(
        text,
        "bright_white",
        config=config,
    )


# ---------------------------------------------------------------------------
# Background Convenience Functions
# ---------------------------------------------------------------------------


def on_black(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply a black background."""

    return apply_background(
        text,
        "black",
        config=config,
    )


def on_red(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply a red background."""

    return apply_background(
        text,
        "red",
        config=config,
    )


def on_green(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply a green background."""

    return apply_background(
        text,
        "green",
        config=config,
    )


def on_yellow(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply a yellow background."""

    return apply_background(
        text,
        "yellow",
        config=config,
    )


def on_blue(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply a blue background."""

    return apply_background(
        text,
        "blue",
        config=config,
    )


def on_magenta(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply a magenta background."""

    return apply_background(
        text,
        "magenta",
        config=config,
    )


def on_cyan(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply a cyan background."""

    return apply_background(
        text,
        "cyan",
        config=config,
    )


def on_white(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply a white background."""

    return apply_background(
        text,
        "white",
        config=config,
    )


# ---------------------------------------------------------------------------
# Combined Style Helpers
# ---------------------------------------------------------------------------


def bold_color(
    text: object,
    color: str,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply a foreground color and bold styling."""

    return style_text(
        text,
        color=color,
        bold=True,
        config=config,
    )


def bold_success(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Format text as bold successful output."""

    return style_text(
        text,
        color="green",
        bold=True,
        config=config,
    )


def bold_warning(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Format text as bold warning output."""

    return style_text(
        text,
        color="yellow",
        bold=True,
        config=config,
    )


def bold_error(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Format text as bold error output."""

    return style_text(
        text,
        color="red",
        bold=True,
        config=config,
    )


def bold_info(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Format text as bold informational output."""

    return style_text(
        text,
        color="cyan",
        bold=True,
        config=config,
    )

# ---------------------------------------------------------------------------
# Bright Background Convenience Functions
# ---------------------------------------------------------------------------


def on_bright_black(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply a bright black background."""

    return apply_background(
        text,
        "bright_black",
        config=config,
    )


def on_bright_red(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply a bright red background."""

    return apply_background(
        text,
        "bright_red",
        config=config,
    )


def on_bright_green(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply a bright green background."""

    return apply_background(
        text,
        "bright_green",
        config=config,
    )


def on_bright_yellow(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply a bright yellow background."""

    return apply_background(
        text,
        "bright_yellow",
        config=config,
    )


def on_bright_blue(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply a bright blue background."""

    return apply_background(
        text,
        "bright_blue",
        config=config,
    )


def on_bright_magenta(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply a bright magenta background."""

    return apply_background(
        text,
        "bright_magenta",
        config=config,
    )


def on_bright_cyan(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply a bright cyan background."""

    return apply_background(
        text,
        "bright_cyan",
        config=config,
    )


def on_bright_white(
    text: object,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Apply a bright white background."""

    return apply_background(
        text,
        "bright_white",
        config=config,
    )


# ---------------------------------------------------------------------------
# Semantic Status Helpers
# ---------------------------------------------------------------------------


def status(
    label: object,
    message: object | None = None,
    *,
    color: str = "cyan",
    config: ColorConfig | None = None,
) -> str:
    """
    Format a status label and optional message.

    Example
    -------
    ``status("READY", "Toolkit initialized")``
    """

    label_text = str(label).strip()

    if not label_text:
        raise ValueError(
            "Status label cannot be empty."
        )

    if message is None:
        return bold_color(
            label_text,
            color,
            config=config,
        )

    message_text = str(message)

    return (
        bold_color(
            label_text,
            color,
            config=config,
        )
        + " "
        + message_text
    )


def success_status(
    label: object = "SUCCESS",
    message: object | None = None,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Create a green success status."""

    return status(
        label,
        message,
        color="green",
        config=config,
    )


def warning_status(
    label: object = "WARNING",
    message: object | None = None,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Create a yellow warning status."""

    return status(
        label,
        message,
        color="yellow",
        config=config,
    )


def error_status(
    label: object = "ERROR",
    message: object | None = None,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Create a red error status."""

    return status(
        label,
        message,
        color="red",
        config=config,
    )


def info_status(
    label: object = "INFO",
    message: object | None = None,
    *,
    config: ColorConfig | None = None,
) -> str:
    """Create a cyan informational status."""

    return status(
        label,
        message,
        color="cyan",
        config=config,
    )


# ---------------------------------------------------------------------------
# Key / Value Formatting
# ---------------------------------------------------------------------------


def color_key_value(
    key: object,
    value: object,
    *,
    key_color: str = "bright_cyan",
    value_color: str | None = None,
    config: ColorConfig | None = None,
) -> str:
    """
    Format a key/value pair using separate colors.

    Example
    -------
    ``Name: Caesar Cipher``
    """

    key_text = str(key).strip()

    if not key_text:
        raise ValueError(
            "Key cannot be empty."
        )

    formatted_key = bold_color(
        f"{key_text}:",
        key_color,
        config=config,
    )

    if value_color is None:
        return (
            f"{formatted_key} "
            f"{value}"
        )

    formatted_value = apply_color(
        value,
        value_color,
        config=config,
    )

    return (
        f"{formatted_key} "
        f"{formatted_value}"
    )


def color_label(
    label: object,
    *,
    color: str = "bright_cyan",
    config: ColorConfig | None = None,
) -> str:
    """Format a standalone label."""

    return bold_color(
        str(label),
        color,
        config=config,
    )


# ---------------------------------------------------------------------------
# Palette Utilities
# ---------------------------------------------------------------------------


def get_palette() -> dict[str, str]:
    """
    Return the toolkit's semantic color palette.

    A new dictionary is returned so callers can safely modify it.
    """

    return {
        "info": COLOR_INFO,
        "success": COLOR_SUCCESS,
        "warning": COLOR_WARNING,
        "error": COLOR_ERROR,
        "debug": COLOR_DEBUG,
        "primary": COLOR_PRIMARY,
        "secondary": COLOR_SECONDARY,
        "accent": COLOR_ACCENT,
    }


def get_foreground_names() -> tuple[str, ...]:
    """Return all supported foreground color names."""

    return tuple(
        FOREGROUND_COLORS.keys()
    )


def get_background_names() -> tuple[str, ...]:
    """Return all supported background color names."""

    return tuple(
        BACKGROUND_COLORS.keys()
    )


# ---------------------------------------------------------------------------
# Configuration Helpers
# ---------------------------------------------------------------------------


_DEFAULT_CONFIG = ColorConfig()


def get_default_config() -> ColorConfig:
    """
    Return a copy of the default color configuration.
    """

    return _DEFAULT_CONFIG.copy()


def set_default_config(
    config: ColorConfig,
) -> None:
    """
    Replace the module-level default color configuration.

    Parameters
    ----------
    config:
        New color configuration.
    """

    if not isinstance(
        config,
        ColorConfig,
    ):
        raise ColorConfigurationError(
            "config must be a ColorConfig instance."
        )

    config.validate()

    _DEFAULT_CONFIG.enabled = config.enabled
    _DEFAULT_CONFIG.use_bright = config.use_bright
    _DEFAULT_CONFIG.reset = config.reset
    _DEFAULT_CONFIG.force = config.force


def colorize(
    text: object,
    color: str | None = None,
    *,
    background: str | None = None,
    bold_text: bool = False,
    underline_text: bool = False,
    config: ColorConfig | None = None,
) -> str:
    """
    General-purpose colorization helper.

    This provides a compact interface for common terminal
    styling operations.
    """

    if config is None:
        config = get_default_config()

    return style_text(
        text,
        color=color,
        background=background,
        bold=bold_text,
        underline=underline_text,
        config=config,
    )


# ---------------------------------------------------------------------------
# Terminal Output Helpers
# ---------------------------------------------------------------------------


def print_color(
    text: object,
    color: str,
    *,
    end: str = "\n",
    config: ColorConfig | None = None,
) -> None:
    """
    Print text using a foreground color.
    """

    print(
        apply_color(
            text,
            color,
            config=config,
        ),
        end=end,
    )


def print_success(
    text: object,
    *,
    end: str = "\n",
    config: ColorConfig | None = None,
) -> None:
    """Print successful output."""

    print(
        success(
            text,
            config=config,
        ),
        end=end,
    )


def print_warning(
    text: object,
    *,
    end: str = "\n",
    config: ColorConfig | None = None,
) -> None:
    """Print warning output."""

    print(
        warning(
            text,
            config=config,
        ),
        end=end,
    )


def print_error(
    text: object,
    *,
    end: str = "\n",
    config: ColorConfig | None = None,
) -> None:
    """Print error output."""

    print(
        error(
            text,
            config=config,
        ),
        end=end,
    )


def print_info(
    text: object,
    *,
    end: str = "\n",
    config: ColorConfig | None = None,
) -> None:
    """Print informational output."""

    print(
        info(
            text,
            config=config,
        ),
        end=end,
    )


def print_debug(
    text: object,
    *,
    end: str = "\n",
    config: ColorConfig | None = None,
) -> None:
    """Print debug output."""

    print(
        debug(
            text,
            config=config,
        ),
        end=end,
    )


# ---------------------------------------------------------------------------
# Color Removal
# ---------------------------------------------------------------------------


def remove_colors(
    text: object,
) -> str:
    """
    Remove all ANSI color and styling sequences from text.

    This is an alias-style convenience wrapper around ``strip_ansi``.
    """

    return strip_ansi(
        text
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


__all__ = [
    # ANSI primitives
    "ANSI_ESCAPE",
    "ANSI_RESET",

    # Styles
    "STYLE_RESET",
    "STYLE_BOLD",
    "STYLE_DIM",
    "STYLE_ITALIC",
    "STYLE_UNDERLINE",
    "STYLE_BLINK",
    "STYLE_REVERSE",
    "STYLE_HIDDEN",
    "STYLE_STRIKETHROUGH",

    # Foreground colors
    "COLOR_BLACK",
    "COLOR_RED",
    "COLOR_GREEN",
    "COLOR_YELLOW",
    "COLOR_BLUE",
    "COLOR_MAGENTA",
    "COLOR_CYAN",
    "COLOR_WHITE",
    "COLOR_BRIGHT_BLACK",
    "COLOR_BRIGHT_RED",
    "COLOR_BRIGHT_GREEN",
    "COLOR_BRIGHT_YELLOW",
    "COLOR_BRIGHT_BLUE",
    "COLOR_BRIGHT_MAGENTA",
    "COLOR_BRIGHT_CYAN",
    "COLOR_BRIGHT_WHITE",

    # Background colors
    "BG_BLACK",
    "BG_RED",
    "BG_GREEN",
    "BG_YELLOW",
    "BG_BLUE",
    "BG_MAGENTA",
    "BG_CYAN",
    "BG_WHITE",
    "BG_BRIGHT_BLACK",
    "BG_BRIGHT_RED",
    "BG_BRIGHT_GREEN",
    "BG_BRIGHT_YELLOW",
    "BG_BRIGHT_BLUE",
    "BG_BRIGHT_MAGENTA",
    "BG_BRIGHT_CYAN",
    "BG_BRIGHT_WHITE",

    # Semantic colors
    "COLOR_INFO",
    "COLOR_SUCCESS",
    "COLOR_WARNING",
    "COLOR_ERROR",
    "COLOR_DEBUG",
    "COLOR_PRIMARY",
    "COLOR_SECONDARY",
    "COLOR_ACCENT",

    # Registries
    "FOREGROUND_COLORS",
    "BACKGROUND_COLORS",

    # Exceptions
    "ColorError",
    "ColorConfigurationError",
    "ColorNameError",
    "ColorFormatError",

    # Configuration
    "ColorConfig",
    "get_default_config",
    "set_default_config",

    # Terminal detection
    "supports_color",
    "colors_enabled",

    # Color lookup
    "normalize_color_name",
    "get_foreground_color",
    "get_background_color",
    "is_valid_foreground_color",
    "is_valid_background_color",

    # ANSI utilities
    "ansi_sequence",
    "combine_styles",
    "contains_ansi",
    "strip_ansi",
    "remove_colors",
    "visible_length",

    # Generic styling
    "apply_color",
    "apply_background",
    "apply_style",
    "style_text",
    "colorize",

    # Semantic styling
    "info",
    "success",
    "warning",
    "error",
    "debug",
    "primary",
    "secondary",
    "accent",

    # Text styles
    "bold",
    "dim",
    "italic",
    "underline",
    "reverse",
    "strike",

    # Foreground helpers
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
    "bright_red",
    "bright_green",
    "bright_yellow",
    "bright_blue",
    "bright_magenta",
    "bright_cyan",
    "bright_white",

    # Background helpers
    "on_black",
    "on_red",
    "on_green",
    "on_yellow",
    "on_blue",
    "on_magenta",
    "on_cyan",
    "on_white",
    "on_bright_black",
    "on_bright_red",
    "on_bright_green",
    "on_bright_yellow",
    "on_bright_blue",
    "on_bright_magenta",
    "on_bright_cyan",
    "on_bright_white",

    # Combined helpers
    "bold_color",
    "bold_success",
    "bold_warning",
    "bold_error",
    "bold_info",

    # Status helpers
    "status",
    "success_status",
    "warning_status",
    "error_status",
    "info_status",

    # Formatting helpers
    "color_key_value",
    "color_label",

    # Palette
    "get_palette",
    "get_foreground_names",
    "get_background_names",

    # Printing
    "print_color",
    "print_success",
    "print_warning",
    "print_error",
    "print_info",
    "print_debug",
]

