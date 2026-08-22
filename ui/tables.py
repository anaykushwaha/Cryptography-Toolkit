# tables.py
# Terminal table formatting and display utilities for the
# entire Cryptography Toolkit
#
# Provides reusable helpers for creating aligned,
# readable, terminal-friendly tables for CLI output,
# analysis results, statistics, file information,
# cryptanalysis reports, and configuration displays.


from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Sequence


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


DEFAULT_TABLE_PADDING = 1

DEFAULT_MIN_COLUMN_WIDTH = 3

DEFAULT_MAX_COLUMN_WIDTH = 60

DEFAULT_SEPARATOR = "─"

DEFAULT_VERTICAL_SEPARATOR = "│"

DEFAULT_CROSS_SEPARATOR = "┼"

DEFAULT_LEFT_CORNER = "┌"

DEFAULT_RIGHT_CORNER = "┐"

DEFAULT_BOTTOM_LEFT_CORNER = "└"

DEFAULT_BOTTOM_RIGHT_CORNER = "┘"

DEFAULT_TOP_CROSS = "┬"

DEFAULT_BOTTOM_CROSS = "┴"

DEFAULT_LEFT_CROSS = "├"

DEFAULT_RIGHT_CROSS = "┤"

DEFAULT_HEADER_SEPARATOR = "─"

DEFAULT_EMPTY_VALUE = ""

DEFAULT_TRUNCATION = "…"


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class TableError(Exception):
    """Base exception for table-related errors."""

    pass


class TableConfigurationError(
    TableError
):
    """Raised when table configuration is invalid."""

    pass


class TableDataError(
    TableError
):
    """Raised when table data is invalid."""

    pass


# ---------------------------------------------------------------------------
# Alignment
# ---------------------------------------------------------------------------


class ColumnAlignment(Enum):
    """
    Supported horizontal column alignments.
    """

    LEFT = "left"

    CENTER = "center"

    RIGHT = "right"


# ---------------------------------------------------------------------------
# Border Styles
# ---------------------------------------------------------------------------


class BorderStyle(Enum):
    """
    Built-in terminal border styles.
    """

    ROUNDED = "rounded"

    SQUARE = "square"

    DOUBLE = "double"

    MINIMAL = "minimal"

    NONE = "none"


# ---------------------------------------------------------------------------
# Table Style
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class TableStyle:
    """
    Characters used to construct a terminal table.

    A style controls the visual appearance of table borders,
    separators, and cell spacing.
    """

    top_left: str = DEFAULT_LEFT_CORNER

    top_right: str = DEFAULT_RIGHT_CORNER

    bottom_left: str = DEFAULT_BOTTOM_LEFT_CORNER

    bottom_right: str = DEFAULT_BOTTOM_RIGHT_CORNER

    top_separator: str = DEFAULT_TOP_CROSS

    bottom_separator: str = DEFAULT_BOTTOM_CROSS

    left_separator: str = DEFAULT_LEFT_CROSS

    right_separator: str = DEFAULT_RIGHT_CROSS

    cross_separator: str = DEFAULT_CROSS_SEPARATOR

    horizontal: str = DEFAULT_SEPARATOR

    vertical: str = DEFAULT_VERTICAL_SEPARATOR

    header_horizontal: str = DEFAULT_HEADER_SEPARATOR

    padding: int = DEFAULT_TABLE_PADDING

    def validate(self) -> None:
        """
        Validate table style configuration.
        """

        character_fields = (
            "top_left",
            "top_right",
            "bottom_left",
            "bottom_right",
            "top_separator",
            "bottom_separator",
            "left_separator",
            "right_separator",
            "cross_separator",
            "horizontal",
            "vertical",
            "header_horizontal",
        )

        for field_name in character_fields:
            value = getattr(
                self,
                field_name,
            )

            if not isinstance(
                value,
                str,
            ):
                raise TableConfigurationError(
                    f"{field_name} must be a string."
                )

            if len(value) != 1:
                raise TableConfigurationError(
                    f"{field_name} must contain exactly "
                    "one character."
                )

        if not isinstance(
            self.padding,
            int,
        ):
            raise TableConfigurationError(
                "padding must be an integer."
            )

        if self.padding < 0:
            raise TableConfigurationError(
                "padding cannot be negative."
            )

    def copy(
        self,
        **changes: object,
    ) -> "TableStyle":
        """
        Return a copy of this style with optional changes.
        """

        values = {
            "top_left": self.top_left,
            "top_right": self.top_right,
            "bottom_left": self.bottom_left,
            "bottom_right": self.bottom_right,
            "top_separator": self.top_separator,
            "bottom_separator": self.bottom_separator,
            "left_separator": self.left_separator,
            "right_separator": self.right_separator,
            "cross_separator": self.cross_separator,
            "horizontal": self.horizontal,
            "vertical": self.vertical,
            "header_horizontal": self.header_horizontal,
            "padding": self.padding,
        }

        values.update(changes)

        style = TableStyle(
            **values
        )

        style.validate()

        return style


# ---------------------------------------------------------------------------
# Built-In Styles
# ---------------------------------------------------------------------------


ROUNDED_STYLE = TableStyle(
    top_left="╭",
    top_right="╮",
    bottom_left="╰",
    bottom_right="╯",
    top_separator="┬",
    bottom_separator="┴",
    left_separator="├",
    right_separator="┤",
    cross_separator="┼",
    horizontal="─",
    vertical="│",
    header_horizontal="─",
    padding=1,
)


SQUARE_STYLE = TableStyle(
    top_left="┌",
    top_right="┐",
    bottom_left="└",
    bottom_right="┘",
    top_separator="┬",
    bottom_separator="┴",
    left_separator="├",
    right_separator="┤",
    cross_separator="┼",
    horizontal="─",
    vertical="│",
    header_horizontal="─",
    padding=1,
)


