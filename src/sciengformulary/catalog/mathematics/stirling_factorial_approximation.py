"""Stirling's Approximation to n!: n! ~ sqrt(2 * pi * n) * (n / e)^n."""

import math

from sciengformulary.catalog._sources import nist_dlmf
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(n: float) -> float:
    return math.sqrt(2.0 * math.pi * n) * (n / math.e) ** n


stirling_factorial_approximation = FormulaSpec(
    id="mathematics.stirling_factorial_approximation",
    name="Stirling's Approximation to n!",
    equation="n! ~ sqrt(2 * pi * n) * (n / e)^n",
    description=(
        "Leading term of the asymptotic expansion of the factorial (gamma function) for large n."
    ),
    inputs=(
        VariableSpec(
            name="n",
            symbol="n",
            description="Argument of the factorial (positive real)",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="n_factorial",
        symbol="n!",
        description="Approximation to n! = Gamma(n + 1)",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Eq. (5.11.7) with a = 1, b = 1 gives Gamma(z + 1) ~ sqrt(2 pi) e^(-z) z^(z + 1/2), the
        # same expression with z = n.
        nist_dlmf("5.11", "sec. 5.11, eq. (5.11.7)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"n": 10.0},
            expected=3598695.618741036,
            rel_tol=1e-12,
            note=(
                "Independent 40-digit decimal evaluation of sqrt(20 pi) (10/e)^10 (exact 10! = "
                "3628800, about 0.8 % higher)."
            ),
        ),
        VerificationCase(
            inputs={"n": 1.0},
            expected=0.9221370088957891,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation of sqrt(2 pi) / e.",
        ),
    ),
    assumptions=(
        "Asymptotic: relative error is about 1/(12 n), so roughly 8 % at n = 1 and 0.8 % at n "
        "= 10. Use exact factorials or more terms when precision matters.",
        "Floating-point overflow above n of about 143.",
    ),
    tags=("Stirling", "factorial", "gamma function", "asymptotic", "combinatorics"),
)
