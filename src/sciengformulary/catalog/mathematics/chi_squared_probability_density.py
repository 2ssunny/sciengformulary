"""Chi-Squared Probability Density:
f = x^(k/2 - 1) * exp(-x / 2) / (2^(k/2) * Gamma(k / 2)) for x >= 0; f = 0 for x < 0.
"""

import math

from sciengformulary.catalog._sources import mathlib, nist_statistics_handbook
from sciengformulary.catalog.mathematics._domain import finite, finite_result, positive
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(x: float, k: float) -> float:
    finite("x", x)
    positive("k", k)
    if x < 0:
        return 0.0
    if x == 0:
        if k < 2:
            raise ValueError(
                f"The chi-squared density is unbounded at x = 0 when k < 2, got k={k!r}."
            )
        return 0.5 if k == 2 else 0.0
    half_k = 0.5 * k
    # Log space keeps 2^(k/2) and Gamma(k/2) from overflowing on their own.
    log_f = (half_k - 1.0) * math.log(x) - 0.5 * x - half_k * math.log(2.0) - math.lgamma(half_k)
    return finite_result(math.exp(log_f))


chi_squared_probability_density = FormulaSpec(
    id="mathematics.chi_squared_probability_density",
    name="Chi-Squared Probability Density",
    equation=(
        "f = x^(k/2 - 1) * exp(-x / 2) / (2^(k/2) * Gamma(k / 2)) for x >= 0; f = 0 for x < 0"
    ),
    description=(
        "Probability density at x of the (central) chi-squared distribution with k degrees of "
        "freedom, the law of a sum of k squared independent standard normal variables. It is "
        "the gamma density with shape k/2 and rate 1/2."
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
            name="k",
            symbol="k",
            description=(
                "Degrees of freedom (shape), positive; a whole number in the sum-of-squares "
                "reading, any positive real allowed"
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
        # The handbook calls the degrees of freedom nu; nu = k, factors reordered.
        nist_statistics_handbook(
            "eda/section3/eda3666.htm",
            "sec. 1.3.6.6.6, Chi-Square Distribution: probability density function",
            accessed="2026-10-09",
        ),
        # Mathlib's gamma density with shape a = k/2 and rate r = 1/2 is this density; it holds
        # for any real k > 0, not only whole numbers.
        mathlib(
            "Mathlib/Probability/Distributions/Gamma.lean#L45",
            "def ProbabilityTheory.gammaPDFReal",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"x": 2.0, "k": 2.0},
            expected=0.18393972058572117,
            rel_tol=1e-12,
            note="k = 2 gives exp(-x/2)/2 = exp(-1)/2 by hand; 50-digit mpmath; scipy 1.5e-16.",
        ),
        VerificationCase(
            inputs={"x": 3.7, "k": 5.0},
            expected=0.1488149647032659,
            rel_tol=1e-12,
            note="Odd k; 50-digit mpmath, scipy within 1.9e-16.",
        ),
        VerificationCase(
            inputs={"x": 0.5, "k": 1.0},
            expected=0.4393912894677224,
            rel_tol=1e-12,
            note="k = 1 (decreasing density); 50-digit mpmath, scipy within 1.3e-16.",
        ),
        VerificationCase(
            inputs={"x": 1.3, "k": 3.4},
            expected=0.2124842259030073,
            rel_tol=1e-12,
            note="Non-integer k; 50-digit mpmath of the gamma form, scipy within 1.3e-16.",
        ),
        VerificationCase(
            inputs={"x": 0.0, "k": 2.0},
            expected=0.5,
            rel_tol=1e-12,
            note="Edge x = 0 with k = 2: the density equals 1/2.",
        ),
        VerificationCase(
            inputs={"x": 0.0, "k": 4.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Edge x = 0 with k > 2, where x^(k/2 - 1) vanishes.",
        ),
        VerificationCase(
            inputs={"x": -1.0, "k": 3.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="x < 0 lies outside the support, where the density is zero.",
        ),
    ),
    assumptions=(
        "Central chi-squared with no location or scale; for shape alpha and rate lam in general "
        "use mathematics.gamma_probability_density (here alpha = k/2, lam = 1/2).",
        "k must be finite and > 0, and x finite; otherwise ValueError is raised. Non-integer k "
        "is accepted.",
        "Returns 0.0 for x < 0, where the density is genuinely zero.",
        "At x = 0 the density is 1/2 for k = 2 and 0 for k > 2; for k < 2 it is unbounded, so "
        "x = 0 raises ValueError.",
        "Evaluated in log space with log-gamma. Relative error measured against 50-digit mpmath on "
        "more than 4000 random points per range of k with 1e-6 <= x <= 400: below 7e-14 for 0.1 <= "
        "k <= 30 (largest observed 5.3e-14) and below 2e-13 for 0.1 <= k <= 200 (largest observed "
        "1.5e-13; it grows with the size of the log terms); outside that range accuracy is not "
        "characterised. A finite input whose density exceeds the float range raises OverflowError.",
        "x is dimensionless (a sum of squared standard scores).",
    ),
    tags=(
        "chi-squared distribution",
        "chi-square",
        "probability density",
        "pdf",
        "degrees of freedom",
        "statistics",
    ),
)
