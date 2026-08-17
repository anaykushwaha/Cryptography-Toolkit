# decorators.py

# Reusable Decorators for the Entire Cryptography Toolkit

# Contains decorators for timing, logging, validation, exception
# handling, caching, and other cross-cutting functionality used
# throughout the project.


from __future__ import annotations

import functools
import logging
from collections.abc import Callable
from typing import (
    Any,
    TypeVar,
    ParamSpec,
)

from .timer import Timer
from .logger import get_logger


# Type Variables

P = ParamSpec(
    "P"
)

T = TypeVar(
    "T"
)


# Module Logger

_logger = get_logger(
    "cryptography_toolkit.decorators"
)


# Internal Helpers


def _function_name(
    function: Callable[..., Any],
) -> str:
    # Returns a readable name for a decorated function

    return getattr(
        function,
        "__name__",
        function.__class__.__name__,
    )


def _log_call(
    function: Callable[..., Any],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> None:
    # Logs a function call

    _logger.debug(
        "Calling %s with %d positional argument(s) and %d keyword argument(s).",
        _function_name(function),
        len(args),
        len(kwargs),
    )


# Timing Decorators


def timed(
    function: Callable[P, T],
) -> Callable[P, T]:
    # Measures the execution time of a function

    @functools.wraps(
        function
    )
    def wrapper(
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T:
        timer = Timer(
            start=True
        )

        try:
            return function(
                *args,
                **kwargs,
            )
        finally:
            elapsed = timer.stop()

            _logger.debug(
                "%s completed in %.6f seconds.",
                _function_name(function),
                elapsed,
            )

    return wrapper


def timed_result(
    function: Callable[P, T],
) -> Callable[P, tuple[T, float]]:
    # Executes a function and returns its result together with elapsed time

    @functools.wraps(
        function
    )
    def wrapper(
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> tuple[T, float]:
        timer = Timer(
            start=True
        )

        try:
            result = function(
                *args,
                **kwargs,
            )
        finally:
            elapsed = timer.stop()

        return result, elapsed

    return wrapper


# Logging Decorators


def logged(
    function: Callable[P, T],
) -> Callable[P, T]:
    # Logs the execution of a function

    @functools.wraps(
        function
    )
    def wrapper(
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T:
        _log_call(
            function,
            args,
            kwargs,
        )

        try:
            result = function(
                *args,
                **kwargs,
            )

            _logger.debug(
                "%s completed successfully.",
                _function_name(function),
            )

            return result

        except Exception:
            _logger.exception(
                "%s raised an exception.",
                _function_name(function),
            )

            raise

    return wrapper


def log_exceptions(
    function: Callable[P, T],
) -> Callable[P, T]:
    # Logs exceptions raised by a function before re-raising them

    @functools.wraps(
        function
    )
    def wrapper(
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T:
        try:
            return function(
                *args,
                **kwargs,
            )
        except Exception:
            _logger.exception(
                "Exception raised by %s.",
                _function_name(function),
            )

            raise

    return wrapper


# Retry Decorator


def retry(
    attempts: int = 3,
    *,
    exceptions: tuple[type[Exception], ...] = (
        Exception,
    ),
) -> Callable[
    [Callable[P, T]],
    Callable[P, T],
]:
    # Repeats a function when one of the specified exceptions occurs

    if not isinstance(
        attempts,
        int,
    ):
        raise TypeError(
            "attempts must be an integer."
        )

    if attempts <= 0:
        raise ValueError(
            "attempts must be greater than zero."
        )

    if not isinstance(
        exceptions,
        tuple,
    ):
        raise TypeError(
            "exceptions must be a tuple."
        )

    def decorator(
        function: Callable[P, T],
    ) -> Callable[P, T]:

        @functools.wraps(
            function
        )
        def wrapper(
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> T:

            last_error: Exception | None = None

            for attempt in range(
                1,
                attempts + 1,
            ):
                try:
                    return function(
                        *args,
                        **kwargs,
                    )

                except exceptions as error:
                    last_error = error

                    _logger.warning(
                        "%s failed on attempt %d/%d.",
                        _function_name(function),
                        attempt,
                        attempts,
                    )

            if last_error is not None:
                raise last_error

            raise RuntimeError(
                "Retry operation failed unexpectedly."
            )

        return wrapper

    return decorator


# Exception Handling Decorator


def suppress_exceptions(
    default: T | None = None,
    *,
    exceptions: tuple[type[Exception], ...] = (
        Exception,
    ),
) -> Callable[
    [Callable[P, T]],
    Callable[P, T | None],
]:
    # Suppresses selected exceptions and returns a default value

    if not isinstance(
        exceptions,
        tuple,
    ):
        raise TypeError(
            "exceptions must be a tuple."
        )

    def decorator(
        function: Callable[P, T],
    ) -> Callable[P, T | None]:

        @functools.wraps(
            function
        )
        def wrapper(
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> T | None:

            try:
                return function(
                    *args,
                    **kwargs,
                )

            except exceptions:
                _logger.debug(
                    "Suppressed exception from %s.",
                    _function_name(function),
                )

                return default

        return wrapper

    return decorator 

# Validation Decorators


def validate_arguments(
    validators: dict[str, Callable[[Any], bool]],
) -> Callable[
    [Callable[P, T]],
    Callable[P, T],
]:
    # Validates selected function arguments before execution

    if not isinstance(
        validators,
        dict,
    ):
        raise TypeError(
            "validators must be a dictionary."
        )

    for name, validator in validators.items():

        if not isinstance(
            name,
            str,
        ):
            raise TypeError(
                "validator argument names must be strings."
            )

        if not callable(
            validator
        ):
            raise TypeError(
                f"Validator for '{name}' must be callable."
            )

    def decorator(
        function: Callable[P, T],
    ) -> Callable[P, T]:

        @functools.wraps(
            function
        )
        def wrapper(
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> T:

            bound_arguments = (
                __import__(
                    "inspect"
                )
                .signature(function)
                .bind(
                    *args,
                    **kwargs,
                )
            )

            bound_arguments.apply_defaults()

            for name, validator in validators.items():

                if name not in bound_arguments.arguments:
                    raise TypeError(
                        f"Missing argument: {name}"
                    )

                value = (
                    bound_arguments
                    .arguments[name]
                )

                if not validator(
                    value
                ):
                    raise ValueError(
                        f"Invalid value for argument '{name}'."
                    )

            return function(
                *args,
                **kwargs,
            )

        return wrapper

    return decorator


def validate_return(
    validator: Callable[[Any], bool],
) -> Callable[
    [Callable[P, T]],
    Callable[P, T],
]:
    # Validates the return value of a function

    if not callable(
        validator
    ):
        raise TypeError(
            "validator must be callable."
        )

    def decorator(
        function: Callable[P, T],
    ) -> Callable[P, T]:

        @functools.wraps(
            function
        )
        def wrapper(
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> T:

            result = function(
                *args,
                **kwargs,
            )

            if not validator(
                result
            ):
                raise ValueError(
                    f"Invalid return value from {_function_name(function)}."
                )

            return result

        return wrapper

    return decorator


# Call Tracking


def counted(
    function: Callable[P, T],
) -> Callable[P, T]:
    # Tracks how many times a function has been called

    count = 0

    @functools.wraps(
        function
    )
    def wrapper(
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T:

        nonlocal count

        count += 1

        wrapper.call_count = count

        return function(
            *args,
            **kwargs,
        )

    wrapper.call_count = 0

    return wrapper


def limited_calls(
    maximum: int,
) -> Callable[
    [Callable[P, T]],
    Callable[P, T],
]:
    # Restricts a function to a maximum number of calls

    if not isinstance(
        maximum,
        int,
    ):
        raise TypeError(
            "maximum must be an integer."
        )

    if maximum <= 0:
        raise ValueError(
            "maximum must be greater than zero."
        )

    def decorator(
        function: Callable[P, T],
    ) -> Callable[P, T]:

        count = 0

        @functools.wraps(
            function
        )
        def wrapper(
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> T:

            nonlocal count

            if count >= maximum:
                raise RuntimeError(
                    f"{_function_name(function)} "
                    f"has reached its maximum call limit of "
                    f"{maximum}."
                )

            count += 1

            return function(
                *args,
                **kwargs,
            )

        return wrapper

    return decorator


# Caching Decorators


def cached(
    function: Callable[P, T],
) -> Callable[P, T]:
    # Caches function results using functools.lru_cache

    return functools.lru_cache(
        maxsize=None
    )(
        function
    )


def cache(
    maxsize: int | None = 128,
) -> Callable[
    [Callable[P, T]],
    Callable[P, T],
]:
    # Creates a configurable caching decorator

    if maxsize is not None:

        if not isinstance(
            maxsize,
            int,
        ):
            raise TypeError(
                "maxsize must be an integer or None."
            )

        if maxsize <= 0:
            raise ValueError(
                "maxsize must be greater than zero."
            )

    def decorator(
        function: Callable[P, T],
    ) -> Callable[P, T]:

        return functools.lru_cache(
            maxsize=maxsize
        )(
            function
        )

    return decorator


# Debugging Decorators


def trace(
    function: Callable[P, T],
) -> Callable[P, T]:
    # Logs function entry, arguments, return value, and exit

    @functools.wraps(
        function
    )
    def wrapper(
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T:

        name = _function_name(
            function
        )

        _logger.debug(
            "ENTER %s",
            name,
        )

        _logger.debug(
            "ARGS %s | KWARGS %s",
            args,
            kwargs,
        )

        try:
            result = function(
                *args,
                **kwargs,
            )

            _logger.debug(
                "RETURN %s -> %r",
                name,
                result,
            )

            return result

        except Exception:
            _logger.exception(
                "ERROR %s",
                name,
            )

            raise

        finally:
            _logger.debug(
                "EXIT %s",
                name,
            )

    return wrapper


# Deprecation Decorator


def deprecated(
    message: str = "This function is deprecated.",
) -> Callable[
    [Callable[P, T]],
    Callable[P, T],
]:
    # Marks a function as deprecated and emits a warning when called

    if not isinstance(
        message,
        str,
    ):
        raise TypeError(
            "message must be a string."
        )

    def decorator(
        function: Callable[P, T],
    ) -> Callable[P, T]:

        @functools.wraps(
            function
        )
        def wrapper(
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> T:

            _logger.warning(
                "%s: %s",
                message,
                _function_name(function),
            )

            return function(
                *args,
                **kwargs,
            )

        return wrapper

    return decorator


# Singleton Decorator


def singleton(
    function: Callable[P, T],
) -> Callable[P, T]:
    # Ensures a function is executed only once

    executed = False
    result: T | None = None

    @functools.wraps(
        function
    )
    def wrapper(
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T:

        nonlocal executed
        nonlocal result

        if not executed:

            result = function(
                *args,
                **kwargs,
            )

            executed = True

        return result  # type: ignore

    return wrapper

# Rate Limiting Decorator


def rate_limit(
    maximum: int,
    period: float,
) -> Callable[
    [Callable[P, T]],
    Callable[P, T],
]:
    # Limits how many times a function can execute within a time period

    if not isinstance(
        maximum,
        int,
    ):
        raise TypeError(
            "maximum must be an integer."
        )

    if maximum <= 0:
        raise ValueError(
            "maximum must be greater than zero."
        )

    if not isinstance(
        period,
        (int, float),
    ):
        raise TypeError(
            "period must be a number."
        )

    if period <= 0:
        raise ValueError(
            "period must be greater than zero."
        )

    import time

    def decorator(
        function: Callable[P, T],
    ) -> Callable[P, T]:

        calls: list[float] = []

        @functools.wraps(
            function
        )
        def wrapper(
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> T:

            current_time = time.monotonic()

            calls[:] = [
                timestamp
                for timestamp in calls
                if current_time - timestamp < period
            ]

            if len(calls) >= maximum:
                raise RuntimeError(
                    f"{_function_name(function)} "
                    f"has exceeded the rate limit of "
                    f"{maximum} call(s) per {period} second(s)."
                )

            calls.append(
                current_time
            )

            return function(
                *args,
                **kwargs,
            )

        return wrapper

    return decorator


# Synchronization Decorator


def synchronized(
    function: Callable[P, T],
) -> Callable[P, T]:
    # Ensures that only one thread executes a function at a time

    import threading

    lock = threading.RLock()

    @functools.wraps(
        function
    )
    def wrapper(
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T:

        with lock:
            return function(
                *args,
                **kwargs,
            )

    return wrapper


# Attribute Helpers


def preserve_attributes(
    source: Callable[..., Any],
    target: Callable[..., Any],
) -> Callable[..., Any]:
    # Copies metadata from one callable to another

    return functools.update_wrapper(
        target,
        source,
    )


# Conditional Execution


def when(
    condition: Callable[..., bool],
) -> Callable[
    [Callable[P, T]],
    Callable[P, T | None],
]:
    # Executes a function only when a condition evaluates to True

    if not callable(
        condition
    ):
        raise TypeError(
            "condition must be callable."
        )

    def decorator(
        function: Callable[P, T],
    ) -> Callable[P, T | None]:

        @functools.wraps(
            function
        )
        def wrapper(
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> T | None:

            if condition(
                *args,
                **kwargs,
            ):
                return function(
                    *args,
                    **kwargs,
                )

            _logger.debug(
                "%s skipped because its condition was false.",
                _function_name(function),
            )

            return None

        return wrapper

    return decorator


# Argument Transformation


def strip_arguments(
    function: Callable[P, T],
) -> Callable[P, T]:
    # Strips leading and trailing whitespace from string arguments

    @functools.wraps(
        function
    )
    def wrapper(
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T:

        transformed_args = tuple(
            argument.strip()
            if isinstance(
                argument,
                str,
            )
            else argument
            for argument in args
        )

        transformed_kwargs = {
            key: (
                value.strip()
                if isinstance(
                    value,
                    str,
                )
                else value
            )
            for key, value in kwargs.items()
        }

        return function(
            *transformed_args,
            **transformed_kwargs,
        )

    return wrapper


def lowercase_arguments(
    function: Callable[P, T],
) -> Callable[P, T]:
    # Converts string arguments to lowercase before execution

    @functools.wraps(
        function
    )
    def wrapper(
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T:

        transformed_args = tuple(
            argument.lower()
            if isinstance(
                argument,
                str,
            )
            else argument
            for argument in args
        )

        transformed_kwargs = {
            key: (
                value.lower()
                if isinstance(
                    value,
                    str,
                )
                else value
            )
            for key, value in kwargs.items()
        }

        return function(
            *transformed_args,
            **transformed_kwargs,
        )

    return wrapper


# Composition


def compose(
    *decorators: Callable[
        [Callable[..., Any]],
        Callable[..., Any],
    ],
) -> Callable[
    [Callable[P, T]],
    Callable[P, T],
]:
    # Combines multiple decorators into one decorator

    def decorator(
        function: Callable[P, T],
    ) -> Callable[P, T]:

        wrapped: Callable[..., Any] = function

        for current_decorator in reversed(
            decorators
        ):
            if not callable(
                current_decorator
            ):
                raise TypeError(
                    "All decorators must be callable."
                )

            wrapped = current_decorator(
                wrapped
            )

        return wrapped  # type: ignore

    return decorator


# Self Test


def self_test() -> bool:
    # Runs a quick internal test of the decorators module

    @timed
    def add(
        first: int,
        second: int,
    ) -> int:
        return first + second

    if add(
        2,
        3,
    ) != 5:
        return False

    @timed_result
    def multiply(
        first: int,
        second: int,
    ) -> int:
        return first * second

    result, elapsed = multiply(
        3,
        4,
    )

    if result != 12:
        return False

    if elapsed < 0:
        return False

    @counted
    def identity(
        value: Any,
    ) -> Any:
        return value

    identity(
        1
    )

    identity(
        2
    )

    if identity.call_count != 2:
        return False

    @limited_calls(
        2
    )
    def limited():
        return True

    limited()
    limited()

    try:
        limited()
        return False
    except RuntimeError:
        pass

    @validate_arguments(
        {
            "value": lambda value: isinstance(
                value,
                int,
            )
        }
    )
    def validated(
        value: int,
    ) -> int:
        return value

    if validated(
        10
    ) != 10:
        return False

    try:
        validated(
            "invalid"
        )
        return False
    except ValueError:
        pass

    @validate_return(
        lambda value: isinstance(
            value,
            int,
        )
    )
    def valid_return():
        return 10

    if valid_return() != 10:
        return False

    @strip_arguments
    def echo(
        value: str,
    ) -> str:
        return value

    if echo(
        "  hello  "
    ) != "hello":
        return False

    @lowercase_arguments
    def upper_echo(
        value: str,
    ) -> str:
        return value

    if upper_echo(
        "HELLO"
    ) != "hello":
        return False

    @when(
        lambda value: value > 0
    )
    def positive(
        value: int,
    ) -> int:
        return value

    if positive(
        5
    ) != 5:
        return False

    if positive(
        -1
    ) is not None:
        return False

    @suppress_exceptions(
        default="fallback"
    )
    def failing():
        raise ValueError(
            "test"
        )

    if failing() != "fallback":
        return False

    @retry(
        attempts=2
    )
    def successful():
        return "success"

    if successful() != "success":
        return False

    @cache(
        maxsize=4
    )
    def cached_function(
        value: int,
    ) -> int:
        return value * 2

    if cached_function(
        5
    ) != 10:
        return False

    @synchronized
    def synchronized_function(
        value: int,
    ) -> int:
        return value

    if synchronized_function(
        5
    ) != 5:
        return False

    @compose(
        lowercase_arguments,
        strip_arguments,
    )
    def composed(
        value: str,
    ) -> str:
        return value

    if composed(
        "  HELLO  "
    ) != "hello":
        return False

    return True


# Module Exports


__all__ = [

    # Timing
    "timed",
    "timed_result",

    # Logging
    "logged",
    "log_exceptions",

    # Retry / Exceptions
    "retry",
    "suppress_exceptions",

    # Validation
    "validate_arguments",
    "validate_return",

    # Call Tracking
    "counted",
    "limited_calls",

    # Caching
    "cached",
    "cache",

    # Debugging
    "trace",

    # Lifecycle
    "deprecated",
    "singleton",

    # Rate Limiting
    "rate_limit",

    # Synchronization
    "synchronized",

    # Metadata
    "preserve_attributes",

    # Conditional Execution
    "when",

    # Argument Transformation
    "strip_arguments",
    "lowercase_arguments",

    # Composition
    "compose",

    # Testing
    "self_test",
]

