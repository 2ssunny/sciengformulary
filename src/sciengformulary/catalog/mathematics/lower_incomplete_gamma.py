"""Lower Incomplete Gamma Function: g = integral_0^x t^(s - 1) * exp(-t) dt."""

import math

from sciengformulary.catalog._sources import MATH_ACCESSED, mathlib, nist_statistics_handbook
from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog.mathematics._incomplete_gamma import (
    exp_in_range,
    gamma_continued_fraction,
    gamma_in_range,
    gamma_series_sum,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(s: float, x: float) -> float:
    positive("s", s)
    non_negative("x", x)
    if x == 0:
        return 0.0
    log_prefactor = s * math.log(x) - x
    if x < s + 1.0:
        # Series region: the sum is positive and the prefactor is taken in log space so that
        # x^s and e^(-x) cannot overflow or underflow on their own.
        return exp_in_range(log_prefactor + math.log(gamma_series_sum(s, x)))
    # Continued-fraction region: here the upper tail is at most about half of Gamma(s), so
    # Gamma(s) minus the tail does not lose digits to cancellation.
    upper = exp_in_range(log_prefactor + math.log(gamma_continued_fraction(s, x)))
    return finite_result(gamma_in_range(s) - upper)


lower_incomplete_gamma = FormulaSpec(
    id="mathematics.lower_incomplete_gamma",
    name="Lower Incomplete Gamma Function",
    equation="g = integral_0^x t^(s - 1) * exp(-t) dt",
    description=(
        "Euler's gamma integral cut off at the upper limit x. It rises from 0 at x = 0 towards "
        "Gamma(s) as x grows, and g / Gamma(s) is the CDF of the standard gamma distribution "
        "with shape s."
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
            description="Upper integration limit, non-negative",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="g",
        symbol="gamma(s, x)",
        description="Lower incomplete gamma value (not regularised)",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib defines partialGamma s X for complex s and real X as the interval integral
        # of exp(-x) x^(s - 1) from 0 to X; real s > 0 and X = x >= 0 is a special case of it.
        mathlib(
            "Mathlib/Analysis/SpecialFunctions/Gamma/Basic.lean#L146",
            "def Complex.partialGamma",
        ),
        mathlib(
            "Mathlib/Analysis/SpecialFunctions/Gamma/Basic.lean#L187",
            "theorem Complex.partialGamma_add_one",
        ),
        # The handbook writes this integral as Gamma_x(a) (its notation for the LOWER function)
        # and uses it, divided by Gamma(a), as the gamma CDF.
        nist_statistics_handbook(
            "eda/section3/eda366b.htm",
            "sec. 1.3.6.6.11, Gamma Distribution: incomplete gamma function",
            accessed=MATH_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"s": 1.0, "x": 2.0},
            expected=0.8646647167633873,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Closed form for s = 1: 1 - exp(-2); 50-digit mpmath gammainc and quadrature.",
        ),
        VerificationCase(
            inputs={"s": 2.0, "x": 1.0},
            expected=0.26424111765711533,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Closed form for s = 2: 1 - 2/e; 50-digit mpmath and quadrature agree.",
        ),
        VerificationCase(
            inputs={"s": 3.0, "x": 2.5},
            expected=0.9123737682333409,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Closed form for s = 3: 2 - (x^2 + 2x + 2) exp(-x); 50-digit mpmath.",
        ),
        VerificationCase(
            inputs={"s": 0.5, "x": 1.0},
            expected=1.493648265624854,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Non-integer s; 50-digit mpmath quadrature of the defining integral.",
        ),
        VerificationCase(
            inputs={"s": 0.1, "x": 0.01},
            expected=6.303852457878518,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Small s and x (integrable singularity at 0); 50-digit mpmath and quadrature.",
        ),
        VerificationCase(
            inputs={"s": 10.0, "x": 3.0},
            expected=400.07089265630526,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="x well below s (series region); 50-digit mpmath and quadrature.",
        ),
        VerificationCase(
            inputs={"s": 5.0, "x": 20.0},
            expected=23.99959332614568,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "x well above s (continued-fraction region), just under Gamma(5) = 24; "
                "50-digit mpmath and quadrature."
            ),
        ),
        VerificationCase(
            inputs={"s": 2.5, "x": 0.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Edge x = 0: integral over an empty interval is 0.",
        ),
    ),
    assumptions=(
        "Real s > 0 and real x >= 0 only; other values raise ValueError. g(s, 0) = 0 and g "
        "approaches Gamma(s) as x grows. The extension to s <= 0 or negative x is out of scope.",
        "Not regularised: divide by Gamma(s) for the gamma-distribution CDF. Notation varies; "
        "the NIST handbook writes this lower function as Gamma_x(a), while Gamma(s, x) usually "
        "means the upper function.",
        "Computed with the power series for x < s + 1 and, for x >= s + 1, as Gamma(s) minus "
        "the upper tail from a continued fraction (modified Lentz), with the factor x^s e^(-x) "
        "formed in log space. Either loop raises ArithmeticError if it has not converged "
        "after 10000 terms.",
        "Accuracy measured against 50-digit mpmath with 0.001 <= s <= 170 and 1e-6 <= x <= "
        "1000: relative error below 2e-13 (largest seen 1.51e-13 over 2500 points), worst at "
        "large s where s * log(x) - x is big; points whose value is below 1e-290 or above "
        "1e308 were excluded. Outside that range the accuracy is not characterised.",
        "Results beyond the float range raise OverflowError (e.g. s above about 171 in the "
        "continued-fraction region, where Gamma(s) itself overflows); results below the "
        "smallest float underflow towards 0.0.",
    ),
    tags=(
        "incomplete gamma function",
        "lower incomplete gamma",
        "partial gamma",
        "special function",
        "gamma distribution",
    ),
)
