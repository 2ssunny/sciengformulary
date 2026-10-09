"""Gamma Function at Half-Integers: Gamma(k + 1/2) = (2*k)! / (4^k * k!) * sqrt(pi)."""

import math

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog.mathematics._domain import finite_result, integer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

# Gamma(172.5) is about 1.6e310, above the largest float; Gamma(171.5) is about 9.5e307.
_MAX_K = 171


def _evaluate(k: float) -> float:
    k = integer("k", k, minimum=0)
    if k > _MAX_K:
        raise OverflowError(
            f"Gamma({k} + 1/2) is outside the floating-point range (k above {_MAX_K})."
        )
    # (2k)! / (4^k k!) is an exact rational; int / int is correctly rounded.
    return finite_result(math.factorial(2 * k) / (4**k * math.factorial(k)) * math.sqrt(math.pi))


gamma_half_integer = FormulaSpec(
    id="mathematics.gamma_half_integer",
    name="Gamma Function at Half-Integers",
    equation="G = (2*k)! / (4^k * k!) * sqrt(pi)",
    description=(
        "Exact value of the gamma function at k + 1/2 for a non-negative integer k: a rational "
        "multiple of sqrt(pi). For k >= 1 it equals (2k - 1)!! * sqrt(pi) / 2^k."
    ),
    inputs=(
        VariableSpec(
            name="k",
            symbol="k",
            description="Non-negative integer; the argument of Gamma is k + 1/2",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="G",
        symbol=r"\Gamma(k + 1/2)",
        description="Gamma function at k + 1/2",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib: for natural k, Gamma(k + 1 + 1/2) = (2k + 1)!! * sqrt(pi) / 2^(k + 1) (no
        # natural subtraction). Step: for k >= 1 put k' = k - 1, so Gamma(k + 1/2) =
        # (2k - 1)!! sqrt(pi) / 2^k; with (2k)! = (2k)!! (2k - 1)!! and (2k)!! = 2^k k! this is
        # (2k)! sqrt(pi) / (4^k k!). The case k = 0 is the next reference.
        mathlib(
            "Mathlib/Analysis/SpecialFunctions/Gaussian/GaussianIntegral.lean#L329",
            "lemma Real.Gamma_nat_add_one_add_half",
        ),
        # Gamma(1/2) = sqrt(pi): the case k = 0 of the equation above.
        mathlib(
            "Mathlib/Analysis/SpecialFunctions/Gaussian/GaussianIntegral.lean#L306",
            "theorem Real.Gamma_one_half_eq",
        ),
        # (2n)!! = 2^n * n! and (n + 1)! = (n + 1)!! * n!!: used to turn the double factorial
        # into ordinary factorials.
        mathlib(
            "Mathlib/Data/Nat/Factorial/DoubleFactorial.lean#L60",
            "theorem Nat.doubleFactorial_two_mul",
        ),
        # The same value stated with natural subtraction, (2k - 1)!! at k = 0 being 0!! = 1;
        # not used as the primary statement because of that truncation at k = 0.
        mathlib(
            "Mathlib/Analysis/SpecialFunctions/Gaussian/GaussianIntegral.lean#L341",
            "lemma Real.Gamma_nat_add_half",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"k": 0},
            expected=1.772453850905516,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Gamma(1/2) = sqrt(pi); mpmath gamma at 50 digits.",
        ),
        VerificationCase(
            inputs={"k": 1},
            expected=0.886226925452758,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Gamma(3/2) = sqrt(pi) / 2 (mpmath).",
        ),
        VerificationCase(
            inputs={"k": 3},
            expected=3.3233509704478426,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Gamma(7/2) = 15 sqrt(pi) / 8 (mpmath).",
        ),
        VerificationCase(
            inputs={"k": 10},
            expected=1133278.3889487856,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="mpmath gamma(10.5) at 50 digits; SciPy's gamma as a second check.",
        ),
        VerificationCase(
            inputs={"k": 171},
            expected=9.4833675668248e307,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Largest k whose value fits a double (about 9.48e307); mpmath gamma(171.5).",
        ),
    ),
    assumptions=(
        "k is a whole number >= 0 (integral floats are accepted), otherwise ValueError is raised; "
        "negative half-integers are not covered.",
        "The argument of the gamma function is k + 1/2. For k >= 172 the value exceeds the "
        "largest float (about 1.8e308) and OverflowError is raised; k = 171 gives about 9.48e307.",
        "Derived result: Mathlib states Gamma(k + 1/2) with the double factorial (2k - 1)!!; the "
        "formula here rewrites it with ordinary factorials, (2k - 1)!! = (2k)! / (2^k k!). The "
        "rewrite was checked symbolically and the values against 50-digit mpmath gamma for "
        "several k including 171; the tests also compare with math.gamma and with the "
        "double-factorial form.",
        "The rational factor (2k)!/(4^k k!) is rounded once and multiplied by sqrt(pi) rounded to "
        "a float. Measured: relative error below 3e-16 against 60+ digit mpmath for every k from "
        "0 to 171.",
    ),
    tags=(
        "gamma function",
        "half-integer",
        "double factorial",
        "special functions",
        "sqrt(pi)",
    ),
)
