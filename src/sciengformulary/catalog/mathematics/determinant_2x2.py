"""Determinant of a 2x2 Matrix: det = a11 * a22 - a12 * a21."""

from sciengformulary.catalog._sources import mathlib, selinger_linear_algebra
from sciengformulary.catalog._domain import finite, finite_result
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(a11: float, a12: float, a21: float, a22: float) -> float:
    for name, value in (("a11", a11), ("a12", a12), ("a21", a21), ("a22", a22)):
        finite(name, value)
    # Integer inputs stay exact until the final conversion.
    return finite_result(float(a11 * a22 - a12 * a21))


def _entry(row: int, column: int) -> VariableSpec:
    return VariableSpec(
        name=f"a{row}{column}",
        symbol=f"a_{{{row}{column}}}",
        description=f"Matrix entry in row {row}, column {column}",
        dimension="1",
        si_unit="-",
    )


determinant_2x2 = FormulaSpec(
    id="mathematics.determinant_2x2",
    name="Determinant of a 2x2 Matrix",
    equation="det = a11 * a22 - a12 * a21",
    description=(
        "Determinant of a real 2-by-2 matrix whose entries are given one by one, row index "
        "first. The value is zero exactly when the matrix is singular (not invertible)."
    ),
    inputs=(_entry(1, 1), _entry(1, 2), _entry(2, 1), _entry(2, 2)),
    output=VariableSpec(
        name="det",
        symbol=r"\det(A)",
        description="Determinant of the matrix [[a11, a12], [a21, a22]]",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Selinger writes the rows as (a, b), (c, d); renamed here to a11, a12, a21, a22.
        selinger_linear_algebra("sec. 7.1, Def. 7.1"),
        # Mathlib states det !![a, b; c, d] = a * d - b * c over any commutative ring.
        mathlib(
            "Mathlib/LinearAlgebra/Matrix/Determinant/Basic.lean#L816",
            "theorem Matrix.det_fin_two_of",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"a11": 2, "a12": 4, "a21": -1, "a22": 6},
            expected=16.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Worked example in Selinger sec. 7.1 (Example 7.2), value 16; confirmed with "
                "exact fraction arithmetic."
            ),
        ),
        VerificationCase(
            inputs={"a11": 1.1, "a12": 2.3, "a21": 3.7, "a22": 4.9},
            expected=-3.12,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Exact decimal arithmetic gives 1.1*4.9 - 2.3*3.7 = -78/25; a Leibniz "
                "permutation sum and numpy.linalg.det agree."
            ),
        ),
        VerificationCase(
            inputs={"a11": 1, "a12": 2, "a21": 2, "a22": 4},
            expected=0.0,
            rel_tol=0.0,
            abs_tol=1e-12,
            note="Second row is twice the first, so the matrix is singular: hand value 0.",
        ),
    ),
    assumptions=(
        "Entries are finite real numbers; a11 and a12 make up the first row.",
        "Entries carrying units give a result in the product of a row-1 and a row-2 unit; "
        "the variables are listed as dimensionless here.",
        "Nearly singular floating-point matrices lose relative accuracy to cancellation in "
        "the subtraction; integer entries are multiplied exactly.",
    ),
    tags=("determinant", "2x2 matrix", "linear algebra", "matrix", "singular matrix"),
)
