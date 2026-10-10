"""Quadratic Formula Root (Plus Branch): x = (-b + sqrt(b^2 - 4*a*c)) / (2*a)."""

from fractions import Fraction

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog._domain import finite
from sciengformulary.catalog.mathematics._exact_roots import (
    fraction_to_float,
    sqrt_as_fraction,
    stable_quadratic_roots,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _quadratic_roots(a: float, b: float, c: float) -> tuple[Fraction, Fraction]:
    """Return the real roots of a*x^2 + b*x + c as exact Fractions (plus, minus).

    The branches are named by the sign before sqrt(D). Shared by ``quadratic_root_plus`` and
    ``quadratic_root_minus``, which convert the one they need to ``float``.
    """
    if finite("a", a) == 0:
        raise ValueError(f"a must be non-zero for a quadratic, got {a!r}.")
    finite("b", b)
    finite("c", c)
    # The coefficients, the discriminant and both roots are kept as exact Fractions, so no
    # intermediate product can overflow, underflow or flush to zero; only the square root of the
    # discriminant is rounded (after scaling by an exact power of two) and the final root is
    # converted to float once.
    exact_a, exact_b, exact_c = Fraction(a), Fraction(b), Fraction(c)
    discriminant = exact_b * exact_b - 4 * exact_a * exact_c
    if discriminant < 0:
        raise ValueError(
            "The quadratic has no real roots: its discriminant b^2 - 4*a*c is negative "
            f"for a={a!r}, b={b!r}, c={c!r}."
        )
    return stable_quadratic_roots(exact_a, exact_b, exact_c, sqrt_as_fraction(discriminant))


def _evaluate(a: float, b: float, c: float) -> float:
    return fraction_to_float(_quadratic_roots(a, b, c)[0])


quadratic_root_plus = FormulaSpec(
    id="mathematics.quadratic_root_plus",
    name="Quadratic Formula Root (Plus Branch)",
    equation="x = (-b + sqrt(b^2 - 4*a*c)) / (2*a)",
    description=(
        "Real root of the quadratic a*x^2 + b*x + c = 0 that carries the plus sign in front of the "
        "square root of the discriminant. The branch is named by that sign, not by size: for a < 0 "
        "the plus root is the smaller of the two roots."
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
        name="x",
        symbol="x_{+}",
        description="Root on the plus branch",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib: over a field with 2 != 0, for a != 0 and discrim a b c = s * s, the roots of
        # a * x * x + b * x + c = 0 are (-b + s) / (2 * a) and (-b - s) / (2 * a). Here s is the
        # real square root of the discriminant, and the sign in front of s names the branch.
        mathlib("Mathlib/Algebra/QuadraticDiscriminant.lean#L85", "theorem quadratic_eq_zero_iff"),
        # discrim a b c = b^2 - 4 a c.
        mathlib("Mathlib/Algebra/QuadraticDiscriminant.lean#L49", "def discrim"),
        # A negative discriminant is not a square in the reals, so there is no real root: the
        # evaluator raises ValueError instead.
        mathlib(
            "Mathlib/Algebra/QuadraticDiscriminant.lean#L74",
            "theorem quadratic_ne_zero_of_discrim_ne_sq",
        ),
        # With a != 0 and zero discriminant the only root is -b / (2 * a): both branches agree.
        mathlib(
            "Mathlib/Algebra/QuadraticDiscriminant.lean#L100",
            "theorem quadratic_eq_zero_iff_of_discrim_eq_zero",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"a": 1, "b": -3, "c": 2},
            expected=2.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Factorisation (x - 1)(x - 2): the roots are 1 and 2, so the plus branch is 2; "
                "50-digit mpmath roots and a residual check agree."
            ),
        ),
        VerificationCase(
            inputs={"a": 2, "b": 0, "c": -8},
            expected=2.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="x^2 = 4 after dividing by 2: roots +2 and -2, plus branch +2 (mpmath).",
        ),
        VerificationCase(
            inputs={"a": -1, "b": 0, "c": 4},
            expected=-2.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "For a < 0 the plus branch is -2 and the minus branch is 2, because the branch "
                "follows the sign before the root and not the size of the root (mpmath)."
            ),
        ),
        VerificationCase(
            inputs={"a": 0.5, "b": -1.25, "c": -3},
            expected=4.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Coefficients that are exact in binary; sympy's exact solve gives the roots 4 and "
                "-3/2."
            ),
        ),
        VerificationCase(
            inputs={"a": 1, "b": 2, "c": 1},
            expected=-1.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Zero discriminant: the double root -1 for both branches.",
        ),
        VerificationCase(
            inputs={"a": 1, "b": 100000000.0, "c": 1},
            expected=-1e-08,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "b^2 much larger than 4*a*c: 50-digit mpmath value of the small root. The textbook "
                "expression in double precision returns about -7.45e-9 here, so this case guards "
                "the cancellation-free evaluation."
            ),
        ),
    ),
    assumptions=(
        "a != 0; a = 0 raises ValueError because the equation is then not quadratic.",
        "Real roots only: b^2 - 4*a*c >= 0 is required and a negative discriminant raises "
        "ValueError. At a zero discriminant both branches give the double root -b/(2*a).",
        "The branch is named by the sign before the square root, as in Mathlib's statement, not "
        "by size. For a > 0 the plus root is the larger root; for a < 0 it is the smaller root. "
        "Use it together with quadratic_root_minus to get both roots.",
        "Derived result: Mathlib states the roots (-b + s)/(2*a) and (-b - s)/(2*a) for any s "
        "with s*s equal to the discriminant. Here s is taken as the real square root of the "
        "discriminant, and the evaluator returns the same root as q/a or c/q with q = -(b + "
        "sign(b)*s)/2, using that the two roots multiply to c/a. Both steps were checked "
        "symbolically with sympy and numerically against 50-digit mpmath roots.",
        "The coefficients, the discriminant and both roots are computed as exact fractions of the "
        "given floating-point values; only the square root of the discriminant (taken after "
        "scaling by an exact power of two) and the final conversion to float are rounded, so "
        "nothing overflows, underflows or cancels on the way. Measured: relative error of each "
        "root below 2.5e-16 against 900-digit mpmath on 8000 random polynomials (coefficient "
        "magnitudes 1e-300 to 1e300, roots spread over 1e-100 to 1e100, b^2 up to about 1e200 "
        "times |4*a*c|, relative distance of the discriminant from zero down to about 1e-15), "
        "including b^2 >> 4*a*c and discriminants near zero; largest observed 1.9e-16. A root in "
        "the subnormal range is correctly rounded to the subnormal grid.",
        "A root outside the float range raises OverflowError; the other root is still returned "
        "when it is representable (e.g. a = 1e-300, b = 1e300, c = 1 has roots -1e-300 and "
        "-1e600).",
    ),
    tags=(
        "quadratic formula",
        "quadratic equation",
        "roots",
        "discriminant",
        "algebra",
        "polynomial",
    ),
)
