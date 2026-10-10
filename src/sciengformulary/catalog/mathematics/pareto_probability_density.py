"""Pareto (Type I) Probability Density: f = alpha * x_m^alpha / x^(alpha + 1) for x >= x_m."""

import math

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog.mathematics._domain import finite, finite_result, positive
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(x: float, x_m: float, alpha: float) -> float:
    finite("x", x)
    positive("x_m", x_m)
    positive("alpha", alpha)
    if x < x_m:
        return 0.0
    # f = (alpha / x) * (x_m / x)^alpha, in log space so x_m^alpha cannot overflow on its own.
    # Near the lower bound log1p keeps the digits of the small log ratio (x_m - x is exact
    # there); further out the plain difference of logs cannot cancel.
    if x <= 2.0 * x_m:
        log_ratio = math.log1p((x_m - x) / x)
    else:
        log_ratio = math.log(x_m) - math.log(x)
    return finite_result(math.exp(math.log(alpha) - math.log(x) + alpha * log_ratio))


pareto_probability_density = FormulaSpec(
    id="mathematics.pareto_probability_density",
    name="Pareto (Type I) Probability Density",
    equation="f = alpha * x_m^alpha / x^(alpha + 1) for x >= x_m; f = 0 for x < x_m",
    description=(
        "Probability density at x of the Pareto type I distribution with scale x_m (the "
        "smallest possible value) and shape alpha (the tail index): a power-law tail that "
        "starts at x_m."
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
            name="x_m",
            symbol="x_m",
            description="Scale parameter: the smallest possible value, positive",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="alpha",
            symbol=r"\alpha",
            description="Shape parameter (tail index), positive",
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
        # Mathlib writes r * t^r * x^(-(r + 1)) for t <= x with scale t and shape r (its
        # docstring calls r a rate); t = x_m, r = alpha. Its t <= 0 or r <= 0 cases are not
        # densities and raise here.
        mathlib(
            "Mathlib/Probability/Distributions/Pareto.lean#L37",
            "def ProbabilityTheory.paretoPDFReal",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"x": 2.0, "x_m": 1.0, "alpha": 2.0},
            expected=0.25,
            rel_tol=1e-12,
            note="Exact 2 * 1 / 2^3 = 1/4 by hand; scipy pareto identical.",
        ),
        VerificationCase(
            inputs={"x": 3.3, "x_m": 2.0, "alpha": 1.7},
            expected=0.21989344148353349,
            rel_tol=1e-12,
            note="Non-integer shape; 50-digit mpmath, scipy within 1.3e-16.",
        ),
        VerificationCase(
            inputs={"x": 1.5, "x_m": 1.5, "alpha": 3.0},
            expected=2.0,
            rel_tol=1e-12,
            note="Support edge x = x_m: alpha / x_m = 2 by hand.",
        ),
        VerificationCase(
            inputs={"x": 1.0, "x_m": 1.5, "alpha": 3.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="x below the minimum value lies outside the support.",
        ),
    ),
    assumptions=(
        "Type I Pareto: the support starts at x_m. This is not the Lomax (type II) form.",
        "x_m and alpha must be finite and > 0, and x finite; otherwise ValueError is raised.",
        "Returns 0.0 for x < x_m; at x = x_m the density is alpha / x_m (closed support).",
        "Relative error measured against 50-digit mpmath on more than 5000 random points per range "
        "of alpha with 1e-3 <= x_m <= 1e3 and x_m <= x <= 1e6 x_m: below 6e-14 for 0.1 <= alpha <= "
        "10 (largest observed 3.9e-14) and below 2.5e-13 for alpha <= 50 (largest observed "
        "1.7e-13); outside that range accuracy is not characterised. A finite input whose density "
        "exceeds the float range raises OverflowError.",
        "x and x_m share one unit; the density carries 1/that unit (listed as dimensionless here).",
    ),
    tags=(
        "Pareto distribution",
        "power law",
        "probability density",
        "pdf",
        "heavy tail",
        "statistics",
    ),
)
