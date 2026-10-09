"""Beta Probability Density (Standard, on [0, 1]):
f = x^(alpha - 1) * (1 - x)^(beta - 1) / B(alpha, beta) for 0 <= x <= 1; f = 0 otherwise.
"""

import math

from sciengformulary.catalog._sources import MATH_ACCESSED, mathlib, nist_statistics_handbook
from sciengformulary.catalog.mathematics._domain import finite, finite_result, positive
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _edge_value(own_shape: float, other_shape: float, name: str, edge: str) -> float:
    """Continuous limit of the density at the edge where ``own_shape`` is the exponent + 1."""
    if own_shape < 1:
        raise ValueError(
            f"The beta density is unbounded at x = {edge} when {name} < 1, "
            f"got {name}={own_shape!r}."
        )
    # With own_shape = 1 the limit is 1 / B(1, other_shape) = other_shape.
    return float(other_shape) if own_shape == 1 else 0.0


def _evaluate(x: float, alpha: float, beta: float) -> float:
    finite("x", x)
    positive("alpha", alpha)
    positive("beta", beta)
    if x < 0 or x > 1:
        return 0.0
    if x == 0:
        return _edge_value(alpha, beta, "alpha", "0")
    if x == 1:
        return _edge_value(beta, alpha, "beta", "1")
    # Log space keeps the powers and the gamma functions in the normaliser from overflowing on
    # their own; log1p(-x) keeps the digits of 1 - x when x is small.
    log_normaliser = math.lgamma(alpha) + math.lgamma(beta) - math.lgamma(alpha + beta)
    return finite_result(
        math.exp((alpha - 1.0) * math.log(x) + (beta - 1.0) * math.log1p(-x) - log_normaliser)
    )


beta_probability_density = FormulaSpec(
    id="mathematics.beta_probability_density",
    name="Beta Probability Density (Standard, on [0, 1])",
    equation=(
        "f = x^(alpha - 1) * (1 - x)^(beta - 1) / B(alpha, beta) for 0 <= x <= 1; f = 0 "
        "otherwise, with B(alpha, beta) = Gamma(alpha) * Gamma(beta) / Gamma(alpha + beta)"
    ),
    description=(
        "Probability density at x of the standard beta distribution on the unit interval with "
        "shape parameters alpha and beta. alpha = beta = 1 gives the uniform density on [0, 1]."
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
            description="First shape parameter (exponent attached to x), positive",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="beta",
            symbol=r"\beta",
            description="Second shape parameter (exponent attached to 1 - x), positive",
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
        # Mathlib's normaliser beta(alpha, beta) is the same gamma ratio. It gives the value 0
        # at x = 0 and x = 1 (open support); here the endpoints take the continuous limits of
        # the closed-interval form below, and raise where the density is unbounded.
        mathlib(
            "Mathlib/Probability/Distributions/Beta.lean#L51",
            "def ProbabilityTheory.betaPDFReal",
        ),
        # The handbook writes the standard form with shapes p, q on 0 <= x <= 1; p = alpha and
        # q = beta.
        nist_statistics_handbook(
            "eda/section3/eda366h.htm",
            "sec. 1.3.6.6.17, Beta Distribution: probability density function",
            accessed=MATH_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"x": 0.5, "alpha": 2.0, "beta": 3.0},
            expected=1.5,
            rel_tol=1e-12,
            note="Exact 3/2 = 12 * 0.5 * 0.25 by hand; 50-digit mpmath; scipy within 3e-16.",
        ),
        VerificationCase(
            inputs={"x": 0.3, "alpha": 2.5, "beta": 0.7},
            expected=0.25689135846847294,
            rel_tol=1e-12,
            note="Non-integer shapes; 50-digit mpmath, scipy within 2.2e-16.",
        ),
        VerificationCase(
            inputs={"x": 0.25, "alpha": 1.0, "beta": 1.0},
            expected=1.0,
            rel_tol=1e-12,
            note="alpha = beta = 1 is the uniform density on [0, 1].",
        ),
        VerificationCase(
            inputs={"x": 0.0, "alpha": 1.0, "beta": 3.0},
            expected=3.0,
            rel_tol=1e-12,
            note="Edge x = 0 with alpha = 1: the limit 1 / B(1, 3) = 3 by hand.",
        ),
        VerificationCase(
            inputs={"x": 1.0, "alpha": 2.0, "beta": 1.0},
            expected=2.0,
            rel_tol=1e-12,
            note="Edge x = 1 with beta = 1: the limit 1 / B(2, 1) = 2 by hand.",
        ),
        VerificationCase(
            inputs={"x": 0.0, "alpha": 2.0, "beta": 3.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Edge x = 0 with alpha > 1, where x^(alpha - 1) vanishes.",
        ),
        VerificationCase(
            inputs={"x": 1.2, "alpha": 2.0, "beta": 3.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="x > 1 lies outside the support, where the density is zero.",
        ),
    ),
    assumptions=(
        "Standard support [0, 1] with no location or scale. For bounds a < b evaluate at "
        "(x - a) / (b - a) and divide the result by (b - a).",
        "alpha and beta must be finite and > 0, and x finite; otherwise ValueError is raised.",
        "Returns 0.0 for x < 0 and x > 1, where the density is genuinely zero.",
        "Endpoints take the continuous limits: at x = 0 the density is beta when alpha = 1 and "
        "0 when alpha > 1; at x = 1 it is alpha when beta = 1 and 0 when beta > 1. Where it is "
        "unbounded (alpha < 1 at x = 0, beta < 1 at x = 1) ValueError is raised.",
        "Evaluated in log space with log-gamma. Relative error measured against 50-digit "
        "mpmath for 1e-6 <= x <= 1 - 1e-6: below 5e-14 for 0.1 <= alpha, beta <= 20 and below "
        "3e-13 for 0.1 <= alpha, beta <= 100 (it grows with the size of the log terms); "
        "outside that range accuracy is not characterised. A finite input whose density "
        "exceeds the float range raises OverflowError.",
        "x is dimensionless (a fraction of the unit interval).",
    ),
    tags=(
        "beta distribution",
        "probability density",
        "pdf",
        "shape parameters",
        "unit interval",
        "statistics",
    ),
)
