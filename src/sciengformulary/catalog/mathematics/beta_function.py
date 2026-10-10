"""Beta Function: B = Gamma(a) * Gamma(b) / Gamma(a + b)."""

import math

from sciengformulary.catalog._sources import MATH_ACCESSED, mathlib, nist_statistics_handbook
from sciengformulary.catalog.mathematics._domain import positive
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

# math.gamma overflows a float just above 171, so larger arguments go through log-gamma.
_DIRECT_GAMMA_LIMIT = 171.0


def _evaluate(a: float, b: float) -> float:
    positive("a", a)
    positive("b", b)
    if a + b < _DIRECT_GAMMA_LIMIT:
        try:
            value = math.gamma(a) * math.gamma(b) / math.gamma(a + b)
        except OverflowError:
            value = math.inf
        if math.isfinite(value):
            return value
    # Gamma itself (or the product) left the float range: work with logarithms instead.
    return math.exp(math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b))


beta_function = FormulaSpec(
    id="mathematics.beta_function",
    name="Beta Function",
    equation="B = Gamma(a) * Gamma(b) / Gamma(a + b)",
    description=(
        "Euler beta function of two positive real arguments, expressed through the gamma "
        "function. It equals the integral of t^(a - 1) (1 - t)^(b - 1) for t from 0 to 1."
    ),
    inputs=(
        VariableSpec(
            name="a",
            symbol="a",
            description="First argument, positive",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="b",
            symbol="b",
            description="Second argument, positive",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="B",
        symbol="B(a, b)",
        description="Value of the beta function",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Stated for complex u, v with positive real parts; real a, b > 0 is a special case.
        mathlib(
            "Mathlib/Analysis/SpecialFunctions/Gamma/Beta.lean#L537",
            "lemma Complex.betaIntegral_eq_Gamma_mul_div",
        ),
        # The handbook defines B(a, b) by the integral over [0, 1] (supports the definition
        # and domain); the gamma-function ratio comes from the Mathlib lemma above.
        nist_statistics_handbook(
            "eda/section3/eda366h.htm",
            "sec. 1.3.6.6.17, Beta Distribution: beta function",
            accessed=MATH_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"a": 2.0, "b": 3.0},
            expected=0.08333333333333333,
            rel_tol=1e-12,
            note=(
                "1! 2! / 4! = 1/12; exact expansion of the defining integral also gives 1/12; "
                "scipy identical."
            ),
        ),
        VerificationCase(
            inputs={"a": 0.5, "b": 0.5},
            expected=3.141592653589793,
            rel_tol=1e-12,
            note="B(1/2, 1/2) = pi; mpmath to 45 digits, numerical quadrature agrees.",
        ),
        VerificationCase(
            inputs={"a": 1.5, "b": 2.5},
            expected=0.19634954084936207,
            rel_tol=1e-12,
            note="pi/16; 50-digit mpmath, scipy within 1.4e-16.",
        ),
        VerificationCase(
            inputs={"a": 0.001, "b": 1.0},
            expected=1000.0,
            rel_tol=1e-12,
            note="B(a, 1) = 1/a near the a -> 0 edge; 50-digit mpmath of the float 0.001.",
        ),
        VerificationCase(
            inputs={"a": 200.0, "b": 300.0},
            expected=1.6485491608664747e-147,
            rel_tol=1e-10,
            note=(
                "Arguments where Gamma overflows: exact 199! 299! / 499! (Fraction) and 50-digit "
                "mpmath agree. rel_tol 1e-10 leaves room for the log-gamma path."
            ),
        ),
    ),
    assumptions=(
        "Real a > 0 and b > 0 only, where the defining integral converges; other values raise "
        "ValueError. The complex extension and analytic continuation are out of scope.",
        "Symmetric, B(a, b) = B(b, a), and B(a, 1) = 1/a.",
        "For a + b of 171 or more, or when Gamma overflows, the value is computed with "
        "log-gamma (relative rounding error near 1e-16 times the size of the log-gamma terms). "
        "Results beyond the float range raise OverflowError; results below the smallest "
        "positive float underflow to 0.0.",
    ),
    tags=(
        "beta function",
        "Euler integral",
        "special function",
        "gamma function",
    ),
)
