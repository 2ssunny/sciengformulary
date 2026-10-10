"""Sum of Reciprocals of Triangular Numbers: S = 2*n / (n + 1)."""

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog._domain import integer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(n: float) -> float:
    n = integer("n", n, minimum=0)
    return 2 * n / (n + 1)


reciprocal_triangular_number_sum = FormulaSpec(
    id="mathematics.reciprocal_triangular_number_sum",
    name="Sum of Reciprocals of Triangular Numbers",
    equation="S = 2*n / (n + 1)",
    description=(
        "Sum of 1/T_k over the first n triangular numbers T_k = k*(k + 1)/2, k = 1 .. n. The sum "
        "telescopes to 2n/(n + 1) and approaches 2 as n grows."
    ),
    inputs=(
        VariableSpec(
            name="n",
            symbol="n",
            description="Number of triangular numbers summed (T_1 .. T_n)",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="S",
        symbol="S",
        description="Sum of 1/T_k for k = 1 .. n",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib: for natural N, sum_{k=0..N-1} 2 / (k * (k + 1)) = if N = 0 then 0 else
        # 2 - 2 / N, over the rationals. Steps: the k = 0 term is 2/0, which Lean's division sets
        # to 0, so the sum has N - 1 genuine terms; with N = n + 1 it reads
        # sum_{k=1..n} 2 / (k * (k + 1)) = 2 - 2 / (n + 1) = 2n / (n + 1), and
        # 2 / (k * (k + 1)) = 1 / T_k for the triangular number T_k = k * (k + 1) / 2.
        mathlib(
            "Archive/Wiedijk100Theorems/InverseTriangleSum.lean#L30",
            "theorem Theorems100.inverse_triangle_sum",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"n": 0},
            expected=0.0,
            rel_tol=0.0,
            abs_tol=0.0,
            note="Empty sum.",
        ),
        VerificationCase(
            inputs={"n": 1},
            expected=1.0,
            rel_tol=0.0,
            abs_tol=0.0,
            note="1 / T_1 = 1.",
        ),
        VerificationCase(
            inputs={"n": 3},
            expected=1.5,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="1 + 1/3 + 1/6 = 3/2 as an exact Fraction sum.",
        ),
        VerificationCase(
            inputs={"n": 99},
            expected=1.98,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Exact Fraction sum of 99 terms, 99/50.",
        ),
    ),
    assumptions=(
        "n is a whole number, n >= 0 (integral floats such as 5.0 are accepted); n = 0 gives the "
        "empty sum 0. Triangular numbers start at T_1 = 1, so T_0 = 0 is not part of the sum.",
        "The result 2n/(n+1) lies in [0, 2) and tends to 2 as n grows.",
        "Derived result: Mathlib's statement counts a k = 0 slot whose term is 0 by the "
        "convention x/0 = 0, so its N equals n + 1 here; dropping that slot (an index shift) and "
        "rewriting 2 - 2/(n+1) as 2n/(n+1) gives the equation above. The shift and the algebra "
        "were checked symbolically with sympy, and the tests compare the closed form with the "
        "exact Fraction sum of 1/T_k for every n up to 300.",
    ),
    tags=(
        "triangular numbers",
        "telescoping series",
        "reciprocal sum",
        "series",
    ),
)
