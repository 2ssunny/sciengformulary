"""Normal Probability Density: p(x) = exp(-(x - mu)^2 / (2 sigma^2)) / sqrt(2 pi sigma^2)."""

import math

from sciengformulary.catalog._sources import nist_statistics_handbook
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(x: float, mu: float, sigma: float) -> float:
    return math.exp(-((x - mu) ** 2) / (2.0 * sigma**2)) / math.sqrt(
        2.0 * math.pi * sigma**2
    )


normal_probability_density = FormulaSpec(
    id="mathematics.normal_probability_density",
    name="Normal Probability Density",
    equation="p(x) = exp(-(x - mu)^2 / (2 sigma^2)) / sqrt(2 pi sigma^2)",
    description=(
        "Probability density of a normal (Gaussian) distribution with mean mu and standard "
        "deviation sigma."
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
            description="Mean (location) of the distribution",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="sigma",
            symbol=r"\sigma",
            description="Standard deviation (scale), positive",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="p",
        symbol="p(x)",
        description="Probability density at x (per unit of x)",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        nist_statistics_handbook(
            "eda/section3/eda3661.htm",
            "sec. 1.3.6.6.1, Normal Distribution: probability density function",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"x": 0.0, "mu": 0.0, "sigma": 1.0},
            expected=0.3989422804014327,
            rel_tol=1e-12,
            note=(
                "Standard normal at its peak: 1 / sqrt(2 pi), independent 40-digit decimal "
                "evaluation."
            ),
        ),
        VerificationCase(
            inputs={"x": 13.0, "mu": 10.0, "sigma": 2.0},
            expected=0.06475879783294586,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation of exp(-9/8) / sqrt(8 pi).",
        ),
    ),
    assumptions=(
        "x, mu and sigma share one unit; the density then has units of 1/that unit (listed as "
        "dimensionless here).",
        "A density, not a probability: integrate over an interval to get a probability.",
    ),
    tags=("normal distribution", "Gaussian", "probability density", "statistics", "pdf"),
)
