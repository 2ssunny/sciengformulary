"""Laplace (Double Exponential) Probability Density: f = exp(-abs(x - mu) / b) / (2 * b)."""

import math

from sciengformulary.catalog._sources import nist_statistics_handbook
from sciengformulary.catalog.mathematics._domain import finite, finite_result, positive
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(x: float, mu: float, b: float) -> float:
    finite("x", x)
    finite("mu", mu)
    positive("b", b)
    return finite_result(math.exp(-abs(x - mu) / b) / (2.0 * b))


laplace_probability_density = FormulaSpec(
    id="mathematics.laplace_probability_density",
    name="Laplace (Double Exponential) Probability Density",
    equation="f = exp(-abs(x - mu) / b) / (2 * b)",
    description=(
        "Probability density at x of the Laplace (double exponential) distribution with "
        "location mu and scale b: two exponential tails joined at a peak of height 1/(2 b) "
        "at x = mu."
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
            name="mu",
            symbol=r"\mu",
            description="Location parameter (mean, median and mode)",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="b",
            symbol="b",
            description="Scale parameter, positive (the standard deviation is sqrt(2) b)",
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
        # The handbook calls the scale beta and writes e^(-|(x - mu)/beta|) / (2 beta); for
        # beta = b > 0, |(x - mu)/b| = |x - mu| / b.
        nist_statistics_handbook(
            "eda/section3/eda366c.htm",
            "sec. 1.3.6.6.12, Double Exponential Distribution: probability density function",
            accessed="2026-10-09",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"x": 0.0, "mu": 0.0, "b": 1.0},
            expected=0.5,
            rel_tol=1e-12,
            note="Peak of the standard Laplace density: 1/2.",
        ),
        VerificationCase(
            inputs={"x": 1.0, "mu": 0.0, "b": 1.0},
            expected=0.18393972058572117,
            rel_tol=1e-12,
            note="exp(-1)/2 by hand; 50-digit mpmath, scipy identical.",
        ),
        VerificationCase(
            inputs={"x": -2.0, "mu": 1.0, "b": 2.0},
            expected=0.055782540037107455,
            rel_tol=1e-12,
            note="Left of the location, exp(-1.5)/4; 50-digit mpmath, scipy identical.",
        ),
        VerificationCase(
            inputs={"x": 4.5, "mu": 1.0, "b": 0.5},
            expected=0.0009118819655545162,
            rel_tol=1e-12,
            note="Right tail, exp(-7); 50-digit mpmath, scipy identical.",
        ),
    ),
    assumptions=(
        "b must be finite and > 0, and x and mu finite; otherwise ValueError is raised.",
        "The support is the whole real line; far in the tails the value underflows to 0.0.",
        "Relative error measured against 50-digit mpmath on more than 5000 random points per range "
        "with 0.01 <= b <= 100: below 1.2e-14 for |x - mu| / b <= 50 (largest observed 7.5e-15) "
        "and below 2e-13 for |x - mu| / b <= 700 (largest observed 1.2e-13; it grows with that "
        "ratio, which is rounded before the exponential); outside that range accuracy is not "
        "characterised.",
        "x, mu and b share one unit; the density carries 1/that unit (listed as dimensionless "
        "here).",
    ),
    tags=(
        "Laplace distribution",
        "double exponential distribution",
        "probability density",
        "pdf",
        "statistics",
    ),
)
