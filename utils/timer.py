# timer.py

# Timing Utilities for the Entire Cryptography Toolkit

# Contains reusable timing functions, elapsed-time measurement,
# duration formatting, and timer utilities used throughout the
# project for performance tracking and operation measurement.


from __future__ import annotations

import time
from dataclasses import dataclass
from typing import (
    Callable,
    TypeVar,
)


# Type Variables

T = TypeVar("T")


# Timer Data Model


@dataclass
class TimerResult:
    # Stores the result and timing information from an operation

    result: object
    elapsed: float

    @property
    def milliseconds(self) -> float:
        # Returns elapsed time in milliseconds

        return self.elapsed * 1000

    @property
    def microseconds(self) -> float:
        # Returns elapsed time in microseconds

        return self.elapsed * 1_000_000

    @property
    def nanoseconds(self) -> int:
        # Returns elapsed time in nanoseconds

        return int(
            self.elapsed * 1_000_000_000
        )

    def formatted(
        self,
        precision: int = 4,
    ) -> str:
        # Returns the elapsed time as a readable string

        if self.elapsed < 0.001:
            return (
                f"{self.microseconds:.{precision}f} μs"
            )

        if self.elapsed < 1:
            return (
                f"{self.milliseconds:.{precision}f} ms"
            )

        return (
            f"{self.elapsed:.{precision}f} s"
        )


# Timer Class


class Timer:
    # Measures elapsed wall-clock time

    def __init__(
        self,
        *,
        start: bool = False,
    ) -> None:
        # Initializes a timer

        self._start_time: float | None = None
        self._end_time: float | None = None

        if start:
            self.start()

    @property
    def is_running(
        self,
    ) -> bool:
        # Determines whether the timer is currently running

        return (
            self._start_time is not None
            and self._end_time is None
        )

    @property
    def elapsed(
        self,
    ) -> float:
        # Returns the elapsed time in seconds

        if self._start_time is None:
            return 0.0

        end_time = (
            self._end_time
            if self._end_time is not None
            else time.perf_counter()
        )

        return max(
            0.0,
            end_time - self._start_time,
        )

    @property
    def milliseconds(
        self,
    ) -> float:
        # Returns elapsed time in milliseconds

        return self.elapsed * 1000

    @property
    def microseconds(
        self,
    ) -> float:
        # Returns elapsed time in microseconds

        return self.elapsed * 1_000_000

    def start(
        self,
    ) -> Timer:
        # Starts or restarts the timer

        self._start_time = (
            time.perf_counter()
        )

        self._end_time = None

        return self

    def stop(
        self,
    ) -> float:
        # Stops the timer and returns elapsed time

        if self._start_time is None:
            raise RuntimeError(
                "Timer has not been started."
            )

        if self._end_time is None:
            self._end_time = (
                time.perf_counter()
            )

        return self.elapsed

    def reset(
        self,
    ) -> Timer:
        # Resets the timer to an unstarted state

        self._start_time = None
        self._end_time = None

        return self

    def restart(
        self,
    ) -> Timer:
        # Resets and immediately starts the timer

        return self.reset().start()

    def formatted(
        self,
        precision: int = 4,
    ) -> str:
        # Returns the current elapsed time in readable form

        if self.elapsed < 0.001:
            return (
                f"{self.microseconds:.{precision}f} μs"
            )

        if self.elapsed < 1:
            return (
                f"{self.milliseconds:.{precision}f} ms"
            )

        return (
            f"{self.elapsed:.{precision}f} s"
        )


# Timing Functions


def elapsed_time(
    function: Callable[..., T],
    *args,
    **kwargs,
) -> TimerResult:
    # Executes a function and measures its elapsed time

    timer = Timer(
        start=True
    )

    result = function(
        *args,
        **kwargs,
    )

    timer.stop()

    return TimerResult(
        result=result,
        elapsed=timer.elapsed,
    )


def time_function(
    function: Callable[..., T],
    *args,
    **kwargs,
) -> float:
    # Executes a function and returns its elapsed time in seconds

    timer = Timer(
        start=True
    )

    function(
        *args,
        **kwargs,
    )

    return timer.stop()


def time_call(
    function: Callable[..., T],
    *args,
    **kwargs,
) -> TimerResult:
    # Alias-style helper that returns both result and timing information

    return elapsed_time(
        function,
        *args,
        **kwargs,
    ) 

# Context Manager Support


def __enter__(
    self,
) -> Timer:
    # Starts the timer when entering a context manager

    return self.start()


def __exit__(
    self,
    exc_type,
    exc_value,
    traceback,
) -> None:
    # Stops the timer when leaving a context manager

    if self.is_running:
        self.stop()


# Formatting Helpers


