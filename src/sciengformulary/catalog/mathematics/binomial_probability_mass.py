"""Binomial Probability Mass: P = comb(n, k) * p^k * (1 - p)^(n - k)."""

import math
import sys

from sciengformulary.catalog._sources import MATH_ACCESSED, mathlib, nist_statistics_handbook
from sciengformulary.catalog._domain import integer, probability
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

LOG_FLOAT_MAX = math.log(sys.float_info.max)


def _evaluate(n: float, k: float, p: float) -> float:
    trials = integer("n", n, minimum=0)
    successes = integer("k", k)
    probability("p", p)
    if successes < 0 or successes > trials:
        return 0.0
    failures = trials - successes
    # 0^0 = 1: a certain outcome puts all of the mass on one count.
    if p == 0:
        return 1.0 if successes == 0 else 0.0
    if p == 1:
        return 1.0 if failures == 0 else 0.0
    log_coefficient = (
        math.lgamma(trials + 1) - math.lgamma(successes + 1) - math.lgamma(failures + 1)
    )
    log_failure_term = failures * math.log1p(-p)  # (1 - p)^(n - k) without forming 1 - p
    # Use the exact coefficient only when it fits a float comfortably (lgamma decides this
    # cheaply, before any big-integer work) and neither power underflows.
    if log_coefficient < LOG_FLOAT_MAX - 1:
        success_term = p**successes
        failure_term = math.exp(log_failure_term)
        if min(success_term, failure_term) >= sys.float_info.min:
            return math.comb(trials, successes) * success_term * failure_term
    # Otherwise work with logarithms throughout.
    return math.exp(log_coefficient + successes * math.log(p) + log_failure_term)


binomial_probability_mass = FormulaSpec(
    id="mathematics.binomial_probability_mass",
    name="Binomial Probability Mass",
    equation="P = comb(n, k) * p^k * (1 - p)^(n - k)",
    description=(
        "Chance of seeing exactly k successes in n independent trials when every trial "
        "succeeds with the same probability p."
    ),
    inputs=(
        VariableSpec(
            name="n",
            symbol="n",
            description="Number of independent trials (whole number, at least 0)",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="k",
            symbol="k",
            description="Number of successes (whole number)",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="p",
            symbol="p",
            description="Success probability of a single trial, in [0, 1]",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="P",
        symbol="P(k)",
        description="Probability of exactly k successes",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        mathlib(
            "Mathlib/Probability/Distributions/Binomial.lean#L83",
            "lemma ProbabilityTheory.binomial_real_singleton",
        ),
        nist_statistics_handbook(
            "eda/section3/eda366i.htm",
            "sec. 1.3.6.6.18, Binomial Distribution: probability mass function",
            accessed=MATH_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"n": 10, "k": 3, "p": 0.5},
            expected=0.1171875,
            rel_tol=1e-12,
            note=(
                "Exactly 15/128: 50-digit mpmath, exact Fraction arithmetic and enumeration of "
                "all 2^10 outcome sequences agree; scipy.stats.binom matches."
            ),
        ),
        VerificationCase(
            inputs={"n": 5, "k": 0, "p": 0.2},
            expected=0.32767999999999997,
            rel_tol=1e-12,
            note=(
                "No successes, (1 - p)^5 for the float 0.2; 50-digit mpmath and exact Fraction "
                "evaluation of the float input agree."
            ),
        ),
        VerificationCase(
            inputs={"n": 6, "k": 0, "p": 0.0},
            expected=1.0,
            rel_tol=1e-12,
            note="Boundary p = 0: every trial fails, so k = 0 is certain (0^0 = 1).",
        ),
        VerificationCase(
            inputs={"n": 3, "k": 5, "p": 0.4},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="More successes than trials: outside the support, comb(3, 5) = 0.",
        ),
        VerificationCase(
            inputs={"n": 1500, "k": 750, "p": 0.5},
            expected=0.02059785751247512,
            rel_tol=1e-9,
            note=(
                "Large n where comb(n, k) exceeds the float range; 50-digit mpmath and exact "
                "Fraction arithmetic agree. rel_tol 1e-9 leaves room for the log-gamma path, "
                "whose rounding error here is about 1e-12."
            ),
        ),
    ),
    assumptions=(
        "Trials are independent, their number n is fixed in advance, and every trial has the "
        "same success probability p.",
        "n must be a whole number >= 0, k a whole number and 0 <= p <= 1; anything else raises "
        "ValueError. Integral floats such as 3.0 are accepted as counts.",
        "Returns 0.0 for k < 0 or k > n, where the mass is genuinely zero.",
        "0^0 is taken as 1, so p = 0 puts all mass on k = 0 and p = 1 on k = n.",
        "When comb(n, k) does not fit in a float or a power underflows, the value is computed "
        "with log-gamma; its relative rounding error grows roughly like 1e-16 * n * ln(n) "
        "(about 1e-12 at n = 1500).",
    ),
    tags=(
        "binomial distribution",
        "probability mass function",
        "pmf",
        "Bernoulli trials",
        "statistics",
        "discrete distribution",
    ),
)
