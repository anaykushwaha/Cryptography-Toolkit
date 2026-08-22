# progress.py
# Progress display and terminal progress utilities for the
# entire Cryptography Toolkit
#
# Provides reusable helpers for progress bars, spinners,
# counters, percentage displays, elapsed-time tracking,
# and terminal-friendly progress reporting.


from __future__ import annotations

import sys
import time

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Iterable, TextIO


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


DEFAULT_BAR_WIDTH = 40

DEFAULT_FILL_CHARACTER = "█"

DEFAULT_EMPTY_CHARACTER = "░"

DEFAULT_PREFIX = ""

DEFAULT_SUFFIX = ""

DEFAULT_UPDATE_INTERVAL = 0.1

DEFAULT_SPINNER_INTERVAL = 0.1

DEFAULT_PERCENTAGE_PRECISION = 1

CARRIAGE_RETURN = "\r"

CLEAR_LINE = "\033[2K"

CURSOR_HIDE = "\033[?25l"

CURSOR_SHOW = "\033[?25h"


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class ProgressError(Exception):
    """Base exception for progress-related errors."""

    pass


class ProgressConfigurationError(
    ProgressError
):
    """Raised when progress configuration is invalid."""

    pass


class ProgressStateError(
    ProgressError
):
    """Raised when a progress object is used in an invalid state."""

    pass


# ---------------------------------------------------------------------------
# Progress State
# ---------------------------------------------------------------------------


class ProgressState(Enum):
    """
    Current state of a progress display.
    """

    IDLE = "idle"

    RUNNING = "running"

    PAUSED = "paused"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"


# ---------------------------------------------------------------------------
# Spinner Styles
# ---------------------------------------------------------------------------


class SpinnerStyle(Enum):
    """
    Built-in spinner animation styles.
    """

    DOTS = (
        "⠋",
        "⠙",
        "⠹",
        "⠸",
        "⠼",
        "⠴",
        "⠦",
        "⠧",
        "⠇",
        "⠏",
    )

    LINE = (
        "|",
        "/",
        "-",
        "\\",
    )

    BLOCKS = (
        "▖",
        "▘",
        "▝",
        "▗",
    )

    ARROWS = (
        "←",
        "↖",
        "↑",
        "↗",
        "→",
        "↘",
        "↓",
        "↙",
    )

    SIMPLE = (
        ".",
        "..",
        "...",
        "..",
    )


# ---------------------------------------------------------------------------
# Progress Configuration
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class ProgressConfig:
    """
    Configuration for progress displays.

    Parameters
    ----------
    width:
        Width of the progress bar.

    fill:
        Character used for completed progress.

    empty:
        Character used for incomplete progress.

    prefix:
        Text displayed before the progress bar.

    suffix:
        Text displayed after the progress bar.

    show_percentage:
        Whether to display completion percentage.

    show_count:
        Whether to display current/total values.

    show_elapsed:
        Whether to display elapsed time.

    show_eta:
        Whether to display estimated remaining time.

    update_interval:
        Minimum interval between visual updates.

    percentage_precision:
        Number of decimal places in the percentage.

    clear_line:
        Whether to clear the previous line before updating.

    hide_cursor:
        Whether the terminal cursor should be hidden while active.
    """

    width: int = DEFAULT_BAR_WIDTH

    fill: str = DEFAULT_FILL_CHARACTER

    empty: str = DEFAULT_EMPTY_CHARACTER

    prefix: str = DEFAULT_PREFIX

    suffix: str = DEFAULT_SUFFIX

    show_percentage: bool = True

    show_count: bool = True

    show_elapsed: bool = False

    show_eta: bool = False

    update_interval: float = (
        DEFAULT_UPDATE_INTERVAL
    )

    percentage_precision: int = (
        DEFAULT_PERCENTAGE_PRECISION
    )

    clear_line: bool = True

    hide_cursor: bool = False

    def validate(self) -> None:
        """Validate progress configuration."""

        if not isinstance(
            self.width,
            int,
        ):
            raise ProgressConfigurationError(
                "width must be an integer."
            )

        if self.width <= 0:
            raise ProgressConfigurationError(
                "width must be positive."
            )

        if not isinstance(
            self.fill,
            str,
        ):
            raise ProgressConfigurationError(
                "fill must be a string."
            )

        if not self.fill:
            raise ProgressConfigurationError(
                "fill cannot be empty."
            )

        if not isinstance(
            self.empty,
            str,
        ):
            raise ProgressConfigurationError(
                "empty must be a string."
            )

        if not self.empty:
            raise ProgressConfigurationError(
                "empty cannot be empty."
            )

        if not isinstance(
            self.prefix,
            str,
        ):
            raise ProgressConfigurationError(
                "prefix must be a string."
            )

        if not isinstance(
            self.suffix,
            str,
        ):
            raise ProgressConfigurationError(
                "suffix must be a string."
            )

        if not isinstance(
            self.show_percentage,
            bool,
        ):
            raise ProgressConfigurationError(
                "show_percentage must be a boolean."
            )

        if not isinstance(
            self.show_count,
            bool,
        ):
            raise ProgressConfigurationError(
                "show_count must be a boolean."
            )

        if not isinstance(
            self.show_elapsed,
            bool,
        ):
            raise ProgressConfigurationError(
                "show_elapsed must be a boolean."
            )

        if not isinstance(
            self.show_eta,
            bool,
        ):
            raise ProgressConfigurationError(
                "show_eta must be a boolean."
            )

        if not isinstance(
            self.update_interval,
            (int, float),
        ):
            raise ProgressConfigurationError(
                "update_interval must be numeric."
            )

        if self.update_interval < 0:
            raise ProgressConfigurationError(
                "update_interval cannot be negative."
            )

        if not isinstance(
            self.percentage_precision,
            int,
        ):
            raise ProgressConfigurationError(
                "percentage_precision must be an integer."
            )

        if self.percentage_precision < 0:
            raise ProgressConfigurationError(
                "percentage_precision cannot be negative."
            )

        if not isinstance(
            self.clear_line,
            bool,
        ):
            raise ProgressConfigurationError(
                "clear_line must be a boolean."
            )

        if not isinstance(
            self.hide_cursor,
            bool,
        ):
            raise ProgressConfigurationError(
                "hide_cursor must be a boolean."
            )

    def copy(
        self,
        **changes: object,
    ) -> "ProgressConfig":
        """
        Return a copy of this configuration with optional changes.
        """

        values = {
            "width": self.width,
            "fill": self.fill,
            "empty": self.empty,
            "prefix": self.prefix,
            "suffix": self.suffix,
            "show_percentage": self.show_percentage,
            "show_count": self.show_count,
            "show_elapsed": self.show_elapsed,
            "show_eta": self.show_eta,
            "update_interval": self.update_interval,
            "percentage_precision": (
                self.percentage_precision
            ),
            "clear_line": self.clear_line,
            "hide_cursor": self.hide_cursor,
        }

        values.update(changes)

        config = ProgressConfig(
            **values
        )

        config.validate()

        return config