DOUBLE_STYLE = TableStyle(
    top_left="╔",
    top_right="╗",
    bottom_left="╚",
    bottom_right="╝",
    top_separator="╦",
    bottom_separator="╩",
    left_separator="╠",
    right_separator="╣",
    cross_separator="╬",
    horizontal="═",
    vertical="║",
    header_horizontal="═",
    padding=1,
)


MINIMAL_STYLE = TableStyle(
    top_left=" ",
    top_right=" ",
    bottom_left=" ",
    bottom_right=" ",
    top_separator=" ",
    bottom_separator=" ",
    left_separator=" ",
    right_separator=" ",
    cross_separator=" ",
    horizontal="─",
    vertical="│",
    header_horizontal="─",
    padding=1,
)


NONE_STYLE = TableStyle(
    top_left="",
    top_right="",
    bottom_left="",
    bottom_right="",
    top_separator="",
    bottom_separator="",
    left_separator="",
    right_separator="",
    cross_separator="",
    horizontal="",
    vertical=" ",
    header_horizontal="",
    padding=1,
)


# ---------------------------------------------------------------------------
# Border Style Resolver
# ---------------------------------------------------------------------------


def get_border_style(
    style: BorderStyle | TableStyle | str,
) -> TableStyle:
    """
    Resolve a border-style value into a TableStyle instance.
    """

    if isinstance(
        style,
        TableStyle,
    ):
        style.validate()
        return style

    if isinstance(
        style,
        str,
    ):
        try:
            style = BorderStyle(
                style.lower()
            )
        except ValueError as exc:
            raise TableConfigurationError(
                f"Unknown border style: {style!r}"
            ) from exc

    styles = {
        BorderStyle.ROUNDED: ROUNDED_STYLE,
        BorderStyle.SQUARE: SQUARE_STYLE,
        BorderStyle.DOUBLE: DOUBLE_STYLE,
        BorderStyle.MINIMAL: MINIMAL_STYLE,
        BorderStyle.NONE: NONE_STYLE,
    }

    try:
        return styles[style]
    except KeyError as exc:
        raise TableConfigurationError(
            f"Unsupported border style: {style!r}"
        ) from exc


# ---------------------------------------------------------------------------
# Column Configuration
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class ColumnConfig:
    """
    Configuration for an individual table column.
    """

    name: str

    alignment: ColumnAlignment = (
        ColumnAlignment.LEFT
    )

    width: int | None = None

    min_width: int = (
        DEFAULT_MIN_COLUMN_WIDTH
    )

    max_width: int = (
        DEFAULT_MAX_COLUMN_WIDTH
    )

    truncate: bool = True

    wrap: bool = False

    def validate(self) -> None:
        """Validate column configuration."""

        if not isinstance(
            self.name,
            str,
        ):
            raise TableConfigurationError(
                "Column name must be a string."
            )

        if not self.name.strip():
            raise TableConfigurationError(
                "Column name cannot be empty."
            )

        if not isinstance(
            self.alignment,
            ColumnAlignment,
        ):
            raise TableConfigurationError(
                "alignment must be a ColumnAlignment."
            )

        if self.width is not None:
            if not isinstance(
                self.width,
                int,
            ):
                raise TableConfigurationError(
                    "width must be an integer or None."
                )

            if self.width <= 0:
                raise TableConfigurationError(
                    "width must be positive."
                )

        if not isinstance(
            self.min_width,
            int,
        ):
            raise TableConfigurationError(
                "min_width must be an integer."
            )

        if self.min_width <= 0:
            raise TableConfigurationError(
                "min_width must be positive."
            )

        if not isinstance(
            self.max_width,
            int,
        ):
            raise TableConfigurationError(
                "max_width must be an integer."
            )

        if self.max_width <= 0:
            raise TableConfigurationError(
                "max_width must be positive."
            )

        if (
            self.min_width
            > self.max_width
        ):
            raise TableConfigurationError(
                "min_width cannot exceed max_width."
            )

        if self.width is not None:
            if self.width < self.min_width:
                raise TableConfigurationError(
                    "width cannot be less than min_width."
                )

            if self.width > self.max_width:
                raise TableConfigurationError(
                    "width cannot exceed max_width."
                )

        if not isinstance(
            self.truncate,
            bool,
        ):
            raise TableConfigurationError(
                "truncate must be a boolean."
            )

        if not isinstance(
            self.wrap,
            bool,
        ):
            raise TableConfigurationError(
                "wrap must be a boolean."
            )


