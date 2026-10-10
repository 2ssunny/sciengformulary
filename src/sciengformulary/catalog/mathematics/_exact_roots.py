"""Exact-rational helpers for roots of a quadratic, shared by the quadratic and eigenvalue formulas.

Intermediate values are kept as ``Fraction`` so that nothing is rounded to a subnormal or flushed
to zero on the way; the one floating-point square root is taken on a number scaled by an exact
power of two, and the result is converted to ``float`` once, at the end.
"""

from __future__ import annotations

import math
from fractions import Fraction


def sqrt_as_fraction(value: Fraction) -> Fraction:
    """Return sqrt(value) for ``value`` >= 0 as the Fraction of a correctly scaled float root.

    ``value`` is multiplied by an even power of two so that it falls in the normal float range,
    its square root is taken in floating point (one rounding, relative error about 1.1e-16), and
    the power of two is restored exactly, so the result is accurate however small or large
    ``value`` is.
    """
    if value == 0:
        return Fraction(0)
    exponent = (value.numerator.bit_length() - value.denominator.bit_length()) // 2
    scaled = value * Fraction(2) ** (-2 * exponent)
    return Fraction(math.sqrt(float(scaled))) * Fraction(2) ** exponent


def fraction_to_float(value: Fraction) -> float:
    """Return ``value`` correctly rounded to a float (subnormal results included).

    Raises:
        OverflowError: If ``value`` is outside the float range.
    """
    try:
        return value.numerator / value.denominator
    except OverflowError as error:
        raise OverflowError("the result is outside the floating-point range.") from error


def stable_quadratic_roots(
    a: Fraction, b: Fraction, c: Fraction, root: Fraction
) -> tuple[Fraction, Fraction]:
    """Return (plus, minus) = ((-b + root) / (2a), (-b - root) / (2a)) without cancellation.

    ``root`` is sqrt(b^2 - 4ac). The root whose numerator -b -/+ root adds terms of equal sign is
    computed directly; the other follows from the product of the roots, c / a. All arithmetic is
    exact, so no digits are lost beyond those of ``root``.
    """
    if b >= 0:
        partial = -(b + root) / 2  # = a * (minus root)
        minus = partial / a
        plus = c / partial if partial != 0 else Fraction(0)
    else:
        partial = (-b + root) / 2  # = a * (plus root)
        plus = partial / a
        minus = c / partial if partial != 0 else Fraction(0)
    return plus, minus
