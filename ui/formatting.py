# formatting.py
# Text formatting and display utilities for the
# entire Cryptography Toolkit
#
# Provides reusable helpers for alignment, indentation,
# wrapping, truncation, padding, key-value formatting,
# and terminal-friendly text presentation.


from __future__ import annotations

import re
import textwrap
from dataclasses import dataclass
from typing import Iterable, Sequence


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


DEFAULT_WIDTH = 70

DEFAULT_INDENT = 4

DEFAULT_SEPARATOR = "-"

DEFAULT_PADDING = 1

ELLIPSIS = "..."

ANSI_ESCAPE_PATTERN = re.compile(
    r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])"
)


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class FormattingError(Exception):
    """Base exception for formatting-related errors."""

    pass


class FormattingConfigurationError(
    FormattingError
):
    """Raised when formatting configuration is invalid."""

    pass


# ---------------------------------------------------------------------------
# Formatting Configuration
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class FormatConfig:
    """
    Configuration for text formatting operations.

    Parameters
    ----------
    width:
        Default display width.

    indent:
        Number of spaces used for indentation.

    padding:
        Default horizontal padding.

    preserve_words:
        Whether wrapping should avoid breaking words.

    strip_whitespace:
        Whether leading and trailing whitespace should be
        removed before formatting.
    """

    width: int = DEFAULT_WIDTH

    indent: int = DEFAULT_INDENT

    padding: int = DEFAULT_PADDING

    preserve_words: bool = True

    strip_whitespace: bool = True

    def validate(self) -> None:
        """Validate formatting configuration."""

        if not isinstance(
            self.width,
            int,
        ):
            raise FormattingConfigurationError(
                "width must be an integer."
            )

        if self.width <= 0:
            raise FormattingConfigurationError(
                "width must be positive."
            )

        if not isinstance(
            self.indent,
            int,
        ):
            raise FormattingConfigurationError(
                "indent must be an integer."
            )

        if self.indent < 0:
            raise FormattingConfigurationError(
                "indent cannot be negative."
            )

        if not isinstance(
            self.padding,
            int,
        ):
            raise FormattingConfigurationError(
                "padding must be an integer."
            )

        if self.padding < 0:
            raise FormattingConfigurationError(
                "padding cannot be negative."
            )

        if not isinstance(
            self.preserve_words,
            bool,
        ):
            raise FormattingConfigurationError(
                "preserve_words must be a boolean."
            )

        if not isinstance(
            self.strip_whitespace,
            bool,
        ):
            raise FormattingConfigurationError(
                "strip_whitespace must be a boolean."
            )

    def copy(
        self,
        **changes: object,
    ) -> "FormatConfig":
        """
        Return a copy of this configuration with optional changes.
        """

        values = {
            "width": self.width,
            "indent": self.indent,
            "padding": self.padding,
            "preserve_words": self.preserve_words,
            "strip_whitespace": self.strip_whitespace,
        }

        values.update(changes)

        config = FormatConfig(
            **values
        )

        config.validate()

        return config


# ---------------------------------------------------------------------------
# Basic Text Normalization
# ---------------------------------------------------------------------------


def normalize_text(
    value: object,
    *,
    strip_whitespace: bool = True,
) -> str:
    """
    Convert a value into displayable text.

    Parameters
    ----------
    value:
        Object to convert into text.

    strip_whitespace:
        Remove leading and trailing whitespace when enabled.
    """

    if value is None:
        text = ""

    else:
        text = str(value)

    if strip_whitespace:
        text = text.strip()

    return text


def normalize_lines(
    lines: Iterable[object],
    *,
    strip_whitespace: bool = False,
) -> list[str]:
    """
    Normalize an iterable of values into a list of strings.
    """

    return [
        normalize_text(
            line,
            strip_whitespace=strip_whitespace,
        )
        for line in lines
    ]


def split_lines(
    text: object,
) -> list[str]:
    """
    Split text into individual lines.
    """

    return str(text).splitlines()


# ---------------------------------------------------------------------------
# ANSI-Aware Length Utilities
# ---------------------------------------------------------------------------


def strip_ansi(
    text: object,
) -> str:
    """
    Remove ANSI escape sequences from text.
    """

    value = str(text)

    return ANSI_ESCAPE_PATTERN.sub(
        "",
        value,
    )


def visible_length(
    text: object,
) -> int:
    """
    Return the visible length of terminal text.

    ANSI escape sequences are ignored.
    """

    return len(
        strip_ansi(text)
    )


def truncate_ansi_safe(
    text: object,
    width: int,
) -> str:
    """
    Truncate text according to visible terminal width.

    ANSI sequences are preserved only when the full sequence
    occurs before the truncation point.
    """

    value = str(text)

    if width <= 0:
        return ""

    if visible_length(value) <= width:
        return value

    result: list[str] = []

    visible_count = 0

    index = 0

    while index < len(value):
        match = ANSI_ESCAPE_PATTERN.match(
            value,
            index,
        )

        if match:
            result.append(
                match.group(0)
            )
            index = match.end()
            continue

        if visible_count >= width:
            break

        result.append(
            value[index]
        )

        visible_count += 1
        index += 1

    return "".join(result)


