"""Rayleigh Probability Density: f = (x / sigma^2) * exp(-x^2 / (2 * sigma^2)) for x >= 0."""

import math

from sciengformulary.catalog._sources import nist_statistics_handbook
from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


# Below this exponent exp() is no longer a normal float (ln of the smallest normal is -708.4).
_SPLIT_BELOW = -700.0


def _evaluate(x: float, sigma: float) -> float:
    finite("x", x)
    positive("sigma", sigma)
    if x < 0:
        return 0.0
    u = x / sigma
    if math.isinf(u):
        # x / sigma is beyond the float range, so exp(-u^2 / 2) is 0 far below anything
        # representable even after the division by sigma.
        return 0.0
    exponent = -0.5 * u * u  # -inf if u * u overflows; exp(-inf) = 0
    if exponent < _SPLIT_BELOW:
        # exp(exponent) would be subnormal or 0 although 1 / sigma may bring the product back
        # into range; folding 1 / sqrt(sigma) into each of two equal halves avoids that.
        half = math.exp(0.5 * exponent) / math.sqrt(sigma)
        return finite_result(u * half * half)
    return finite_result(u * math.exp(exponent) / sigma)


rayleigh_probability_density = FormulaSpec(
    id="mathematics.rayleigh_probability_density",
    name="Rayleigh Probability Density",
    equation="f = (x / sigma^2) * exp(-x^2 / (2 * sigma^2)) for x >= 0; f = 0 for x < 0",
    description=(
        "Probability density at x of the Rayleigh distribution: the distance from the origin "
        "of a point whose two Cartesian coordinates are independent zero-mean normal variables "
        "with standard deviation sigma. It is the Weibull law with shape 2 and scale "
        "sigma * sqrt(2)."
    ),
    inputs=(
        VariableSpec(
            name="x",
            symbol="x",
            description="Value (radial distance) at which the density is evaluated",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="sigma",
            symbol=r"\sigma",
            description=(
                "Scale parameter: standard deviation of each coordinate (also the mode), "
                "positive; the Weibull scale is sigma * sqrt(2)"
            ),
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
        # Derived result. The handbook names the Weibull law with shape gamma = 2 the Rayleigh
        # distribution and identifies it as the radial error of two independent zero-mean
        # normal coordinates with a common standard deviation sigma. Its Weibull density
        # (gamma/t)(t/alpha)^gamma exp(-(t/alpha)^gamma) with gamma = 2 and scale
        # alpha = sigma * sqrt(2) (fixed by that radial-error statement) is
        # (x / sigma^2) exp(-x^2 / (2 sigma^2)).
        nist_statistics_handbook(
            "apr/section1/apr162.htm",
            "sec. 8.1.6.2, Weibull: uses of the Weibull distribution model (Rayleigh special case)",
            accessed="2026-10-09",
        ),
        # General Weibull density; location mu = 0, shape gamma = 2, scale alpha = sigma sqrt(2).
        nist_statistics_handbook(
            "eda/section3/eda3668.htm",
            "sec. 1.3.6.6.8, Weibull Distribution: probability density function",
            accessed="2026-10-09",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"x": 1.0, "sigma": 1.0},
            expected=0.6065306597126334,
            rel_tol=1e-12,
            note="Mode of the standard law: exp(-1/2) by hand; 50-digit mpmath, scipy identical.",
        ),
        VerificationCase(
            inputs={"x": 3.0, "sigma": 2.0},
            expected=0.2434893505187623,
            rel_tol=1e-12,
            note="0.75 exp(-9/8); 50-digit mpmath, scipy rayleigh(scale=2) identical.",
        ),
        VerificationCase(
            inputs={"x": 0.1, "sigma": 0.5},
            expected=0.39207946932270216,
            rel_tol=1e-12,
            note="Near the origin; 50-digit mpmath, scipy identical.",
        ),
        VerificationCase(
            inputs={"x": 0.0, "sigma": 1.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Support edge x = 0, where the density is zero.",
        ),
        VerificationCase(
            inputs={"x": -0.5, "sigma": 1.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="x < 0 lies outside the support, where the density is zero.",
        ),
    ),
    assumptions=(
        "Scale convention: sigma is the standard deviation of each underlying coordinate (and "
        "the mode), not the Weibull characteristic life, which is sigma * sqrt(2).",
        "Derived result: the Weibull density with shape 2 and scale sigma * sqrt(2), the scale "
        "being fixed by the source's radial-error description; checked symbolically and "
        "numerically (2-D quadrature of two independent normal densities over a disk).",
        "sigma must be finite and > 0, and x finite; otherwise ValueError is raised.",
        "Returns 0.0 for x < 0; f(0) = 0. Far in the tail the value underflows to 0.0.",
        "Relative error measured against 50-digit mpmath (the explicit Rayleigh density) on more "
        "than 5000 random points per range with 1e-3 <= sigma <= 1e3: below 2e-14 for 0 < x / "
        "sigma <= 10 (largest observed 1.2e-14) and below 2.5e-13 for x / sigma <= 37 (largest "
        "observed 1.6e-13; the error grows like (x / sigma)^2 times the rounding unit); outside "
        "that range accuracy is not characterised.",
        "Only a result beyond the float range raises OverflowError (for example a tiny sigma). "
        "If x / sigma itself is beyond the float range the density is 0.0, and for tiny sigma "
        "the division by sigma is folded into the exponential so that a value that is "
        "representable is not lost to underflow of exp(-x^2 / (2 sigma^2)).",
        "x and sigma share one unit; the density carries 1/that unit (listed as dimensionless "
        "here).",
    ),
    tags=(
        "Rayleigh distribution",
        "Weibull shape 2",
        "radial error",
        "probability density",
        "pdf",
        "statistics",
    ),
)
