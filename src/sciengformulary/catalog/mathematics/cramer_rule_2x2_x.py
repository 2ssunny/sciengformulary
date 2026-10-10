"""Cramer's Rule for a 2x2 System (x): x = (b1 * a22 - a12 * b2) / (a11 * a22 - a12 * a21)."""

from sciengformulary.catalog._sources import mathlib, selinger_linear_algebra
from sciengformulary.catalog.mathematics._domain import finite, finite_result
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(a11: float, a12: float, a21: float, a22: float, b1: float, b2: float) -> float:
    values = (("a11", a11), ("a12", a12), ("a21", a21), ("a22", a22), ("b1", b1), ("b2", b2))
    for name, value in values:
        finite(name, value)
    det = a11 * a22 - a12 * a21
    if det == 0:
        raise ValueError(
            "The coefficient matrix is singular (a11*a22 - a12*a21 = 0), so the system has no "
            "unique solution and Cramer's rule does not apply."
        )
    return finite_result(float((b1 * a22 - a12 * b2) / det))


def _entry(row: int, column: int) -> VariableSpec:
    return VariableSpec(
        name=f"a{row}{column}",
        symbol=f"a_{{{row}{column}}}",
        description=f"Coefficient matrix entry in row {row}, column {column}",
        dimension="1",
        si_unit="-",
    )


def _rhs(row: int, equation: str) -> VariableSpec:
    return VariableSpec(
        name=f"b{row}",
        symbol=f"b_{row}",
        description=f"Right-hand side of equation {row}, {equation}",
        dimension="1",
        si_unit="-",
    )


cramer_rule_2x2_x = FormulaSpec(
    id="mathematics.cramer_rule_2x2_x",
    name="Cramer's Rule for a 2x2 System (x)",
    equation="x = (b1 * a22 - a12 * b2) / (a11 * a22 - a12 * a21)",
    description=(
        "First unknown x of the linear system a11*x + a12*y = b1, a21*x + a22*y = b2 by "
        "Cramer's rule: the determinant of the coefficient matrix with its first column "
        "replaced by (b1, b2), divided by the determinant of the coefficient matrix. "
        "Companion of cramer_rule_2x2_y."
    ),
    inputs=(
        _entry(1, 1),
        _entry(1, 2),
        _entry(2, 1),
        _entry(2, 2),
        _rhs(1, "a11*x + a12*y = b1"),
        _rhs(2, "a21*x + a22*y = b2"),
    ),
    output=VariableSpec(
        name="x",
        symbol="x",
        description="Unique solution component x of the 2x2 system",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Selinger states the n x n rule x_i = det(A_i) / det(A) for invertible A; with n = 2,
        # det(A_1) = b1*a22 - a12*b2 and det(A) = a11*a22 - a12*a21 (Def. 7.1).
        selinger_linear_algebra("sec. 7.7, Cramer's rule theorem (source label thm:cramers-rule)"),
        # Invertible if and only if det(A) != 0: the domain check in the evaluator.
        selinger_linear_algebra(
            "sec. 7.5, theorem: invertible iff determinant non-zero "
            "(source label thm:determinant-invertible)"
        ),
        # x = A^-1 b with the 2x2 adjugate inverse gives the same closed form.
        selinger_linear_algebra(
            "sec. 7.6, formula for the inverse of a 2x2 matrix (source label eqn:inverse-2-by-2)"
        ),
        # Mathlib states A *v cramer A b = det(A) * b with no invertibility hypothesis;
        # dividing by det(A) != 0 gives x_i = det(A_i) / det(A). Cited for the relation only.
        mathlib("Mathlib/LinearAlgebra/Matrix/Adjugate.lean#L283", "theorem Matrix.mulVec_cramer"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"a11": 2, "a12": 1, "a21": 1, "a22": 3, "b1": 5, "b2": 10},
            expected=1.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Exact fractions: 2x + y = 5, x + 3y = 10 solves to (x, y) = (1, 3) with zero "
                "residuals; numpy.linalg.solve agrees."
            ),
        ),
        VerificationCase(
            inputs={"a11": 1, "a12": 2, "a21": 3, "a22": 4, "b1": 5, "b2": 6},
            expected=-4.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Exact fractions with det = -2: (x, y) = (-4, 9/2), residuals zero; checks a "
                "negative determinant."
            ),
        ),
        VerificationCase(
            inputs={
                "a11": 1,
                "a12": 1,
                "a21": 1,
                "a22": 1.0000009536743164,
                "b1": 2,
                "b2": 2.0000009536743164,
            },
            expected=1.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Nearly singular but invertible: a22 = 1 + 2^-20 and b2 = 2 + 2^-20 are exact "
                "binary floats, det = 2^-20, exact solution (1, 1)."
            ),
        ),
        VerificationCase(
            inputs={"a11": 3, "a12": -1, "a21": 2, "a22": 5, "b1": 0, "b2": 0},
            expected=0.0,
            rel_tol=0.0,
            abs_tol=1e-12,
            note="Homogeneous system with det = 17: the only solution is (0, 0), by hand.",
        ),
    ),
    assumptions=(
        "Two linear equations in two unknowns with finite real coefficients.",
        "The coefficient determinant a11*a22 - a12*a21 must be non-zero; the solution then "
        "exists and is unique. An exactly zero determinant raises ValueError, because the "
        "system then has no solution or infinitely many.",
        "Only an exactly zero determinant is rejected: an ill-conditioned floating-point "
        "system returns a large, input-sensitive value.",
    ),
    tags=("Cramer's rule", "linear system", "2x2", "determinant", "simultaneous equations"),
)