# ---------------------------------------------------------------------------
# Padding Utilities
# ---------------------------------------------------------------------------


def pad_left(
    text: object,
    width: int,
    *,
    fill: str = " ",
) -> str:
    """
    Pad text on the left to a specified visible width.
    """

    value = str(text)

    if width < 0:
        raise ValueError(
            "width cannot be negative."
        )

    if len(fill) != 1:
        raise ValueError(
            "fill must contain exactly one character."
        )

    current = visible_length(
        value
    )

    if current >= width:
        return value

    return (
        fill * (width - current)
        + value
    )


def pad_right(
    text: object,
    width: int,
    *,
    fill: str = " ",
) -> str:
    """
    Pad text on the right to a specified visible width.
    """

    value = str(text)

    if width < 0:
        raise ValueError(
            "width cannot be negative."
        )

    if len(fill) != 1:
        raise ValueError(
            "fill must contain exactly one character."
        )

    current = visible_length(
        value
    )

    if current >= width:
        return value

    return (
        value
        + fill * (width - current)
    )


def pad_center(
    text: object,
    width: int,
    *,
    fill: str = " ",
) -> str:
    """
    Center text within a specified visible width.
    """

    value = str(text)

    if width < 0:
        raise ValueError(
            "width cannot be negative."
        )

    if len(fill) != 1:
        raise ValueError(
            "fill must contain exactly one character."
        )

    current = visible_length(
        value
    )

    if current >= width:
        return value

    remaining = width - current

    left = remaining // 2

    right = remaining - left

    return (
        fill * left
        + value
        + fill * right
    )


# ---------------------------------------------------------------------------
# Alignment Utilities
# ---------------------------------------------------------------------------


def align_left(
    text: object,
    width: int,
    *,
    fill: str = " ",
) -> str:
    """
    Left-align text within a fixed-width field.
    """

    return pad_right(
        text,
        width,
        fill=fill,
    )


def align_right(
    text: object,
    width: int,
    *,
    fill: str = " ",
) -> str:
    """
    Right-align text within a fixed-width field.
    """

    return pad_left(
        text,
        width,
        fill=fill,
    )


def align_center(
    text: object,
    width: int,
    *,
    fill: str = " ",
) -> str:
    """
    Center text within a fixed-width field.
    """

    return pad_center(
        text,
        width,
        fill=fill,
    )


def align(
    text: object,
    width: int,
    mode: str = "left",
    *,
    fill: str = " ",
) -> str:
    """
    Align text according to a named alignment mode.

    Supported modes:

    - ``left``
    - ``right``
    - ``center``
    """

    normalized = (
        mode.strip().lower()
    )

    if normalized == "left":
        return align_left(
            text,
            width,
            fill=fill,
        )

    if normalized == "right":
        return align_right(
            text,
            width,
            fill=fill,
        )

    if normalized in {
        "center",
        "centre",
    }:
        return align_center(
            text,
            width,
            fill=fill,
        )

    raise FormattingError(
        f"Unsupported alignment mode: {mode!r}"
    )


# ---------------------------------------------------------------------------
# Indentation
# ---------------------------------------------------------------------------


def indent_text(
    text: object,
    spaces: int = DEFAULT_INDENT,
    *,
    prefix: str | None = None,
) -> str:
    """
    Indent every line of text.

    Parameters
    ----------
    text:
        Text to indent.

    spaces:
        Number of spaces to insert.

    prefix:
        Optional custom indentation prefix.
    """

    if spaces < 0:
        raise ValueError(
            "spaces cannot be negative."
        )

    if prefix is None:
        prefix = " " * spaces

    return textwrap.indent(
        str(text),
        prefix,
    )


def dedent_text(
    text: object,
) -> str:
    """
    Remove common indentation from multiline text.
    """

    return textwrap.dedent(
        str(text)
    )


def indent_lines(
    lines: Iterable[object],
    spaces: int = DEFAULT_INDENT,
) -> list[str]:
    """
    Indent each line in an iterable.
    """

    prefix = " " * spaces

    return [
        prefix + str(line)
        for line in lines
    ]


# ---------------------------------------------------------------------------
# Wrapping
# ---------------------------------------------------------------------------


def wrap_text(
    text: object,
    width: int = DEFAULT_WIDTH,
    *,
    preserve_words: bool = True,
    break_long_words: bool = False,
) -> list[str]:
    """
    Wrap text to a specified width.

    Returns a list of wrapped lines.
    """

    if width <= 0:
        raise ValueError(
            "width must be positive."
        )

    value = str(text)

    wrapper = textwrap.TextWrapper(
        width=width,
        break_long_words=break_long_words,
        break_on_hyphens=preserve_words,
        replace_whitespace=False,
        drop_whitespace=True,
    )

    return wrapper.wrap(
        value
    )


