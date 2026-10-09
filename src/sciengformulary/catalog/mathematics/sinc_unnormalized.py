"""Unnormalized Sinc Function: sinc = sin(x) / x for x != 0; sinc = 1 for x = 0."""

import math

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog._domain import finite
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(x: float) -> float:
    finite("x", x)
    if x == 0:
        return 1.0
    # For tiny x, math.sin(x) is x to full precision, so the ratio stays accurate.
    return math.sin(x) / x


sinc_unnormalized = FormulaSpec(
    id="mathematics.sinc_unnormalized",
    name="Unnormalized Sinc Function",
    equation="sinc = sin(x) / x for x != 0; sinc = 1 for x = 0",
    description=(
        "Ratio of sin(x) to x for an argument in radians, filled in with its limit 1 at the "
        "origin. It vanishes at every nonzero integer multiple of pi."
    ),
    inputs=(
        VariableSpec(
            name="x",
            symbol="x",
            description="Argument, in radians",
            dimension="1",
            si_unit="rad",
        ),
    ),
    output=VariableSpec(
        name="sinc",
        symbol="sinc(x)",
        description="Unnormalized sinc value, between -1 and 1",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        mathlib("Mathlib/Analysis/SpecialFunctions/Trigonometric/Sinc.lean#L40", "def Real.sinc"),
        # Continuity of sinc shows the value 1 at 0 is the limit of sin(x)/x, not an arbitrary
        # filler value.
        mathlib(
            "Mathlib/Analysis/SpecialFunctions/Trigonometric/Sinc.lean#L88",
            "lemma Real.continuous_sinc",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"x": 0.0},
            expected=1.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge x = 0: the defined value 1, the limit of sin(x)/x.",
        ),
        VerificationCase(
            inputs={"x": 1.5707963267948966},
            expected=0.6366197723675814,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Float pi/2: about 2/pi; 50-digit mpmath of sin(x)/x at the float input.",
        ),
        VerificationCase(
            inputs={"x": 3.141592653589793},
            expected=3.8981718325193755e-17,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note=(
                "Float pi is not exactly pi, so the value is about 3.9e-17 rather than 0; "
                "50-digit mpmath at the float input (abs_tol for the near-zero value)."
            ),
        ),
        VerificationCase(
            inputs={"x": -3.0},
            expected=0.04704000268662241,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Even function: sin(3)/3; 50-digit mpmath.",
        ),
        VerificationCase(
            inputs={"x": 1e-08},
            expected=1.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Tiny argument: 1 - x^2/6 rounds to 1.0; 50-digit mpmath.",
        ),
        VerificationCase(
            inputs={"x": 100.0},
            expected=-0.005063656411097588,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Large argument: sin(100)/100 with 50-digit mpmath.",
        ),
    ),
    assumptions=(
        "Unnormalized convention sin(x)/x with x in radians; the normalized signal-processing "
        "sinc, sin(pi x)/(pi x), is a different function.",
        "Real, finite x only; NaN and infinities raise ValueError. At x = 0 (including -0.0) "
        "the value is the continuous limit 1.",
        "Even function with |sinc(x)| <= 1.",
        "Computed as math.sin(x) / x. Accuracy measured against 50-digit mpmath on 300 points "
        "with 1e-300 <= |x| <= 1e6: largest relative error 1.5e-16. Near the zeros at "
        "multiples of pi only the absolute error is small, because a float input is never "
        "exactly a multiple of pi. Outside that range the accuracy is not characterised.",
    ),
    tags=(
        "sinc",
        "unnormalized sinc",
        "cardinal sine",
        "trigonometric",
        "special function",
    ),
)
