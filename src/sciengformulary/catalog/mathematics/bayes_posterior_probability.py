"""Bayes Posterior Probability: P_A_given_B = P_B_given_A * P_A / P_B."""

from sciengformulary.catalog._sources import MATH_ACCESSED, mathlib, nist_statistics_handbook
from sciengformulary.catalog.mathematics._domain import positive, probability
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

# Relative slack allowed when checking P(B|A) * P(A) <= P(B), to absorb float rounding.
_CONSISTENCY_SLACK = 1e-12


def _evaluate(P_B_given_A: float, P_A: float, P_B: float) -> float:  # noqa: N803
    probability("P_B_given_A", P_B_given_A)
    probability("P_A", P_A)
    probability("P_B", P_B)
    positive("P_B", P_B)
    joint = P_B_given_A * P_A
    if joint > P_B * (1.0 + _CONSISTENCY_SLACK):
        raise ValueError(
            "Inconsistent inputs: P_B_given_A * P_A is P(A and B), which cannot exceed P_B; "
            f"got {joint!r} > {P_B!r}."
        )
    # Within the rounding slack the ratio may land a hair above 1; cap it there.
    return min(1.0, joint / P_B)


bayes_posterior_probability = FormulaSpec(
    id="mathematics.bayes_posterior_probability",
    name="Bayes Posterior Probability",
    equation="P_A_given_B = P_B_given_A * P_A / P_B",
    description=(
        "Bayes' rule: the probability of event A once event B is known to have occurred, "
        "from the likelihood P(B|A), the prior P(A) and the evidence P(B)."
    ),
    inputs=(
        VariableSpec(
            name="P_B_given_A",
            symbol="P(B|A)",
            description="Probability of B given A (likelihood), in [0, 1]",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="P_A",
            symbol="P(A)",
            description="Probability of A (prior), in [0, 1]",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="P_B",
            symbol="P(B)",
            description="Probability of B (evidence), in (0, 1]",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="P_A_given_B",
        symbol="P(A|B)",
        description="Probability of A given B (posterior)",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib states mu[t | s] = (mu s)^-1 * mu[s | t] * mu t for a finite measure; with
        # s = B, t = A and a probability measure this is P(A|B) = P(B|A) P(A) / P(B).
        mathlib(
            "Mathlib/Probability/ConditionalProbability.lean#L274",
            "theorem ProbabilityTheory.cond_eq_inv_mul_cond_mul",
        ),
        nist_statistics_handbook(
            "apr/section1/apr1a.htm",
            "sec. 8.1.10, Bayes formula",
            accessed=MATH_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"P_B_given_A": 0.9, "P_A": 0.01, "P_B": 0.0189},
            expected=0.4761904761904762,
            rel_tol=1e-12,
            note=(
                "10/21 by exact Fraction arithmetic on the decimal inputs; 50-digit mpmath of "
                "the float inputs agrees to 1.2e-16."
            ),
        ),
        VerificationCase(
            inputs={"P_B_given_A": 1.0, "P_A": 0.4, "P_B": 0.4},
            expected=1.0,
            rel_tol=1e-12,
            note="A implies B and P(A) = P(B), so the posterior is exactly 1.",
        ),
        VerificationCase(
            inputs={"P_B_given_A": 0.0, "P_A": 0.5, "P_B": 0.2},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="A likelihood of zero gives a posterior of zero.",
        ),
        VerificationCase(
            inputs={"P_B_given_A": 1.0, "P_A": 0.25, "P_B": 1.0},
            expected=0.25,
            rel_tol=1e-12,
            note="Certain evidence P(B) = 1 leaves the prior times the likelihood; exact.",
        ),
    ),
    assumptions=(
        "All three inputs are probabilities in [0, 1] and P(B) > 0; conditioning on an "
        "impossible event is undefined and raises ValueError.",
        "The inputs must come from one probability model, so P(B|A) P(A) = P(A and B) <= P(B). "
        "Inputs that break this by more than a relative 1e-12 raise ValueError; within that "
        "rounding slack the result is capped at 1.0.",
        "P(B) can be found from the law of total probability over a partition that contains A.",
    ),
    tags=(
        "Bayes theorem",
        "Bayes rule",
        "conditional probability",
        "posterior",
        "prior",
        "likelihood",
        "statistics",
    ),
)
