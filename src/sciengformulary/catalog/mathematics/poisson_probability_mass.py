"""Poisson Probability Mass: P = exp(-lam) * lam^k / k!."""

import math

from sciengformulary.catalog._sources import MATH_ACCESSED, mathlib, nist_statistics_handbook
from sciengformulary.catalog.mathematics._domain import integer, non_negative
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(lam: float, k: float) -> float:
    non_negative("lam", lam)
    count = integer("k", k)
    if count < 0:
        return 0.0
    # lam = 0: no events ever occur (0^0 = 1), and log(0) must be avoided.
    if lam == 0:
        return 1.0 if count == 0 else 0.0
    # Log space keeps lam^k, k! and exp(-lam) from overflowing or underflowing on their own.
    return math.exp(-lam + count * math.log(lam) - math.lgamma(count + 1))


poisson_probability_mass = FormulaSpec(
    id="mathematics.poisson_probability_mass",
    name="Poisson Probability Mass",
    equation="P = exp(-lam) * lam^k / k!",
    description=(
        "Chance of observing exactly k events when the event count follows a Poisson "
        "distribution with mean lam."
    ),
    inputs=(
        VariableSpec(
            name="lam",
            symbol=r"\lambda",
            description="Mean (expected) number of events in the interval, at least 0",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="k",
            symbol="k",
            description="Number of events observed (whole number)",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="P",
        symbol="P(k)",
        description="Probability of exactly k events",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        mathlib(
            "Mathlib/Probability/Distributions/Poisson/Basic.lean#L53",
            "lemma ProbabilityTheory.poissonMeasure_real_singleton",
        ),
        nist_statistics_handbook(
            "eda/section3/eda366j.htm",
            "sec. 1.3.6.6.19, Poisson Distribution: probability mass function",
            accessed=MATH_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"lam": 2.0, "k": 3},
            expected=0.18044704431548358,
            rel_tol=1e-12,
            note="(4/3) e^-2 from 50-digit mpmath; scipy.stats.poisson agrees to 1.5e-16.",
        ),
        VerificationCase(
            inputs={"lam": 1.0, "k": 0},
            expected=0.36787944117144233,
            rel_tol=1e-12,
            note="k = 0 gives e^-1; 50-digit mpmath, scipy identical.",
        ),
        VerificationCase(
            inputs={"lam": 0.0, "k": 0},
            expected=1.0,
            rel_tol=1e-12,
            note="Boundary lam = 0 (allowed by the Mathlib statement): all mass at k = 0.",
        ),
        VerificationCase(
            inputs={"lam": 1000.0, "k": 1000},
            expected=0.012614611348721499,
            rel_tol=1e-9,
            note=(
                "Large lam and k, where lam^k and k! overflow a float; 50-digit mpmath. "
                "rel_tol 1e-9 leaves room for log-space rounding (scipy is 1.1e-12 off)."
            ),
        ),
    ),
    assumptions=(
        "Events happen independently at a constant mean rate, so the count in the interval is "
        "Poisson distributed with mean lam.",
        "lam must be finite and >= 0 and k a whole number; anything else raises ValueError. "
        "Integral floats such as 3.0 are accepted as counts.",
        "Returns 0.0 for k < 0, where the mass is genuinely zero.",
        "lam = 0 is the no-event limit: P(0) = 1 and P(k) = 0 for k > 0 (0^0 = 1).",
        "Computed in log space with log-gamma; relative rounding error grows roughly like "
        "1e-16 * (lam + k * ln(lam)), about 1e-12 at lam = k = 1000.",
    ),
    tags=(
        "Poisson distribution",
        "probability mass function",
        "pmf",
        "counting process",
        "statistics",
        "discrete distribution",
    ),
)
