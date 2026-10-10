"""Fibonacci Number (Binet's Formula): F = (phi^n - psi^n) / sqrt(5)."""

import math

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog.mathematics._domain import integer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

# phi**n overflows a double from n = 1475 on.
_MAX_N = 1474


def _evaluate(n: float) -> float:
    n = integer("n", n, minimum=0)
    if n > _MAX_N:
        raise ValueError(f"n must be at most {_MAX_N} (phi^n overflows a float), got {n!r}.")
    root5 = math.sqrt(5.0)
    phi = (1.0 + root5) / 2.0
    psi = (1.0 - root5) / 2.0
    return (phi**n - psi**n) / root5


fibonacci_binet = FormulaSpec(
    id="mathematics.fibonacci_binet",
    name="Fibonacci Number (Binet's Formula)",
    equation="F = (phi^n - psi^n) / sqrt(5), phi = (1 + sqrt(5)) / 2, psi = (1 - sqrt(5)) / 2",
    description=(
        "Closed form of the n-th Fibonacci number (F_0 = 0, F_1 = 1, every later term the sum "
        "of the previous two) through the golden ratio phi and its conjugate psi."
    ),
    inputs=(
        VariableSpec(
            name="n",
            symbol="n",
            description="Index of the Fibonacci number, integer from 0 to 1474",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="F",
        symbol="F_n",
        description="n-th Fibonacci number, as a float",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        mathlib("Mathlib/NumberTheory/Real/GoldenRatio.lean#L196", "theorem Real.coe_fib_eq"),
        # Fixes the indexing F_0 = 0, F_1 = 1.
        mathlib("Mathlib/Data/Nat/Fib/Basic.lean#L56", "def Nat.fib"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"n": 10},
            expected=55,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Exact integer recurrence F_0 = 0, F_1 = 1; a 60-digit mpmath Binet evaluation "
                "agrees to 1e-40."
            ),
        ),
        VerificationCase(
            inputs={"n": 30},
            expected=832040,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Exact integer recurrence; float Binet measured within about 1e-15 relative.",
        ),
        VerificationCase(
            inputs={"n": 70},
            expected=190392490709135,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Exact integer recurrence; the last index where the float result still rounds "
                "to the exact integer (measured relative error 2.3e-15)."
            ),
        ),
        VerificationCase(
            inputs={"n": 1},
            expected=1,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge n = 1: exact integer recurrence.",
        ),
        VerificationCase(
            inputs={"n": 0},
            expected=0,
            rel_tol=1e-12,
            abs_tol=1e-12,
            note="Edge n = 0: exact integer recurrence gives F_0 = 0.",
        ),
    ),
    assumptions=(
        "Whole-number index 0 <= n <= 1474 only; the cited relation is for natural n, and "
        "neither negative nor non-integer n is supported.",
        "Evaluated in floating point and returned unrounded: the relative error stays below "
        "about 5e-14 for every allowed n, but rounding gives the exact integer only up to n = "
        "70 (first failure at n = 71). Use an integer recurrence when an exact large F_n is "
        "needed.",
        "n > 1474 is rejected because phi^n overflows a double from n = 1475.",
    ),
    tags=("Fibonacci", "Binet formula", "golden ratio", "integer sequence", "number theory"),
)