# ---------------------------------------------------------------------------
# Table Configuration
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class TableConfig:
    """
    Configuration for a terminal table.
    """

    style: TableStyle = field(
        default_factory=lambda: SQUARE_STYLE.copy()
    )

    show_header: bool = True

    show_border: bool = True

    header_alignment: ColumnAlignment = (
        ColumnAlignment.CENTER
    )

    default_alignment: ColumnAlignment = (
        ColumnAlignment.LEFT
    )

    padding: int = DEFAULT_TABLE_PADDING

    min_column_width: int = (
        DEFAULT_MIN_COLUMN_WIDTH
    )

    max_column_width: int = (
        DEFAULT_MAX_COLUMN_WIDTH
    )

    truncate_long_values: bool = True

    wrap_long_values: bool = False

    empty_value: str = DEFAULT_EMPTY_VALUE

    def validate(self) -> None:
        """Validate table configuration."""

        if not isinstance(
            self.style,
            TableStyle,
        ):
            raise TableConfigurationError(
                "style must be a TableStyle."
            )

        self.style.validate()

        if not isinstance(
            self.show_header,
            bool,
        ):
            raise TableConfigurationError(
                "show_header must be a boolean."
            )

        if not isinstance(
            self.show_border,
            bool,
        ):
            raise TableConfigurationError(
                "show_border must be a boolean."
            )

        if not isinstance(
            self.header_alignment,
            ColumnAlignment,
        ):
            raise TableConfigurationError(
                "header_alignment must be a ColumnAlignment."
            )

        if not isinstance(
            self.default_alignment,
            ColumnAlignment,
        ):
            raise TableConfigurationError(
                "default_alignment must be a ColumnAlignment."
            )

        if not isinstance(
            self.padding,
            int,
        ):
            raise TableConfigurationError(
                "padding must be an integer."
            )

        if self.padding < 0:
            raise TableConfigurationError(
                "padding cannot be negative."
            )

        if not isinstance(
            self.min_column_width,
            int,
        ):
            raise TableConfigurationError(
                "min_column_width must be an integer."
            )

        if self.min_column_width <= 0:
            raise TableConfigurationError(
                "min_column_width must be positive."
            )

        if not isinstance(
            self.max_column_width,
            int,
        ):
            raise TableConfigurationError(
                "max_column_width must be an integer."
            )

        if self.max_column_width <= 0:
            raise TableConfigurationError(
                "max_column_width must be positive."
            )

        if (
            self.min_column_width
            > self.max_column_width
        ):
            raise TableConfigurationError(
                "min_column_width cannot exceed "
                "max_column_width."
            )

        if not isinstance(
            self.truncate_long_values,
            bool,
        ):
            raise TableConfigurationError(
                "truncate_long_values must be a boolean."
            )

        if not isinstance(
            self.wrap_long_values,
            bool,
        ):
            raise TableConfigurationError(
                "wrap_long_values must be a boolean."
            )

        if not isinstance(
            self.empty_value,
            str,
        ):
            raise TableConfigurationError(
                "empty_value must be a string."
            )

    def copy(
        self,
        **changes: object,
    ) -> "TableConfig":
        """
        Return a copy of this configuration with optional changes.
        """

        values = {
            "style": self.style.copy(),
            "show_header": self.show_header,
            "show_border": self.show_border,
            "header_alignment": self.header_alignment,
            "default_alignment": self.default_alignment,
            "padding": self.padding,
            "min_column_width": self.min_column_width,
            "max_column_width": self.max_column_width,
            "truncate_long_values": (
                self.truncate_long_values
            ),
            "wrap_long_values": (
                self.wrap_long_values
            ),
            "empty_value": self.empty_value,
        }

        values.update(changes)

        config = TableConfig(
            **values
        )

        config.validate()

        return config


# ---------------------------------------------------------------------------
# Table Data Normalization
# ---------------------------------------------------------------------------


def normalize_value(
    value: object,
    *,
    empty_value: str = DEFAULT_EMPTY_VALUE,
) -> str:
    """
    Convert a table value into a display string.
    """

    if value is None:
        return empty_value

    return str(value)


def normalize_row(
    row: Iterable[object],
    *,
    empty_value: str = DEFAULT_EMPTY_VALUE,
) -> list[str]:
    """
    Convert a row of values into display strings.
    """

    return [
        normalize_value(
            value,
            empty_value=empty_value,
        )
        for value in row
    ]


def normalize_rows(
    rows: Iterable[Iterable[object]],
    *,
    empty_value: str = DEFAULT_EMPTY_VALUE,
) -> list[list[str]]:
    """
    Normalize all table rows.
    """

    return [
        normalize_row(
            row,
            empty_value=empty_value,
        )
        for row in rows
    ]


# ---------------------------------------------------------------------------
# ANSI / Visible Width Helpers
# ---------------------------------------------------------------------------


def strip_ansi(
    text: object,
) -> str:
    """
    Remove common ANSI escape sequences from text.
    """

    import re

    value = str(text)

    return re.sub(
        r"\x1b\[[0-?]*[ -/]*[@-~]",
        "",
        value,
    )


def visible_length(
    text: object,
) -> int:
    """
    Return the visible terminal width of text.

    ANSI escape sequences are ignored.
    """

    return len(
        strip_ansi(text)
    )


# ---------------------------------------------------------------------------
# Text Truncation
# ---------------------------------------------------------------------------


def truncate_text(
    text: object,
    width: int,
    *,
    marker: str = DEFAULT_TRUNCATION,
) -> str:
    """
    Truncate text to a maximum visible width.
    """

    value = str(text)

    if width <= 0:
        return ""

    if visible_length(value) <= width:
        return value

    if not marker:
        return value[:width]

    marker_length = visible_length(
        marker
    )

    if marker_length >= width:
        return marker[:width]

    return (
        value[
            : width - marker_length
        ]
        + marker
    )


# ---------------------------------------------------------------------------
# Column Width Calculation
# ---------------------------------------------------------------------------


def calculate_column_widths(
    rows: Sequence[Sequence[object]],
    *,
    headers: Sequence[object] | None = None,
    padding: int = DEFAULT_TABLE_PADDING,
    min_width: int = DEFAULT_MIN_COLUMN_WIDTH,
    max_width: int = DEFAULT_MAX_COLUMN_WIDTH,
) -> list[int]:
    """
    Calculate appropriate widths for table columns.

    Width values include the content area but exclude
    cell padding.
    """

    if padding < 0:
        raise ValueError(
            "padding cannot be negative."
        )

    if min_width <= 0:
        raise ValueError(
            "min_width must be positive."
        )

    if max_width < min_width:
        raise ValueError(
            "max_width cannot be less than min_width."
        )

    row_data = [
        list(row)
        for row in rows
    ]

    if headers is not None:
        row_data.insert(
            0,
            list(headers),
        )

    if not row_data:
        return []

    column_count = max(
        len(row)
        for row in row_data
    )

    widths = [
        min_width
        for _ in range(column_count)
    ]

    for row in row_data:
        for index in range(
            column_count
        ):
            if index >= len(row):
                continue

            value = normalize_value(
                row[index]
            )

            length = visible_length(
                value
            )

            widths[index] = max(
                widths[index],
                min(
                    length,
                    max_width,
                ),
            )

    return widths


