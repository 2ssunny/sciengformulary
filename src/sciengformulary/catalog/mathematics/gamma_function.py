"""Gamma Function: Gamma = integral_0^inf t^(x - 1) * exp(-t) dt."""

import math

from sciengformulary.catalog._sources import MATH_ACCESSED, mathlib, nist_statistics_handbook
from sciengformulary.catalog._domain import positive
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(x: float) -> float:
    positive("x", x)
    try:
        return math.gamma(x)
    except OverflowError as error:
        raise OverflowError(
            f"Gamma({x!r}) is outside the floating-point range (x above about 171.62, or x so "
            "close to 0 that 1/x overflows)."
        ) from error


gamma_function = FormulaSpec(
    id="mathematics.gamma_function",
    name="Gamma Function",
    equation="Gamma = integral_0^inf t^(x - 1) * exp(-t) dt",
    description=(
        "Euler's integral of the second kind for a positive real argument. It extends the "
        "factorial to real numbers: Gamma(n + 1) = n! for whole n >= 0."
    ),
    inputs=(
        VariableSpec(
            name="x",
            symbol="x",
            description="Argument, positive",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="Gamma",
        symbol="Gamma(x)",
        description="Gamma function value",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # States Real.Gamma s = integral over (0, inf) of exp(-x) x^(s - 1) for real s > 0;
        # here s -> x and the integration variable is t.
        mathlib(
            "Mathlib/Analysis/SpecialFunctions/Gamma/Basic.lean#L405",
            "theorem Real.Gamma_eq_integral",
        ),
        mathlib(
            "Mathlib/Analysis/SpecialFunctions/Gamma/Basic.lean#L422",
            "theorem Real.Gamma_nat_eq_factorial",
        ),
        nist_statistics_handbook(
            "eda/section3/eda366b.htm",
            "sec. 1.3.6.6.11, Gamma Distribution: gamma function",
            accessed=MATH_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"x": 1.0},
            expected=1.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Gamma(1) = 0! = 1; 50-digit mpmath and quadrature of Euler's integral.",
        ),
        VerificationCase(
            inputs={"x": 4.0},
            expected=6.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Gamma(4) = 3! = 6 (exact factorial); quadrature agrees.",
        ),
        VerificationCase(
            inputs={"x": 5.0},
            expected=24.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Gamma(5) = 4! = 24 (exact factorial); quadrature agrees.",
        ),
        VerificationCase(
            inputs={"x": 0.5},
            expected=1.772453850905516,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Gamma(1/2) = sqrt(pi); 50-digit mpmath and quadrature of Euler's integral.",
        ),
        VerificationCase(
            inputs={"x": 2.5},
            expected=1.329340388179137,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Gamma(5/2) = 3 sqrt(pi) / 4; 50-digit mpmath and quadrature agree.",
        ),
        VerificationCase(
            inputs={"x": 0.001},
            expected=999.4237724845955,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Close to the pole at 0; 50-digit mpmath at the float 0.001, quadrature agrees.",
        ),
        VerificationCase(
            inputs={"x": 100.0},
            expected=9.332621544394415e155,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Large argument: 99! as an exact integer, rounded once to float.",
        ),
    ),
    assumptions=(
        "Real x > 0 only, where Euler's integral converges; x <= 0 raises ValueError. The "
        "analytic continuation to negative non-integers is out of scope (and the poles at 0, "
        "-1, -2, ... are not given any value).",
        "Gamma(x + 1) = x Gamma(x), so Gamma(n + 1) = n! for whole n >= 0.",
        "Grows without bound as x -> 0+ (pole at 0); x above about 171.62, or x so small that "
        "Gamma(x) exceeds the float range, raises OverflowError.",
        "Computed with the standard library's math.gamma. Accuracy measured against 50-digit "
        "mpmath on 300 points with 1e-300 <= x <= 171.6: largest relative error 5.2e-16. "
        "Outside that range the accuracy is not characterised.",
    ),
    tags=(
        "gamma function",
        "Euler integral",
        "special function",
        "factorial",
    ),
)
