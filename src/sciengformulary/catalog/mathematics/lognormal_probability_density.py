"""Lognormal Probability Density:
f = exp(-(ln(x) - mu)^2 / (2 * sigma^2)) / (x * sigma * sqrt(2 * pi)) for x > 0; f = 0 for x <= 0.
"""

import math

from sciengformulary.catalog._sources import nist_statistics_handbook
from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

_SQRT_2PI = math.sqrt(2.0 * math.pi)


def _evaluate(x: float, mu: float, sigma: float) -> float:
    finite("x", x)
    finite("mu", mu)
    positive("sigma", sigma)
    if x <= 0:
        return 0.0
    log_x = math.log(x)
    u = (log_x - mu) / sigma
    # The 1/x factor goes into the exponent so a tiny x cannot overflow it on its own.
    return finite_result(math.exp(-0.5 * u * u - log_x) / (sigma * _SQRT_2PI))


lognormal_probability_density = FormulaSpec(
    id="mathematics.lognormal_probability_density",
    name="Lognormal Probability Density",
    equation=(
        "f = exp(-(ln(x) - mu)^2 / (2 * sigma^2)) / (x * sigma * sqrt(2 * pi)) for x > 0; "
        "f = 0 for x <= 0"
    ),
    description=(
        "Probability density at x of a two-parameter lognormal variable, one whose natural "
        "logarithm is normal with mean mu and standard deviation sigma. In the NIST handbook's "
        "terms sigma is the shape parameter, exp(mu) the scale parameter m (the median of the "
        "variable itself) and the location theta is 0."
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
            description=(
                "Log-scale parameter: mean of ln(X), not the mean of X; the scale (median of "
                "X) is m = exp(mu)"
            ),
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="sigma",
            symbol=r"\sigma",
            description=("Shape parameter: standard deviation of ln(X), not of X; positive"),
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
        # The handbook gives the density with location theta and, as an alternative to its
        # median m, the parameter mu = ln(m). The two-parameter case theta = 0 is this form;
        # with m = exp(mu), ln(x/m) = ln(x) - mu, so the m form is the same density.
        nist_statistics_handbook(
            "eda/section3/eda3669.htm",
            "sec. 1.3.6.6.9, Lognormal Distribution: probability density function "
            "(mu parameterization)",
            accessed="2026-10-09",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"x": 1.0, "mu": 0.0, "sigma": 1.0},
            expected=0.3989422804014327,
            rel_tol=1e-12,
            note="ln(1) = 0 gives 1/sqrt(2 pi); 50-digit mpmath, scipy identical.",
        ),
        VerificationCase(
            inputs={"x": 2.5, "mu": 0.5, "sigma": 0.8},
            expected=0.17421331967496656,
            rel_tol=1e-12,
            note="50-digit mpmath; scipy lognorm(s=0.8, scale=exp(0.5)) identical.",
        ),
        VerificationCase(
            inputs={"x": 0.05, "mu": -1.0, "sigma": 0.4},
            expected=7.840476421901059e-05,
            rel_tol=1e-12,
            note="Lower tail; 50-digit mpmath, scipy within 1.2e-15.",
        ),
        VerificationCase(
            inputs={"x": 0.0, "mu": 0.0, "sigma": 1.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Support edge x = 0, where the source sets the density to zero.",
        ),
        VerificationCase(
            inputs={"x": -1.0, "mu": 0.0, "sigma": 1.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="x < 0 lies outside the support, where the density is zero.",
        ),
    ),
    assumptions=(
        "Two-parameter form (location theta = 0). For a shifted variable use x - theta.",
        "mu and sigma describe ln(X): X has median exp(mu) and mean exp(mu + sigma^2 / 2).",
        "sigma must be finite and > 0, and x and mu finite; otherwise ValueError is raised.",
        "Returns 0.0 for x <= 0; the density tends to 0 as x approaches 0 from above.",
        "Relative error measured against 50-digit mpmath for 0.05 <= sigma <= 10 and "
        "-10 <= mu <= 10: below 2e-14 for |ln(x) - mu| / sigma <= 10 and below 1e-13 for "
        "|ln(x) - mu| / sigma <= 30; outside that range accuracy is not characterised. A "
        "finite input whose density exceeds the float range raises OverflowError.",
        "x and exp(mu) share one unit; the density carries 1/that unit (listed as "
        "dimensionless here).",
    ),
    tags=(
        "lognormal distribution",
        "log-normal",
        "probability density",
        "pdf",
        "statistics",
    ),
)
