"""True Stress from Engineering Values: sigma_t = sigma_n * (1 + epsilon_n)."""

from sciengformulary.catalog._sources import roylance
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(sigma_n: float, epsilon_n: float) -> float:
    return sigma_n * (1.0 + epsilon_n)


true_stress = FormulaSpec(
    id="materials.true_stress",
    name="True Stress from Engineering Values",
    equation="sigma_t = sigma_n * (1 + epsilon_n)",
    description=(
        "True (current-area) stress in a tensile specimen computed from engineering stress and "
        "strain."
    ),
    inputs=(
        VariableSpec(
            name="sigma_n",
            symbol=r"\sigma_n",
            description="Engineering stress",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="epsilon_n",
            symbol=r"\epsilon_n",
            description="Engineering strain",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="sigma_t",
        symbol=r"\sigma_t",
        description="True stress",
        dimension="M L^-1 T^-2",
        si_unit="Pa",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes sigma_t = sigma_e (1 + eps_e).
        roylance("Stress-Strain Curves", "mit3_11f99_ss", 2001, "eq. (6)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"sigma_n": 200000000.0, "epsilon_n": 0.1},
            expected=220000000.0,
            rel_tol=1e-12,
            note="Hand calculation: 200e6 * 1.1 = 220e6 Pa.",
        ),
    ),
    assumptions=(
        "Constant volume during plastic deformation.",
        "Uniform deformation: valid only up to the onset of necking.",
    ),
    tags=("true stress", "tensile test", "plasticity", "necking"),
)
