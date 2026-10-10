"""Gumbel (Maximum) Probability Density: f = exp(-z - exp(-z)) / beta, z = (x - mu) / beta."""

import math

from sciengformulary.catalog._sources import nist_statistics_handbook
from sciengformulary.catalog.mathematics._domain import finite, finite_result, positive
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

# exp(t) overflows a float above about 709.78; past this point exp(-exp(t)) is far below the
# smallest float, so the density is returned as 0.0 without forming exp(t).
_EXP_LIMIT = 709.0


def _evaluate(x: float, mu: float, beta: float) -> float:
    finite("x", x)
    finite("mu", mu)
    positive("beta", beta)
    t = -(x - mu) / beta
    if t > _EXP_LIMIT:
        return 0.0
    return finite_result(math.exp(t - math.exp(t)) / beta)


gumbel_max_probability_density = FormulaSpec(
    id="mathematics.gumbel_max_probability_density",
    name="Gumbel (Maximum) Probability Density",
    equation="f = exp(-z - exp(-z)) / beta, z = (x - mu) / beta",
    description=(
        "Probability density at x of the type I extreme value (Gumbel) law for the largest of "
        "many observations, with location mu (the mode) and scale beta. Its long tail points "
        "to the right."
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
            description="Location parameter (the mode)",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="beta",
            symbol=r"\beta",
            description="Scale parameter, positive",
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
        # The handbook writes (1/beta) e^(-z) e^(-e^(-z)) with z = (x - mu)/beta for the maximum
        # case; the two exponentials are combined here into exp(-z - exp(-z)) / beta.
        nist_statistics_handbook(
            "eda/section3/eda366g.htm",
            "sec. 1.3.6.6.16, Extreme Value Type I Distribution: probability density function, "
            "Gumbel (maximum) case",
            accessed="2026-10-09",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"x": 0.0, "mu": 0.0, "beta": 1.0},
            expected=0.36787944117144233,
            rel_tol=1e-12,
            note="Standard maximum Gumbel at its mode: exp(-1) by hand; 50-digit mpmath.",
        ),
        VerificationCase(
            inputs={"x": 5.5, "mu": 2.0, "beta": 3.0},
            expected=0.07602582610501196,
            rel_tol=1e-12,
            note="Right of the mode; 50-digit mpmath, scipy gumbel_r within 1.8e-16.",
        ),
        VerificationCase(
            inputs={"x": -2.0, "mu": 0.0, "beta": 1.0},
            expected=0.004566281420127915,
            rel_tol=1e-12,
            note="Short (left) tail; 50-digit mpmath, scipy identical.",
        ),
        VerificationCase(
            inputs={"x": -20.0, "mu": 0.0, "beta": 1.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note=(
                "Far short tail: the 50-digit mpmath value is about 3e-210704559, below the "
                "float range; exp(20) must not raise."
            ),
        ),
    ),
    assumptions=(
        "Maximum variant (largest extreme). The minimum variant is "
        "mathematics.gumbel_min_probability_density, its mirror image: "
        "f_min(x; mu, beta) = f_max(-x; -mu, beta).",
        "beta must be finite and > 0, and x and mu finite; otherwise ValueError is raised.",
        "The support is the whole real line. Far in the short (left) tail the value underflows "
        "to 0.0.",
        "Relative error below 2e-13 measured against 50-digit mpmath for 0.01 <= beta <= 100 "
        "and -6 <= z <= 600, z = (x - mu)/beta; the largest errors are in the short tail "
        "(z < 0), where exp(-z) amplifies the rounding of z, and the error stays below 5e-14 "
        "for z >= 30. Outside that range accuracy is not characterised.",
        "x, mu and beta share one unit; the density carries 1/that unit (listed as "
        "dimensionless here).",
    ),
    tags=(
        "Gumbel distribution",
        "extreme value type I",
        "maximum extreme",
        "probability density",
        "pdf",
        "statistics",
    ),
)
