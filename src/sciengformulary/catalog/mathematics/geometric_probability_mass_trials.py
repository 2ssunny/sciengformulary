"""Geometric Probability Mass (Trials Until First Success): P = p * (1 - p)^(k - 1)."""

import math

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog._domain import integer, probability
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(p: float, k: float) -> float:
    if probability("p", p) == 0:
        raise ValueError("p must be greater than 0: with p = 0 no success ever occurs.")
    trial = integer("k", k)
    if trial < 1:
        return 0.0
    if p == 1:
        return 1.0 if trial == 1 else 0.0
    # (1 - p)^(k - 1) as exp((k - 1) * log1p(-p)): forming 1 - p first would lose the digits
    # of a tiny p. The result is at most 1, so it can only underflow (to 0.0), never overflow.
    return math.exp((trial - 1) * math.log1p(-p)) * p


geometric_probability_mass_trials = FormulaSpec(
    id="mathematics.geometric_probability_mass_trials",
    name="Geometric Probability Mass (Trials Until First Success)",
    equation="P = p * (1 - p)^(k - 1) for integer k >= 1; P = 0 for k < 1",
    description=(
        "Chance that the first success in a run of independent trials, each succeeding with "
        "probability p, happens on trial number k, counting that successful trial. The support "
        "starts at k = 1; this is not the failures-before-success convention, whose support "
        "starts at 0."
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
            description="Index of the trial on which the first success occurs (whole number)",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="P",
        symbol="P(k)",
        description="Probability that the first success occurs on trial k",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Derived by an index shift. Mathlib states the mass (1 - p)^n * p for n = the number
        # of failures before the first success (n >= 0; module docstring of the same file).
        # The trial of the first success is k = n + 1, so P(k) = (1 - p)^(k - 1) * p for k >= 1.
        mathlib(
            "Mathlib/Probability/Distributions/Geometric.lean#L75",
            "lemma ProbabilityTheory.geometricMeasure_real_singleton",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"p": 0.5, "k": 3},
            expected=0.125,
            rel_tol=1e-12,
            note="Exact 1/8 by hand; enumeration of length-3 outcome strings agrees; scipy geom.",
        ),
        VerificationCase(
            inputs={"p": 0.2, "k": 2},
            expected=0.16,
            rel_tol=1e-12,
            note=(
                "0.8 * 0.2 as an exact Fraction of the float inputs, rounded; enumeration and "
                "scipy geom agree to 2e-16."
            ),
        ),
        VerificationCase(
            inputs={"p": 0.35, "k": 6},
            expected=0.040610171875000003,
            rel_tol=1e-12,
            note="0.65^5 * 0.35 as an exact Fraction; enumeration agrees; scipy geom identical.",
        ),
        VerificationCase(
            inputs={"p": 0.3, "k": 1},
            expected=0.3,
            rel_tol=1e-12,
            note="Support edge k = 1: the first trial succeeds, so P = p.",
        ),
        VerificationCase(
            inputs={"p": 1.0, "k": 1},
            expected=1.0,
            rel_tol=1e-12,
            note="Boundary p = 1: success on trial 1 is certain.",
        ),
        VerificationCase(
            inputs={"p": 0.4, "k": 0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="k = 0 lies outside the trials support, where the mass is zero.",
        ),
    ),
    assumptions=(
        "Trials are independent and share the same success probability p.",
        "k counts trials up to and including the first success (k = 1 means the first trial "
        "succeeds). The failures convention is mathematics.geometric_probability_mass_failures, "
        "with P_trials(k) = P_failures(k - 1).",
        "Derived result: obtained from the Mathlib failures-count mass by the index shift "
        "k = n + 1; the shift was checked symbolically and against exact enumeration of "
        "success/failure sequences.",
        "0 < p <= 1 and k a whole number; p = 0, values outside [0, 1] and non-integral k "
        "raise ValueError. Integral floats such as 3.0 are accepted as counts.",
        "Returns 0.0 for k < 1, where the mass is genuinely zero. p = 1 gives P(1) = 1 and "
        "P(k) = 0 for k > 1.",
        "Relative error below 1.5e-13 measured against 50-digit mpmath on 3500 random points "
        "with 1e-9 <= p <= 1 - 1e-6 and 1 <= k <= 1e9 wherever the mass is within the float "
        "range (largest observed 1.0e-13; the error grows with the size of the exponent "
        "(k - 1) log(1 - p), up to about 745 here); outside that range accuracy is not "
        "characterised. For very large k the value underflows smoothly "
        "to 0.0.",
    ),
    tags=(
        "geometric distribution",
        "probability mass function",
        "pmf",
        "trials until first success",
        "Bernoulli trials",
        "waiting time",
        "discrete distribution",
    ),
)