# ---------------------------------------------------------------------------
# Spinner Configuration
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class SpinnerConfig:
    """
    Configuration for spinner displays.
    """

    style: SpinnerStyle = SpinnerStyle.DOTS

    interval: float = DEFAULT_SPINNER_INTERVAL

    message: str = ""

    prefix: str = ""

    suffix: str = ""

    hide_cursor: bool = True

    clear_line: bool = True

    def validate(self) -> None:
        """Validate spinner configuration."""

        if not isinstance(
            self.style,
            SpinnerStyle,
        ):
            raise ProgressConfigurationError(
                "style must be a SpinnerStyle."
            )

        if not isinstance(
            self.interval,
            (int, float),
        ):
            raise ProgressConfigurationError(
                "interval must be numeric."
            )

        if self.interval < 0:
            raise ProgressConfigurationError(
                "interval cannot be negative."
            )

        if not isinstance(
            self.message,
            str,
        ):
            raise ProgressConfigurationError(
                "message must be a string."
            )

        if not isinstance(
            self.prefix,
            str,
        ):
            raise ProgressConfigurationError(
                "prefix must be a string."
            )

        if not isinstance(
            self.suffix,
            str,
        ):
            raise ProgressConfigurationError(
                "suffix must be a string."
            )

        if not isinstance(
            self.hide_cursor,
            bool,
        ):
            raise ProgressConfigurationError(
                "hide_cursor must be a boolean."
            )

        if not isinstance(
            self.clear_line,
            bool,
        ):
            raise ProgressConfigurationError(
                "clear_line must be a boolean."
            )


# ---------------------------------------------------------------------------
# Progress Statistics
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class ProgressStats:
    """
    Runtime statistics for a progress operation.

    Attributes
    ----------
    current:
        Current progress value.

    total:
        Total expected progress value.

    elapsed:
        Elapsed time in seconds.

    rate:
        Average progress rate per second.

    eta:
        Estimated remaining time in seconds.
    """

    current: float = 0.0

    total: float = 0.0

    elapsed: float = 0.0

    rate: float = 0.0

    eta: float | None = None

    @property
    def percentage(self) -> float:
        """Return progress as a percentage."""

        if self.total <= 0:
            return 0.0

        return (
            self.current
            / self.total
            * 100
        )

    @property
    def remaining(self) -> float:
        """Return remaining progress."""

        return max(
            0.0,
            self.total - self.current,
        )


# ---------------------------------------------------------------------------
# Time Helpers
# ---------------------------------------------------------------------------


def get_time() -> float:
    """
    Return the current monotonic clock value.

    ``time.monotonic`` is used so elapsed-time measurements
    are unaffected by system clock changes.
    """

    return time.monotonic()


def calculate_elapsed(
    start_time: float | None,
    *,
    end_time: float | None = None,
) -> float:
    """
    Calculate elapsed time between two monotonic timestamps.
    """

    if start_time is None:
        return 0.0

    if end_time is None:
        end_time = get_time()

    return max(
        0.0,
        end_time - start_time,
    )


def calculate_rate(
    current: float,
    elapsed: float,
) -> float:
    """
    Calculate progress units per second.
    """

    if elapsed <= 0:
        return 0.0

    return max(
        0.0,
        current / elapsed,
    )


def calculate_eta(
    current: float,
    total: float,
    elapsed: float,
) -> float | None:
    """
    Estimate remaining time based on average progress rate.
    """

    if current <= 0:
        return None

    if total <= current:
        return 0.0

    if elapsed <= 0:
        return None

    rate = calculate_rate(
        current,
        elapsed,
    )

    if rate <= 0:
        return None

    remaining = (
        total - current
    )

    return remaining / rate


