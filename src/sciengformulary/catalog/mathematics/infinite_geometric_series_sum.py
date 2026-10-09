"""Infinite Geometric Series Sum: S = 1 / (1 - r)."""

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog._domain import finite
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(r: float) -> float:
    if abs(finite("r", r)) >= 1:
        raise ValueError(f"|r| must be below 1 for the series to converge, got {r!r}.")
    return 1.0 / (1.0 - r)


infinite_geometric_series_sum = FormulaSpec(
    id="mathematics.infinite_geometric_series_sum",
    name="Infinite Geometric Series Sum",
    equation="S = 1 / (1 - r)",
    description=(
        "Value of the infinite geometric series 1 + r + r^2 + ..., which converges when the "
        "common ratio has absolute value below 1."
    ),
    inputs=(
        VariableSpec(
            name="r",
            symbol="r",
            description="Common ratio (real), |r| < 1",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="S",
        symbol="S",
        description="Sum of r^k for k = 0, 1, 2, ...",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib gives the sum as (1 - r)^-1, i.e. 1 / (1 - r), for real |r| < 1.
        mathlib(
            "Mathlib/Analysis/SpecificLimits/Normed.lean#L489",
            "theorem hasSum_geometric_of_abs_lt_one",
        ),
        # Summable if and only if |r| < 1: the series has no sum for |r| >= 1.
        mathlib(
            "Mathlib/Analysis/SpecificLimits/Normed.lean#L502",
            "theorem summable_geometric_iff_norm_lt_one",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"r": 0.5},
            expected=2.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Exact Fraction partial sum with a rigorous tail bound, and 60-digit mpmath "
                "direct summation of r^k."
            ),
        ),
        VerificationCase(
            inputs={"r": -0.5},
            expected=0.6666666666666666,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Negative ratio: 60-digit mpmath direct summation and exact Fraction give 2/3.",
        ),
        VerificationCase(
            inputs={"r": 0.9},
            expected=10.000000000000002,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Exact Fraction 1/(1 - r) for the binary value of the float 0.9, confirmed by "
                "60-digit mpmath direct summation."
            ),
        ),
        VerificationCase(
            inputs={"r": -0.999},
            expected=0.5002501250625313,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Near r = -1 (sum tends to 1/2): exact Fraction value for the float input, "
                "confirmed by 60-digit mpmath direct summation."
            ),
        ),
        VerificationCase(
            inputs={"r": 0.0},
            expected=1.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge r = 0: only the first term 1 is nonzero (exact Fraction).",
        ),
    ),
    assumptions=(
        "Real common ratio with |r| < 1; for |r| >= 1 the series diverges and the evaluator "
        "rejects the input instead of returning a value.",
        "The first term is 1; for a first term a, multiply the result by a (not an input).",
        "Close to r = 1 the sum grows like 1 / (1 - r) and inherits the relative rounding error "
        "of the float input r.",
    ),
    tags=(
        "geometric series",
        "infinite series",
        "convergent series",
        "sum to infinity",
        "series",
    ),
)
