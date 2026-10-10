"""Binomial Coefficient: C = n! / (k! * (n - k)!)."""

import math

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog._domain import integer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(n: float, k: float) -> int:
    n = integer("n", n, minimum=0)
    k = integer("k", k, minimum=0)
    if k > n:
        raise ValueError(f"k must not exceed n, got n={n!r}, k={k!r}.")
    return math.comb(n, k)


binomial_coefficient = FormulaSpec(
    id="mathematics.binomial_coefficient",
    name="Binomial Coefficient",
    equation="C = n! / (k! * (n - k)!)",
    description=(
        "Count of the unordered selections of k items out of n distinct items, i.e. the number "
        "of k-element subsets of a set with n elements."
    ),
    inputs=(
        VariableSpec(
            name="n",
            symbol="n",
            description="Number of distinct items (set size), integer",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="k",
            symbol="k",
            description="Number of items chosen, integer",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="C",
        symbol="C(n, k)",
        description="Number of k-element subsets of an n-element set",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        mathlib(
            "Mathlib/Data/Nat/Choose/Basic.lean#L171",
            "theorem Nat.choose_eq_factorial_div_factorial",
        ),
        # Mathlib names the subset size n; here it is k, taken from a set of n items.
        mathlib("Mathlib/Data/Finset/Powerset.lean#L211", "theorem Finset.card_powersetCard"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"n": 5, "k": 2},
            expected=10,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Brute-force count of length-5 0/1 vectors with two ones; matches the exact "
                "integer ratio 5!/(2! 3!)."
            ),
        ),
        VerificationCase(
            inputs={"n": 52, "k": 5},
            expected=2598960,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Five-card hands: itertools.combinations enumeration over 52 items, equal to the "
                "exact integer ratio 52!/(5! 47!)."
            ),
        ),
        VerificationCase(
            inputs={"n": 10, "k": 0},
            expected=1,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge k = 0: brute-force enumeration finds only the empty subset.",
        ),
        VerificationCase(
            inputs={"n": 10, "k": 10},
            expected=1,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge k = n: brute-force enumeration finds only the full set.",
        ),
        VerificationCase(
            inputs={"n": 0, "k": 0},
            expected=1,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge n = 0: brute-force enumeration of the empty set gives one empty subset.",
        ),
    ),
    assumptions=(
        "n and k are whole numbers with 0 <= k <= n; k > n is rejected because the factorial "
        "form is undefined there (the subset count itself would be 0).",
        "Selection is unordered and without repetition.",
        "Computed exactly in integer arithmetic; the result is a Python int of any size.",
    ),
    tags=("binomial coefficient", "n choose k", "combinations", "nCr", "combinatorics", "counting"),
)
