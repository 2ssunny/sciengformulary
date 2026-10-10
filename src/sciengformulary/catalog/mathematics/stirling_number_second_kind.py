"""Stirling Number of the Second Kind:
S(n, k) = k * S(n - 1, k) + S(n - 1, k - 1) for n, k >= 1; S(0, 0) = 1; S(n, 0) = S(0, k) = 0.
"""

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog._domain import integer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(n: float, k: float) -> int:
    n = integer("n", n, minimum=0)
    k = integer("k", k, minimum=0)
    if k > n:
        return 0
    if k == 0:
        return 1 if n == 0 else 0
    # row[j] holds S(m, j) for the current m; update from the right so S(m - 1, j - 1) is
    # still the previous row's value when it is used.
    row = [1] + [0] * k
    for _ in range(n):
        for j in range(k, 0, -1):
            row[j] = j * row[j] + row[j - 1]
        row[0] = 0
    return row[k]


stirling_number_second_kind = FormulaSpec(
    id="mathematics.stirling_number_second_kind",
    name="Stirling Number of the Second Kind",
    equation=(
        "S(n, k) = k * S(n - 1, k) + S(n - 1, k - 1) for n, k >= 1; S(0, 0) = 1; "
        "S(n, 0) = S(0, k) = 0 for n, k >= 1"
    ),
    description=(
        "Stirling number of the second kind, defined by the recurrence above. It counts the "
        "ways to partition a set of n distinct elements into exactly k non-empty, unlabelled "
        "blocks."
    ),
    inputs=(
        VariableSpec(
            name="n",
            symbol="n",
            description="Number of distinct elements, integer",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="k",
            symbol="k",
            description="Number of non-empty blocks, integer",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="S",
        symbol="S(n, k)",
        description="Stirling number of the second kind",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib defines S(n + 1, k + 1) = (k + 1) S(n, k + 1) + S(n, k) with S(0, 0) = 1,
        # S(0, k + 1) = 0 and S(n + 1, 0) = 0. Replacing n + 1 by n and k + 1 by k (n, k >= 1)
        # gives the recurrence above.
        mathlib("Mathlib/Combinatorics/Enumerative/Stirling.lean#L117", "def Nat.stirlingSecond"),
        mathlib(
            "Mathlib/Combinatorics/Enumerative/Stirling.lean#L177",
            "theorem Nat.pow_eq_sum_stirlingSecond_mul_descFactorial",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"n": 5, "k": 2},
            expected=15,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Brute-force enumeration of the set partitions of 5 elements into 2 blocks.",
        ),
        VerificationCase(
            inputs={"n": 4, "k": 2},
            expected=7,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Brute-force enumeration of set partitions.",
        ),
        VerificationCase(
            inputs={"n": 10, "k": 4},
            expected=34105,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Exact-integer recurrence and the explicit inclusion-exclusion sum agree.",
        ),
        VerificationCase(
            inputs={"n": 0, "k": 0},
            expected=1,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge n = k = 0: the empty set has one partition, with no blocks.",
        ),
        VerificationCase(
            inputs={"n": 6, "k": 6},
            expected=1,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge k = n: only the partition into singletons.",
        ),
        VerificationCase(
            inputs={"n": 5, "k": 0},
            expected=0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge k = 0 < n: a non-empty set has no partition into 0 blocks.",
        ),
        VerificationCase(
            inputs={"n": 3, "k": 5},
            expected=0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge k > n: more non-empty blocks than elements is impossible.",
        ),
    ),
    assumptions=(
        "n and k are non-negative whole numbers. k > n, and k = 0 < n, give the genuine count "
        "0 rather than an error.",
        "Derived result: the cited definition is stated for S(n + 1, k + 1); the recurrence "
        "here is the same one with n + 1 replaced by n and k + 1 by k (an index shift). It was "
        "checked numerically against the explicit inclusion-exclusion sum for n, k <= 14 and "
        "against Mathlib's identity n^k = sum_j S(k, j) n (n - 1) ... (n - j + 1).",
        "The counting meaning (partitions into k unlabelled, non-empty blocks) was checked by "
        "brute-force enumeration for n <= 7; it is not what the cited Mathlib declarations "
        "formally prove (it appears only in their documentation).",
        "Summing S(n, k) over k gives the Bell number B(n).",
        "Computed exactly in integer arithmetic; the work grows roughly with n * k "
        "big-integer operations.",
    ),
    tags=(
        "Stirling numbers",
        "second kind",
        "set partitions",
        "combinatorics",
        "counting",
    ),
)
