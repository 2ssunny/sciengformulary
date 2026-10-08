"""Exponential Cumulative Distribution: F = 1 - exp(-lam * x) for x >= 0; F = 0 for x < 0."""

import math

from sciengformulary.catalog._sources import MATH_ACCESSED, mathlib, nist_statistics_handbook
from sciengformulary.catalog.mathematics._domain import finite, positive
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(x: float, lam: float) -> float:
    finite("x", x)
    positive("lam", lam)
    if x < 0:
        return 0.0
    # expm1 keeps full precision when lam * x is small, where 1 - exp(...) cancels.
    return -math.expm1(-lam * x)


exponential_cumulative_distribution = FormulaSpec(
    id="mathematics.exponential_cumulative_distribution",
    name="Exponential Cumulative Distribution",
    equation="F = 1 - exp(-lam * x) for x >= 0; F = 0 for x < 0",
    description=(
        "Probability that a variable following an exponential distribution with rate lam "
        "takes a value no greater than x."
    ),
    inputs=(
        VariableSpec(
            name="x",
            symbol="x",
            description="Upper limit of the event X <= x",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="lam",
            symbol=r"\lambda",
            description="Rate parameter, positive (reciprocal of the mean and of the scale)",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="F",
        symbol="F(x)",
        description="Cumulative probability P(X <= x)",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        mathlib(
            "Mathlib/Probability/Distributions/Exponential.lean#L163",
            "lemma ProbabilityTheory.cdf_expMeasure_eq",
        ),
        # The handbook gives F = 1 - exp(-x/beta) with scale beta; beta = 1/lam gives
        # 1 - exp(-lam * x).
        nist_statistics_handbook(
            "eda/section3/eda3667.htm",
            "sec. 1.3.6.6.7, Exponential Distribution: cumulative distribution function",
            accessed=MATH_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"x": 0.6931471805599453, "lam": 1.0},
            expected=0.5,
            rel_tol=1e-12,
            note=(
                "x = float(ln 2) is the median; 50-digit mpmath of the float input rounds to "
                "0.5, scipy identical."
            ),
        ),
        VerificationCase(
            inputs={"x": 3.0, "lam": 0.5},
            expected=0.7768698398515702,
            rel_tol=1e-12,
            note="1 - e^-1.5 from 50-digit mpmath; scipy identical.",
        ),
        VerificationCase(
            inputs={"x": 0.0, "lam": 2.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Support edge x = 0: no probability has accumulated yet.",
        ),
        VerificationCase(
            inputs={"x": 1e-06, "lam": 0.001},
            expected=9.999999995e-10,
            rel_tol=1e-12,
            note=(
                "lam * x = 1e-9, from 50-digit mpmath; checks the cancellation-free form "
                "(a naive 1 - exp loses about 7 digits here)."
            ),
        ),
    ),
    assumptions=(
        "Rate form with location 0: the mean and scale are both 1/lam.",
        "lam must be finite and > 0, and x finite; otherwise ValueError is raised.",
        "Returns 0.0 for x < 0, where no probability lies below x.",
        "x and 1/lam share one unit, so lam * x is dimensionless.",
    ),
    tags=(
        "exponential distribution",
        "cumulative distribution function",
        "cdf",
        "rate",
        "reliability",
        "statistics",
    ),
)