def wrap_lines(
    text: object,
    width: int = DEFAULT_WIDTH,
    *,
    preserve_words: bool = True,
) -> str:
    """
    Wrap text and return the result as a newline-separated string.
    """

    return "\n".join(
        wrap_text(
            text,
            width,
            preserve_words=preserve_words,
        )
    )


def wrap_paragraphs(
    text: object,
    width: int = DEFAULT_WIDTH,
) -> list[str]:
    """
    Wrap multiple paragraphs independently.
    """

    paragraphs = re.split(
        r"\n\s*\n",
        str(text).strip(),
    )

    return [
        wrap_lines(
            paragraph,
            width,
        )
        for paragraph in paragraphs
        if paragraph.strip()
    ]


# ---------------------------------------------------------------------------
# Truncation
# ---------------------------------------------------------------------------


def truncate_text(
    text: object,
    width: int,
    *,
    suffix: str = ELLIPSIS,
) -> str:
    """
    Truncate text to a specified visible width.

    The suffix is included in the final width.
    """

    value = str(text)

    if width <= 0:
        return ""

    if visible_length(value) <= width:
        return value

    suffix_length = visible_length(
        suffix
    )

    if suffix_length >= width:
        return truncate_ansi_safe(
            suffix,
            width,
        )

    available = width - suffix_length

    return (
        truncate_ansi_safe(
            value,
            available,
        )
        + suffix
    )


def truncate_middle(
    text: object,
    width: int,
    *,
    separator: str = ELLIPSIS,
) -> str:
    """
    Truncate text from the middle while preserving both ends.
    """

    value = str(text)

    if width <= 0:
        return ""

    if visible_length(value) <= width:
        return value

    separator_length = visible_length(
        separator
    )

    if separator_length >= width:
        return truncate_ansi_safe(
            separator,
            width,
        )

    available = width - separator_length

    left_width = (
        available + 1
    ) // 2

    right_width = (
        available // 2
    )

    left = truncate_ansi_safe(
        value,
        left_width,
    )

    plain = strip_ansi(
        value
    )

    right = plain[
        max(
            0,
            len(plain) - right_width,
        ):
    ]

    return (
        left
        + separator
        + right
    )

# ---------------------------------------------------------------------------
# Repeated Lines and Separators
# ---------------------------------------------------------------------------


def separator(
    width: int = DEFAULT_WIDTH,
    *,
    character: str = DEFAULT_SEPARATOR,
) -> str:
    """
    Create a horizontal separator line.

    Parameters
    ----------
    width:
        Number of characters in the separator.

    character:
        Character used to construct the separator.
    """

    if width < 0:
        raise ValueError(
            "width cannot be negative."
        )

    if len(character) != 1:
        raise ValueError(
            "character must contain exactly one character."
        )

    return character * width


def double_separator(
    width: int = DEFAULT_WIDTH,
) -> str:
    """Create a double-line separator."""

    return separator(
        width,
        character="=",
    )


def dotted_separator(
    width: int = DEFAULT_WIDTH,
) -> str:
    """Create a dotted separator."""

    return separator(
        width,
        character=".",
    )


def bullet_line(
    text: object,
    *,
    bullet: str = "•",
    spacing: int = 1,
) -> str:
    """
    Format text as a bullet point.
    """

    if spacing < 0:
        raise ValueError(
            "spacing cannot be negative."
        )

    return (
        bullet
        + (" " * spacing)
        + str(text)
    )


def numbered_line(
    number: int,
    text: object,
    *,
    spacing: int = 1,
) -> str:
    """
    Format text as a numbered list item.
    """

    if spacing < 0:
        raise ValueError(
            "spacing cannot be negative."
        )

    return (
        f"{number}."
        + (" " * spacing)
        + str(text)
    )


# ---------------------------------------------------------------------------
# Multi-Line Formatting
# ---------------------------------------------------------------------------


def format_lines(
    lines: Iterable[object],
    *,
    separator_text: str = "\n",
) -> str:
    """
    Join multiple values into formatted lines.
    """

    return separator_text.join(
        str(line)
        for line in lines
    )


def join_nonempty(
    values: Iterable[object],
    *,
    separator_text: str = " ",
) -> str:
    """
    Join non-empty values while ignoring blank entries.
    """

    result: list[str] = []

    for value in values:
        text = str(value).strip()

        if text:
            result.append(text)

    return separator_text.join(
        result
    )


def compact_lines(
    text: object,
) -> str:
    """
    Remove blank lines from a block of text.
    """

    lines = str(text).splitlines()

    return "\n".join(
        line
        for line in lines
        if line.strip()
    )


