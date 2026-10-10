"""Normal Cumulative Distribution: F = erfc(-(x - mu) / (sigma * sqrt(2))) / 2."""

import math

from sciengformulary.catalog._sources import MATH_ACCESSED, mathlib, nist_statistics_handbook
from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(x: float, mu: float, sigma: float) -> float:
    finite("x", x)
    finite("mu", mu)
    positive("sigma", sigma)
    # erfc of the negated argument rather than (1 + erf) / 2: in the lower tail 1 + erf
    # cancels to 0 (e.g. x = mu - 10 sigma, where F is about 7.6e-24), while erfc keeps the
    # relative accuracy.
    return finite_result(0.5 * math.erfc(-(x - mu) / (sigma * math.sqrt(2.0))))


normal_cumulative_distribution = FormulaSpec(
    id="mathematics.normal_cumulative_distribution",
    name="Normal Cumulative Distribution",
    equation=(
        "F = integral_{-inf}^{x} exp(-(t - mu)^2 / (2 * sigma^2)) / (sigma * sqrt(2 * pi)) dt "
        "= erfc(-(x - mu) / (sigma * sqrt(2))) / 2"
    ),
    description=(
        "Probability that a normal variable with mean mu and standard deviation sigma is at "
        "most x: the integral of the normal density from minus infinity to x, written with the "
        "complementary error function erfc(z) = (2 / sqrt(pi)) * integral_z^inf exp(-t^2) dt."
    ),
    inputs=(
        VariableSpec(
            name="x",
            symbol="x",
            description="Upper limit of the probability",
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
        name="F",
        symbol="F(x)",
        description="Cumulative probability P(X <= x)",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Derived result. The handbook states the standard normal CDF as the integral of
        # e^(-t^2/2) / sqrt(2 pi) from -inf to x, but typesets it with x reused as the
        # integration variable and no dt; restated correctly, F(x) = int_{-inf}^{x} phi(t) dt.
        # Substituting t = sqrt(2) u gives (1 + erf(x / sqrt(2))) / 2 = erfc(-x / sqrt(2)) / 2.
        nist_statistics_handbook(
            "eda/section3/eda3661.htm",
            "sec. 1.3.6.6.1, Normal Distribution: cumulative distribution function",
            accessed=MATH_ACCESSED,
        ),
        # F(x; a, b) = F((x - a)/b; 0, 1) with location a = mu and scale b = sigma.
        nist_statistics_handbook(
            "eda/section3/eda364.htm",
            "sec. 1.3.6.4, Location and Scale Parameters: formulas for location and scale based "
            "on the standard form",
            accessed=MATH_ACCESSED,
        ),
        # Mathlib gives the Gaussian measure of a set as the integral of the density over it
        # (variance v = sigma^2 != 0); with the set (-inf, x] that is the CDF, and the same
        # substitution yields the erfc form. Mathlib's v = 0 (Dirac) case is excluded here.
        mathlib(
            "Mathlib/Probability/Distributions/Gaussian/Real.lean#L245",
            "lemma ProbabilityTheory.gaussianReal_apply_eq_integral",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"x": 0.0, "mu": 0.0, "sigma": 1.0},
            expected=0.5,
            rel_tol=1e-12,
            note="At the mean, by symmetry: 1/2.",
        ),
        VerificationCase(
            inputs={"x": 1.0, "mu": 0.0, "sigma": 1.0},
            expected=0.8413447460685429,
            rel_tol=1e-12,
            note=(
                "One sigma above the mean; 50-digit quadrature of the density equals the erfc "
                "form; scipy identical."
            ),
        ),
        VerificationCase(
            inputs={"x": -1.0, "mu": 0.0, "sigma": 1.0},
            expected=0.15865525393145705,
            rel_tol=1e-12,
            note="One sigma below; 50-digit mpmath quadrature, scipy within 1.7e-16.",
        ),
        VerificationCase(
            inputs={"x": 13.0, "mu": 10.0, "sigma": 2.0},
            expected=0.9331927987311419,
            rel_tol=1e-12,
            note="Non-standard location and scale (z = 1.5); 50-digit mpmath quadrature.",
        ),
        VerificationCase(
            inputs={"x": -10.0, "mu": 0.0, "sigma": 1.0},
            expected=7.619853024160525e-24,
            rel_tol=1e-12,
            note=(
                "Deep lower tail, where (1 + erf)/2 would round to 0; 50-digit quadrature and "
                "erfc agree to 1.4e-49."
            ),
        ),
        VerificationCase(
            inputs={"x": 7.0, "mu": 0.0, "sigma": 1.0},
            expected=0.9999999999987201,
            rel_tol=1e-12,
            note="Upper tail close to 1; 50-digit mpmath quadrature, scipy identical.",
        ),
    ),
    assumptions=(
        "sigma must be finite and > 0, and x and mu finite; otherwise ValueError is raised. "
        "sigma = 0 (a point mass) is not covered.",
        "Derived result: the erfc form follows from the source's integral of the density by "
        "the substitution t = sqrt(2) u and the location-scale rule; checked symbolically "
        "(sympy) and numerically against 50-digit quadrature of the density.",
        "Evaluated with math.erfc, so the lower tail keeps its relative accuracy. Relative "
        "error measured against 50-digit mpmath, z = (x - mu)/sigma: below 2e-14 for "
        "-10 <= z <= 8 and below 3e-13 for -37 <= z < -10 (erfc amplifies the rounding of z "
        "there). Outside that range accuracy is not characterised (above it F rounds to 1.0, "
        "below it F underflows towards 0.0). In the upper tail the complement 1 - F is not "
        "resolved; evaluate the lower tail at mu - (x - mu) for it.",
        "x, mu and sigma share one unit; F is a pure probability.",
    ),
    tags=(
        "normal distribution",
        "Gaussian",
        "cumulative distribution function",
        "cdf",
        "error function",
        "erfc",
        "statistics",
    ),
)
