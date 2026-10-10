"""Regularized Incomplete Beta Function:
I = (integral_0^z t^(a - 1) * (1 - t)^(b - 1) dt) / B(a, b),
B(a, b) = Gamma(a) * Gamma(b) / Gamma(a + b).
"""

import math

from sciengformulary.catalog._sources import MATH_ACCESSED, mathlib, nist_statistics_handbook
from sciengformulary.catalog.mathematics._domain import finite, positive
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

# Iteration cap for the continued fraction; reaching it raises ArithmeticError.
MAX_ITERATIONS = 10_000
_EPSILON = 1e-17
# Lentz guard against a zero denominator.
_TINY = 1e-300
# Largest excursion outside [0, 1] treated as rounding and clamped; a bigger one raises.
_ROUNDING_EXCURSION = 1e-9
# math.gamma overflows a float just above 171, so larger shapes go through log-gamma.
_DIRECT_GAMMA_LIMIT = 171.0


def _digamma_estimate(x: float) -> float:
    """Return psi(x) for x > 0 to a few significant digits (enough for a tiny correction)."""
    shift = 0.0
    while x < 6.0:
        shift -= 1.0 / x
        x += 1.0
    return shift + math.log(x) - 0.5 / x - 1.0 / (12.0 * x * x)


def _log_beta(a: float, b: float) -> float:
    """Return log B(a, b), from Gamma itself while it stays in range, else from log-gamma."""
    total = a + b
    # a + b is rounded in floating point; the exact remainder (two-sum) shifts log Gamma(a + b)
    # by about psi(a + b) * remainder, which matters once log Gamma is steep (large a + b).
    rounding = (a - (total - (total - a))) + (b - (total - a))
    correction = _digamma_estimate(total) * rounding
    if total < _DIRECT_GAMMA_LIMIT:
        try:
            value = math.gamma(a) * math.gamma(b) / math.gamma(total)
        except OverflowError:
            value = math.inf
        if 0.0 < value < math.inf:
            return math.log(value) - correction
    return math.lgamma(a) + math.lgamma(b) - math.lgamma(total) - correction


def _continued_fraction(z: float, a: float, b: float) -> float:
    """Return F with I_z(a, b) = z^a (1 - z)^b / (a B(a, b)) * F.

    F = 1 / (1 + d_1 / (1 + d_2 / (1 + ...))) with
    d_(2m+1) = -(a + m)(a + b + m) z / ((a + 2m)(a + 2m + 1)) and
    d_(2m) = m (b - m) z / ((a + 2m - 1)(a + 2m)), evaluated by the modified Lentz method.
    It converges quickly for z < (a + 1) / (a + b + 2).
    """
    c = 1.0
    d = 1.0 - (a + b) * z / (a + 1.0)
    if abs(d) < _TINY:
        d = _TINY
    d = 1.0 / d
    value = d
    for m in range(1, MAX_ITERATIONS + 1):
        two_m = 2.0 * m
        for coefficient in (
            m * (b - m) * z / ((a + two_m - 1.0) * (a + two_m)),
            -(a + m) * (a + b + m) * z / ((a + two_m) * (a + two_m + 1.0)),
        ):
            d = 1.0 + coefficient * d
            if abs(d) < _TINY:
                d = _TINY
            c = 1.0 + coefficient / c
            if abs(c) < _TINY:
                c = _TINY
            d = 1.0 / d
            delta = d * c
            value *= delta
        if abs(delta - 1.0) < _EPSILON:
            return value
    raise ArithmeticError(
        "incomplete beta continued fraction did not converge in "
        f"{MAX_ITERATIONS} terms (z={z!r}, a={a!r}, b={b!r})."
    )


def _evaluate(z: float, a: float, b: float) -> float:
    if not 0 <= finite("z", z) <= 1:
        raise ValueError(f"z must lie in [0, 1], got {z!r}.")
    positive("a", a)
    positive("b", b)
    if z == 0:
        return 0.0
    if z == 1:
        return 1.0
    # z^a (1 - z)^b / B(a, b) is symmetric in (z, a) <-> (1 - z, b), so one log-space prefactor
    # serves both branches.
    prefactor = math.exp(a * math.log(z) + b * math.log1p(-z) - _log_beta(a, b))
    if z < (a + 1.0) / (a + b + 2.0):
        value = prefactor * _continued_fraction(z, a, b) / a
    else:
        # Symmetry I_z(a, b) = 1 - I_(1-z)(b, a) keeps the continued fraction in its fast region.
        value = 1.0 - prefactor * _continued_fraction(1.0 - z, b, a) / b
    return _within_unit_interval(value, z, a, b)


def _within_unit_interval(value: float, z: float, a: float, b: float) -> float:
    """Return ``value`` clamped to [0, 1] if it lies within rounding of that interval.

    For extreme shapes the error of the log-space prefactor can push the result a little outside
    [0, 1]. An excursion of up to 1e-9 is rounding and is clamped; anything larger is not a
    probability and raises ArithmeticError instead of being returned.
    """
    if not -_ROUNDING_EXCURSION <= value <= 1.0 + _ROUNDING_EXCURSION:
        raise ArithmeticError(
            f"the regularized incomplete beta is not reliable here: the computed value {value!r} "
            f"lies outside [0, 1] (z={z!r}, a={a!r}, b={b!r})."
        )
    return min(max(value, 0.0), 1.0)