def collapse_whitespace(
    text: object,
) -> str:
    """
    Collapse consecutive whitespace into single spaces.
    """

    return re.sub(
        r"\s+",
        " ",
        str(text).strip(),
    )


# ---------------------------------------------------------------------------
# Key / Value Formatting
# ---------------------------------------------------------------------------


def format_key_value(
    key: object,
    value: object,
    *,
    separator_text: str = ": ",
    key_width: int | None = None,
) -> str:
    """
    Format a key/value pair.

    Examples
    --------
    ``format_key_value("Mode", "Encrypt")``

    Returns::

        Mode: Encrypt
    """

    key_text = str(key)

    if key_width is not None:
        if key_width < 0:
            raise ValueError(
                "key_width cannot be negative."
            )

        key_text = pad_right(
            key_text,
            key_width,
        )

    return (
        key_text
        + separator_text
        + str(value)
    )


def format_key_value_block(
    values: dict[object, object],
    *,
    separator_text: str = ": ",
    align_keys: bool = True,
) -> str:
    """
    Format a dictionary-like collection as aligned key/value lines.
    """

    if not values:
        return ""

    items = list(
        values.items()
    )

    key_width = None

    if align_keys:
        key_width = max(
            visible_length(key)
            for key, _ in items
        )

    return "\n".join(
        format_key_value(
            key,
            value,
            separator_text=separator_text,
            key_width=key_width,
        )
        for key, value in items
    )


# ---------------------------------------------------------------------------
# Title and Heading Formatting
# ---------------------------------------------------------------------------


def format_title(
    title: object,
    width: int = DEFAULT_WIDTH,
    *,
    character: str = "=",
    padding: int = 1,
) -> str:
    """
    Create a centered title surrounded by separator lines.

    Example::

        ==============================
               BLACKJACK
        ==============================
    """

    if width <= 0:
        raise ValueError(
            "width must be positive."
        )

    if padding < 0:
        raise ValueError(
            "padding cannot be negative."
        )

    top = separator(
        width,
        character=character,
    )

    title_text = str(title).strip()

    centered = align_center(
        title_text,
        width,
    )

    if padding == 0:
        return (
            f"{top}\n"
            f"{centered}\n"
            f"{top}"
        )

    blank = "\n" * padding

    return (
        f"{top}\n"
        f"{blank}"
        f"{centered}\n"
        f"{blank}"
        f"{top}"
    )


def format_heading(
    heading: object,
    *,
    level: int = 1,
    width: int | None = None,
) -> str:
    """
    Format a heading according to its hierarchy level.
    """

    text = str(heading).strip()

    if not text:
        return ""

    if level < 1:
        raise ValueError(
            "level must be at least 1."
        )

    if level == 1:
        result = text.upper()

    elif level == 2:
        result = text

    else:
        result = f"› {text}"

    if width is not None:
        if width <= 0:
            raise ValueError(
                "width must be positive."
            )

        result = truncate_text(
            result,
            width,
        )

    return result


def underline_heading(
    heading: object,
    *,
    character: str = "-",
) -> str:
    """
    Create a heading followed by an underline.
    """

    text = str(heading).strip()

    if not text:
        return ""

    return (
        f"{text}\n"
        f"{separator("
            len(text),
            character=character,
        )}"
    )


# ---------------------------------------------------------------------------
# Box Formatting
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class BoxStyle:
    """
    Configuration for boxed text.

    Parameters
    ----------
    top_left:
        Top-left corner character.

    top_right:
        Top-right corner character.

    bottom_left:
        Bottom-left corner character.

    bottom_right:
        Bottom-right corner character.

    horizontal:
        Horizontal border character.

    vertical:
        Vertical border character.
    """

    top_left: str = "┌"

    top_right: str = "┐"

    bottom_left: str = "└"

    bottom_right: str = "┘"

    horizontal: str = "─"

    vertical: str = "│"

    def validate(self) -> None:
        """Validate box-style characters."""

        fields = (
            self.top_left,
            self.top_right,
            self.bottom_left,
            self.bottom_right,
            self.horizontal,
            self.vertical,
        )

        if any(
            len(value) != 1
            for value in fields
        ):
            raise FormattingConfigurationError(
                "All BoxStyle characters must be exactly one character."
            )


DEFAULT_BOX_STYLE = BoxStyle()