# ---------------------------------------------------------------------------
# Column Normalization
# ---------------------------------------------------------------------------


def normalize_column_configs(
    columns: Sequence[
        ColumnConfig | str
    ],
) -> list[ColumnConfig]:
    """
    Normalize column definitions into ColumnConfig objects.
    """

    result: list[ColumnConfig] = []

    for column in columns:
        if isinstance(
            column,
            ColumnConfig,
        ):
            column.validate()

            result.append(
                column
            )

        elif isinstance(
            column,
            str,
        ):
            config = ColumnConfig(
                name=column
            )

            config.validate()

            result.append(
                config
            )

        else:
            raise TableConfigurationError(
                "Columns must contain strings "
                "or ColumnConfig objects."
            )

    return result


# ---------------------------------------------------------------------------
# Cell Formatting
# ---------------------------------------------------------------------------


def align_cell(
    value: object,
    width: int,
    alignment: ColumnAlignment,
    *,
    padding: int = DEFAULT_TABLE_PADDING,
) -> str:
    """
    Align a single table cell.
    """

    text = normalize_value(
        value
    )

    content_width = max(
        0,
        width - (padding * 2),
    )

    text = truncate_text(
        text,
        content_width,
    )

    remaining = max(
        0,
        content_width
        - visible_length(text),
    )

    if alignment == ColumnAlignment.LEFT:
        text = (
            text
            + " " * remaining
        )

    elif alignment == ColumnAlignment.RIGHT:
        text = (
            " " * remaining
            + text
        )

    elif alignment == ColumnAlignment.CENTER:
        left = remaining // 2

        right = (
            remaining - left
        )

        text = (
            " " * left
            + text
            + " " * right
        )

    else:
        raise TableConfigurationError(
            f"Unsupported alignment: "
            f"{alignment!r}"
        )

    return (
        " " * padding
        + text
        + " " * padding
    )


def format_row(
    row: Sequence[object],
    widths: Sequence[int],
    *,
    alignments: Sequence[
        ColumnAlignment
    ] | None = None,
    style: TableStyle | None = None,
    padding: int = DEFAULT_TABLE_PADDING,
) -> str:
    """
    Format a single table row.
    """

    if style is None:
        style = SQUARE_STYLE

    style.validate()

    if alignments is None:
        alignments = [
            ColumnAlignment.LEFT
            for _ in widths
        ]

    if len(row) > len(widths):
        raise TableDataError(
            "Row contains more values "
            "than available columns."
        )

    cells: list[str] = []

    for index, width in enumerate(
        widths
    ):
        value = (
            row[index]
            if index < len(row)
            else DEFAULT_EMPTY_VALUE
        )

        alignment = (
            alignments[index]
            if index < len(alignments)
            else ColumnAlignment.LEFT
        )

        cells.append(
            align_cell(
                value,
                width,
                alignment,
                padding=padding,
            )
        )

    if style.vertical:
        return (
            style.vertical
            + style.vertical.join(cells)
            + style.vertical
        )

    return " ".join(cells)

# ---------------------------------------------------------------------------
# Separator Rendering
# ---------------------------------------------------------------------------


def build_separator(
    widths: Sequence[int],
    *,
    style: TableStyle | None = None,
    position: str = "middle",
) -> str:
    """
    Build a horizontal table separator.

    Parameters
    ----------
    widths:
        Column widths.

    style:
        Table style.

    position:
        Separator position. Supported values are:

        - ``top``
        - ``middle``
        - ``header``
        - ``bottom``
    """

    if style is None:
        style = SQUARE_STYLE

    style.validate()

    if not widths:
        return ""

    if position == "top":
        left = style.top_left
        right = style.top_right
        junction = style.top_separator

    elif position == "bottom":
        left = style.bottom_left
        right = style.bottom_right
        junction = style.bottom_separator

    elif position in {
        "middle",
        "header",
    }:
        left = style.left_separator
        right = style.right_separator
        junction = style.cross_separator

    else:
        raise ValueError(
            "position must be one of: "
            "top, middle, header, bottom."
        )

    sections = [
        style.horizontal * width
        for width in widths
    ]

    return (
        left
        + junction.join(sections)
        + right
    )


def build_header_separator(
    widths: Sequence[int],
    *,
    style: TableStyle | None = None,
) -> str:
    """
    Build the separator directly below a table header.
    """

    if style is None:
        style = SQUARE_STYLE

    style.validate()

    sections = [
        style.header_horizontal * width
        for width in widths
    ]

    return (
        style.left_separator
        + style.cross_separator.join(
            sections
        )
        + style.right_separator
    )


# ---------------------------------------------------------------------------
# Header Formatting
# ---------------------------------------------------------------------------


def format_header(
    headers: Sequence[object],
    widths: Sequence[int],
    *,
    alignment: ColumnAlignment = (
        ColumnAlignment.CENTER
    ),
    style: TableStyle | None = None,
    padding: int = DEFAULT_TABLE_PADDING,
) -> str:
    """
    Format a table header row.
    """

    if style is None:
        style = SQUARE_STYLE

    style.validate()

    alignments = [
        alignment
        for _ in widths
    ]

    return format_row(
        headers,
        widths,
        alignments=alignments,
        style=style,
        padding=padding,
    )


