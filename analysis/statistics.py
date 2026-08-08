# statistics.py
# Statistical utilities for the Cryptography Toolkit

# Contains general-purpose statistical calculations used
# throughout the cryptanalysis and analysis modules


from __future__ import annotations
import math


# Basic Statistics

def mean(
    values: list[float],
) -> float:
    # Calculates the arithmetic mean of a collection of values

    if not values:
        raise ValueError(
            "Values cannot be empty."
        )

    return sum(
        values
    ) / len(values)


def median(
    values: list[float],
) -> float:
    # Calculates the median value of a collection

    if not values:
        raise ValueError(
            "Values cannot be empty."
        )

    ordered = sorted(
        values
    )

    middle = len(
        ordered
    ) // 2

    if len(
        ordered
    ) % 2 == 0:
        return (
            ordered[middle - 1]
            + ordered[middle]
        ) / 2

    return ordered[
        middle
    ]


def minimum(
    values: list[float],
) -> float:
    # Returns the smallest value in a collection

    if not values:
        raise ValueError(
            "Values cannot be empty."
        )

    return min(
        values
    )


def maximum(
    values: list[float],
) -> float:
    # Returns the largest value in a collection

    if not values:
        raise ValueError(
            "Values cannot be empty."
        )

    return max(
        values
    )


def data_range(
    values: list[float],
) -> float:
    # Calculates the difference between the largest and smallest values

    if not values:
        raise ValueError(
            "Values cannot be empty."
        )

    return (
        maximum(values)
        - minimum(values)
    )


# Deviation Statistics

def variance(
    values: list[float],
    *,
    sample: bool = False,
) -> float:
    # Calculates population or sample variance

    if not values:
        raise ValueError(
            "Values cannot be empty."
        )

    if sample and len(
        values
    ) < 2:
        raise ValueError(
            "At least two values are required "
            "for sample variance."
        )

    average = mean(
        values
    )

    squared_deviations = [
        (
            value
            - average
        ) ** 2
        for value in values
    ]

    divisor = (
        len(values) - 1
        if sample
        else len(values)
    )

    return sum(
        squared_deviations
    ) / divisor


def standard_deviation(
    values: list[float],
    *,
    sample: bool = False,
) -> float:
    # Calculates population or sample standard deviation

    return math.sqrt(
        variance(
            values,
            sample=sample,
        )
    )


def mean_absolute_deviation(
    values: list[float],
) -> float:
    # Calculates the mean absolute deviation from the mean

    if not values:
        raise ValueError(
            "Values cannot be empty."
        )

    average = mean(
        values
    )

    deviations = [
        abs(
            value
            - average
        )
        for value in values
    ]

    return mean(
        deviations
    )


# Frequency Statistics

def frequency_table(
    values: list[str],
) -> dict[str, int]:
    # Creates a frequency table for a collection of values

    frequencies = {}

    for value in values:
        frequencies[value] = (
            frequencies.get(
                value,
                0,
            )
            + 1
        )

    return frequencies


def relative_frequencies(
    values: list[str],
) -> dict[str, float]:
    # Calculates the relative frequency of each value

    if not values:
        return {}

    frequencies = frequency_table(
        values
    )

    total = len(
        values
    )

    return {
        value: count / total
        for value, count
        in frequencies.items()
    } 

# Distribution Analysis

def normalize(
    values: list[float],
) -> list[float]:
    # Normalizes values so that they sum to one

    if not values:
        return []

    total = sum(
        values
    )

    if total == 0:
        return [
            0.0
            for _ in values
        ]

    return [
        value / total
        for value in values
    ]


def z_scores(
    values: list[float],
) -> list[float]:
    # Calculates the z-score of every value

    if not values:
        return []

    deviation = standard_deviation(
        values
    )

    if deviation == 0:
        return [
            0.0
            for _ in values
        ]

    average = mean(
        values
    )

    return [
        (
            value - average
        ) / deviation
        for value in values
    ]


def percentile(
    values: list[float],
    percentage: float,
) -> float:
    # Calculates a percentile using linear interpolation

    if not values:
        raise ValueError(
            "Values cannot be empty."
        )

    if not 0 <= percentage <= 100:
        raise ValueError(
            "Percentage must be between 0 and 100."
        )

    ordered = sorted(
        values
    )

    if len(
        ordered
    ) == 1:
        return ordered[0]

    position = (
        percentage
        / 100
        * (len(ordered) - 1)
    )

    lower = math.floor(
        position
    )

    upper = math.ceil(
        position
    )

    if lower == upper:
        return ordered[
            lower
        ]

    weight = (
        position - lower
    )

    return (
        ordered[lower]
        * (1 - weight)
        + ordered[upper]
        * weight
    )