def box_text(
    text: object,
    *,
    width: int | None = None,
    padding: int = DEFAULT_PADDING,
    style: BoxStyle | None = None,
    align_mode: str = "left",
) -> str:
    """
    Place text inside a terminal-style box.
    """

    if padding < 0:
        raise ValueError(
            "padding cannot be negative."
        )

    if style is None:
        style = DEFAULT_BOX_STYLE

    style.validate()

    lines = str(text).splitlines()

    if not lines:
        lines = [""]

    content_width = max(
        visible_length(line)
        for line in lines
    )

    if width is not None:
        if width <= 0:
            raise ValueError(
                "width must be positive."
            )

        minimum_width = (
            content_width
            + (padding * 2)
        )

        content_width = max(
            content_width,
            width - (padding * 2),
        )

        if width < minimum_width:
            raise ValueError(
                "width is too small for the supplied content."
            )

    inner_width = (
        content_width
        + (padding * 2)
    )

    top = (
        style.top_left
        + (
            style.horizontal
            * inner_width
        )
        + style.top_right
    )

    bottom = (
        style.bottom_left
        + (
            style.horizontal
            * inner_width
        )
        + style.bottom_right
    )

    body: list[str] = []

    for line in lines:
        formatted = align(
            line,
            content_width,
            mode=align_mode,
        )

        body.append(
            style.vertical
            + (" " * padding)
            + formatted
            + (" " * padding)
            + style.vertical
        )

    return "\n".join(
        [top, *body, bottom]
    )


def simple_box(
    text: object,
    *,
    width: int | None = None,
) -> str:
    """
    Create a simple ASCII box around text.
    """

    style = BoxStyle(
        top_left="+",
        top_right="+",
        bottom_left="+",
        bottom_right="+",
        horizontal="-",
        vertical="|",
    )

    return box_text(
        text,
        width=width,
        style=style,
    )


# ---------------------------------------------------------------------------
# Table-Like Text Formatting
# ---------------------------------------------------------------------------


def calculate_column_widths(
    rows: Sequence[Sequence[object]],
    *,
    minimum_width: int = 1,
    maximum_width: int | None = None,
) -> list[int]:
    """
    Calculate visible widths for columns in a row collection.
    """

    if minimum_width < 0:
        raise ValueError(
            "minimum_width cannot be negative."
        )

    if maximum_width is not None:
        if maximum_width <= 0:
            raise ValueError(
                "maximum_width must be positive."
            )

        if maximum_width < minimum_width:
            raise ValueError(
                "maximum_width cannot be smaller than minimum_width."
            )

    if not rows:
        return []

    column_count = max(
        len(row)
        for row in rows
    )

    widths = [
        minimum_width
        for _ in range(column_count)
    ]

    for row in rows:
        for index, value in enumerate(row):
            length = visible_length(
                value
            )

            if maximum_width is not None:
                length = min(
                    length,
                    maximum_width,
                )

            widths[index] = max(
                widths[index],
                length,
            )

    return widths


def format_row(
    row: Sequence[object],
    widths: Sequence[int],
    *,
    separator_text: str = " | ",
    alignments: Sequence[str] | None = None,
) -> str:
    """
    Format a single row using predefined column widths.
    """

    if len(row) != len(widths):
        raise FormattingError(
            "Row length must match the number of column widths."
        )

    if alignments is None:
        alignments = [
            "left"
            for _ in widths
        ]

    if len(alignments) != len(widths):
        raise FormattingError(
            "Alignment count must match the number of columns."
        )

    cells: list[str] = []

    for value, width, mode in zip(
        row,
        widths,
        alignments,
    ):
        cells.append(
            align(
                value,
                width,
                mode=mode,
            )
        )

    return separator_text.join(
        cells
    )


def format_table(
    rows: Sequence[Sequence[object]],
    *,
    headers: Sequence[object] | None = None,
    separator_text: str = " | ",
    alignments: Sequence[str] | None = None,
    header_separator: str = "-",
) -> str:
    """
    Format rows of data as a simple terminal table.
    """

    all_rows: list[Sequence[object]] = []

    if headers is not None:
        all_rows.append(
            headers
        )

    all_rows.extend(
        rows
    )

    if not all_rows:
        return ""

    widths = calculate_column_widths(
        all_rows
    )

    output: list[str] = []

    if headers is not None:
        output.append(
            format_row(
                headers,
                widths,
                separator_text=separator_text,
                alignments=alignments,
            )
        )

        output.append(
            separator(
                len(output[0]),
                character=header_separator,
            )
        )

    for row in rows:
        output.append(
            format_row(
                row,
                widths,
                separator_text=separator_text,
                alignments=alignments,
            )
        )

    return "\n".join(
        output
    )

# ---------------------------------------------------------------------------
# Number Formatting
# ---------------------------------------------------------------------------


def format_number(
    value: int | float,
    *,
    decimals: int | None = None,
    thousands_separator: str = ",",
) -> str:
    """
    Format a numeric value for terminal display.

    Parameters
    ----------
    value:
        Numeric value to format.

    decimals:
        Optional number of decimal places.

    thousands_separator:
        Character used between thousands groups.
    """

    if not isinstance(value, (int, float)):
        raise TypeError(
            "value must be an integer or float."
        )

    if isinstance(value, bool):
        raise TypeError(
            "value must be numeric, not boolean."
        )

    if not isinstance(
        thousands_separator,
        str,
    ):
        raise TypeError(
            "thousands_separator must be a string."
        )

    if decimals is not None:
        if not isinstance(decimals, int):
            raise TypeError(
                "decimals must be an integer or None."
            )

        if decimals < 0:
            raise ValueError(
                "decimals cannot be negative."
            )

        formatted = f"{value:,.{decimals}f}"

    else:
        formatted = f"{value:,}"

    if thousands_separator != ",":
        formatted = formatted.replace(
            ",",
            thousands_separator,
        )

    return formatted


