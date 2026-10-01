"""True Strain from Engineering Strain: epsilon_t = ln(1 + epsilon_n)."""

import math

from sciengformulary.catalog._sources import roylance
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(epsilon_n: float) -> float:
    return math.log(1.0 + epsilon_n)


true_strain = FormulaSpec(
    id="materials.true_strain",
    name="True Strain from Engineering Strain",
    equation="epsilon_t = ln(1 + epsilon_n)",
    description="Logarithmic (true) strain from engineering strain.",
    inputs=(
        VariableSpec(
            name="epsilon_n",
            symbol=r"\epsilon_n",
            description="Engineering strain",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="epsilon_t",
        symbol=r"\epsilon_t",
        description="True strain",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        roylance("Stress-Strain Curves", "mit3_11f99_ss", 2001, "eq. (6)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"epsilon_n": 0.1},
            expected=0.09531017980432487,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation of ln(1.1).",
        ),
    ),
    assumptions=(
        "Uniform deformation: valid only up to the onset of necking.",
        "Natural logarithm.",
    ),
    tags=("true strain", "logarithmic strain", "tensile test"),
)