def format_duration(
    seconds: float,
    *,
    precision: int = 4,
) -> str:
    # Converts seconds into a human-readable duration

    if not isinstance(
        seconds,
        (int, float),
    ):
        raise TypeError(
            "seconds must be a number."
        )

    if seconds < 0:
        raise ValueError(
            "seconds cannot be negative."
        )

    if seconds < 0.001:
        return (
            f"{seconds * 1_000_000:.{precision}f} μs"
        )

    if seconds < 1:
        return (
            f"{seconds * 1000:.{precision}f} ms"
        )

    if seconds < 60:
        return (
            f"{seconds:.{precision}f} s"
        )

    minutes = int(
        seconds // 60
    )

    remaining_seconds = (
        seconds % 60
    )

    if minutes < 60:
        return (
            f"{minutes}m "
            f"{remaining_seconds:.{precision}f}s"
        )

    hours = int(
        minutes // 60
    )

    remaining_minutes = (
        minutes % 60
    )

    return (
        f"{hours}h "
        f"{remaining_minutes}m "
        f"{remaining_seconds:.{precision}f}s"
    )


def format_milliseconds(
    milliseconds: float,
    *,
    precision: int = 4,
) -> str:
    # Converts milliseconds into a human-readable duration

    if not isinstance(
        milliseconds,
        (int, float),
    ):
        raise TypeError(
            "milliseconds must be a number."
        )

    if milliseconds < 0:
        raise ValueError(
            "milliseconds cannot be negative."
        )

    return format_duration(
        milliseconds / 1000,
        precision=precision,
    )


# High-Resolution Timing


def perf_counter() -> float:
    # Returns the current high-resolution performance counter

    return time.perf_counter()


def measure(
    function: Callable[..., T],
    *args,
    **kwargs,
) -> float:
    # Measures execution time without storing the function result

    start = time.perf_counter()

    function(
        *args,
        **kwargs,
    )

    end = time.perf_counter()

    return end - start


def measure_result(
    function: Callable[..., T],
    *args,
    **kwargs,
) -> TimerResult:
    # Measures execution time while preserving the function result

    start = time.perf_counter()

    result = function(
        *args,
        **kwargs,
    )

    end = time.perf_counter()

    return TimerResult(
        result=result,
        elapsed=end - start,
    )


# Benchmarking


def benchmark(
    function: Callable[..., T],
    *,
    iterations: int = 1,
    warmup: int = 0,
    args: tuple = (),
    kwargs: dict | None = None,
) -> dict[str, float]:
    # Runs a function repeatedly and returns timing statistics

    if not isinstance(
        iterations,
        int,
    ):
        raise TypeError(
            "iterations must be an integer."
        )

    if iterations <= 0:
        raise ValueError(
            "iterations must be greater than zero."
        )

    if not isinstance(
        warmup,
        int,
    ):
        raise TypeError(
            "warmup must be an integer."
        )

    if warmup < 0:
        raise ValueError(
            "warmup cannot be negative."
        )

    if kwargs is None:
        kwargs = {}

    for _ in range(
        warmup
    ):
        function(
            *args,
            **kwargs,
        )

    start = time.perf_counter()

    for _ in range(
        iterations
    ):
        function(
            *args,
            **kwargs,
        )

    elapsed = (
        time.perf_counter()
        - start
    )

    average = (
        elapsed / iterations
    )

    return {
        "iterations": float(
            iterations
        ),
        "total": elapsed,
        "average": average,
        "minimum": average,
        "maximum": average,
        "milliseconds": average * 1000,
    }


# Timer Factory


def create_timer(
    *,
    start: bool = False,
) -> Timer:
    # Creates a new Timer instance

    return Timer(
        start=start
    )


# Self Test


def self_test() -> bool:
    # Runs a quick internal test of the timer module

    timer = Timer()

    if timer.is_running:
        return False

    timer.start()

    if not timer.is_running:
        return False

    time.sleep(
        0.001
    )

    elapsed = timer.stop()

    if elapsed <= 0:
        return False

    if timer.is_running:
        return False

    if timer.milliseconds <= 0:
        return False

    formatted = timer.formatted()

    if not isinstance(
        formatted,
        str,
    ):
        return False

    result = elapsed_time(
        lambda: 42
    )

    if result.result != 42:
        return False

    if result.elapsed < 0:
        return False

    measured = measure(
        lambda: 42
    )

    if measured < 0:
        return False

    measured_result = measure_result(
        lambda: "test"
    )

    if measured_result.result != "test":
        return False

    benchmark_result = benchmark(
        lambda: 1 + 1,
        iterations=2,
    )

    if benchmark_result["iterations"] != 2.0:
        return False

    if benchmark_result["total"] < 0:
        return False

    if format_duration(
        0.5
    ) == "":
        return False

    if format_duration(
        65
    ) == "":
        return False

    with Timer() as context_timer:
        time.sleep(
            0.001
        )

    if context_timer.elapsed <= 0:
        return False

    return True


# Module Exports


__all__ = [
    # Data Model
    "TimerResult",
    # Timer
    "Timer",
    # Timing Functions
    "elapsed_time",
    "time_function",
    "time_call",
    # Formatting
    "format_duration",
    "format_milliseconds",
    # High-Resolution Timing
    "perf_counter",
    "measure",
    "measure_result",
    # Benchmarking
    "benchmark",
    # Factory
    "create_timer",
    # Testing
    "self_test",
]