# ---------------------------------------------------------------------------
# Table Row Validation
# ---------------------------------------------------------------------------


def validate_rows(
    rows: Sequence[Sequence[object]],
    column_count: int,
    *,
    allow_short_rows: bool = True,
) -> None:
    """
    Validate table rows against the expected column count.
    """

    if column_count < 0:
        raise TableDataError(
            "column_count cannot be negative."
        )

    for index, row in enumerate(
        rows
    ):
        if not isinstance(
            row,
            Sequence,
        ):
            raise TableDataError(
                f"Row {index} must be a sequence."
            )

        if len(row) > column_count:
            raise TableDataError(
                f"Row {index} contains "
                f"{len(row)} values, but the table "
                f"only has {column_count} columns."
            )

        if (
            not allow_short_rows
            and len(row) != column_count
        ):
            raise TableDataError(
                f"Row {index} must contain exactly "
                f"{column_count} values."
            )


def determine_column_count(
    rows: Sequence[Sequence[object]],
    headers: Sequence[object] | None = None,
) -> int:
    """
    Determine the required number of table columns.
    """

    count = 0

    if headers is not None:
        count = max(
            count,
            len(headers),
        )

    for row in rows:
        count = max(
            count,
            len(row),
        )

    return count


# ---------------------------------------------------------------------------
# Table Builder
# ---------------------------------------------------------------------------


class TableBuilder:
    """
    Build and render terminal-friendly tables.

    The builder supports incremental construction of headers,
    rows, columns, and table configuration.
    """

    def __init__(
        self,
        *,
        headers: Sequence[object] | None = None,
        config: TableConfig | None = None,
    ) -> None:
        if config is None:
            config = TableConfig()

        config.validate()

        self.config = config

        self.headers = (
            list(headers)
            if headers is not None
            else []
        )

        self.rows: list[list[object]] = []

        self.columns: list[
            ColumnConfig
        ] = []

    # -----------------------------------------------------------------------
    # Configuration
    # -----------------------------------------------------------------------

    def set_config(
        self,
        config: TableConfig,
    ) -> "TableBuilder":
        """
        Replace the current table configuration.
        """

        config.validate()

        self.config = config

        return self

    def set_style(
        self,
        style: (
            TableStyle
            | BorderStyle
            | str
        ),
    ) -> "TableBuilder":
        """
        Set the table border style.
        """

        self.config.style = get_border_style(
            style
        )

        return self

    def set_header_visibility(
        self,
        visible: bool,
    ) -> "TableBuilder":
        """
        Enable or disable the table header.
        """

        if not isinstance(
            visible,
            bool,
        ):
            raise TableConfigurationError(
                "visible must be a boolean."
            )

        self.config.show_header = visible

        return self

    # -----------------------------------------------------------------------
    # Headers
    # -----------------------------------------------------------------------

    def set_headers(
        self,
        headers: Sequence[object],
    ) -> "TableBuilder":
        """
        Replace the table headers.
        """

        self.headers = list(
            headers
        )

        return self

    def add_header(
        self,
        header: object,
    ) -> "TableBuilder":
        """
        Append one header.
        """

        self.headers.append(
            header
        )

        return self

    def clear_headers(
        self,
    ) -> "TableBuilder":
        """
        Remove all headers.
        """

        self.headers.clear()

        return self

    # -----------------------------------------------------------------------
    # Rows
    # -----------------------------------------------------------------------

    def add_row(
        self,
        row: Iterable[object],
    ) -> "TableBuilder":
        """
        Add one row to the table.
        """

        self.rows.append(
            list(row)
        )

        return self

    def add_rows(
        self,
        rows: Iterable[
            Iterable[object]
        ],
    ) -> "TableBuilder":
        """
        Add multiple rows.
        """

        for row in rows:
            self.add_row(
                row
            )

        return self

    def set_rows(
        self,
        rows: Iterable[
            Iterable[object]
        ],
    ) -> "TableBuilder":
        """
        Replace all table rows.
        """

        self.rows = [
            list(row)
            for row in rows
        ]

        return self

    def clear_rows(
        self,
    ) -> "TableBuilder":
        """
        Remove all table rows.
        """

        self.rows.clear()

        return self

    # -----------------------------------------------------------------------
    # Columns
    # -----------------------------------------------------------------------

    def set_columns(
        self,
        columns: Sequence[
            ColumnConfig | str
        ],
    ) -> "TableBuilder":
        """
        Configure table columns.
        """

        self.columns = (
            normalize_column_configs(
                columns
            )
        )

        return self

    def add_column(
        self,
        column: ColumnConfig | str,
    ) -> "TableBuilder":
        """
        Add a column configuration.
        """

        self.columns.extend(
            normalize_column_configs(
                [column]
            )
        )

        return self

    def clear_columns(
        self,
    ) -> "TableBuilder":
        """
        Remove all column configurations.
        """

        self.columns.clear()

        return self

    # -----------------------------------------------------------------------
    # Column Resolution
    # -----------------------------------------------------------------------

    def _column_count(self) -> int:
        """
        Determine the effective number of columns.
        """

        return determine_column_count(
            self.rows,
            self.headers or None,
        )

    def _resolved_columns(
        self,
    ) -> list[ColumnConfig]:
        """
        Resolve explicit or automatic column configurations.
        """

        count = self._column_count()

        if count == 0:
            return []

        columns = list(
            self.columns
        )

        while len(columns) < count:
            index = len(columns)

            if index < len(
                self.headers
            ):
                name = str(
                    self.headers[index]
                )

            else:
                name = (
                    f"Column {index + 1}"
                )

            columns.append(
                ColumnConfig(
                    name=name,
                    alignment=(
                        self.config.default_alignment
                    ),
                    min_width=(
                        self.config.min_column_width
                    ),
                    max_width=(
                        self.config.max_column_width
                    ),
                    truncate=(
                        self.config.truncate_long_values
                    ),
                    wrap=(
                        self.config.wrap_long_values
                    ),
                )
            )

        for column in columns:
            column.validate()

        return columns[:count]

    # -----------------------------------------------------------------------
    # Width Resolution
    # -----------------------------------------------------------------------

    def _calculate_widths(
        self,
    ) -> list[int]:
        """
        Calculate effective column widths.
        """

        columns = self._resolved_columns()

        if not columns:
            return []

        widths = calculate_column_widths(
            self.rows,
            headers=(
                self.headers
                if self.headers
                else None
            ),
            padding=self.config.padding,
            min_width=self.config.min_column_width,
            max_width=self.config.max_column_width,
        )

        for index, column in enumerate(
            columns
        ):
            if column.width is not None:
                widths[index] = (
                    column.width
                )

            else:
                widths[index] = max(
                    widths[index],
                    column.min_width,
                )

                widths[index] = min(
                    widths[index],
                    column.max_width,
                )

        return widths

    # -----------------------------------------------------------------------
    # Alignment Resolution
    # -----------------------------------------------------------------------

    def _alignments(
        self,
    ) -> list[ColumnAlignment]:
        """
        Resolve alignment for each column.
        """

        columns = self._resolved_columns()

        return [
            column.alignment
            for column in columns
        ]

    # -----------------------------------------------------------------------
    # Validation
    # -----------------------------------------------------------------------

    def validate(
        self,
    ) -> None:
        """
        Validate the complete table definition.
        """

        self.config.validate()

        count = self._column_count()

        if count == 0:
            return

        validate_rows(
            self.rows,
            count,
            allow_short_rows=True,
        )

        if (
            self.headers
            and len(self.headers) > count
        ):
            raise TableDataError(
                "Header contains too many values."
            )

        self._resolved_columns()

    # -----------------------------------------------------------------------
    # Rendering
    # -----------------------------------------------------------------------

    def render(
        self,
    ) -> str:
        """
        Render the complete table as a string.
        """

        self.validate()

        count = self._column_count()

        if count == 0:
            return ""

        widths = self._calculate_widths()

        alignments = self._alignments()

        style = self.config.style

        lines: list[str] = []

        # Top border
        if self.config.show_border:
            lines.append(
                build_separator(
                    widths,
                    style=style,
                    position="top",
                )
            )

        # Header
        if (
            self.config.show_header
            and self.headers
        ):
            lines.append(
                format_header(
                    self.headers,
                    widths,
                    alignment=(
                        self.config.header_alignment
                    ),
                    style=style,
                    padding=self.config.padding,
                )
            )

            if self.config.show_border:
                lines.append(
                    build_header_separator(
                        widths,
                        style=style,
                    )
                )

        # Data rows
        for index, row in enumerate(
            self.rows
        ):
            lines.append(
                format_row(
                    row,
                    widths,
                    alignments=alignments,
                    style=style,
                    padding=self.config.padding,
                )
            )

            if (
                self.config.show_border
                and index < len(self.rows) - 1
            ):
                lines.append(
                    build_separator(
                        widths,
                        style=style,
                        position="middle",
                    )
                )

        # Bottom border
        if self.config.show_border:
            lines.append(
                build_separator(
                    widths,
                    style=style,
                    position="bottom",
                )
            )

        return "\n".join(
            lines
        )

    def __str__(
        self,
    ) -> str:
        """
        Return the rendered table.
        """

        return self.render()

    # ---------------------------------------------------------------------------
