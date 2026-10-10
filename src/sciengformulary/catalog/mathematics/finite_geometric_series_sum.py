"""Finite Geometric Series Sum: S = (x^n - 1) / (x - 1)."""

import math

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog._domain import finite, integer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(x: float, n: float) -> float:
    x = float(finite("x", x))
    if x == 1.0:
        raise ValueError("x must not equal 1 (the closed form is 0/0 there; the sum is n).")
    n = integer("n", n, minimum=0)
    try:
        result = (x**n - 1.0) / (x - 1.0)
    except OverflowError as error:
        raise ValueError(f"x^n overflows a float for x={x!r}, n={n!r}.") from error
    if not math.isfinite(result):
        raise ValueError(f"The sum overflows a float for x={x!r}, n={n!r}.")
    return result


finite_geometric_series_sum = FormulaSpec(
    id="mathematics.finite_geometric_series_sum",
    name="Finite Geometric Series Sum",
    equation="S = (x^n - 1) / (x - 1)",
    description=(
        "Closed form of 1 + x + x^2 + ... + x^(n-1), the sum of the first n powers of a common "
        "ratio x other than 1."
    ),
    inputs=(
        VariableSpec(
            name="x",
            symbol="x",
            description="Common ratio (real, not equal to 1)",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="n",
            symbol="n",
            description="Number of terms, integer",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="S",
        symbol="S_n",
        description="Sum of x^i for i = 0..n-1",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(mathlib("Mathlib/Algebra/Field/GeomSum.lean#L43", "theorem geom_sum_eq"),),
    verification_cases=(
        VerificationCase(
            inputs={"x": 2.0, "n": 10},
            expected=1023.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Exact Fraction direct summation of 1 + 2 + ... + 2^9.",
        ),
        VerificationCase(
            inputs={"x": 0.5, "n": 4},
            expected=1.875,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Exact Fraction direct summation 1 + 1/2 + 1/4 + 1/8 = 15/8.",
        ),
        VerificationCase(
            inputs={"x": -2.0, "n": 5},
            expected=11.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Negative ratio: exact Fraction direct summation 1 - 2 + 4 - 8 + 16.",
        ),
        VerificationCase(
            inputs={"x": -1.0, "n": 3},
            expected=1.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Ratio -1: exact Fraction direct summation 1 - 1 + 1.",
        ),
        VerificationCase(
            inputs={"x": 0.999, "n": 1000},
            expected=632.3045752290358,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Near the excluded x = 1: exact Fraction direct summation using the exact "
                "binary value of the float 0.999, rounded to float."
            ),
        ),
        VerificationCase(
            inputs={"x": 0.0, "n": 5},
            expected=1.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge x = 0: exact direct summation; only the x^0 = 1 term is nonzero.",
        ),
        VerificationCase(
            inputs={"x": 3.0, "n": 0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-12,
            note="Edge n = 0: the empty sum.",
        ),
    ),
    assumptions=(
        "The first term is 1 (x^0); for a first term a, multiply the result by a. The source "
        "states the unscaled sum, so a is not an input.",
        "x is a finite real number other than 1; at x = 1 the closed form is 0/0 (the sum is "
        "then simply n), so the evaluator rejects it. n is a non-negative whole number; n = 0 "
        "gives 0.",
        "Evaluated in floating point: close to x = 1 cancellation costs relative accuracy of "
        "roughly machine epsilon / |x - 1|, and inputs whose x^n or sum overflow a float are "
        "rejected.",
    ),
    tags=("geometric series", "geometric progression", "finite sum", "partial sum", "series"),
)