def format_percentage(
    value: float,
    *,
    decimals: int = 1,
    multiply: bool = True,
) -> str:
    """
    Format a value as a percentage.

    Parameters
    ----------
    value:
        Percentage value or decimal fraction.

    decimals:
        Number of decimal places.

    multiply:
        If True, ``0.75`` becomes ``75.0%``.
        If False, ``75`` becomes ``75.0%``.
    """

    if not isinstance(
        value,
        (int, float),
    ):
        raise TypeError(
            "value must be numeric."
        )

    if decimals < 0:
        raise ValueError(
            "decimals cannot be negative."
        )

    number = (
        value * 100
        if multiply
        else value
    )

    return (
        f"{number:.{decimals}f}%"
    )


def format_bytes(
    size: int | float,
    *,
    precision: int = 2,
    binary: bool = True,
) -> str:
    """
    Format a byte count using human-readable units.

    Examples
    --------
    ``1024`` becomes ``1.00 KiB`` when binary mode is enabled.
    """

    if not isinstance(
        size,
        (int, float),
    ):
        raise TypeError(
            "size must be numeric."
        )

    if size < 0:
        raise ValueError(
            "size cannot be negative."
        )

    if precision < 0:
        raise ValueError(
            "precision cannot be negative."
        )

    base = 1024 if binary else 1000

    units = (
        (
            "B",
            "KiB",
            "MiB",
            "GiB",
            "TiB",
            "PiB",
        )
        if binary
        else
        (
            "B",
            "KB",
            "MB",
            "GB",
            "TB",
            "PB",
        )
    )

    value = float(size)

    unit_index = 0

    while (
        value >= base
        and unit_index < len(units) - 1
    ):
        value /= base
        unit_index += 1

    if unit_index == 0:
        return f"{int(value)} {units[unit_index]}"

    return (
        f"{value:.{precision}f} "
        f"{units[unit_index]}"
    )


# ---------------------------------------------------------------------------
# Duration Formatting
# ---------------------------------------------------------------------------


def format_duration(
    seconds: float,
    *,
    precision: int = 2,
) -> str:
    """
    Format a duration in seconds into a human-readable representation.
    """

    if not isinstance(
        seconds,
        (int, float),
    ):
        raise TypeError(
            "seconds must be numeric."
        )

    if seconds < 0:
        raise ValueError(
            "seconds cannot be negative."
        )

    if precision < 0:
        raise ValueError(
            "precision cannot be negative."
        )

    if seconds < 1:
        return (
            f"{seconds:.{precision}f}s"
        )

    if seconds < 60:
        return (
            f"{seconds:.{precision}f}s"
        )

    minutes, remainder = divmod(
        seconds,
        60,
    )

    if minutes < 60:
        return (
            f"{int(minutes)}m "
            f"{remainder:.{precision}f}s"
        )

    hours, minutes = divmod(
        int(minutes),
        60,
    )

    if hours < 24:
        return (
            f"{hours}h "
            f"{minutes}m "
            f"{remainder:.{precision}f}s"
        )

    days, hours = divmod(
        hours,
        24,
    )

    return (
        f"{days}d "
        f"{hours}h "
        f"{minutes}m "
        f"{remainder:.{precision}f}s"
    )


# ---------------------------------------------------------------------------
# Boolean / Status Formatting
# ---------------------------------------------------------------------------


def format_boolean(
    value: bool,
    *,
    true_text: str = "Yes",
    false_text: str = "No",
) -> str:
    """
    Convert a boolean value into display-friendly text.
    """

    if not isinstance(
        value,
        bool,
    ):
        raise TypeError(
            "value must be a boolean."
        )

    return (
        true_text
        if value
        else false_text
    )


def format_status(
    status: object,
    *,
    success_values: Iterable[object] = (
        "success",
        "successful",
        "ok",
        "complete",
        "completed",
        "done",
    ),
    failure_values: Iterable[object] = (
        "error",
        "failed",
        "failure",
        "invalid",
    ),
) -> str:
    """
    Normalize a status value for display.
    """

    value = str(status).strip()

    normalized = value.lower()

    success_set = {
        str(item).lower()
        for item in success_values
    }

    failure_set = {
        str(item).lower()
        for item in failure_values
    }

    if normalized in success_set:
        return value.upper()

    if normalized in failure_set:
        return value.upper()

    return value


# ---------------------------------------------------------------------------
# File / Path Formatting
# ---------------------------------------------------------------------------