# ---------------------------------------------------------------------------
# Percentage Helpers
# ---------------------------------------------------------------------------


def clamp_percentage(
    percentage: float,
) -> float:
    """
    Clamp a percentage to the range 0–100.
    """

    return max(
        0.0,
        min(
            100.0,
            float(percentage),
        ),
    )


def calculate_percentage(
    current: float,
    total: float,
) -> float:
    """
    Calculate progress percentage.
    """

    if total <= 0:
        return 0.0

    return clamp_percentage(
        current / total * 100
    )


def format_percentage(
    percentage: float,
    *,
    precision: int = DEFAULT_PERCENTAGE_PRECISION,
) -> str:
    """
    Format a percentage for terminal display.
    """

    if precision < 0:
        raise ValueError(
            "precision cannot be negative."
        )

    value = clamp_percentage(
        percentage
    )

    return (
        f"{value:.{precision}f}%"
    )


# ---------------------------------------------------------------------------
# Progress Bar Rendering
# ---------------------------------------------------------------------------


def render_bar(
    current: float,
    total: float,
    *,
    width: int = DEFAULT_BAR_WIDTH,
    fill: str = DEFAULT_FILL_CHARACTER,
    empty: str = DEFAULT_EMPTY_CHARACTER,
) -> str:
    """
    Render a progress bar without additional metadata.
    """

    if width <= 0:
        raise ValueError(
            "width must be positive."
        )

    if len(fill) != 1:
        raise ValueError(
            "fill must contain exactly one character."
        )

    if len(empty) != 1:
        raise ValueError(
            "empty must contain exactly one character."
        )

    percentage = calculate_percentage(
        current,
        total,
    )

    filled = round(
        width
        * percentage
        / 100
    )

    filled = max(
        0,
        min(
            width,
            filled,
        ),
    )

    return (
        fill * filled
        + empty * (width - filled)
    )


def render_progress(
    current: float,
    total: float,
    *,
    config: ProgressConfig | None = None,
    elapsed: float = 0.0,
) -> str:
    """
    Render a complete progress display.
    """

    if config is None:
        config = ProgressConfig()

    config.validate()

    bar = render_bar(
        current,
        total,
        width=config.width,
        fill=config.fill,
        empty=config.empty,
    )

    parts: list[str] = []

    if config.prefix:
        parts.append(
            config.prefix
        )

    parts.append(
        f"[{bar}]"
    )

    if config.show_percentage:
        parts.append(
            format_percentage(
                calculate_percentage(
                    current,
                    total,
                ),
                precision=config.percentage_precision,
            )
        )

    if config.show_count:
        parts.append(
            f"{current:g}/{total:g}"
        )

    if config.show_elapsed:
        parts.append(
            f"elapsed={elapsed:.2f}s"
        )

    if config.show_eta:
        eta = calculate_eta(
            current,
            total,
            elapsed,
        )

        if eta is None:
            parts.append(
                "ETA=--"
            )

        else:
            parts.append(
                f"ETA={eta:.2f}s"
            )

    if config.suffix:
        parts.append(
            config.suffix
        )

    return " ".join(
        parts
    )


# ---------------------------------------------------------------------------
# Progress Renderer Callback
# ---------------------------------------------------------------------------


ProgressRenderer = Callable[
    [float, float, float],
    str,
]


def default_renderer(
    current: float,
    total: float,
    elapsed: float,
) -> str:
    """
    Default progress renderer.
    """

    return render_progress(
        current,
        total,
        elapsed=elapsed,
    )

# ---------------------------------------------------------------------------
# Progress Display
# ---------------------------------------------------------------------------