regularized_incomplete_beta = FormulaSpec(
    id="mathematics.regularized_incomplete_beta",
    name="Regularized Incomplete Beta Function",
    equation=(
        "I = (integral_0^z t^(a - 1) * (1 - t)^(b - 1) dt) / B(a, b), "
        "B(a, b) = Gamma(a) * Gamma(b) / Gamma(a + b)"
    ),
    description=(
        "Share of the complete beta integral accumulated between 0 and z. It equals the CDF of "
        "the standard beta distribution with shape parameters a and b."
    ),
    inputs=(
        VariableSpec(
            name="z",
            symbol="z",
            description="Upper integration limit, in [0, 1]",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="a",
            symbol="a",
            description="First shape parameter, positive",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="b",
            symbol="b",
            description="Second shape parameter, positive",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="I",
        symbol="I_z(a, b)",
        description="Regularized incomplete beta value, in [0, 1]",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The handbook writes the beta CDF as the incomplete beta function ratio I_x(p, q): the
        # integral from 0 to x of t^(p - 1) (1 - t)^(q - 1) divided by B(p, q). Here x -> z,
        # p -> a and q -> b.
        nist_statistics_handbook(
            "eda/section3/eda366h.htm",
            "sec. 1.3.6.6.17, Beta Distribution: cumulative distribution function",
            accessed=MATH_ACCESSED,
        ),
        # Normaliser B(a, b) as a ratio of Gamma values; stated for complex u, v with positive
        # real parts, so real a, b > 0 is a special case (as for mathematics.beta_function).
        mathlib(
            "Mathlib/Analysis/SpecialFunctions/Gamma/Beta.lean#L537",
            "lemma Complex.betaIntegral_eq_Gamma_mul_div",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"z": 0.3, "a": 1.0, "b": 1.0},
            expected=0.3,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="I_z(1, 1) = z (uniform CDF); 50-digit mpmath betainc and quadrature agree.",
        ),
        VerificationCase(
            inputs={"z": 0.5, "a": 2.0, "b": 2.0},
            expected=0.5,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Equal shapes at z = 1/2 give exactly 0.5 by symmetry; exact binomial sum.",
        ),
        VerificationCase(
            inputs={"z": 0.4, "a": 2.5, "b": 1.0},
            expected=0.10119288512538815,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="I_z(a, 1) = z^a; 50-digit mpmath and quadrature.",
        ),
        VerificationCase(
            inputs={"z": 0.25, "a": 1.0, "b": 3.0},
            expected=0.578125,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="I_z(1, b) = 1 - (1 - z)^b = 37/64 exactly.",
        ),
        VerificationCase(
            inputs={"z": 0.7, "a": 0.5, "b": 0.5},
            expected=0.6309898804344546,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Arcsine law (2/pi) asin(sqrt(z)), integrand singular at both ends; 50-digit "
                "mpmath and quadrature."
            ),
        ),
        VerificationCase(
            inputs={"z": 0.2, "a": 10.0, "b": 5.0},
            expected=4.604968960000002e-05,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Lower tail with larger shapes; exact binomial-sum identity and 50-digit mpmath.",
        ),
        VerificationCase(
            inputs={"z": 0.1, "a": 2.0, "b": 30.0},
            expected=0.8304353668991352,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "z above (a + 1)/(a + b + 2), where the symmetry branch is used; exact "
                "binomial-sum identity and 50-digit mpmath."
            ),
        ),
        VerificationCase(
            inputs={"z": 0.0, "a": 2.0, "b": 3.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Edge z = 0: empty integral, 0.",
        ),
        VerificationCase(
            inputs={"z": 1.0, "a": 2.0, "b": 3.0},
            expected=1.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge z = 1: the complete integral, ratio 1.",
        ),
    ),
    assumptions=(
        "0 <= z <= 1 and real a > 0, b > 0; other values raise ValueError. I_0 = 0 and I_1 = 1 "
        "exactly.",
        "Satisfies I_z(a, b) = 1 - I_(1-z)(b, a); with a = b = 1 it is the uniform CDF z.",
        "Computed from the continued fraction for the incomplete beta (modified Lentz) times "
        "z^a (1 - z)^b / (a B(a, b)) formed in log space, using the symmetry above whenever "
        "z >= (a + 1)/(a + b + 2). B(a, b) comes from Gamma directly for a + b < 171 and from "
        "log-gamma above that, with a first-order correction for the rounding of a + b. The "
        "loop raises ArithmeticError if it has not converged after 10000 steps.",
        "Accuracy measured against 50-digit mpmath on 500 points with 1e-8 <= z <= 1 - 1e-8 "
        "and 0.1 <= a, b <= 1000 (38 points whose value is below 1e-290 excluded): largest "
        "relative error 7.3e-14 when both shapes are at most 100, and 1.8e-12 with shapes up "
        "to 1000, where the log-gamma terms are large. Outside that range the accuracy is not "
        "characterised.",
        "Values below the smallest float underflow to 0.0; near 1 only the absolute error is "
        "small, so a tiny upper tail 1 - I cannot be read off this function.",
        "The result always lies in [0, 1]. For extreme shapes (outside the range above) rounding "
        "in the log-space prefactor can put the computed value slightly outside that interval; "
        "an excursion of up to 1e-9 is clamped to 0 or 1, and a larger one raises "
        "ArithmeticError rather than returning a value that is not a probability.",
    ),
    tags=(
        "incomplete beta function",
        "regularized incomplete beta",
        "beta distribution",
        "CDF",
        "special function",
    ),
)
