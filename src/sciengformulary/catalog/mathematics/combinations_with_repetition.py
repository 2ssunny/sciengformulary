"""Combinations with Repetition (Multisets): M = (n + k - 1)! / (k! * (n - 1)!)."""

import math

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog.mathematics._domain import integer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(n: float, k: float) -> int:
    n = integer("n", n, minimum=1)
    k = integer("k", k, minimum=0)
    return math.comb(n + k - 1, k)


combinations_with_repetition = FormulaSpec(
    id="mathematics.combinations_with_repetition",
    name="Combinations with Repetition (Multisets)",
    equation="M = (n + k - 1)! / (k! * (n - 1)!)",
    description=(
        "Count of the unordered selections of k items from n types when a type may be picked "
        "more than once (size-k multisets over n types, 'stars and bars'); it equals the "
        "binomial coefficient C(n + k - 1, k)."
    ),
    inputs=(
        VariableSpec(
            name="n",
            symbol="n",
            description="Number of distinct types available, integer",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="k",
            symbol="k",
            description="Number of items selected (multiset size), integer",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="M",
        symbol="M(n, k)",
        description="Number of size-k multisets over n types",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib states multichoose n k = choose (n + k - 1) k. For n >= 1 the subtraction is
        # exact, and choose (n + k - 1) k = (n + k - 1)! / (k! (n - 1)!) by
        # Nat.choose_eq_factorial_div_factorial, since (n + k - 1) - k = n - 1.
        mathlib("Mathlib/Data/Nat/Choose/Basic.lean#L413", "theorem Nat.multichoose_eq"),
        # Counting meaning: size-k multisets over a type with n elements.
        mathlib("Mathlib/Data/Sym/Card.lean#L105", "theorem Sym.card_sym_eq_multichoose"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"n": 3, "k": 2},
            expected=6,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Brute-force count of nondecreasing length-2 tuples over 3 types (aa, ab, ac, "
                "bb, bc, cc); equals C(4, 2)."
            ),
        ),
        VerificationCase(
            inputs={"n": 5, "k": 3},
            expected=35,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Brute-force count of nondecreasing tuples; equals C(7, 3).",
        ),
        VerificationCase(
            inputs={"n": 10, "k": 4},
            expected=715,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Brute-force count of nondecreasing tuples; equals C(13, 4).",
        ),
        VerificationCase(
            inputs={"n": 1, "k": 7},
            expected=1,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge n = 1: brute force finds one multiset (every item of the single type).",
        ),
        VerificationCase(
            inputs={"n": 4, "k": 0},
            expected=1,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge k = 0: brute force finds only the empty multiset.",
        ),
    ),
    assumptions=(
        "n >= 1 and k >= 0 are whole numbers; k may exceed n. n = 0 is rejected because the "
        "closed form would need (-1)!.",
        "A type may be selected any number of times and the order of selection does not matter.",
        "Computed exactly in integer arithmetic; the result is a Python int of any size.",
    ),
    tags=(
        "combinations with repetition",
        "multiset coefficient",
        "multichoose",
        "stars and bars",
        "combinatorics",
        "counting",
    ),
)
