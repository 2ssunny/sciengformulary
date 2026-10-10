"""Logarithm Change of Base: y = ln(x) / ln(b)."""

import math

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog.mathematics._domain import positive
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(b: float, x: float) -> float:
    if positive("b", b) == 1:
        raise ValueError(f"b must not be 1 (ln 1 = 0), got {b!r}.")
    positive("x", x)
    return math.log(x) / math.log(b)


logarithm_change_of_base = FormulaSpec(
    id="mathematics.logarithm_change_of_base",
    name="Logarithm Change of Base",
    equation="y = ln(x) / ln(b)",
    description=(
        "Logarithm of x to an arbitrary base b, written with natural logarithms; y is the "
        "exponent for which b^y = x."
    ),
    inputs=(
        VariableSpec(
            name="b",
            symbol="b",
            description="Base of the logarithm (positive, not 1)",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="x",
            symbol="x",
            description="Argument of the logarithm (positive)",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="y",
        symbol="y",
        description="Base-b logarithm of x",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib defines logb b x = log x / log b as a total function (|x| for negative x,
        # 0 for x = 0 or b in {0, 1}); those conventions are not adopted here.
        mathlib("Mathlib/Analysis/SpecialFunctions/Log/Base.lean#L44", "def Real.logb"),
        # Stated under 0 < b, b != 1 and a positive argument: the domain used here.
        mathlib(
            "Mathlib/Analysis/SpecialFunctions/Log/Base.lean#L155",
            "theorem Real.logb_eq_iff_rpow_eq",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"b": 2, "x": 8},
            expected=3.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="2^3 = 8; mpmath 50-digit ln(8)/ln(2), cross-checked by solving 2^y = 8.",
        ),
        VerificationCase(
            inputs={"b": 10, "x": 1000},
            expected=3.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "10^3 = 1000; mpmath 50-digit quotient and root of 10^y = 1000 (the float "
                "quotient lands one ulp below 3, inside the tolerance)."
            ),
        ),
        VerificationCase(
            inputs={"b": 0.5, "x": 4},
            expected=-2.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Base below 1: 0.5^-2 = 4; mpmath quotient and root of 0.5^y = 4.",
        ),
        VerificationCase(
            inputs={"b": 3, "x": 1},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-12,
            note="ln(1) = 0 exactly, so y = 0 for any admissible base; confirmed by root finding.",
        ),
        VerificationCase(
            inputs={"b": 7.5, "x": 0.02},
            expected=-1.9415440671558053,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "mpmath 50-digit ln(0.02)/ln(7.5) = -1.941544067155805403..., agreeing with "
                "the root of 7.5^y = 0.02."
            ),
        ),
        VerificationCase(
            inputs={"b": 1.001, "x": 2},
            expected=693.4936964168994,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Base close to the excluded value 1: mpmath 50-digit quotient with the exact "
                "binary value of 1.001 (693.4936964168994287...), agreeing with root finding."
            ),
        ),
    ),
    assumptions=(
        "Real logarithms only: x must be positive, and b positive and different from 1; other "
        "values raise ValueError.",
        "Any admissible base works, including 0 < b < 1, where y has the opposite sign to ln x.",
        "For b close to 1 the result is large and very sensitive to the value of b.",
    ),
    tags=("logarithm", "change of base", "log base b", "algebra"),
)
