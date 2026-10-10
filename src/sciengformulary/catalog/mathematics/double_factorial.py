"""Double Factorial: dfact = n * (n - 2) * (n - 4) * ... (last factor 2 or 1), dfact = 1 for n = 0
and n = 1.
"""

import math

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog.mathematics._domain import integer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(n: float) -> int:
    n = integer("n", n, minimum=0)
    # Empty product for n = 0 gives 1.
    return math.prod(range(n, 0, -2))


double_factorial = FormulaSpec(
    id="mathematics.double_factorial",
    name="Double Factorial",
    equation=(
        "dfact = n * (n - 2) * (n - 4) * ... (last factor 2 or 1), dfact = 1 for n = 0 and n = 1"
    ),
    description=(
        "Product of the positive integers up to n that have the same parity as n. For even "
        "n = 2m it equals 2^m m!."
    ),
    inputs=(
        VariableSpec(
            name="n",
            symbol="n",
            description="Argument, integer",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="dfact",
        symbol="n!!",
        description="Double factorial of n",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib defines 0!! = 1, 1!! = 1 and (k + 2)!! = (k + 2) * k!!. Unrolling this
        # recurrence gives the product n (n - 2) (n - 4) ... ending at 2 or 1.
        mathlib("Mathlib/Data/Nat/Factorial/DoubleFactorial.lean#L32", "def Nat.doubleFactorial"),
        mathlib(
            "Mathlib/Data/Nat/Factorial/DoubleFactorial.lean#L60",
            "theorem Nat.doubleFactorial_two_mul",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"n": 0},
            expected=1,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge n = 0: empty product 1 (Mathlib base case).",
        ),
        VerificationCase(
            inputs={"n": 1},
            expected=1,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge n = 1: 1 (Mathlib base case).",
        ),
        VerificationCase(
            inputs={"n": 5},
            expected=15,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Hand calculation: 5 * 3 * 1 = 15.",
        ),
        VerificationCase(
            inputs={"n": 6},
            expected=48,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Hand calculation: 6 * 4 * 2 = 48 = 2^3 * 3!.",
        ),
        VerificationCase(
            inputs={"n": 9},
            expected=945,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Hand calculation: 9 * 7 * 5 * 3 * 1 = 945.",
        ),
        VerificationCase(
            inputs={"n": 20},
            expected=3715891200,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Exact integers: 2^10 * 10! = 3715891200 (doubleFactorial_two_mul).",
        ),
    ),
    assumptions=(
        "Non-negative whole n only; the extension to negative odd integers ((-1)!! = 1, "
        "(-3)!! = -1, ...) is not supported and raises ValueError.",
        "Derived result: the cited definition is the recurrence (n + 2)!! = (n + 2) * n!! with "
        "0!! = 1!! = 1; the product form is that recurrence unrolled. It was checked "
        "numerically in exact integers against (2m)!! = 2^m m! and "
        "(n + 1)! = (n + 1)!! * n!!.",
        "n!! is not the same as (n!)!.",
        "Computed exactly in integer arithmetic; the result is a Python int of any size.",
    ),
    tags=(
        "double factorial",
        "semifactorial",
        "factorial",
        "combinatorics",
    ),
)
