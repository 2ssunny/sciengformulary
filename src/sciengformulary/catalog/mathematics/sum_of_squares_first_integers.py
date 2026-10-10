"""Sum of the First n Squares: S = n * (n + 1) * (2*n + 1) / 6."""

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog._domain import integer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(n: float) -> int:
    n = integer("n", n, minimum=0)
    return n * (n + 1) * (2 * n + 1) // 6


sum_of_squares_first_integers = FormulaSpec(
    id="mathematics.sum_of_squares_first_integers",
    name="Sum of the First n Squares",
    equation="S = n * (n + 1) * (2*n + 1) / 6",
    description=(
        "Closed form of 1^2 + 2^2 + ... + n^2, the sum of the squares of the first n positive "
        "integers (the square pyramidal number)."
    ),
    inputs=(
        VariableSpec(
            name="n",
            symbol="n",
            description="Number of terms (largest integer squared)",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="S",
        symbol="S",
        description="Sum of k^2 for k = 1 .. n",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib (Faulhaber, sum starting at 1): sum_{k=1..n} k^p =
        # sum_{i=0..p} bernoulli'(i) * choose(p + 1, i) * n^(p + 1 - i) / (p + 1), with
        # bernoulli' 0, 1, 2 = 1, 1/2, 1/6 (the next reference). Step: p = 2 gives
        # (n^3 + (3/2) n^2 + (1/2) n) / 3 = n (n + 1) (2n + 1) / 6.
        mathlib("Mathlib/NumberTheory/Bernoulli.lean#L358", "theorem sum_Ico_pow"),
        # The three Bernoulli values used above; bernoulli'_one and bernoulli'_two are the
        # neighbouring theorems at lines 118 and 123 of the same file.
        mathlib("Mathlib/NumberTheory/Bernoulli.lean#L113", "theorem bernoulli'_zero"),
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
            note="Single term 1.",
        ),
        VerificationCase(
            inputs={"n": 3},
            expected=14.0,
            rel_tol=0.0,
            abs_tol=0.0,
            note="Term-by-term sum 1 + 4 + 9 = 14.",
        ),
        VerificationCase(
            inputs={"n": 10},
            expected=385.0,
            rel_tol=0.0,
            abs_tol=0.0,
            note="Term-by-term sum of the ten squares, 385.",
        ),
        VerificationCase(
            inputs={"n": 1000},
            expected=333833500.0,
            rel_tol=0.0,
            abs_tol=0.0,
            note="Term-by-term sum of one thousand squares, 333833500.",
        ),
        VerificationCase(
            inputs={"n": 100000},
            expected=333338333350000,
            rel_tol=0.0,
            abs_tol=0.0,
            note=(
                "Term-by-term integer sum of one hundred thousand squares, exactly 333338333350000."
            ),
        ),
    ),
    assumptions=(
        "n is a whole number, n >= 0 (integral floats such as 5.0 are accepted); n = 0 gives the "
        "empty sum 0. The sum starts at k = 1.",
        "The result is an exact Python integer for any size of n; there is no overflow.",
        "Derived result: Mathlib states the general power-sum formula; the closed form here is "
        "its p = 2 instance with the Bernoulli numbers substituted and the polynomial simplified. "
        "The expansion was checked symbolically with sympy, and the tests compare the closed form "
        "with the term-by-term sum for every n up to 200 and with the independent oracle values.",
    ),
    tags=(
        "sum of squares",
        "Faulhaber",
        "power sum",
        "series",
        "square pyramidal number",
    ),
)
