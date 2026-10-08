"""Input-domain checks shared by mathematics evaluators.

A formula used outside its domain should fail loudly rather than return a number that looks
plausible, so evaluators call these before computing. Each check raises ``ValueError`` naming
the input and the rule it broke.
"""

from __future__ import annotations

import math


def finite(name: str, value: float) -> float:
    """Return ``value`` if it is a finite real number (any ``int`` is finite)."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite real number, got {value!r}.")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{name} must be a finite real number, got {value!r}.")
    return value


def integer(name: str, value: float, minimum: int | None = None) -> int:
    """Return ``value`` as an ``int`` if it is a whole number no smaller than ``minimum``.

    Integral floats such as ``5.0`` are accepted, since callers often pass floats.
    """
    finite(name, value)
    if isinstance(value, float) and not value.is_integer():
        raise ValueError(f"{name} must be a whole number, got {value!r}.")
    number = int(value)
    if minimum is not None and number < minimum:
        raise ValueError(f"{name} must be at least {minimum}, got {value!r}.")
    return number


def positive(name: str, value: float) -> float:
    """Return ``value`` if it is finite and strictly positive."""
    if finite(name, value) <= 0:
        raise ValueError(f"{name} must be positive, got {value!r}.")
    return value


def non_negative(name: str, value: float) -> float:
    """Return ``value`` if it is finite and not negative."""
    if finite(name, value) < 0:
        raise ValueError(f"{name} must not be negative, got {value!r}.")
    return value


def probability(name: str, value: float) -> float:
    """Return ``value`` if it lies in the closed interval [0, 1]."""
    if not 0 <= finite(name, value) <= 1:
        raise ValueError(f"{name} must be a probability in [0, 1], got {value!r}.")
    return value


def finite_result(value: float) -> float:
    """Return ``value`` if the computed result is finite.

    Raises:
        OverflowError: If finite inputs produced a result outside the float range (or an
            undefined ``inf - inf``), so no misleading ``inf`` or ``nan`` is returned.
    """
    if not math.isfinite(value):
        raise OverflowError(f"the result is outside the floating-point range ({value!r}).")
    return value
