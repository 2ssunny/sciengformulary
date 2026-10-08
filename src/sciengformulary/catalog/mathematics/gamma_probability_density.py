"""Gamma Probability Density (Shape-Rate):
f = lam^alpha * x^(alpha - 1) * exp(-lam * x) / Gamma(alpha) for x >= 0; f = 0 for x < 0.
"""

import math

from sciengformulary.catalog._sources import MATH_ACCESSED, mathlib, nist_statistics_handbook
from sciengformulary.catalog.mathematics._domain import finite, positive
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(x: float, alpha: float, lam: float) -> float:
    finite("x", x)
    positive("alpha", alpha)
    positive("lam", lam)
    if x < 0:
        return 0.0
    if x == 0:
        if alpha < 1:
            raise ValueError(
                f"The gamma density is unbounded at x = 0 when alpha < 1, got alpha={alpha!r}."
            )
        return float(lam) if alpha == 1 else 0.0
    # Log space keeps lam^alpha and Gamma(alpha) from overflowing on their own.
    return math.exp(
        alpha * math.log(lam) + (alpha - 1.0) * math.log(x) - lam * x - math.lgamma(alpha)
    )


gamma_probability_density = FormulaSpec(
    id="mathematics.gamma_probability_density",
    name="Gamma Probability Density (Shape-Rate)",
    equation=(
        "f = lam^alpha * x^(alpha - 1) * exp(-lam * x) / Gamma(alpha) for x >= 0; f = 0 for x < 0"
    ),
    description=(
        "Probability density at x of a gamma distribution with shape alpha and rate lam "
        "(scale 1/lam). Setting alpha = 1 recovers the exponential density with rate lam."
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
            name="alpha",
            symbol=r"\alpha",
            description="Shape parameter, positive",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="lam",
            symbol=r"\lambda",
            description="Rate parameter, positive (reciprocal of the scale)",
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
        # Mathlib's real power makes 0^(alpha - 1) = 0 for alpha < 1; the true density is
        # unbounded there, so this implementation raises instead.
        mathlib(
            "Mathlib/Probability/Distributions/Gamma.lean#L45",
            "def ProbabilityTheory.gammaPDFReal",
        ),
        # The handbook uses shape gamma, location mu and scale beta; with mu = 0, gamma = alpha
        # and beta = 1/lam its density equals lam^alpha x^(alpha - 1) e^(-lam x) / Gamma(alpha)
        # for x > 0.
        nist_statistics_handbook(
            "eda/section3/eda366b.htm",
            "sec. 1.3.6.6.11, Gamma Distribution: probability density function",
            accessed=MATH_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"x": 2.0, "alpha": 3.0, "lam": 0.5},
            expected=0.09196986029286058,
            rel_tol=1e-12,
            note=(
                "Integer shape, e^-1 / 4 by hand; 50-digit mpmath; scipy gamma(a, scale=1/lam) "
                "agrees to 1.5e-16."
            ),
        ),
        VerificationCase(
            inputs={"x": 0.7, "alpha": 2.5, "lam": 1.5},
            expected=0.4248443059528857,
            rel_tol=1e-12,
            note="Non-integer shape; 50-digit mpmath, scipy identical.",
        ),
        VerificationCase(
            inputs={"x": 0.25, "alpha": 0.5, "lam": 1.0},
            expected=0.8787825789354448,
            rel_tol=1e-12,
            note="Shape below 1 (decreasing density); 50-digit mpmath, scipy within 1.3e-16.",
        ),
        VerificationCase(
            inputs={"x": 0.0, "alpha": 1.0, "lam": 2.0},
            expected=2.0,
            rel_tol=1e-12,
            note="Support edge x = 0 with alpha = 1 (the exponential case): f = lam.",
        ),
        VerificationCase(
            inputs={"x": 0.0, "alpha": 2.0, "lam": 1.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Support edge x = 0 with alpha > 1, where x^(alpha - 1) = 0.",
        ),
    ),
    assumptions=(
        "Shape-rate form with location 0. For shape k and scale theta use alpha = k and "
        "lam = 1/theta.",
        "alpha and lam must be finite and > 0, and x finite; otherwise ValueError is raised.",
        "Returns 0.0 for x < 0, where the density is genuinely zero.",
        "At x = 0 the density is lam for alpha = 1 and 0 for alpha > 1; for alpha < 1 it is "
        "unbounded, so x = 0 raises ValueError.",
        "Evaluated in log space with log-gamma, so large alpha or lam do not overflow. The "
        "relative error grows with the size of the log terms (about 1e-16 times their "
        "magnitude), e.g. near 1e-13 for alpha around 1000.",
        "x and 1/lam share one unit; the density carries 1/that unit (listed as dimensionless "
        "here).",
    ),
    tags=(
        "gamma distribution",
        "probability density",
        "pdf",
        "shape",
        "rate",
        "Erlang",
        "statistics",
    ),
)
