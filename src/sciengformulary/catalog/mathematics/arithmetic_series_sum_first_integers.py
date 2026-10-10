"""Sum of the First n Positive Integers: S = n * (n + 1) / 2."""

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog._domain import integer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(n: float) -> int:
    n = integer("n", n, minimum=0)
    return n * (n + 1) // 2


arithmetic_series_sum_first_integers = FormulaSpec(
    id="mathematics.arithmetic_series_sum_first_integers",
    name="Sum of the First n Positive Integers",
    equation="S = n * (n + 1) / 2",
    description="Closed form of 1 + 2 + ... + n, the sum of the first n positive integers.",
    inputs=(
        VariableSpec(
            name="n",
            symbol="n",
            description="Number of terms (largest integer summed), integer",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="S",
        symbol="S",
        description="Sum 1 + 2 + ... + n",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib states (sum of i over range m, i.e. 0..m-1) * 2 = m * (m - 1). With m = n + 1
        # the sum is 0 + 1 + ... + n = 1 + ... + n and (n + 1) - 1 = n, so S = n (n + 1) / 2.
        mathlib(
            "Mathlib/Algebra/BigOperators/Intervals.lean#L172",
            "theorem Finset.sum_range_id_mul_two",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"n": 100},
            expected=5050,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Direct summation of 1..100 in exact integers.",
        ),
        VerificationCase(
            inputs={"n": 1000000},
            expected=500000500000,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Direct summation of 1..10^6 in exact integers.",
        ),
        VerificationCase(
            inputs={"n": 4},
            expected=10,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Direct summation 1 + 2 + 3 + 4.",
        ),
        VerificationCase(
            inputs={"n": 1},
            expected=1,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge n = 1: a single term.",
        ),
        VerificationCase(
            inputs={"n": 0},
            expected=0,
            rel_tol=1e-12,
            abs_tol=1e-12,
            note="Edge n = 0: the empty sum.",
        ),
    ),
    assumptions=(
        "n is a non-negative whole number; the sum runs over 1..n and n = 0 gives the empty sum 0.",
        "The cited source sums 0..m-1; this is the same statement with m = n + 1.",
        "Computed exactly in integer arithmetic; the result is a Python int of any size.",
    ),
    tags=("arithmetic series", "Gauss sum", "triangular number", "sum of integers", "series"),
)
