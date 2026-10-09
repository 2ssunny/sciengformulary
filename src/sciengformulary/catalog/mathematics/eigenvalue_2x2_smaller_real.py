"""Smaller Real Eigenvalue of a 2x2 Matrix.

lambda = ((a11 + a22) - sqrt((a11 - a22)^2 + 4*a12*a21)) / 2
"""

from sciengformulary.catalog._sources import mathlib, selinger_linear_algebra
from sciengformulary.catalog.mathematics._exact_roots import fraction_to_float
from sciengformulary.catalog.mathematics.eigenvalue_2x2_larger_real import _real_eigenvalues
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(a11: float, a12: float, a21: float, a22: float) -> float:
    return fraction_to_float(_real_eigenvalues(a11, a12, a21, a22)[1])


eigenvalue_2x2_smaller_real = FormulaSpec(
    id="mathematics.eigenvalue_2x2_smaller_real",
    name="Smaller Real Eigenvalue of a 2x2 Matrix",
    equation="lambda_smaller = ((a11 + a22) - sqrt((a11 - a22)^2 + 4*a12*a21)) / 2",
    description=(
        "The smaller of the two real eigenvalues of a real 2-by-2 matrix, obtained as a root of "
        "its characteristic polynomial lambda^2 - trace*lambda + determinant. It exists only when "
        "the eigenvalues are real, i.e. (a11 - a22)^2 + 4*a12*a21 >= 0."
    ),
    inputs=(
        VariableSpec(
            name="a11",
            symbol="a_{11}",
            description="Matrix entry in row 1, column 1",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="a12",
            symbol="a_{12}",
            description="Matrix entry in row 1, column 2",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="a21",
            symbol="a_{21}",
            description="Matrix entry in row 2, column 1",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="a22",
            symbol="a_{22}",
            description="Matrix entry in row 2, column 2",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="lambda_smaller",
        symbol=r"\lambda_{\mathrm{min}}",
        description="Smaller real eigenvalue of [[a11, a12], [a21, a22]]",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Selinger, theorem on eigenvalues: lambda is an eigenvalue of A exactly when
        # det(A - lambda*I) = 0; the worked example there has eigenvalues 2 and -3, and a second
        # example with no real eigenvalue (the evaluator raises ValueError for that case).
        # Step: with the 2x2 determinant below, det(A - lambda*I) = lambda^2 - t*lambda + d for
        # t = a11 + a22 and d = a11*a22 - a12*a21; the quadratic formula then gives the roots
        # (t +/- sqrt((a11 - a22)^2 + 4*a12*a21)) / 2.
        selinger_linear_algebra("sec. 8.2, thm:eigenvalues"),
        # Definition of the determinant of a 2x2 matrix, ad - bc.
        selinger_linear_algebra("sec. 7.1, Def. 7.1"),
        # Roots of a quadratic with a = 1, b = -t, c = d; the plus sign gives the larger root and
        # the minus sign the smaller one because a = 1 > 0.
        mathlib("Mathlib/Algebra/QuadraticDiscriminant.lean#L85", "theorem quadratic_eq_zero_iff"),
        # No root when the discriminant is not a square: a negative discriminant means no real
        # eigenvalue.
        mathlib(
            "Mathlib/Algebra/QuadraticDiscriminant.lean#L74",
            "theorem quadratic_ne_zero_of_discrim_ne_sq",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"a11": -5, "a12": 2, "a21": -7, "a22": 4},
            expected=-3.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Worked example of the source, characteristic polynomial lambda^2 + lambda - 6: "
                "the eigenvalues are 2 and -3 (smaller: -3); a 50-digit mpmath eigenvalue routine "
                "agrees."
            ),
        ),
        VerificationCase(
            inputs={"a11": 2, "a12": 1, "a21": 1, "a22": 2},
            expected=1.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Symmetric matrix with eigenvalues 3 and 1 (mpmath eigenvalue routine).",
        ),
        VerificationCase(
            inputs={"a11": 1.5, "a12": 0.5, "a21": 0.25, "a22": -1},
            expected=-1.049038105676658,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "(0.5 +/- sqrt(6.75)) / 2 from the trace 0.5 and determinant -1.625; mpmath "
                "eigenvalue routine at 50 digits, NumPy as a second check."
            ),
        ),
        VerificationCase(
            inputs={"a11": 2, "a12": 1, "a21": 0, "a22": 2},
            expected=2.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Jordan block: zero discriminant, repeated eigenvalue 2 for both variants.",
        ),
        VerificationCase(
            inputs={"a11": 100000000.0, "a12": 0, "a21": 0, "a22": 1e-08},
            expected=1e-08,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Diagonal matrix, so the eigenvalues are the entries 1e8 and 1e-8; the small "
                "eigenvalue is what a naive trace/discriminant form gets wrong, so this case "
                "guards the cancellation-free evaluation."
            ),
        ),
    ),
    assumptions=(
        "Real matrix entries; only real eigenvalues are returned. If (a11 - a22)^2 + 4*a12*a21 < "
        "0 the eigenvalues are a complex-conjugate pair and ValueError is raised. Symmetric "
        "matrices (a12 = a21) always qualify.",
        "The matrix is [[a11, a12], [a21, a22]]: a11 and a12 form the first row. A repeated "
        "eigenvalue is returned by both the larger and the smaller variant.",
        "Derived result: the source states that eigenvalues are the roots of det(A - lambda*I) "
        "but prints no trace/determinant closed form. Expanding the 2x2 determinant gives "
        "lambda^2 - (a11 + a22)*lambda + (a11*a22 - a12*a21), whose roots follow from the "
        "quadratic formula with discriminant (a11 - a22)^2 + 4*a12*a21. The expansion was checked "
        "symbolically with sympy and values were checked against 50-digit mpmath eigenvalues.",
        "The trace, determinant and discriminant are computed as exact fractions of the given "
        "floating-point entries, and the eigenvalue of smaller magnitude is obtained from the "
        "determinant divided by the other one, so nothing overflows, underflows or cancels on "
        "the way, whatever the ratio of the entries; only the square root of the discriminant "
        "(taken after scaling by an exact power of two) and the final conversion to float are "
        "rounded. Measured: relative error of the smaller eigenvalue below 2.5e-16 against "
        "900-digit mpmath on 8000 random matrices (entry magnitudes 1e-300 to 1e300, including "
        "triangular, strongly non-normal and nearly defective matrices, relative distance of the "
        "discriminant from zero down to about 1e-15); largest observed 2.0e-16. An eigenvalue in "
        "the subnormal range is correctly rounded to the subnormal grid.",
        "An eigenvalue outside the float range raises OverflowError, but only for the variant "
        "that returns it: the other eigenvalue is still returned when it is representable.",
    ),
    tags=(
        "eigenvalue",
        "2x2 matrix",
        "characteristic polynomial",
        "trace",
        "determinant",
        "linear algebra",
    ),
)
