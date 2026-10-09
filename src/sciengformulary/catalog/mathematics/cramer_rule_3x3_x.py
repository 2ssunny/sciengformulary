"""Cramer's Rule for a 3x3 System (x): x = det(A_1) / det(A), A_1 = A with column 1 -> b."""

from sciengformulary.catalog._sources import mathlib, selinger_linear_algebra
from sciengformulary.catalog._domain import finite, finite_result
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

_NAMES = ("a11", "a12", "a13", "a21", "a22", "a23", "a31", "a32", "a33", "b1", "b2", "b3")


def _evaluate(
    a11: float,
    a12: float,
    a13: float,
    a21: float,
    a22: float,
    a23: float,
    a31: float,
    a32: float,
    a33: float,
    b1: float,
    b2: float,
    b3: float,
) -> float:
    values = (a11, a12, a13, a21, a22, a23, a31, a32, a33, b1, b2, b3)
    for name, value in zip(_NAMES, values):
        finite(name, value)
    # Both determinants are expanded along the first row, so the numerator is det(A) with
    # the first column replaced by b.
    det = (
        a11 * (a22 * a33 - a23 * a32)
        - a12 * (a21 * a33 - a23 * a31)
        + a13 * (a21 * a32 - a22 * a31)
    )
    if det == 0:
        raise ValueError(
            "The coefficient matrix is singular (determinant = 0), so the system has no unique "
            "solution and Cramer's rule does not apply."
        )
    numerator = (
        b1 * (a22 * a33 - a23 * a32) - a12 * (b2 * a33 - a23 * b3) + a13 * (b2 * a32 - a22 * b3)
    )
    # Integer inputs stay exact until the single division, which is correctly rounded.
    return finite_result(float(numerator / det))


def _entry(row: int, column: int) -> VariableSpec:
    return VariableSpec(
        name=f"a{row}{column}",
        symbol=f"a_{{{row}{column}}}",
        description=f"Coefficient matrix entry in row {row}, column {column}",
        dimension="1",
        si_unit="-",
    )


def _rhs(row: int) -> VariableSpec:
    return VariableSpec(
        name=f"b{row}",
        symbol=f"b_{row}",
        description=f"Right-hand side of equation {row}",
        dimension="1",
        si_unit="-",
    )


