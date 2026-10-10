"""Law of Total Probability (Two Cases): P_A = P_A_given_B * P_B + P_A_given_notB * (1 - P_B)."""

from sciengformulary.catalog._sources import MATH_ACCESSED, mathlib, nist_statistics_handbook
from sciengformulary.catalog.mathematics._domain import probability
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(P_A_given_B: float, P_A_given_notB: float, P_B: float) -> float:  # noqa: N803
    probability("P_A_given_B", P_A_given_B)
    probability("P_A_given_notB", P_A_given_notB)
    probability("P_B", P_B)
    if not 0 < P_B < 1:
        raise ValueError(
            f"P_B must lie strictly between 0 and 1 so both conditional probabilities are "
            f"defined, got {P_B!r}."
        )
    total = P_A_given_B * P_B + P_A_given_notB * (1.0 - P_B)
    # A convex combination lies between its two conditionals; clamp only rounding overshoot.
    return min(max(total, min(P_A_given_B, P_A_given_notB)), max(P_A_given_B, P_A_given_notB))


total_probability_two_events = FormulaSpec(
    id="mathematics.total_probability_two_events",
    name="Law of Total Probability (Two Cases)",
    equation="P_A = P_A_given_B * P_B + P_A_given_notB * (1 - P_B)",
    description=(
        "Probability of an event A obtained by splitting on whether an event B occurs: the "
        "conditional probabilities of A given B and given not-B, weighted by the probabilities of "
        "those two cases."
    ),
    inputs=(
        VariableSpec(
            name="P_A_given_B",
            symbol="P(A|B)",
            description="Probability of A given that B occurs",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="P_A_given_notB",
            symbol=r"P(A|\bar{B})",
            description="Probability of A given that B does not occur",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="P_B",
            symbol="P(B)",
            description="Probability of B",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="P_A",
        symbol="P(A)",
        description="Total probability of A",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # NIST states the law of total probability for events A_i that exclude each other and
        # exhaust all possibilities: P(B) = sum_i P(B | A_i) P(A_i). Step: rename NIST's B to our
        # A and take the two-event partition {B, not B}, giving
        # P(A) = P(A | B) P(B) + P(A | not B) P(not B), and P(not B) = 1 - P(B).
        nist_statistics_handbook(
            "apr/section1/apr1a.htm",
            "sec. 8.1.10, Bayes formula: law of total probability",
            accessed=MATH_ACCESSED,
        ),
        # Mathlib: for measurable s and a finite measure mu,
        # mu[t | s] * mu(s) + mu[t | s^c] * mu(s^c) = mu(t); with s = B and t = A.
        mathlib(
            "Mathlib/Probability/ConditionalProbability.lean#L267",
            "theorem ProbabilityTheory.cond_add_cond_compl_eq",
        ),
        # For a probability measure mu(s) + mu(s^c) = 1, so P(not B) = 1 - P(B).
        mathlib(
            "Mathlib/MeasureTheory/Measure/Typeclasses/Probability.lean#L92",
            "theorem MeasureTheory.prob_add_prob_compl",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"P_A_given_B": 0.9, "P_A_given_notB": 0.1, "P_B": 0.01},
            expected=0.108,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Exact Fraction arithmetic: 0.009 + 0.099 = 0.108.",
        ),
        VerificationCase(
            inputs={"P_A_given_B": 0.37, "P_A_given_notB": 0.82, "P_B": 0.6125},
            expected=0.544375,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Exact Fraction arithmetic; cross-checked by summing a four-cell joint table.",
        ),
        VerificationCase(
            inputs={"P_A_given_B": 0.5, "P_A_given_notB": 0.5, "P_B": 0.3},
            expected=0.5,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Equal conditionals: A is independent of B, so P(A) = 0.5.",
        ),
        VerificationCase(
            inputs={"P_A_given_B": 1, "P_A_given_notB": 0, "P_B": 0.25},
            expected=0.25,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Conditionals 1 and 0: A coincides with B, so P(A) = P(B).",
        ),
    ),
    assumptions=(
        "B and not-B partition the sample space: they are mutually exclusive and exhaustive. The "
        "two conditional probabilities and P_B must be probabilities in [0, 1], and P_B must "
        "satisfy 0 < P_B < 1 so that both conditionings are defined; otherwise ValueError is "
        "raised.",
        "Mathlib defines a conditional measure given a null event as zero; that totalisation is "
        "not adopted here.",
        "The result lies between the two conditional probabilities (it is a weighted average of "
        "them); the evaluator clamps it to that interval only to remove floating-point overshoot.",
        "Derived result: the cited sources state the law of total probability for a general "
        "partition and for a measurable set and its complement; the formula here is the two-event "
        "case with P(not B) replaced by 1 - P(B). The substitution was checked by summing a "
        "four-cell joint probability table in exact fractions.",
    ),
    tags=(
        "law of total probability",
        "conditional probability",
        "partition",
        "probability",
        "Bayes",
    ),
)
