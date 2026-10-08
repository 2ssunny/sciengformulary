"""Geometric Probability Mass (Failures Before First Success): P = (1 - p)^k * p."""

import math

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog.mathematics._domain import integer, probability
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(p: float, k: float) -> float:
    if probability("p", p) == 0:
        raise ValueError("p must be greater than 0: with p = 0 no success ever occurs.")
    failures = integer("k", k)
    if failures < 0:
        return 0.0
    if p == 1:
        return 1.0 if failures == 0 else 0.0
    # (1 - p)^k as exp(k * log1p(-p)): forming 1 - p first would lose the digits of a tiny p.
    # The result is at most 1, so it can only underflow (to 0.0), never overflow.
    return math.exp(failures * math.log1p(-p)) * p


geometric_probability_mass_failures = FormulaSpec(
    id="mathematics.geometric_probability_mass_failures",
    name="Geometric Probability Mass (Failures Before First Success)",
    equation="P = (1 - p)^k * p",
    description=(
        "Chance that exactly k failures happen before the first success in a run of "
        "independent trials with success probability p. The support starts at k = 0; this is "
        "not the trials-until-success convention, whose support starts at 1."
    ),
    inputs=(
        VariableSpec(
            name="p",
            symbol="p",
            description="Success probability of a single trial, in (0, 1]",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="k",
            symbol="k",
            description="Number of failures before the first success (whole number)",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="P",
        symbol="P(k)",
        description="Probability of exactly k failures before the first success",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The module docstring of the same file states that the count is the number of
        # failures before the first success; the lemma gives the singleton mass.
        mathlib(
            "Mathlib/Probability/Distributions/Geometric.lean#L75",
            "lemma ProbabilityTheory.geometricMeasure_real_singleton",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"p": 0.5, "k": 0},
            expected=0.5,
            rel_tol=1e-12,
            note="First trial succeeds (k = 0): the mass equals p; exact.",
        ),
        VerificationCase(
            inputs={"p": 0.2, "k": 3},
            expected=0.1024,
            rel_tol=1e-12,
            note=(
                "0.8^3 * 0.2 by hand; 50-digit mpmath and enumeration of Bernoulli sequences "
                "agree; scipy nbinom(1, p).pmf(3) and geom.pmf(4) (shifted) match."
            ),
        ),
        VerificationCase(
            inputs={"p": 1.0, "k": 3},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Boundary p = 1: a failure is impossible, so three failures have mass 0.",
        ),
    ),
    assumptions=(
        "Trials are independent and share the same success probability p.",
        "k counts failures before the first success (k = 0 means the first trial succeeds); "
        "the number of trials up to and including the first success is k + 1.",
        "0 < p <= 1 and k a whole number; p = 0, values outside [0, 1] and non-integral k "
        "raise ValueError. Integral floats such as 3.0 are accepted as counts.",
        "Returns 0.0 for k < 0, where the mass is genuinely zero. p = 1 gives P(0) = 1 and "
        "P(k) = 0 for k > 0.",
        "For very large k the value underflows smoothly to 0.0.",
    ),
    tags=(
        "geometric distribution",
        "probability mass function",
        "pmf",
        "failures before first success",
        "waiting time",
        "discrete distribution",
    ),
)