# Table Output
# ---------------------------------------------------------------------------


def print_table(
    rows: Iterable[Iterable[object]],
    *,
    headers: Sequence[object] | None = None,
    config: TableConfig | None = None,
    columns: Sequence[
        ColumnConfig | str
    ] | None = None,
    stream=None,
) -> None:
    """
    Render and print a table to a text stream.

    Parameters
    ----------
    rows:
        Table data.

    headers:
        Optional table headers.

    config:
        Optional table configuration.

    columns:
        Optional column configurations.

    stream:
        Output stream. Defaults to ``sys.stdout``.
    """

    import sys

    if stream is None:
        stream = sys.stdout

    builder = TableBuilder(
        headers=headers,
        config=config,
    )

    builder.add_rows(
        rows
    )

    if columns is not None:
        builder.set_columns(
            columns
        )

    stream.write(
        builder.render()
    )

    stream.write(
        "\n"
    )

    stream.flush()


def table_to_string(
    rows: Iterable[Iterable[object]],
    *,
    headers: Sequence[object] | None = None,
    config: TableConfig | None = None,
    columns: Sequence[
        ColumnConfig | str
    ] | None = None,
) -> str:
    """
    Convert table data directly into a string.
    """

    builder = TableBuilder(
        headers=headers,
        config=config,
    )

    builder.add_rows(
        rows
    )

    if columns is not None:
        builder.set_columns(
            columns
        )

    return builder.render()


# ---------------------------------------------------------------------------
# Key-Value Tables
# ---------------------------------------------------------------------------


def key_value_table(
    values: dict[object, object],
    *,
    key_header: object = "Key",
    value_header: object = "Value",
    config: TableConfig | None = None,
) -> str:
    """
    Create a two-column key-value table.
    """

    rows = [
        [key, value]
        for key, value in values.items()
    ]

    return table_to_string(
        rows,
        headers=[
            key_header,
            value_header,
        ],
        config=config,
    )


def print_key_value_table(
    values: dict[object, object],
    *,
    key_header: object = "Key",
    value_header: object = "Value",
    config: TableConfig | None = None,
    stream=None,
) -> None:
    """
    Print a two-column key-value table.
    """

    import sys

    if stream is None:
        stream = sys.stdout

    text = key_value_table(
        values,
        key_header=key_header,
        value_header=value_header,
        config=config,
    )

    stream.write(
        text
        + "\n"
    )

    stream.flush()