def format_path(
    path: object,
    *,
    max_length: int | None = None,
) -> str:
    """
    Format a filesystem path for terminal display.
    """

    value = str(path)

    if max_length is None:
        return value

    if max_length <= 0:
        return ""

    return truncate_middle(
        value,
        max_length,
    )


def format_filename(
    filename: object,
    *,
    max_length: int | None = None,
) -> str:
    """
    Format a filename for display.

    Long filenames preserve the extension when possible.
    """

    value = str(filename)

    if (
        max_length is None
        or visible_length(value) <= max_length
    ):
        return value

    if max_length <= 0:
        return ""

    if "." not in value:
        return truncate_text(
            value,
            max_length,
        )

    stem, extension = value.rsplit(
        ".",
        1,
    )

    suffix = f".{extension}"

    if visible_length(suffix) >= max_length:
        return truncate_text(
            suffix,
            max_length,
        )

    available = (
        max_length
        - visible_length(suffix)
    )

    return (
        truncate_text(
            stem,
            available,
            suffix=ELLIPSIS,
        )
        + suffix
    )


# ---------------------------------------------------------------------------
# Prompt Formatting
# ---------------------------------------------------------------------------


def format_prompt(
    prompt: object,
    *,
    suffix: str = ": ",
) -> str:
    """
    Format an interactive command-line prompt.
    """

    value = str(prompt).strip()

    if not value:
        return suffix.lstrip()

    if value.endswith(
        (":", "?", ">")
    ):
        return f"{value} "

    return (
        f"{value}"
        f"{suffix}"
    )


def format_option(
    key: object,
    description: object,
    *,
    key_width: int = 4,
) -> str:
    """
    Format a CLI option with its description.
    """

    formatted_key = align_right(
        key,
        key_width,
    )

    return (
        f"{formatted_key}  "
        f"{description}"
    )


def format_menu_item(
    number: int,
    label: object,
    *,
    description: object | None = None,
) -> str:
    """
    Format an interactive menu item.
    """

    result = (
        f"{number}. "
        f"{label}"
    )

    if description is not None:
        result += (
            f" - {description}"
        )

    return result


# ---------------------------------------------------------------------------
# Code / Text Block Formatting
# ---------------------------------------------------------------------------


def format_code_block(
    code: object,
    *,
    language: str | None = None,
    width: int | None = None,
    indent: int = 4,
) -> str:
    """
    Format source code as an indented terminal block.
    """

    value = str(code).strip("\n")

    if width is not None:
        lines = []

        for line in value.splitlines():
            lines.extend(
                wrap_text(
                    line,
                    width=max(
                        1,
                        width - indent,
                    ),
                    break_long_words=False,
                )
            )

        value = "\n".join(
            lines
        )

    if language:
        header = (
            f"[{language}]"
        )

        value = (
            f"{header}\n"
            f"{value}"
        )

    return indent_text(
        value,
        indent,
    )


def format_block(
    text: object,
    *,
    width: int = DEFAULT_WIDTH,
    indent: int = 0,
) -> str:
    """
    Wrap and optionally indent a block of text.
    """

    wrapped = wrap_lines(
        text,
        width,
    )

    if indent:
        return indent_text(
            wrapped,
            indent,
        )

    return wrapped


# ---------------------------------------------------------------------------
# Collection Formatting
# ---------------------------------------------------------------------------


def format_list(
    values: Iterable[object],
    *,
    bullet: str = "•",
    spacing: int = 1,
    indent: int = 0,
) -> str:
    """
    Format an iterable as a bulleted list.
    """

    lines = [
        bullet_line(
            value,
            bullet=bullet,
            spacing=spacing,
        )
        for value in values
    ]

    result = "\n".join(
        lines
    )

    if indent:
        result = indent_text(
            result,
            indent,
        )

    return result


def format_numbered_list(
    values: Iterable[object],
    *,
    start: int = 1,
    spacing: int = 1,
    indent: int = 0,
) -> str:
    """
    Format an iterable as a numbered list.
    """

    lines = [
        numbered_line(
            index,
            value,
            spacing=spacing,
        )
        for index, value in enumerate(
            values,
            start=start,
        )
    ]

    result = "\n".join(
        lines
    )

    if indent:
        result = indent_text(
            result,
            indent,
        )

    return result


def format_set(
    values: Iterable[object],
    *,
    prefix: str = "{",
    suffix: str = "}",
    separator_text: str = ", ",
    sort_values: bool = False,
) -> str:
    """
    Format an iterable as a set-like representation.
    """

    items = [
        str(value)
        for value in values
    ]

    if sort_values:
        items.sort()

    return (
        prefix
        + separator_text.join(items)
        + suffix
    )


# ---------------------------------------------------------------------------
# Width Management
# ---------------------------------------------------------------------------