class ProgressBar:
    """
    Stateful terminal progress bar.

    The progress bar tracks the current value, total value,
    elapsed time, rate, ETA, and display state.
    """

    def __init__(
        self,
        total: float,
        *,
        current: float = 0.0,
        config: ProgressConfig | None = None,
        stream: TextIO | None = None,
        renderer: ProgressRenderer | None = None,
    ) -> None:
        if total <= 0:
            raise ValueError(
                "total must be positive."
            )

        if config is None:
            config = ProgressConfig()

        config.validate()

        if stream is None:
            stream = sys.stdout

        self.total = float(total)

        self.current = max(
            0.0,
            min(
                float(current),
                self.total,
            ),
        )

        self.config = config

        self.stream = stream

        self.renderer = (
            renderer
            or default_renderer
        )

        self.state = ProgressState.IDLE

        self.start_time: float | None = None

        self.end_time: float | None = None

        self.last_update_time: float = 0.0

        self._cursor_hidden = False

    # -----------------------------------------------------------------------
    # Properties
    # -----------------------------------------------------------------------

    @property
    def percentage(self) -> float:
        """Return the current completion percentage."""

        return calculate_percentage(
            self.current,
            self.total,
        )

    @property
    def remaining(self) -> float:
        """Return the amount of progress remaining."""

        return max(
            0.0,
            self.total - self.current,
        )

    @property
    def elapsed(self) -> float:
        """Return elapsed time in seconds."""

        return calculate_elapsed(
            self.start_time,
            end_time=self.end_time,
        )

    @property
    def rate(self) -> float:
        """Return average progress rate."""

        return calculate_rate(
            self.current,
            self.elapsed,
        )

    @property
    def eta(self) -> float | None:
        """Return estimated remaining time."""

        return calculate_eta(
            self.current,
            self.total,
            self.elapsed,
        )

    @property
    def completed(self) -> bool:
        """Return whether progress is complete."""

        return (
            self.state
            == ProgressState.COMPLETED
        )

    @property
    def active(self) -> bool:
        """Return whether the progress bar is currently running."""

        return self.state in {
            ProgressState.RUNNING,
            ProgressState.PAUSED,
        }

    # -----------------------------------------------------------------------
    # Lifecycle
    # -----------------------------------------------------------------------

    def start(self) -> "ProgressBar":
        """
        Start the progress bar.
        """

        if self.state == ProgressState.COMPLETED:
            raise ProgressStateError(
                "Cannot restart a completed progress bar."
            )

        if self.state == ProgressState.FAILED:
            raise ProgressStateError(
                "Cannot restart a failed progress bar."
            )

        if self.state == ProgressState.CANCELLED:
            raise ProgressStateError(
                "Cannot restart a cancelled progress bar."
            )

        if self.start_time is None:
            self.start_time = get_time()

        self.end_time = None

        self.state = ProgressState.RUNNING

        if self.config.hide_cursor:
            self._hide_cursor()

        self.refresh(
            force=True
        )

        return self

    def pause(self) -> "ProgressBar":
        """
        Pause the progress bar.
        """

        if self.state != ProgressState.RUNNING:
            raise ProgressStateError(
                "Progress bar is not running."
            )

        self.state = ProgressState.PAUSED

        self.refresh(
            force=True
        )

        return self

    def resume(self) -> "ProgressBar":
        """
        Resume a paused progress bar.
        """

        if self.state != ProgressState.PAUSED:
            raise ProgressStateError(
                "Progress bar is not paused."
            )

        self.state = ProgressState.RUNNING

        self.refresh(
            force=True
        )

        return self

    def complete(self) -> "ProgressBar":
        """
        Mark the progress operation as completed.
        """

        if self.state in {
            ProgressState.FAILED,
            ProgressState.CANCELLED,
        }:
            raise ProgressStateError(
                "Cannot complete a failed or cancelled progress bar."
            )

        self.current = self.total

        self.state = ProgressState.COMPLETED

        self.end_time = get_time()

        self.refresh(
            force=True
        )

        self._show_cursor()

        self._write_newline()

        return self

    def fail(self) -> "ProgressBar":
        """
        Mark the progress operation as failed.
        """

        if self.state == ProgressState.COMPLETED:
            raise ProgressStateError(
                "Cannot fail a completed progress bar."
            )

        self.state = ProgressState.FAILED

        self.end_time = get_time()

        self.refresh(
            force=True
        )

        self._show_cursor()

        self._write_newline()

        return self

    def cancel(self) -> "ProgressBar":
        """
        Cancel the progress operation.
        """

        if self.state == ProgressState.COMPLETED:
            raise ProgressStateError(
                "Cannot cancel a completed progress bar."
            )

        self.state = ProgressState.CANCELLED

        self.end_time = get_time()

        self.refresh(
            force=True
        )

        self._show_cursor()

        self._write_newline()

        return self

    # -----------------------------------------------------------------------
    # Updating
    # -----------------------------------------------------------------------

    def update(
        self,
        value: float,
        *,
        refresh: bool = True,
    ) -> "ProgressBar":
        """
        Set the current progress value.
        """

        if self.state in {
            ProgressState.COMPLETED,
            ProgressState.FAILED,
            ProgressState.CANCELLED,
        }:
            raise ProgressStateError(
                "Cannot update a finished progress bar."
            )

        self.current = max(
            0.0,
            min(
                float(value),
                self.total,
            ),
        )

        if (
            self.current >= self.total
            and self.state == ProgressState.RUNNING
        ):
            self.current = self.total

        if refresh:
            self.refresh()

        return self

    def increment(
        self,
        amount: float = 1.0,
        *,
        refresh: bool = True,
    ) -> "ProgressBar":
        """
        Increment progress by a specified amount.
        """

        return self.update(
            self.current + amount,
            refresh=refresh,
        )

    def decrement(
        self,
        amount: float = 1.0,
        *,
        refresh: bool = True,
    ) -> "ProgressBar":
        """
        Decrease progress by a specified amount.
        """

        return self.update(
            self.current - amount,
            refresh=refresh,
        )

    # -----------------------------------------------------------------------
    # Rendering
    # -----------------------------------------------------------------------

    def render(self) -> str:
        """
        Render the current progress state.
        """

        return self.renderer(
            self.current,
            self.total,
            self.elapsed,
        )

    def refresh(
        self,
        *,
        force: bool = False,
    ) -> bool:
        """
        Refresh the terminal display.

        Returns
        -------
        bool
            True if the display was updated.
        """

        now = get_time()

        if not force:
            if (
                now - self.last_update_time
                < self.config.update_interval
            ):
                return False

        self.last_update_time = now

        self._write(
            self.render()
        )

        return True

    # -----------------------------------------------------------------------
    # Output Helpers
    # -----------------------------------------------------------------------

    def _write(
        self,
        text: str,
    ) -> None:
        """Write progress output to the configured stream."""

        if self.config.clear_line:
            self.stream.write(
                CLEAR_LINE
            )

        self.stream.write(
            CARRIAGE_RETURN
        )

        self.stream.write(
            text
        )

        self.stream.flush()

    def _write_newline(
        self,
    ) -> None:
        """Write a final newline."""

        self.stream.write(
            "\n"
        )

        self.stream.flush()

    def _hide_cursor(
        self,
    ) -> None:
        """Hide the terminal cursor."""

        if self._cursor_hidden:
            return

        self.stream.write(
            CURSOR_HIDE
        )

        self.stream.flush()

        self._cursor_hidden = True

    def _show_cursor(
        self,
    ) -> None:
        """Restore the terminal cursor."""

        if not self._cursor_hidden:
            return

        self.stream.write(
            CURSOR_SHOW
        )

        self.stream.flush()

        self._cursor_hidden = False

    # -----------------------------------------------------------------------
    # Context Manager
    # -----------------------------------------------------------------------

    def __enter__(
        self,
    ) -> "ProgressBar":
        """Start the progress bar as a context manager."""

        return self.start()

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> bool:
        """
        Complete or fail the progress bar when leaving a context.
        """

        if exc_type is None:
            if not self.completed:
                self.complete()

        else:
            if self.state not in {
                ProgressState.FAILED,
                ProgressState.CANCELLED,
            }:
                self.fail()

        return False