# ---------------------------------------------------------------------------
# Statistics Tables
# ---------------------------------------------------------------------------


def statistics_table(
    statistics: dict[
        object,
        object,
    ],
    *,
    name_header: object = "Statistic",
    value_header: object = "Value",
    config: TableConfig | None = None,
) -> str:
    """
    Create a table for statistical or analytical results.

    Useful for displaying frequency analysis, entropy,
    index-of-coincidence values, scores, and other
    cryptanalysis metrics.
    """

    return key_value_table(
        statistics,
        key_header=name_header,
        value_header=value_header,
        config=config,
    )


# ---------------------------------------------------------------------------
# Result Tables
# ---------------------------------------------------------------------------


def result_table(
    results: Iterable[
        dict[object, object]
    ],
    *,
    headers: Sequence[object] | None = None,
    config: TableConfig | None = None,
) -> str:
    """
    Convert a collection of dictionaries into a table.

    If headers are not supplied, the keys from the first
    result dictionary are used.
    """

    result_list = list(
        results
    )

    if not result_list:
        return ""

    if headers is None:
        headers = list(
            result_list[0].keys()
        )

    rows: list[list[object]] = []

    for result in result_list:
        rows.append(
            [
                result.get(
                    header,
                    None,
                )
                for header in headers
            ]
        )

    return table_to_string(
        rows,
        headers=headers,
        config=config,
    )


# ---------------------------------------------------------------------------
# Table Sorting
# ---------------------------------------------------------------------------


def sort_rows(
    rows: Iterable[Sequence[object]],
    *,
    column: int,
    reverse: bool = False,
    key=None,
) -> list[list[object]]:
    """
    Sort table rows by a specified column.

    Parameters
    ----------
    rows:
        Rows to sort.

    column:
        Zero-based column index.

    reverse:
        Reverse the sort order.

    key:
        Optional transformation applied to the
        selected column value.
    """

    row_list = [
        list(row)
        for row in rows
    ]

    if column < 0:
        raise ValueError(
            "column cannot be negative."
        )

    for index, row in enumerate(
        row_list
    ):
        if column >= len(row):
            raise TableDataError(
                f"Column {column} does not exist "
                f"in row {index}."
            )

    if key is None:
        return sorted(
            row_list,
            key=lambda row: row[column],
            reverse=reverse,
        )

    return sorted(
        row_list,
        key=lambda row: key(
            row[column]
        ),
        reverse=reverse,
    )


# ---------------------------------------------------------------------------
# Table Filtering
# ---------------------------------------------------------------------------


def filter_rows(
    rows: Iterable[Sequence[object]],
    predicate,
) -> list[list[object]]:
    """
    Filter rows using a predicate function.

    The predicate receives the complete row.
    """

    return [
        list(row)
        for row in rows
        if predicate(row)
    ]


def filter_column(
    rows: Iterable[Sequence[object]],
    *,
    column: int,
    predicate,
) -> list[list[object]]:
    """
    Filter rows based on a specific column.
    """

    if column < 0:
        raise ValueError(
            "column cannot be negative."
        )

    result: list[list[object]] = []

    for index, row in enumerate(
        rows
    ):
        row_list = list(row)

        if column >= len(row_list):
            raise TableDataError(
                f"Column {column} does not exist "
                f"in row {index}."
            )

        if predicate(
            row_list[column]
        ):
            result.append(
                row_list
            )

    return result


# ---------------------------------------------------------------------------
# Table Projection
# ---------------------------------------------------------------------------


def select_columns(
    rows: Iterable[Sequence[object]],
    columns: Sequence[int],
) -> list[list[object]]:
    """
    Select specific columns from table rows.
    """

    normalized_columns = list(
        columns
    )

    for column in normalized_columns:
        if column < 0:
            raise ValueError(
                "Column indexes cannot be negative."
            )

    result: list[list[object]] = []

    for row_index, row in enumerate(
        rows
    ):
        row_list = list(row)

        selected: list[object] = []

        for column in normalized_columns:
            if column >= len(row_list):
                raise TableDataError(
                    f"Column {column} does not exist "
                    f"in row {row_index}."
                )

            selected.append(
                row_list[column]
            )

        result.append(
            selected
        )

    return result


# ---------------------------------------------------------------------------
# Table Transformation
# ---------------------------------------------------------------------------


def transpose_rows(
    rows: Iterable[Sequence[object]],
    *,
    fill_value: object = None,
) -> list[list[object]]:
    """
    Transpose a table.

    Short rows are padded with ``fill_value``.
    """

    row_list = [
        list(row)
        for row in rows
    ]

    if not row_list:
        return []

    width = max(
        len(row)
        for row in row_list
    )

    result: list[list[object]] = []

    for column in range(
        width
    ):
        result.append(
            [
                (
                    row[column]
                    if column < len(row)
                    else fill_value
                )
                for row in row_list
            ]
        )

    return result


# ---------------------------------------------------------------------------
# Table Summary
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class TableSummary:
    """
    Summary information about a table.
    """

    rows: int

    columns: int

    cells: int

    headers: bool

    empty_cells: int

    @property
    def populated_cells(self) -> int:
        """Return the number of non-empty cells."""

        return max(
            0,
            self.cells - self.empty_cells,
        )


