"""Exponential Probability Density: f = lam * exp(-lam * x) for x >= 0; f = 0 for x < 0."""

import math

from sciengformulary.catalog._sources import MATH_ACCESSED, mathlib, nist_statistics_handbook
from sciengformulary.catalog.mathematics._domain import finite, positive
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(x: float, lam: float) -> float:
    finite("x", x)
    positive("lam", lam)
    if x < 0:
        return 0.0
    return lam * math.exp(-lam * x)


exponential_probability_density = FormulaSpec(
    id="mathematics.exponential_probability_density",
    name="Exponential Probability Density",
    equation="f = lam * exp(-lam * x) for x >= 0; f = 0 for x < 0",
    description=(
        "Probability density at x of an exponential distribution with rate lam, whose mean "
        "is 1/lam."
    ),
    inputs=(
        VariableSpec(
            name="x",
            symbol="x",
            description="Value at which the density is evaluated",
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
        name="f",
        symbol="f(x)",
        description="Probability density at x (per unit of x)",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        mathlib(
            "Mathlib/Probability/Distributions/Exponential.lean#L47",
            "lemma ProbabilityTheory.exponentialPDF_eq",
        ),
        # The handbook writes the density with location mu and scale beta; with mu = 0 and
        # beta = 1/lam, (1/beta) exp(-x/beta) becomes lam * exp(-lam * x) for x >= 0.
        nist_statistics_handbook(
            "eda/section3/eda3667.htm",
            "sec. 1.3.6.6.7, Exponential Distribution: probability density function",
            accessed=MATH_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"x": 0.5, "lam": 2.0},
            expected=0.7357588823428847,
            rel_tol=1e-12,
            note="2 e^-1 from 50-digit mpmath; scipy expon(scale=1/lam) identical.",
        ),
        VerificationCase(
            inputs={"x": 0.0, "lam": 2.0},
            expected=2.0,
            rel_tol=1e-12,
            note="Support edge x = 0, where the density equals lam exactly.",
        ),
        VerificationCase(
            inputs={"x": -1.0, "lam": 1.5},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="x < 0 lies outside the support, where the density is zero.",
        ),
    ),
    assumptions=(
        "Rate form with location 0: the mean and scale are both 1/lam.",
        "lam must be finite and > 0, and x finite; otherwise ValueError is raised.",
        "Returns 0.0 for x < 0, where the density is genuinely zero; f(0) = lam.",
        "x and 1/lam share one unit; lam and the density then carry 1/that unit (listed as "
        "dimensionless here).",
        "A density, not a probability: integrate it over an interval to get a probability.",
    ),
    tags=(
        "exponential distribution",
        "probability density",
        "pdf",
        "rate",
        "waiting time",
        "statistics",
    ),
)