def fit_to_width(
    text: object,
    width: int,
    *,
    alignment: str = "left",
) -> str:
    """
    Fit text exactly into a specified width.

    Text longer than the width is truncated.
    Shorter text is padded.
    """

    if width <= 0:
        return ""

    value = str(text)

    if visible_length(value) > width:
        return truncate_text(
            value,
            width,
        )

    return align(
        value,
        width,
        mode=alignment,
    )


def fit_lines_to_width(
    lines: Iterable[object],
    width: int,
    *,
    alignment: str = "left",
) -> list[str]:
    """
    Fit multiple lines to a fixed display width.
    """

    return [
        fit_to_width(
            line,
            width,
            alignment=alignment,
        )
        for line in lines
    ]


# ---------------------------------------------------------------------------
# Configuration Helpers
# ---------------------------------------------------------------------------


_DEFAULT_CONFIG = FormatConfig()


def get_default_config() -> FormatConfig:
    """
    Return a copy of the default formatting configuration.
    """

    return _DEFAULT_CONFIG.copy()


def set_default_config(
    config: FormatConfig,
) -> None:
    """
    Replace the module-level default formatting configuration.
    """

    if not isinstance(
        config,
        FormatConfig,
    ):
        raise FormattingConfigurationError(
            "config must be a FormatConfig instance."
        )

    config.validate()

    _DEFAULT_CONFIG.width = config.width
    _DEFAULT_CONFIG.indent = config.indent
    _DEFAULT_CONFIG.padding = config.padding
    _DEFAULT_CONFIG.preserve_words = (
        config.preserve_words
    )
    _DEFAULT_CONFIG.strip_whitespace = (
        config.strip_whitespace
    )


# ---------------------------------------------------------------------------
# High-Level Formatting Helper
# ---------------------------------------------------------------------------


def format_text(
    text: object,
    *,
    width: int | None = None,
    alignment: str = "left",
    indent: int | None = None,
    truncate: bool = False,
    preserve_words: bool | None = None,
) -> str:
    """
    High-level text formatting helper.

    Combines normalization, wrapping, alignment,
    truncation, and indentation.
    """

    config = get_default_config()

    value = normalize_text(
        text,
        strip_whitespace=config.strip_whitespace,
    )

    if width is None:
        width = config.width

    if indent is None:
        indent = config.indent

    if preserve_words is None:
        preserve_words = config.preserve_words

    if truncate:
        value = truncate_text(
            value,
            width,
        )

    else:
        value = wrap_lines(
            value,
            width,
            preserve_words=preserve_words,
        )

    if alignment != "left":
        lines = [
            align(
                line,
                width,
                mode=alignment,
            )
            for line in value.splitlines()
        ]

        value = "\n".join(
            lines
        )

    if indent:
        value = indent_text(
            value,
            indent,
        )

    return value


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


__all__ = [
    # Constants
    "DEFAULT_WIDTH",
    "DEFAULT_INDENT",
    "DEFAULT_SEPARATOR",
    "DEFAULT_PADDING",
    "ELLIPSIS",

    # Exceptions
    "FormattingError",
    "FormattingConfigurationError",

    # Configuration
    "FormatConfig",
    "BoxStyle",
    "DEFAULT_BOX_STYLE",
    "get_default_config",
    "set_default_config",

    # Normalization
    "normalize_text",
    "normalize_lines",
    "split_lines",

    # ANSI utilities
    "strip_ansi",
    "visible_length",
    "truncate_ansi_safe",

    # Padding
    "pad_left",
    "pad_right",
    "pad_center",

    # Alignment
    "align_left",
    "align_right",
    "align_center",
    "align",

    # Indentation
    "indent_text",
    "dedent_text",
    "indent_lines",

    # Wrapping
    "wrap_text",
    "wrap_lines",
    "wrap_paragraphs",

    # Truncation
    "truncate_text",
    "truncate_middle",

    # Separators
    "separator",
    "double_separator",
    "dotted_separator",

    # List helpers
    "bullet_line",
    "numbered_line",
    "format_list",
    "format_numbered_list",

    # Multi-line helpers
    "format_lines",
    "join_nonempty",
    "compact_lines",
    "collapse_whitespace",

    # Key/value formatting
    "format_key_value",
    "format_key_value_block",

    # Headings
    "format_title",
    "format_heading",
    "underline_heading",

    # Boxes
    "box_text",
    "simple_box",

    # Tables
    "calculate_column_widths",
    "format_row",
    "format_table",

    # Numbers
    "format_number",
    "format_percentage",
    "format_bytes",

    # Durations
    "format_duration",

    # Status
    "format_boolean",
    "format_status",

    # Files
    "format_path",
    "format_filename",

    # Prompts / CLI
    "format_prompt",
    "format_option",
    "format_menu_item",

    # Code / blocks
    "format_code_block",
    "format_block",

    # Collections
    "format_set",

    # Width management
    "fit_to_width",
    "fit_lines_to_width",

    # High-level formatting
    "format_text",
]

