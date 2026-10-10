"""Upper Incomplete Gamma Function:
G = integral_x^inf t^(s - 1) * exp(-t) dt = Gamma(s) - integral_0^x t^(s - 1) * exp(-t) dt.
"""

import math

from sciengformulary.catalog._sources import MATH_ACCESSED, mathlib, nist_statistics_handbook
from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog.mathematics._incomplete_gamma import (
    exp_in_range,
    gamma_continued_fraction,
    gamma_in_range,
    gamma_series_sum,
    small_shape_upper_gamma,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

# For s < 1 the lower part is most of Gamma(s) once x is moderate, so subtracting it would lose
# digits; the continued fraction still converges there and is used from this x upwards. Below
# it (and for s < 1) the cancellation-free small-shape form of _incomplete_gamma is used.
_SMALL_S_CONTINUED_FRACTION_FROM = 0.25


def _evaluate(s: float, x: float) -> float:
    positive("s", s)
    non_negative("x", x)
    if x == 0:
        return finite_result(gamma_in_range(s))
    log_prefactor = s * math.log(x) - x
    if x >= s + 1.0 or (s < 1.0 and x >= _SMALL_S_CONTINUED_FRACTION_FROM):
        # Stable branch: the tail is computed directly from its continued fraction, so no two
        # nearly equal numbers are subtracted.
        return exp_in_range(log_prefactor + math.log(gamma_continued_fraction(s, x)))
    if s < 1.0:
        # x < 0.25: Gamma(s) is about 1/s while the tail is O(1), so Gamma(s) minus the lower
        # series would lose log10(1/s) digits; the rearranged form has no such subtraction.
        return finite_result(small_shape_upper_gamma(s, x))
    # Remaining region (s >= 1 and x < s + 1): Gamma(s, x) / Gamma(s) is at least 0.13 here, so
    # Gamma(s) minus the lower series loses at most one digit.
    lower = exp_in_range(log_prefactor + math.log(gamma_series_sum(s, x)))
    return finite_result(gamma_in_range(s) - lower)


upper_incomplete_gamma = FormulaSpec(
    id="mathematics.upper_incomplete_gamma",
    name="Upper Incomplete Gamma Function",
    equation=(
        "G = integral_x^inf t^(s - 1) * exp(-t) dt = Gamma(s) - integral_0^x t^(s - 1) * exp(-t) dt"
    ),
    description=(
        "Tail of Euler's gamma integral beyond x. Together with the lower incomplete gamma "
        "function it adds up to Gamma(s), and G / Gamma(s) is the survival function of the "
        "standard gamma distribution with shape s."
    ),
    inputs=(
        VariableSpec(
            name="s",
            symbol="s",
            description="Shape (order) parameter, positive",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="x",
            symbol="x",
            description="Lower integration limit, non-negative",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="G",
        symbol="Gamma(s, x)",
        description="Upper incomplete gamma value (not regularised)",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib states Gamma(s) = integral over (0, inf) of exp(-t) t^(s - 1) for real s > 0.
        # Splitting that convergent integral at x >= 0 gives integral_x^inf = Gamma(s) minus the
        # integral from 0 to x (partialGamma below); this additivity step is ours.
        mathlib(
            "Mathlib/Analysis/SpecialFunctions/Gamma/Basic.lean#L405",
            "theorem Real.Gamma_eq_integral",
        ),
        mathlib(
            "Mathlib/Analysis/SpecialFunctions/Gamma/Basic.lean#L146",
            "def Complex.partialGamma",
        ),
        # The handbook's gamma survival and hazard functions use Gamma(a) - Gamma_x(a), where
        # Gamma_x(a) is its lower incomplete gamma; that difference is G here (with a = s).
        nist_statistics_handbook(
            "eda/section3/eda366b.htm",
            "sec. 1.3.6.6.11, Gamma Distribution: hazard and survival functions",
            accessed=MATH_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"s": 1.0, "x": 2.0},
            expected=0.1353352832366127,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Closed form for s = 1: exp(-2); 50-digit mpmath tail quadrature agrees.",
        ),
        VerificationCase(
            inputs={"s": 2.0, "x": 1.0},
            expected=0.7357588823428847,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Closed form for s = 2: 2/e; 50-digit mpmath tail quadrature agrees.",
        ),
        VerificationCase(
            inputs={"s": 0.5, "x": 3.0},
            expected=0.025356509323463443,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Non-integer s; 50-digit mpmath quadrature of the tail integral.",
        ),
        VerificationCase(
            inputs={"s": 3.0, "x": 10.0},
            expected=0.005538791431023152,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Far tail, closed form for s = 3: (x^2 + 2x + 2) exp(-x); 50-digit mpmath.",
        ),
        VerificationCase(
            inputs={"s": 10.0, "x": 3.0},
            expected=362479.9291073437,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "x well below s, most of Gamma(10) = 362880; 50-digit mpmath tail quadrature "
                "and Gamma minus the lower integral agree."
            ),
        ),
        VerificationCase(
            inputs={"s": 2.5, "x": 0.0},
            expected=1.329340388179137,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge x = 0: the whole integral, Gamma(2.5) = 3 sqrt(pi) / 4; 50-digit mpmath.",
        ),
    ),
    assumptions=(
        "Derived result: G is obtained as Gamma(s) - gamma(s, x) by splitting Euler's "
        "convergent integral at x (additivity of the integral); the sources state Gamma(s) as "
        "the full integral and gamma(s, x) as the part from 0 to x. The step was checked "
        "numerically by 50-digit mpmath quadrature of the tail against the difference.",
        "Real s > 0 and real x >= 0 only; other values raise ValueError. G(s, 0) = Gamma(s) "
        "and G decreases to 0 as x grows. The extension to s <= 0 is out of scope.",
        "Not regularised: divide by Gamma(s) for the gamma-distribution survival function.",
        "For x >= s + 1, and for s < 1 with x >= 0.25, the tail is computed directly from a "
        "continued fraction (modified Lentz) with the factor x^s e^(-x) formed in log space, "
        "so nearly equal numbers are never subtracted. For s >= 1 and x < s + 1, where the tail "
        "is at least 13 percent of Gamma(s), it is Gamma(s) minus the lower power series. For "
        "s < 1 and x < 0.25 that subtraction would lose about log10(1/s) digits, so the tail is "
        "computed as (Gamma(1 + s) - 1)/s - expm1(s*ln(x))/s - x^s times a short power series in "
        "x, with Gamma(1 + s) - 1 taken from the zeta-value series of ln Gamma(1 + s) for "
        "s < 0.5; the two leading terms differ by at least about 0.8, so any s > 0 is handled "
        "(down to the smallest subnormal). Every loop raises ArithmeticError if it has not "
        "converged after 10000 terms, which is what very large s with x near s does.",
        "Accuracy measured against 60-digit mpmath on 2500 random points with 1e-300 <= s <= 170 "
        "and 1e-300 <= x <= 1000 (log-uniform, plus a denser sample of 0.001 <= s <= 170 and of "
        "1 <= s <= 170; points whose value is below 1e-290 or above 1e308 were excluded): "
        "largest relative error 1.2e-13, at s and x near 120 where s * log(x) - x is large; "
        "below 5e-16 in the small-shape branch (s < 1, x < 0.25). Outside that range the "
        "accuracy is not characterised.",
        "Results beyond the float range raise OverflowError (e.g. Gamma(s) for s above about "
        "171.6); far-tail results below the smallest float underflow towards 0.0.",
    ),
    tags=(
        "incomplete gamma function",
        "upper incomplete gamma",
        "special function",
        "survival function",
        "gamma distribution",
    ),
)
