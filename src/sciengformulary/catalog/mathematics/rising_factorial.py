"""Rising Factorial (Pochhammer Symbol): rf = prod_{i=0}^{k-1} (x + i)."""

import math

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog.mathematics._domain import finite, integer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(x: float, k: float) -> float:
    finite("x", x)
    k = integer("k", k, minimum=0)
    if float(x).is_integer() and -k < x <= 0:
        # One factor is exactly zero; returning early also avoids inf * 0 when the partial
        # product before that factor already overflowed.
        return 0.0
    # The product is carried as mantissa * 2^exponent, so a partial product beyond the float
    # range does not raise when a later factor below 1 would bring it back; only a final value
    # outside the range does.
    mantissa, exponent = 1.0, 0
    for i in range(k):
        factor, factor_exponent = math.frexp(x + i)
        mantissa, product_exponent = math.frexp(mantissa * factor)
        exponent += factor_exponent + product_exponent
    try:
        return math.ldexp(mantissa, exponent)
    except OverflowError as error:
        raise OverflowError("the result is outside the floating-point range.") from error


rising_factorial = FormulaSpec(
    id="mathematics.rising_factorial",
    name="Rising Factorial (Pochhammer Symbol)",
    equation="rf = prod_{i=0}^{k-1} (x + i)",
    description=(
        "Product of k ascending factors x (x + 1) ... (x + k - 1) for a real starting value x. "
        "For x > 0 it equals Gamma(x + k) / Gamma(x), and at x = 1 it is k!."
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
        name="rf",
        symbol="x^(k)",
        description="Rising factorial",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib defines ascPochhammer S n as the polynomial X (X + 1) ... (X + n - 1) and
        # states the step value(n + 1) = value(n) * (x + n) with value(0) = 1; induction on n
        # turns that step into the explicit product above, evaluated at a real x.
        mathlib("Mathlib/RingTheory/Polynomial/Pochhammer.lean#L51", "def ascPochhammer"),
        mathlib(
            "Mathlib/RingTheory/Polynomial/Pochhammer.lean#L130",
            "theorem ascPochhammer_succ_eval",
        ),
        mathlib(
            "Mathlib/RingTheory/Polynomial/Pochhammer.lean#L371",
            "theorem descPochhammer_eval_eq_ascPochhammer",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"x": 1.0, "k": 5},
            expected=120.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="x = 1 gives k! = 120; mpmath rf agrees.",
        ),
        VerificationCase(
            inputs={"x": 2.0, "k": 3},
            expected=24.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Hand calculation: 2 * 3 * 4 = 24.",
        ),
        VerificationCase(
            inputs={"x": 0.5, "k": 2},
            expected=0.75,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Exact Fraction product 0.5 * 1.5 = 0.75.",
        ),
        VerificationCase(
            inputs={"x": -1.5, "k": 3},
            expected=0.375,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Exact Fraction product (-1.5)(-0.5)(0.5) = 0.375.",
        ),
        VerificationCase(
            inputs={"x": -2.0, "k": 4},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Non-positive whole x with k > -x: the factor x + 2 is 0, so the value is 0.",
        ),
        VerificationCase(
            inputs={"x": 3.3, "k": 0},
            expected=1.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge k = 0: empty product 1.",
        ),
    ),
    assumptions=(
        "x is any finite real number and k a non-negative whole number; k = 0 gives 1. NaN, "
        "infinite x, negative k or non-whole k raise ValueError.",
        "Derived result: Mathlib gives the rising factorial as a polynomial with the step "
        "value(k + 1) = value(k) * (x + k); the explicit product follows by induction on k. "
        "It was checked numerically against mpmath's rf and, for x > 0, against "
        "Gamma(x + k) / Gamma(x).",
        "For a non-positive whole number x with k > -x one factor is zero, so the value is "
        "exactly 0.",
        "Notation differs between fields ((x)_k means the rising factorial in special-function "
        "work and the falling one in combinatorics); this formula is always the ascending "
        "product.",
        "Computed as a floating-point product with one rounding per factor, so the relative "
        "error grows roughly in proportion to k. Only a final value beyond the "
        "float range raises OverflowError, not a partial product that later factors reduce "
        "again.",
    ),
    tags=(
        "rising factorial",
        "Pochhammer symbol",
        "ascending factorial",
        "combinatorics",
    ),
)