def quartiles(
    values: list[float],
) -> dict[str, float]:
    # Calculates the first, second, and third quartiles

    if not values:
        raise ValueError(
            "Values cannot be empty."
        )

    return {
        "Q1": percentile(
            values,
            25,
        ),
        "Q2": percentile(
            values,
            50,
        ),
        "Q3": percentile(
            values,
            75,
        ),
    }


def interquartile_range(
    values: list[float],
) -> float:
    # Calculates the interquartile range

    quartile_data = quartiles(
        values
    )

    return (
        quartile_data["Q3"]
        - quartile_data["Q1"]
    )


# Distribution Comparison

def absolute_difference(
    first: float,
    second: float,
) -> float:
    # Calculates the absolute difference between two values

    return abs(
        first - second
    )


def relative_difference(
    first: float,
    second: float,
) -> float:
    # Calculates the relative difference between two values

    if second == 0:
        if first == 0:
            return 0.0

        return float("inf")

    return abs(
        first - second
    ) / abs(
        second
    )


def mean_squared_error(
    actual: list[float],
    expected: list[float],
) -> float:
    # Calculates the mean squared error between two datasets

    if len(
        actual
    ) != len(
        expected
    ):
        raise ValueError(
            "Datasets must have the same length."
        )

    if not actual:
        raise ValueError(
            "Datasets cannot be empty."
        )

    squared_errors = [
        (
            actual_value
            - expected_value
        ) ** 2
        for actual_value, expected_value
        in zip(
            actual,
            expected,
        )
    ]

    return mean(
        squared_errors
    )


def root_mean_squared_error(
    actual: list[float],
    expected: list[float],
) -> float:
    # Calculates the root mean squared error

    return math.sqrt(
        mean_squared_error(
            actual,
            expected,
        )
    )


# Covariance and Correlation

def covariance(
    first: list[float],
    second: list[float],
    *,
    sample: bool = False,
) -> float:
    # Calculates covariance between two datasets

    if len(
        first
    ) != len(
        second
    ):
        raise ValueError(
            "Datasets must have the same length."
        )

    if not first:
        raise ValueError(
            "Datasets cannot be empty."
        )

    if sample and len(
        first
    ) < 2:
        raise ValueError(
            "At least two values are required "
            "for sample covariance."
        )

    first_mean = mean(
        first
    )

    second_mean = mean(
        second
    )

    products = [
        (
            first_value
            - first_mean
        )
        * (
            second_value
            - second_mean
        )
        for first_value, second_value
        in zip(
            first,
            second,
        )
    ]

    divisor = (
        len(first) - 1
        if sample
        else len(first)
    )

    return sum(
        products
    ) / divisor


def correlation(
    first: list[float],
    second: list[float],
) -> float:
    # Calculates the Pearson correlation coefficient

    if len(
        first
    ) != len(
        second
    ):
        raise ValueError(
            "Datasets must have the same length."
        )

    if not first:
        raise ValueError(
            "Datasets cannot be empty."
        )

    first_deviation = standard_deviation(
        first
    )

    second_deviation = standard_deviation(
        second
    )

    if (
        first_deviation == 0
        or second_deviation == 0
    ):
        return 0.0

    return covariance(
        first,
        second,
    ) / (
        first_deviation
        * second_deviation
    )

# Weighted Statistics


def weighted_mean(
    values: list[float],
    weights: list[float],
) -> float:
    # Calculates the weighted arithmetic mean

    if len(
        values
    ) != len(
        weights
    ):
        raise ValueError(
            "Values and weights must have the same length."
        )

    if not values:
        raise ValueError(
            "Values cannot be empty."
        )

    if any(
        weight < 0
        for weight in weights
    ):
        raise ValueError(
            "Weights cannot be negative."
        )

    total_weight = sum(
        weights
    )

    if total_weight == 0:
        raise ValueError(
            "Total weight cannot be zero."
        )

    return sum(
        value * weight
        for value, weight
        in zip(
            values,
            weights,
        )
    ) / total_weight


def weighted_variance(
    values: list[float],
    weights: list[float],
) -> float:
    # Calculates the weighted population variance

    if len(
        values
    ) != len(
        weights
    ):
        raise ValueError(
            "Values and weights must have the same length."
        )

    if not values:
        raise ValueError(
            "Values cannot be empty."
        )

    average = weighted_mean(
        values,
        weights,
    )

    total_weight = sum(
        weights
    )

    return sum(
        weight
        * (
            value - average
        ) ** 2
        for value, weight
        in zip(
            values,
            weights,
        )
    ) / total_weight