def summarize_table(
    rows: Iterable[Sequence[object]],
    *,
    headers: Sequence[object] | None = None,
) -> TableSummary:
    """
    Calculate basic structural information about table data.
    """

    row_list = [
        list(row)
        for row in rows
    ]

    column_count = determine_column_count(
        row_list,
        headers,
    )

    cell_count = (
        len(row_list)
        * column_count
    )

    empty_cells = 0

    for row in row_list:
        for index in range(
            column_count
        ):
            if index >= len(row):
                empty_cells += 1

            elif row[index] is None:
                empty_cells += 1

            elif str(
                row[index]
            ).strip() == "":
                empty_cells += 1

    return TableSummary(
        rows=len(row_list),
        columns=column_count,
        cells=cell_count,
        headers=headers is not None,
        empty_cells=empty_cells,
    )


# ---------------------------------------------------------------------------
# Specialized Cryptography Tables
# ---------------------------------------------------------------------------


def frequency_table(
    frequencies: dict[
        object,
        int | float,
    ],
    *,
    symbol_header: object = "Symbol",
    frequency_header: object = "Frequency",
    percentage_header: object = "Percentage",
    config: TableConfig | None = None,
) -> str:
    """
    Create a frequency-analysis table.

    Frequencies are automatically sorted from highest
    to lowest.
    """

    items = sorted(
        frequencies.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    total = sum(
        value
        for _, value in items
    )

    rows: list[list[object]] = []

    for symbol, frequency in items:
        if total > 0:
            percentage = (
                float(frequency)
                / total
                * 100
            )
        else:
            percentage = 0.0

        rows.append(
            [
                symbol,
                frequency,
                f"{percentage:.2f}%",
            ]
        )

    return table_to_string(
        rows,
        headers=[
            symbol_header,
            frequency_header,
            percentage_header,
        ],
        config=config,
    )


def score_table(
    scores: Iterable[
        tuple[object, float]
    ],
    *,
    key_header: object = "Key",
    score_header: object = "Score",
    descending: bool = True,
    config: TableConfig | None = None,
) -> str:
    """
    Create a cryptanalysis score table.
    """

    sorted_scores = sorted(
        scores,
        key=lambda item: item[1],
        reverse=descending,
    )

    rows = [
        [key, score]
        for key, score in sorted_scores
    ]

    return table_to_string(
        rows,
        headers=[
            key_header,
            score_header,
        ],
        config=config,
    )


def candidates_table(
    candidates: Iterable[
        tuple[object, object]
    ],
    *,
    key_header: object = "Key",
    plaintext_header: object = "Plaintext",
    config: TableConfig | None = None,
) -> str:
    """
    Create a table of cipher-analysis candidates.
    """

    rows = [
        [key, plaintext]
        for key, plaintext in candidates
    ]

    return table_to_string(
        rows,
        headers=[
            key_header,
            plaintext_header,
        ],
        config=config,
    )


# ---------------------------------------------------------------------------
# Table Presets
# ---------------------------------------------------------------------------


def default_table_config() -> TableConfig:
    """
    Return the standard toolkit table configuration.
    """

    return TableConfig(
        style=SQUARE_STYLE.copy(),
        show_header=True,
        show_border=True,
        header_alignment=(
            ColumnAlignment.CENTER
        ),
        default_alignment=(
            ColumnAlignment.LEFT
        ),
        padding=1,
        min_column_width=3,
        max_column_width=60,
        truncate_long_values=True,
        wrap_long_values=False,
    )


def compact_table_config() -> TableConfig:
    """
    Return a compact table configuration.
    """

    return TableConfig(
        style=MINIMAL_STYLE.copy(
            padding=0
        ),
        show_header=True,
        show_border=True,
        header_alignment=(
            ColumnAlignment.LEFT
        ),
        default_alignment=(
            ColumnAlignment.LEFT
        ),
        padding=0,
        min_column_width=1,
        max_column_width=40,
        truncate_long_values=True,
        wrap_long_values=False,
    )


def borderless_table_config() -> TableConfig:
    """
    Return a borderless table configuration.
    """

    return TableConfig(
        style=NONE_STYLE.copy(),
        show_header=True,
        show_border=False,
        header_alignment=(
            ColumnAlignment.LEFT
        ),
        default_alignment=(
            ColumnAlignment.LEFT
        ),
        padding=1,
        min_column_width=3,
        max_column_width=60,
        truncate_long_values=True,
        wrap_long_values=False,
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


__all__ = [
    # Exceptions
    "TableError",
    "TableConfigurationError",
    "TableDataError",

    # Enums
    "ColumnAlignment",
    "BorderStyle",

    # Styles
    "TableStyle",
    "ROUNDED_STYLE",
    "SQUARE_STYLE",
    "DOUBLE_STYLE",
    "MINIMAL_STYLE",
    "NONE_STYLE",
    "get_border_style",

    # Configuration
    "ColumnConfig",
    "TableConfig",

    # Data normalization
    "normalize_value",
    "normalize_row",
    "normalize_rows",

    # ANSI / width helpers
    "strip_ansi",
    "visible_length",
    "truncate_text",
    "calculate_column_widths",

    # Column helpers
    "normalize_column_configs",

    # Cell / row formatting
    "align_cell",
    "format_row",
    "format_header",

    # Separators
    "build_separator",
    "build_header_separator",

    # Validation
    "validate_rows",
    "determine_column_count",

    # Main builder
    "TableBuilder",

    # Output
    "print_table",
    "table_to_string",

    # Key-value tables
    "key_value_table",
    "print_key_value_table",

    # Analysis tables
    "statistics_table",
    "frequency_table",
    "score_table",
    "candidates_table",
    "result_table",

    # Table operations
    "sort_rows",
    "filter_rows",
    "filter_column",
    "select_columns",
    "transpose_rows",

    # Table information
    "TableSummary",
    "summarize_table",

    # Configuration presets
    "default_table_config",
    "compact_table_config",
    "borderless_table_config",
]