cramer_rule_3x3_x = FormulaSpec(
    id="mathematics.cramer_rule_3x3_x",
    name="Cramer's Rule for a 3x3 System (x)",
    equation=(
        "x = (b1*(a22*a33 - a23*a32) - a12*(b2*a33 - a23*b3) + a13*(b2*a32 - a22*b3)) / D, "
        "D = a11*(a22*a33 - a23*a32) - a12*(a21*a33 - a23*a31) + a13*(a21*a32 - a22*a31)"
    ),
    description=(
        "Unknown x of the 3-by-3 linear system a11*x + a12*y + a13*z = b1, "
        "a21*x + a22*y + a23*z = b2, a31*x + a32*y + a33*z = b3 by Cramer's rule: the "
        "determinant with column 1 replaced by (b1, b2, b3), divided by the determinant D of "
        "the coefficient matrix. Companion of cramer_rule_3x3_y and cramer_rule_3x3_z."
    ),
    inputs=(
        _entry(1, 1),
        _entry(1, 2),
        _entry(1, 3),
        _entry(2, 1),
        _entry(2, 2),
        _entry(2, 3),
        _entry(3, 1),
        _entry(3, 2),
        _entry(3, 3),
        _rhs(1),
        _rhs(2),
        _rhs(3),
    ),
    output=VariableSpec(
        name="x",
        symbol="x",
        description="Unique solution component x of the 3x3 system",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Selinger states the n x n rule x_i = det(A_i) / det(A) for invertible A, A_i being A
        # with column i replaced by b. Derived step: n = 3, i = 1, with det(A_1) and det(A)
        # written out by the 3x3 expansion (Def. 7.3); checked symbolically against a linear
        # solve.
        selinger_linear_algebra("sec. 7.7, Cramer's rule theorem (source label thm:cramers-rule)"),
        # Six-term expansion of a 3x3 determinant, used for D and for the numerator.
        selinger_linear_algebra("sec. 7.1, Def. 7.3"),
        # Invertible if and only if det(A) != 0: the domain check in the evaluator.
        selinger_linear_algebra(
            "sec. 7.5, theorem: invertible iff determinant non-zero "
            "(source label thm:determinant-invertible)"
        ),
        # Mathlib states A *v cramer A b = det(A) * b with no invertibility hypothesis;
        # dividing by det(A) != 0 gives x_i = det(A_i) / det(A). Cited for the relation only.
        mathlib("Mathlib/LinearAlgebra/Matrix/Adjugate.lean#L283", "theorem Matrix.mulVec_cramer"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={
                "a11": 1,
                "a12": 2,
                "a13": 1,
                "a21": 3,
                "a22": 2,
                "a23": 1,
                "a31": 1,
                "a32": 4,
                "a33": 1,
                "b1": 3,
                "b2": 5,
                "b3": 6,
            },
            expected=1.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Selinger sec. 7.7 worked example exa:cramers-rule: det A = 4, det A1 = 4, "
                "det A2 = 6, det A3 = -4, solution (1, 3/2, -1); exact Fractions, numpy "
                "agrees."
            ),
        ),
        VerificationCase(
            inputs={
                "a11": 2,
                "a12": 1,
                "a13": -1,
                "a21": -3,
                "a22": -1,
                "a23": 2,
                "a31": -2,
                "a32": 1,
                "a33": 2,
                "b1": 8,
                "b2": -11,
                "b3": -3,
            },
            expected=2.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Exact Fractions (Leibniz determinants), det = -1 (negative), solution (2, 3, "
                "-1) with zero residuals; numpy.linalg.solve agrees."
            ),
        ),
        VerificationCase(
            inputs={
                "a11": 0.5,
                "a12": 1,
                "a13": -1.5,
                "a21": 2,
                "a22": -0.25,
                "a23": 1,
                "a31": -1,
                "a32": 3,
                "a33": 2.5,
                "b1": 1,
                "b2": 2,
                "b3": 3,
            },
            expected=0.9581749049429658,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Decimal coefficients: exact rational solution (Fractions of the decimal "
                "literals) rounded to float; well conditioned, so binary rounding of the "
                "inputs is far below rel_tol; numpy agrees."
            ),
        ),
        VerificationCase(
            inputs={
                "a11": 3,
                "a12": -1,
                "a13": 2,
                "a21": 1,
                "a22": 4,
                "a23": -1,
                "a31": 2,
                "a32": 0,
                "a33": 5,
                "b1": 0,
                "b2": 0,
                "b3": 0,
            },
            expected=0.0,
            rel_tol=0.0,
            abs_tol=1e-12,
            note="Homogeneous system with non-zero determinant: only the zero solution.",
        ),
    ),
    assumptions=(
        "Three linear equations in three unknowns with finite real coefficients.",
        "The coefficient determinant D must be non-zero; the solution then exists and is "
        "unique. A computed determinant of exactly zero raises ValueError, because the system "
        "then has no solution or infinitely many.",
        "Only an exactly zero determinant is rejected: an ill-conditioned floating-point "
        "system returns a large, input-sensitive value. For integer inputs D is exact.",
        "Derived result: the source's general n x n theorem is specialised to n = 3 and "
        "unknown 1, with both determinants expanded along the first row. The expansion was "
        "checked symbolically against a linear solve and numerically against exact fractions.",
        "A result outside the floating-point range raises OverflowError.",
    ),
    tags=("Cramer's rule", "linear system", "3x3", "determinant", "simultaneous equations"),
)