# ---------------------------------------------------------------------------
# Spinner
# ---------------------------------------------------------------------------


class Spinner:
    """
    Stateful terminal spinner.

    A spinner is useful for operations where the total amount
    of work is unknown.
    """

    def __init__(
        self,
        *,
        config: SpinnerConfig | None = None,
        stream: TextIO | None = None,
    ) -> None:
        if config is None:
            config = SpinnerConfig()

        config.validate()

        if stream is None:
            stream = sys.stdout

        self.config = config

        self.stream = stream

        self.state = ProgressState.IDLE

        self.index = 0

        self.start_time: float | None = None

        self.last_update_time = 0.0

        self._cursor_hidden = False

    # -----------------------------------------------------------------------
    # Properties
    # -----------------------------------------------------------------------

    @property
    def frames(self) -> tuple[str, ...]:
        """Return the configured spinner frames."""

        return self.config.style.value

    @property
    def frame(self) -> str:
        """Return the current spinner frame."""

        return self.frames[
            self.index % len(self.frames)
        ]

    @property
    def elapsed(self) -> float:
        """Return spinner elapsed time."""

        return calculate_elapsed(
            self.start_time
        )

    @property
    def active(self) -> bool:
        """Return whether the spinner is active."""

        return self.state == ProgressState.RUNNING

    # -----------------------------------------------------------------------
    # Lifecycle
    # -----------------------------------------------------------------------

    def start(
        self,
        message: str | None = None,
    ) -> "Spinner":
        """
        Start the spinner.
        """

        if self.state == ProgressState.RUNNING:
            return self

        if message is not None:
            self.config.message = str(
                message
            )

        self.state = ProgressState.RUNNING

        self.index = 0

        self.start_time = get_time()

        self.last_update_time = 0.0

        if self.config.hide_cursor:
            self._hide_cursor()

        self.refresh(
            force=True
        )

        return self

    def stop(
        self,
        *,
        final_message: str | None = None,
    ) -> "Spinner":
        """
        Stop the spinner.
        """

        if self.state != ProgressState.RUNNING:
            return self

        self.state = ProgressState.COMPLETED

        if final_message is not None:
            self.config.message = str(
                final_message
            )

        self.refresh(
            force=True
        )

        self._show_cursor()

        self._write_newline()

        return self

    def fail(
        self,
        *,
        final_message: str | None = None,
    ) -> "Spinner":
        """
        Stop the spinner in a failed state.
        """

        if final_message is not None:
            self.config.message = str(
                final_message
            )

        self.state = ProgressState.FAILED

        self.refresh(
            force=True
        )

        self._show_cursor()

        self._write_newline()

        return self

    # -----------------------------------------------------------------------
    # Message Management
    # -----------------------------------------------------------------------

    def set_message(
        self,
        message: object,
    ) -> "Spinner":
        """
        Change the spinner message.
        """

        self.config.message = str(
            message
        )

        if self.active:
            self.refresh(
                force=True
            )

        return self

    # -----------------------------------------------------------------------
    # Rendering
    # -----------------------------------------------------------------------

    def render(self) -> str:
        """
        Render the current spinner state.
        """

        parts: list[str] = []

        if self.config.prefix:
            parts.append(
                self.config.prefix
            )

        parts.append(
            self.frame
        )

        if self.config.message:
            parts.append(
                self.config.message
            )

        if self.config.suffix:
            parts.append(
                self.config.suffix
            )

        return " ".join(
            parts
        )

    def refresh(
        self,
        *,
        force: bool = False,
    ) -> bool:
        """
        Refresh the spinner display.
        """

        now = get_time()

        if not force:
            if (
                now - self.last_update_time
                < self.config.interval
            ):
                return False

        self.last_update_time = now

        self._write(
            self.render()
        )

        self.index = (
            self.index + 1
        ) % len(self.frames)

        return True

    # -----------------------------------------------------------------------
    # Output
    # -----------------------------------------------------------------------

    def _write(
        self,
        text: str,
    ) -> None:
        """Write spinner output."""

        if self.config.clear_line:
            self.stream.write(
                CLEAR_LINE
            )

        self.stream.write(
            CARRIAGE_RETURN
        )

        self.stream.write(
            text
        )

        self.stream.flush()

    def _write_newline(
        self,
    ) -> None:
        """Write a final newline."""

        self.stream.write(
            "\n"
        )

        self.stream.flush()

    def _hide_cursor(
        self,
    ) -> None:
        """Hide the terminal cursor."""

        if self._cursor_hidden:
            return

        self.stream.write(
            CURSOR_HIDE
        )

        self.stream.flush()

        self._cursor_hidden = True

    def _show_cursor(
        self,
    ) -> None:
        """Restore the terminal cursor."""

        if not self._cursor_hidden:
            return

        self.stream.write(
            CURSOR_SHOW
        )

        self.stream.flush()

        self._cursor_hidden = False

    # -----------------------------------------------------------------------
    # Context Manager
    # -----------------------------------------------------------------------

    def __enter__(
        self,
    ) -> "Spinner":
        """Start the spinner as a context manager."""

        return self.start()

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> bool:
        """Stop or fail the spinner when leaving a context."""

        if exc_type is None:
            self.stop()

        else:
            self.fail()

        return False


