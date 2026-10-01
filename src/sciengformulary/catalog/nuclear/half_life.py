"""Half-Life from Decay Constant: t_half = ln(2) / lambda."""

import math

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(decay_constant: float) -> float:
    return math.log(2.0) / decay_constant


half_life = FormulaSpec(
    id="nuclear.half_life",
    name="Half-Life from Decay Constant",
    equation="t_half = ln(2) / lambda",
    description="Time for half of a radioactive sample to decay.",
    inputs=(
        VariableSpec(
            name="decay_constant",
            symbol=r"\lambda",
            description="Decay constant",
            dimension="T^-1",
            si_unit="1/s",
        ),
    ),
    output=VariableSpec(
        name="t_half",
        symbol="T_{1/2}",
        description="Half-life",
        dimension="T",
        si_unit="s",
    ),
    evaluator=_evaluate,
    references=(
        # Eqs. (10.13)-(10.14) give ln 2 exactly; eq. (10.15) rounds it to 0.693.
        openstax_university_physics(3, "10-3-radioactive-decay", "sec. 10.3, eqs. (10.13)-(10.15)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"decay_constant": 0.1},
            expected=6.931471805599453,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation of ln 2 / 0.1.",
        ),
    ),
    assumptions=(
        "Single-step exponential decay.",
    ),
    tags=("half-life", "decay constant", "radioactivity", "nuclear"),
)
