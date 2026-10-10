"""Determinant of a 3x3 Matrix: det = sum of six signed triple products (rule of Sarrus).

det = a11*a22*a33 + a12*a23*a31 + a13*a21*a32 - a31*a22*a13 - a32*a23*a11 - a33*a21*a12.
"""

from sciengformulary.catalog._sources import mathlib, selinger_linear_algebra
from sciengformulary.catalog.mathematics._domain import finite, finite_result
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

_NAMES = ("a11", "a12", "a13", "a21", "a22", "a23", "a31", "a32", "a33")


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
) -> float:
    entries = (a11, a12, a13, a21, a22, a23, a31, a32, a33)
    for name, value in zip(_NAMES, entries):
        finite(name, value)
    # Integer inputs stay exact until the final conversion.
    return finite_result(
        float(
            a11 * a22 * a33
            + a12 * a23 * a31
            + a13 * a21 * a32
            - a31 * a22 * a13
            - a32 * a23 * a11
            - a33 * a21 * a12
        )
    )


def _entry(row: int, column: int) -> VariableSpec:
    return VariableSpec(
        name=f"a{row}{column}",
        symbol=f"a_{{{row}{column}}}",
        description=f"Matrix entry in row {row}, column {column}",
        dimension="1",
        si_unit="-",
    )


determinant_3x3 = FormulaSpec(
    id="mathematics.determinant_3x3",
    name="Determinant of a 3x3 Matrix",
    equation=(
        "det = a11*a22*a33 + a12*a23*a31 + a13*a21*a32 - a31*a22*a13 - a32*a23*a11 - a33*a21*a12"
    ),
    description=(
        "Determinant of a real 3-by-3 matrix by the six-term expansion (rule of Sarrus), with "
        "the entries given row by row. The value is zero exactly when the matrix is singular."
    ),
    inputs=tuple(_entry(row, column) for row in (1, 2, 3) for column in (1, 2, 3)),
    output=VariableSpec(
        name="det",
        symbol=r"\det(A)",
        description="Determinant of the 3x3 matrix with entries a_ij",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        selinger_linear_algebra("sec. 7.1, Def. 7.3"),
        # Mathlib uses 0-based A i j and a different term order; with A i j -> a(i+1)(j+1)
        # the two six-term sums expand to the same polynomial.
        mathlib(
            "Mathlib/LinearAlgebra/Matrix/Determinant/Basic.lean#L820",
            "theorem Matrix.det_fin_three",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={
                "a11": 0,
                "a12": 1,
                "a13": 2,
                "a21": 3,
                "a22": 1,
                "a23": 0,
                "a31": 1,
                "a32": 1,
                "a33": -1,
            },
            expected=7.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Worked example in Selinger sec. 7.1 (Example 7.4), value 7; exact fraction "
                "arithmetic and a Leibniz permutation sum agree."
            ),
        ),
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
            },
            expected=4.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Coefficient determinant printed as 4 in the Cramer's rule example of Selinger "
                "sec. 7.7; confirmed exactly."
            ),
        ),
        VerificationCase(
            inputs={
                "a11": 0.5,
                "a12": -1.5,
                "a13": 2.25,
                "a21": 3.0,
                "a22": 0.75,
                "a23": -1.0,
                "a31": -2.5,
                "a32": 4.0,
                "a33": 1.5,
            },
            expected=36.78125,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Dyadic entries, so exact fraction arithmetic gives 1177/32; a Leibniz sum and "
                "numpy.linalg.det agree."
            ),
        ),
        VerificationCase(
            inputs={
                "a11": 1,
                "a12": 2,
                "a13": 3,
                "a21": 4,
                "a22": 5,
                "a23": 6,
                "a31": 7,
                "a32": 8,
                "a33": 9,
            },
            expected=0.0,
            rel_tol=0.0,
            abs_tol=1e-12,
            note="Rows form an arithmetic progression, so the matrix is singular: value 0.",
        ),
    ),
    assumptions=(
        "Entries are finite real numbers; aij is the entry in row i, column j.",
        "The six-term pattern holds only for 3x3 matrices and does not extend to larger ones.",
        "Integer entries are multiplied exactly; nearly singular floating-point matrices lose "
        "relative accuracy to cancellation between the six terms.",
    ),
    tags=("determinant", "3x3 matrix", "rule of Sarrus", "linear algebra", "matrix"),
)