# ---------------------------------------------------------------------------
# Counter
# ---------------------------------------------------------------------------


class ProgressCounter:
    """
    Lightweight counter for iterative operations.

    Unlike ProgressBar, the counter does not require a known total.
    """

    def __init__(
        self,
        *,
        label: str = "",
        stream: TextIO | None = None,
        update_interval: float = DEFAULT_UPDATE_INTERVAL,
    ) -> None:
        if stream is None:
            stream = sys.stdout

        if update_interval < 0:
            raise ValueError(
                "update_interval cannot be negative."
            )

        self.label = label

        self.stream = stream

        self.update_interval = (
            update_interval
        )

        self.count = 0

        self.start_time: float | None = None

        self.last_update_time = 0.0

        self.state = ProgressState.IDLE

    @property
    def elapsed(self) -> float:
        """Return elapsed counter time."""

        return calculate_elapsed(
            self.start_time
        )

    @property
    def rate(self) -> float:
        """Return the average count rate."""

        return calculate_rate(
            self.count,
            self.elapsed,
        )

    def start(self) -> "ProgressCounter":
        """Start the counter."""

        self.state = ProgressState.RUNNING

        self.start_time = get_time()

        self.count = 0

        self.refresh(
            force=True
        )

        return self

    def increment(
        self,
        amount: int = 1,
        *,
        refresh: bool = True,
    ) -> "ProgressCounter":
        """Increment the counter."""

        if self.state != ProgressState.RUNNING:
            raise ProgressStateError(
                "Counter is not running."
            )

        self.count += amount

        if refresh:
            self.refresh()

        return self

    def refresh(
        self,
        *,
        force: bool = False,
    ) -> bool:
        """Refresh the counter display."""

        now = get_time()

        if not force:
            if (
                now - self.last_update_time
                < self.update_interval
            ):
                return False

        self.last_update_time = now

        prefix = (
            f"{self.label}: "
            if self.label
            else ""
        )

        self.stream.write(
            CARRIAGE_RETURN
            + f"{prefix}{self.count}"
        )

        self.stream.flush()

        return True

    def stop(self) -> "ProgressCounter":
        """Stop the counter."""

        self.state = ProgressState.COMPLETED

        self.refresh(
            force=True
        )

        self.stream.write(
            "\n"
        )

        self.stream.flush()

        return self

    def __enter__(
        self,
    ) -> "ProgressCounter":
        """Start the counter."""

        return self.start()

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> bool:
        """Stop the counter."""

        self.stop()

        return False

    # ---------------------------------------------------------------------------
# Progress Utilities
# ---------------------------------------------------------------------------


def progress_bar(
    current: float,
    total: float,
    *,
    width: int = DEFAULT_BAR_WIDTH,
    fill: str = DEFAULT_FILL_CHARACTER,
    empty: str = DEFAULT_EMPTY_CHARACTER,
    show_percentage: bool = True,
    show_count: bool = True,
    prefix: str = "",
    suffix: str = "",
    precision: int = DEFAULT_PERCENTAGE_PRECISION,
) -> str:
    """
    Create a one-shot progress bar string.

    Unlike ``ProgressBar``, this function does not maintain
    any runtime state.
    """

    bar = render_bar(
        current,
        total,
        width=width,
        fill=fill,
        empty=empty,
    )

    parts: list[str] = []

    if prefix:
        parts.append(
            prefix
        )

    parts.append(
        f"[{bar}]"
    )

    if show_percentage:
        parts.append(
            format_percentage(
                calculate_percentage(
                    current,
                    total,
                ),
                precision=precision,
            )
        )

    if show_count:
        parts.append(
            f"{current:g}/{total:g}"
        )

    if suffix:
        parts.append(
            suffix
        )

    return " ".join(
        parts
    )


def print_progress(
    current: float,
    total: float,
    *,
    config: ProgressConfig | None = None,
    stream: TextIO | None = None,
) -> None:
    """
    Print a one-shot progress display.
    """

    if stream is None:
        stream = sys.stdout

    text = render_progress(
        current,
        total,
        config=config,
    )

    stream.write(
        text
    )

    stream.flush()


