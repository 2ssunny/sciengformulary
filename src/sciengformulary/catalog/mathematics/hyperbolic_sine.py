"""Hyperbolic Sine: sinh = (exp(x) - exp(-x)) / 2."""

import math

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog._domain import finite
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(x: float) -> float:
    finite("x", x)
    # math.sinh, not the literal difference of exponentials, which loses most digits near 0.
    try:
        return math.sinh(x)
    except OverflowError as error:
        raise OverflowError(
            f"sinh({x!r}) is outside the floating-point range (|x| above about 710.47)."
        ) from error


hyperbolic_sine = FormulaSpec(
    id="mathematics.hyperbolic_sine",
    name="Hyperbolic Sine",
    equation="sinh = (exp(x) - exp(-x)) / 2",
    description="Odd part of the exponential function, evaluated at a real argument.",
    inputs=(
        VariableSpec(
            name="x",
            symbol="x",
            description="Real argument",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="sinh",
        symbol="sinh(x)",
        description="Hyperbolic sine of x",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        mathlib("Mathlib/Analysis/Complex/Trigonometric.lean#L750", "theorem Real.sinh_eq"),
        mathlib("Mathlib/Analysis/Complex/Trigonometric.lean#L94", "def Real.sinh"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"x": 0.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Edge x = 0: exp(0) - exp(0) = 0.",
        ),
        VerificationCase(
            inputs={"x": 1.0},
            expected=1.1752011936438014,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="(e - 1/e) / 2 with 50-digit mpmath.",
        ),
        VerificationCase(
            inputs={"x": -2.5},
            expected=-6.0502044810397875,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Negative argument (odd function); 50-digit mpmath of the exponential form.",
        ),
        VerificationCase(
            inputs={"x": 1e-10},
            expected=1e-10,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Tiny argument, sinh(x) = x to double precision; 50-digit mpmath of the "
                "exponential form (the literal float difference would be off by 8e-8)."
            ),
        ),
        VerificationCase(
            inputs={"x": 20.0},
            expected=242582597.70489514,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Large argument, close to exp(20)/2; 50-digit mpmath of the exponential form.",
        ),
    ),
    assumptions=(
        "Real, finite x only; NaN and infinities raise ValueError.",
        "Odd function: sinh(-x) = -sinh(x), and sinh(0) = 0.",
        "Computed with the standard library's math.sinh rather than the literal difference of "
        "exponentials, which cancels near x = 0. Accuracy measured against 50-digit mpmath on "
        "300 points with 1e-300 <= |x| <= 710: largest relative error 1.2e-16. Outside "
        "that range the accuracy is not characterised.",
        "|x| above about 710.47 gives a result outside the float range and raises OverflowError.",
    ),
    tags=(
        "hyperbolic sine",
        "sinh",
        "hyperbolic functions",
        "exponential",
    ),
)
