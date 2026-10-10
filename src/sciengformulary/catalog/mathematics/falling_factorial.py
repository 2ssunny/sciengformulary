"""Falling Factorial (Real Argument): ff = prod_{i=0}^{k-1} (x - i)."""

import math

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog.mathematics._domain import finite, integer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(x: float, k: float) -> float:
    finite("x", x)
    k = integer("k", k, minimum=0)
    if float(x).is_integer() and 0 <= x < k:
        # One factor is exactly zero; returning early also avoids inf * 0 when the partial
        # product before that factor already overflowed.
        return 0.0
    # The product is carried as mantissa * 2^exponent, so a partial product beyond the float
    # range does not raise when a later factor below 1 would bring it back; only a final value
    # outside the range does.
    mantissa, exponent = 1.0, 0
    for i in range(k):
        factor, factor_exponent = math.frexp(x - i)
        mantissa, product_exponent = math.frexp(mantissa * factor)
        exponent += factor_exponent + product_exponent
    try:
        return math.ldexp(mantissa, exponent)
    except OverflowError as error:
        raise OverflowError("the result is outside the floating-point range.") from error


falling_factorial = FormulaSpec(
    id="mathematics.falling_factorial",
    name="Falling Factorial (Real Argument)",
    equation="ff = prod_{i=0}^{k-1} (x - i)",
    description=(
        "Product of k descending factors x (x - 1) ... (x - k + 1) for a real starting value x. "
        "For a whole number x >= k it equals the k-permutation count "
        "mathematics.k_permutations with n = x."
    ),
    inputs=(
        VariableSpec(
            name="x",
            symbol="x",
            description="Real starting value",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="k",
            symbol="k",
            description="Number of factors, integer",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="ff",
        symbol="(x)_k",
        description="Falling factorial",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Stated for any commutative ring R: descPochhammer R n evaluated at r is the product
        # of (r - j) for j < n. Here R is the real numbers, r = x and n = k.
        mathlib(
            "Mathlib/RingTheory/Polynomial/Pochhammer.lean#L458",
            "lemma descPochhammer_eval_eq_prod_range",
        ),
        mathlib("Mathlib/RingTheory/Polynomial/Pochhammer.lean#L266", "def descPochhammer"),
        # At a natural-number argument the value is Nat.descFactorial, the k-permutation count.
        mathlib(
            "Mathlib/RingTheory/Polynomial/Pochhammer.lean#L401",
            "theorem descPochhammer_eval_eq_descFactorial",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"x": 5.0, "k": 2},
            expected=20.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Whole x: 5 * 4 = 20, the k-permutation count P(5, 2); mpmath ff agrees.",
        ),
        VerificationCase(
            inputs={"x": 2.5, "k": 2},
            expected=3.75,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Exact Fraction product 2.5 * 1.5 = 3.75.",
        ),
        VerificationCase(
            inputs={"x": 0.5, "k": 3},
            expected=0.375,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Exact Fraction product 0.5 * (-0.5) * (-1.5) = 0.375.",
        ),
        VerificationCase(
            inputs={"x": -2.0, "k": 3},
            expected=-24.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Negative x: (-2)(-3)(-4) = -24 (exact).",
        ),
        VerificationCase(
            inputs={"x": 3.0, "k": 5},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Whole x < k: the product contains the factor 0, so the value is exactly 0.",
        ),
        VerificationCase(
            inputs={"x": 7.25, "k": 0},
            expected=1.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge k = 0: empty product 1.",
        ),
    ),
    assumptions=(
        "x is any finite real number and k a non-negative whole number; k = 0 gives 1. NaN, "
        "infinite x, negative k or non-whole k raise ValueError (the negative-k extension is "
        "not supported).",
        "For a whole number x with 0 <= x < k one factor is zero, so the value is exactly 0 "
        "(a genuine value, not an error). For whole x >= k it equals "
        "mathematics.k_permutations, which instead rejects k > n.",
        "Notation differs between fields ((x)_k is also used for the rising factorial); this "
        "formula is always the descending product.",
        "Computed as a floating-point product with one rounding per factor, so the relative "
        "error grows roughly in proportion to k. Only a final value beyond the "
        "float range raises OverflowError, not a partial product that later factors reduce "
        "again.",
    ),
    tags=(
        "falling factorial",
        "descending factorial",
        "Pochhammer",
        "combinatorics",
    ),
)
