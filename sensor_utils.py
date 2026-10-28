"""Utilities for cleaning mixed sensor readings."""

from typing import Iterable, Optional


def clean_sensor_readings(values: Optional[Iterable[object]]) -> list[float]:
    """Return valid sensor readings as floats, capped at 500.0.

    Rules:
    - Ignore None values.
    - Ignore values that cannot be converted to float.
    - Ignore negative values.
    - Cap values greater than 500.0 at 500.0.
    - Return an empty list for None, empty, or entirely invalid input.
    """
    if values is None:
        return []

    cleaned: list[float] = []

    for value in values:
        if value is None:
            continue

        try:
            number = float(value)
        except (TypeError, ValueError):
            continue

        # NaN is not a meaningful sensor reading. It is also the only float
        # value that is not equal to itself.
        if number != number or number < 0:
            continue

        cleaned.append(min(number, 500.0))

    return cleaned