def print_progress_line(
    current: float,
    total: float,
    *,
    config: ProgressConfig | None = None,
    stream: TextIO | None = None,
) -> None:
    """
    Print a progress display followed by a newline.
    """

    if stream is None:
        stream = sys.stdout

    text = render_progress(
        current,
        total,
        config=config,
    )

    stream.write(
        text
        + "\n"
    )

    stream.flush()


# ---------------------------------------------------------------------------
# Iterable Progress
# ---------------------------------------------------------------------------


def iter_progress(
    iterable: Iterable,
    *,
    total: int | float | None = None,
    config: ProgressConfig | None = None,
    stream: TextIO | None = None,
    description: str = "",
):
    """
    Iterate over an iterable while displaying progress.

    Parameters
    ----------
    iterable:
        Iterable to process.

    total:
        Optional total number of items.

        If omitted, the function attempts to use ``len(iterable)``.

    config:
        Optional progress configuration.

    stream:
        Output stream.

    description:
        Optional description displayed before the progress bar.
    """

    if stream is None:
        stream = sys.stdout

    if total is None:
        try:
            total = len(iterable)
        except TypeError:
            total = None

    if total is None:
        counter = ProgressCounter(
            label=description,
            stream=stream,
        )

        counter.start()

        try:
            for item in iterable:
                yield item
                counter.increment()

        finally:
            counter.stop()

        return

    if total <= 0:
        raise ValueError(
            "total must be positive."
        )

    if config is None:
        config = ProgressConfig()

    if description:
        config = config.copy(
            prefix=description
        )

    progress = ProgressBar(
        total,
        config=config,
        stream=stream,
    )

    progress.start()

    try:
        for item in iterable:
            yield item
            progress.increment()

    except Exception:
        progress.fail()
        raise

    else:
        progress.complete()


# ---------------------------------------------------------------------------
# Timed Progress
# ---------------------------------------------------------------------------


class TimedProgress:
    """
    Progress helper that measures the execution time of an operation.
    """

    def __init__(
        self,
        *,
        label: str = "Processing",
        stream: TextIO | None = None,
    ) -> None:
        if stream is None:
            stream = sys.stdout

        self.label = label

        self.stream = stream

        self.start_time: float | None = None

        self.end_time: float | None = None

        self.state = ProgressState.IDLE

    @property
    def elapsed(self) -> float:
        """Return elapsed time."""

        return calculate_elapsed(
            self.start_time,
            end_time=self.end_time,
        )

    def start(self) -> "TimedProgress":
        """Start the timer."""

        self.start_time = get_time()

        self.end_time = None

        self.state = ProgressState.RUNNING

        return self

    def stop(self) -> float:
        """
        Stop the timer and return elapsed seconds.
        """

        if self.state != ProgressState.RUNNING:
            raise ProgressStateError(
                "Timed progress is not running."
            )

        self.end_time = get_time()

        self.state = ProgressState.COMPLETED

        return self.elapsed

    def display(self) -> str:
        """Return a formatted timing message."""

        return (
            f"{self.label}: "
            f"{self.elapsed:.2f}s"
        )

    def print(
        self,
    ) -> None:
        """Print the timing message."""

        self.stream.write(
            self.display()
            + "\n"
        )

        self.stream.flush()

    def __enter__(
        self,
    ) -> "TimedProgress":
        """Start timing."""

        return self.start()

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> bool:
        """Stop timing and display the result."""

        if self.state == ProgressState.RUNNING:
            self.stop()

        self.print()

        return False


# ---------------------------------------------------------------------------
# Progress Message Helpers
# ---------------------------------------------------------------------------


def progress_message(
    message: object,
    *,
    symbol: str = "→",
) -> str:
    """
    Format a simple progress message.
    """

    return (
        f"{symbol} "
        f"{str(message).strip()}"
    )


def success_message(
    message: object,
    *,
    symbol: str = "✓",
) -> str:
    """
    Format a successful progress message.
    """

    return (
        f"{symbol} "
        f"{str(message).strip()}"
    )


def failure_message(
    message: object,
    *,
    symbol: str = "✗",
) -> str:
    """
    Format a failed progress message.
    """

    return (
        f"{symbol} "
        f"{str(message).strip()}"
    )


def warning_message(
    message: object,
    *,
    symbol: str = "!",
) -> str:
    """
    Format a warning progress message.
    """

    return (
        f"{symbol} "
        f"{str(message).strip()}"
    )


