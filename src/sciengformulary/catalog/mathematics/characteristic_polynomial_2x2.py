"""Characteristic Polynomial of a 2x2 Matrix: p = (a11 - lam)*(a22 - lam) - a12*a21."""

from sciengformulary.catalog._sources import mathlib, selinger_linear_algebra
from sciengformulary.catalog.mathematics._domain import finite, finite_result
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(a11: float, a12: float, a21: float, a22: float, lam: float) -> float:
    values = (("a11", a11), ("a12", a12), ("a21", a21), ("a22", a22), ("lam", lam))
    for name, value in values:
        finite(name, value)
    # Integer inputs stay exact until the final conversion.
    return finite_result(float((a11 - lam) * (a22 - lam) - a12 * a21))


def _entry(row: int, column: int) -> VariableSpec:
    return VariableSpec(
        name=f"a{row}{column}",
        symbol=f"a_{{{row}{column}}}",
        description=f"Matrix entry in row {row}, column {column}",
        dimension="1",
        si_unit="-",
    )


characteristic_polynomial_2x2 = FormulaSpec(
    id="mathematics.characteristic_polynomial_2x2",
    name="Characteristic Polynomial of a 2x2 Matrix",
    equation="p = (a11 - lam)*(a22 - lam) - a12*a21",
    description=(
        "Value of the characteristic polynomial det(A - lam*I) of a real 2-by-2 matrix A at a "
        "given real scalar lam, with the entries given row by row. It is zero exactly when lam "
        "is a real eigenvalue of the matrix."
    ),
    inputs=(
        _entry(1, 1),
        _entry(1, 2),
        _entry(2, 1),
        _entry(2, 2),
        VariableSpec(
            name="lam",
            symbol=r"\lambda",
            description="Scalar at which the polynomial is evaluated",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="p",
        symbol=r"p(\lambda)",
        description="Characteristic polynomial value det(A - lam*I)",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Selinger defines the characteristic polynomial as p(lambda) = det(A - lambda I) for a
        # square matrix and works the 2x2 examples. The equation above is that definition with
        # the 2x2 determinant rule applied to A - lambda I (derived step, see assumptions).
        selinger_linear_algebra(
            "sec. 8.2, definition of the characteristic polynomial "
            "(source label def:characteristic-polynomial)"
        ),
        # Determinant of [[a, b], [c, d]] is a*d - b*c; the entries here are a -> a11 - lam,
        # b -> a12, c -> a21, d -> a22 - lam.
        selinger_linear_algebra(
            "sec. 7.1, Def. 7.1, 2x2 determinant (source label def:two-by-two-determinant)"
        ),
        # Mathlib states det A = A 0 0 * A 1 1 - A 0 1 * A 1 0 (0-based indices). Mathlib's
        # charpoly uses det(X*I - A); for a 2x2 matrix this equals det(A - X*I) because the
        # sign (-1)^2 is 1, so the two conventions give the same polynomial here.
        mathlib(
            "Mathlib/LinearAlgebra/Matrix/Determinant/Basic.lean#L809", "theorem Matrix.det_fin_two"
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"a11": -5, "a12": 2, "a21": -7, "a22": 4, "lam": 2},
            expected=0.0,
            rel_tol=0.0,
            abs_tol=1e-12,
            note=(
                "Selinger sec. 8.2 exa:finding-eigenvalues: lam = 2 is an eigenvalue, p = 0 "
                "(exact Fraction; Leibniz determinant and printed lambda^2 + lambda - 6 "
                "agree)."
            ),
        ),
        VerificationCase(
            inputs={"a11": -5, "a12": 2, "a21": -7, "a22": 4, "lam": -3},
            expected=0.0,
            rel_tol=0.0,
            abs_tol=1e-12,
            note="Same example, the other eigenvalue lam = -3: p = 0.",
        ),
        VerificationCase(
            inputs={"a11": -5, "a12": 2, "a21": -7, "a22": 4, "lam": 0},
            expected=-6.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=("lam = 0 gives det(A) = -20 + 14 = -6 (constant term of lambda^2 + lambda - 6)."),
        ),
        VerificationCase(
            inputs={"a11": -5, "a12": 2, "a21": -7, "a22": 4, "lam": 0.5},
            expected=-5.25,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Non-root: 0.25 + 0.5 - 6 = -5.25 exactly (Fraction); numpy det agrees.",
        ),
        VerificationCase(
            inputs={"a11": 0, "a12": -1, "a21": 1, "a22": 0, "lam": 1.5},
            expected=3.25,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Selinger exa:no-real-eigenvalue matrix [[0,-1],[1,0]]: p = lam^2 + 1 = 3.25.",
        ),
        VerificationCase(
            inputs={"a11": 3, "a12": 1.5, "a21": -0.25, "a22": 2, "lam": 2.75},
            expected=0.1875,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Decimal entries: exact Fraction value 3/16; numpy.polyval(numpy.poly(A)) agrees."
            ),
        ),
    ),
    assumptions=(
        "Real 2-by-2 matrix with entries given row by row; lam is a real number.",
        "Convention det(A - lam*I). For a 2x2 matrix it coincides with det(lam*I - A), so the "
        "sign convention does not change the value.",
        "Real roots of p are the real eigenvalues. When p has no real root the matrix has no "
        "real eigenvalue; complex eigenvalues are outside this formula.",
        "Derived result: the cited definition det(A - lam*I) is expanded with the 2x2 "
        "determinant rule applied to the matrix [[a11 - lam, a12], [a21, a22 - lam]]. The "
        "expansion was checked symbolically (sympy) and numerically against exact fractions.",
        "An intermediate or final value outside the floating-point range raises OverflowError.",
    ),
    tags=(
        "characteristic polynomial",
        "eigenvalue",
        "2x2 matrix",
        "determinant",
        "linear algebra",
    ),
)
