"""Harmonic Number: H = sum_{i=1}^{n} 1 / i."""

import math

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog.mathematics._domain import integer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(n: float) -> float:
    n = integer("n", n, minimum=0)
    # fsum adds the rounded terms with a single final rounding.
    return math.fsum(1.0 / i for i in range(1, n + 1))


harmonic_number = FormulaSpec(
    id="mathematics.harmonic_number",
    name="Harmonic Number",
    equation="H = sum_{i=1}^{n} 1 / i",
    description=(
        "Sum of the reciprocals of the first n positive integers (the ordinary harmonic "
        "number, of order 1)."
    ),
    inputs=(
        VariableSpec(
            name="n",
            symbol="n",
            description="Number of terms, integer",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="H",
        symbol="H_n",
        description="n-th harmonic number",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib defines harmonic n as the sum over i in range n of 1 / (i + 1); writing the
        # summation index as i + 1 -> i gives the sum of 1 / i for i = 1..n.
        mathlib("Mathlib/NumberTheory/Harmonic/Defs.lean#L23", "def harmonic"),
        mathlib("Mathlib/NumberTheory/Harmonic/Defs.lean#L30", "lemma harmonic_succ"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"n": 0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Edge n = 0: empty sum 0.",
        ),
        VerificationCase(
            inputs={"n": 1},
            expected=1.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge n = 1: 1.",
        ),
        VerificationCase(
            inputs={"n": 4},
            expected=2.0833333333333335,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Exact Fraction sum 25/12, rounded once to float.",
        ),
        VerificationCase(
            inputs={"n": 5},
            expected=2.283333333333333,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Exact Fraction sum 137/60, rounded once to float.",
        ),
        VerificationCase(
            inputs={"n": 100},
            expected=5.187377517639621,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Exact Fraction sum of 100 terms, rounded once; mpmath harmonic(100) agrees.",
        ),
    ),
    assumptions=(
        "n is a non-negative whole number; H_0 = 0 (empty sum).",
        "Derived result: Mathlib sums 1 / (i + 1) over i = 0..n - 1; the form here only "
        "renumbers the summation index (i + 1 -> i). It was checked numerically against "
        "exact Fraction sums.",
        "The exact value is rational; this returns the float value. Each positive term is "
        "rounded once (relative error at most 1.1e-16) and math.fsum rounds the sum once, so "
        "the relative error is at most about 2.2e-16. The work grows linearly with n.",
    ),
    tags=(
        "harmonic number",
        "harmonic series",
        "partial sum",
        "number theory",
    ),
)