# ---------------------------------------------------------------------------
# Batch Progress
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class BatchProgress:
    """
    Track progress across multiple operations.
    """

    total_tasks: int

    completed_tasks: int = 0

    failed_tasks: int = 0

    skipped_tasks: int = 0

    def __post_init__(self) -> None:
        if self.total_tasks < 0:
            raise ValueError(
                "total_tasks cannot be negative."
            )

    @property
    def processed_tasks(self) -> int:
        """Return the number of processed tasks."""

        return (
            self.completed_tasks
            + self.failed_tasks
            + self.skipped_tasks
        )

    @property
    def remaining_tasks(self) -> int:
        """Return the number of remaining tasks."""

        return max(
            0,
            self.total_tasks
            - self.processed_tasks,
        )

    @property
    def percentage(self) -> float:
        """Return batch completion percentage."""

        return calculate_percentage(
            self.processed_tasks,
            self.total_tasks,
        )

    @property
    def successful(self) -> bool:
        """Return whether all tasks completed successfully."""

        return (
            self.processed_tasks
            >= self.total_tasks
            and self.failed_tasks == 0
        )

    def complete(
        self,
        count: int = 1,
    ) -> None:
        """Record completed tasks."""

        if count < 0:
            raise ValueError(
                "count cannot be negative."
            )

        self.completed_tasks += count

    def fail(
        self,
        count: int = 1,
    ) -> None:
        """Record failed tasks."""

        if count < 0:
            raise ValueError(
                "count cannot be negative."
            )

        self.failed_tasks += count

    def skip(
        self,
        count: int = 1,
    ) -> None:
        """Record skipped tasks."""

        if count < 0:
            raise ValueError(
                "count cannot be negative."
            )

        self.skipped_tasks += count

    def reset(self) -> None:
        """Reset all task counters."""

        self.completed_tasks = 0

        self.failed_tasks = 0

        self.skipped_tasks = 0

    def render(
        self,
        *,
        width: int = DEFAULT_BAR_WIDTH,
    ) -> str:
        """Render batch progress."""

        bar = render_bar(
            self.processed_tasks,
            self.total_tasks,
            width=width,
        )

        return (
            f"[{bar}] "
            f"{format_percentage(self.percentage)} "
            f"({self.processed_tasks}/"
            f"{self.total_tasks})"
        )


# ---------------------------------------------------------------------------
# Progress Pipeline
# ---------------------------------------------------------------------------


def run_with_progress(
    iterable: Iterable,
    callback: Callable,
    *,
    total: int | float | None = None,
    config: ProgressConfig | None = None,
    stream: TextIO | None = None,
):
    """
    Execute a callback for every item while tracking progress.

    Yields each callback result.
    """

    if stream is None:
        stream = sys.stdout

    if total is None:
        try:
            total = len(iterable)
        except TypeError:
            total = None

    if total is None:
        raise ValueError(
            "total is required for run_with_progress "
            "when iterable has no length."
        )

    progress = ProgressBar(
        total,
        config=config,
        stream=stream,
    )

    progress.start()

    try:
        for item in iterable:
            result = callback(item)

            yield result

            progress.increment()

    except Exception:
        progress.fail()
        raise

    else:
        progress.complete()


# ---------------------------------------------------------------------------
# Console Progress Helpers
# ---------------------------------------------------------------------------


def clear_progress_line(
    *,
    stream: TextIO | None = None,
) -> None:
    """
    Clear the current terminal line.
    """

    if stream is None:
        stream = sys.stdout

    stream.write(
        CLEAR_LINE
        + CARRIAGE_RETURN
    )

    stream.flush()


def finish_progress_line(
    *,
    stream: TextIO | None = None,
) -> None:
    """
    Move to the next terminal line after progress output.
    """

    if stream is None:
        stream = sys.stdout

    stream.write(
        "\n"
    )

    stream.flush()


def hide_cursor(
    *,
    stream: TextIO | None = None,
) -> None:
    """
    Hide the terminal cursor.
    """

    if stream is None:
        stream = sys.stdout

    stream.write(
        CURSOR_HIDE
    )

    stream.flush()


def show_cursor(
    *,
    stream: TextIO | None = None,
) -> None:
    """
    Restore the terminal cursor.
    """

    if stream is None:
        stream = sys.stdout

    stream.write(
        CURSOR_SHOW
    )

    stream.flush()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


__all__ = [
    # Constants
    "DEFAULT_BAR_WIDTH",
    "DEFAULT_FILL_CHARACTER",
    "DEFAULT_EMPTY_CHARACTER",
    "DEFAULT_PREFIX",
    "DEFAULT_SUFFIX",
    "DEFAULT_UPDATE_INTERVAL",
    "DEFAULT_SPINNER_INTERVAL",
    "DEFAULT_PERCENTAGE_PRECISION",
    "CARRIAGE_RETURN",
    "CLEAR_LINE",
    "CURSOR_HIDE",
    "CURSOR_SHOW",

    # Exceptions
    "ProgressError",
    "ProgressConfigurationError",
    "ProgressStateError",

    # Enums
    "ProgressState",
    "SpinnerStyle",

    # Configuration
    "ProgressConfig",
    "SpinnerConfig",

    # Statistics
    "ProgressStats",

    # Timing
    "get_time",
    "calculate_elapsed",
    "calculate_rate",
    "calculate_eta",

    # Percentages
    "clamp_percentage",
    "calculate_percentage",
    "format_percentage",

    # Rendering
    "render_bar",
    "render_progress",
    "ProgressRenderer",
    "default_renderer",

    # Main progress classes
    "ProgressBar",
    "Spinner",
    "ProgressCounter",

    # Simple progress helpers
    "progress_bar",
    "print_progress",
    "print_progress_line",

    # Iterable helpers
    "iter_progress",
    "run_with_progress",

    # Timed operations
    "TimedProgress",

    # Messages
    "progress_message",
    "success_message",
    "failure_message",
    "warning_message",

    # Batch operations
    "BatchProgress",

    # Terminal helpers
    "clear_progress_line",
    "finish_progress_line",
    "hide_cursor",
    "show_cursor",
]

