"""Quadratic Discriminant: D = b^2 - 4*a*c."""

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog._domain import finite, finite_result
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(a: float, b: float, c: float) -> float:
    if finite("a", a) == 0:
        raise ValueError(f"a must be non-zero for a quadratic, got {a!r}.")
    finite("b", b)
    finite("c", c)
    return finite_result(b * b - 4.0 * a * c)


quadratic_discriminant = FormulaSpec(
    id="mathematics.quadratic_discriminant",
    name="Quadratic Discriminant",
    equation="D = b^2 - 4*a*c",
    description=(
        "Discriminant of the real quadratic a*x^2 + b*x + c. Its sign tells whether the "
        "quadratic has two distinct real roots (D > 0), one repeated real root (D = 0) or no "
        "real roots (D < 0)."
    ),
    inputs=(
        VariableSpec(
            name="a",
            symbol="a",
            description="Coefficient of x^2 (non-zero)",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="b",
            symbol="b",
            description="Coefficient of x",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="c",
            symbol="c",
            description="Constant term",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="D",
        symbol="D",
        description="Discriminant b^2 - 4 a c",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        mathlib("Mathlib/Algebra/QuadraticDiscriminant.lean#L49", "def discrim"),
        # Mathlib's definition is total over any ring; the root theorem below assumes a != 0,
        # which is the hypothesis adopted here.
        mathlib("Mathlib/Algebra/QuadraticDiscriminant.lean#L85", "theorem quadratic_eq_zero_iff"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"a": 1, "b": -3, "c": 2},
            expected=1.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Exact rational arithmetic: (-3)^2 - 4*1*2 = 1; cross-checked as a^2 (r1 - r2)^2 "
                "from the roots 1 and 2."
            ),
        ),
        VerificationCase(
            inputs={"a": 1, "b": 2, "c": 1},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-12,
            note=(
                "Exact rational arithmetic: 4 - 4 = 0 (double root -1); cross-checked as "
                "(2 a r + b)^2 at the root."
            ),
        ),
        VerificationCase(
            inputs={"a": 1, "b": 0, "c": 1},
            expected=-4.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Exact rational arithmetic: 0 - 4 = -4 (x^2 + 1 has no real root); cross-checked "
                "by completing the square."
            ),
        ),
        VerificationCase(
            inputs={"a": 0.5, "b": 1.25, "c": -3},
            expected=7.5625,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Exact rational arithmetic: 25/16 + 6 = 121/16 = 7.5625; cross-checked by "
                "completing the square."
            ),
        ),
        VerificationCase(
            inputs={"a": -2, "b": 3, "c": 5},
            expected=49.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Exact rational arithmetic: 9 + 40 = 49; cross-checked as a^2 (r1 - r2)^2 from "
                "the roots 5/2 and -1."
            ),
        ),
    ),
    assumptions=(
        "Real quadratic a*x^2 + b*x + c with a != 0; a = 0 is rejected because the polynomial "
        "is then not quadratic.",
        "Coefficients are treated as pure numbers; with dimensional coefficients D carries the "
        "units of b^2.",
        "When b^2 is close to 4 a c the floating-point subtraction loses relative accuracy; "
        "this cancellation is inherent to the expression.",
    ),
    tags=("quadratic", "discriminant", "polynomial", "roots", "algebra"),
)