def weighted_standard_deviation(
    values: list[float],
    weights: list[float],
) -> float:
    # Calculates the weighted population standard deviation

    return math.sqrt(
        weighted_variance(
            values,
            weights,
        )
    )


# Frequency Distribution Helpers


def frequency_percentages(
    frequencies: dict[str, int],
) -> dict[str, float]:
    # Converts frequency counts into percentages

    if not frequencies:
        return {}

    total = sum(
        frequencies.values()
    )

    if total == 0:
        return {
            key: 0.0
            for key in frequencies
        }

    return {
        key: (
            value / total
        ) * 100
        for key, value
        in frequencies.items()
    }


def sorted_frequencies(
    frequencies: dict[str, int],
) -> list[tuple[str, int]]:
    # Returns frequencies ordered from highest to lowest

    return sorted(
        frequencies.items(),
        key=lambda item: item[1],
        reverse=True,
    )


def distribution_summary(
    values: list[float],
) -> dict[str, float]:
    # Returns a statistical summary of a numerical dataset

    if not values:
        raise ValueError(
            "Values cannot be empty."
        )

    quartile_data = quartiles(
        values
    )

    return {
        "count": len(
            values
        ),
        "mean": mean(
            values
        ),
        "median": median(
            values
        ),
        "minimum": minimum(
            values
        ),
        "maximum": maximum(
            values
        ),
        "range": data_range(
            values
        ),
        "variance": variance(
            values
        ),
        "standard_deviation": standard_deviation(
            values
        ),
        "Q1": quartile_data["Q1"],
        "Q2": quartile_data["Q2"],
        "Q3": quartile_data["Q3"],
        "IQR": interquartile_range(
            values
        ),
    }


# Statistical Comparison


def compare_distributions(
    actual: list[float],
    expected: list[float],
) -> dict[str, float]:
    # Compares two numerical distributions using several metrics

    if len(
        actual
    ) != len(
        expected
    ):
        raise ValueError(
            "Distributions must have the same length."
        )

    if not actual:
        raise ValueError(
            "Distributions cannot be empty."
        )

    return {
        "mean_difference": absolute_difference(
            mean(actual),
            mean(expected),
        ),
        "relative_mean_difference": relative_difference(
            mean(actual),
            mean(expected),
        ),
        "mean_squared_error": mean_squared_error(
            actual,
            expected,
        ),
        "root_mean_squared_error": root_mean_squared_error(
            actual,
            expected,
        ),
        "correlation": correlation(
            actual,
            expected,
        ),
    }


# Self Test


def self_test() -> bool:
    # Runs a quick internal test of the statistical utilities

    values = [
        1.0,
        2.0,
        3.0,
        4.0,
        5.0,
    ]

    if mean(
        values
    ) != 3.0:
        return False

    if median(
        values
    ) != 3.0:
        return False

    if minimum(
        values
    ) != 1.0:
        return False

    if maximum(
        values
    ) != 5.0:
        return False

    if data_range(
        values
    ) != 4.0:
        return False

    if round(
        variance(values),
        5,
    ) != 2.0:
        return False

    if round(
        standard_deviation(values),
        5,
    ) != round(
        math.sqrt(2),
        5,
    ):
        return False

    if percentile(
        values,
        50,
    ) != 3.0:
        return False

    if interquartile_range(
        values
    ) != 2.0:
        return False

    if weighted_mean(
        values,
        [1, 1, 1, 1, 1],
    ) != 3.0:
        return False

    frequencies = {
        "A": 2,
        "B": 3,
        "C": 5,
    }

    percentages = frequency_percentages(
        frequencies
    )

    if round(
        sum(percentages.values()),
        5,
    ) != 100.0:
        return False

    return True


# Module Exports

__all__ = [
    "mean",
    "median",
    "minimum",
    "maximum",
    "data_range",
    "variance",
    "standard_deviation",
    "mean_absolute_deviation",
    "frequency_table",
    "relative_frequencies",
    "normalize",
    "z_scores",
    "percentile",
    "quartiles",
    "interquartile_range",
    "absolute_difference",
    "relative_difference",
    "mean_squared_error",
    "root_mean_squared_error",
    "covariance",
    "correlation",
    "weighted_mean",
    "weighted_variance",
    "weighted_standard_deviation",
    "frequency_percentages",
    "sorted_frequencies",
    "distribution_summary",
    "compare_distributions",
    "self_test",
] 

