"""Free Thermal Strain: epsilon_th = alpha * delta_T."""

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    alpha: float,
    delta_T: float,  # noqa: N803
) -> float:
    return alpha * delta_T


thermal_strain = FormulaSpec(
    id="materials.thermal_strain",
    name="Free Thermal Strain",
    equation="epsilon_th = alpha * delta_T",
    description="Strain of an unrestrained body caused by a temperature change.",
    inputs=(
        VariableSpec(
            name="alpha",
            symbol=r"\alpha",
            description="Coefficient of linear thermal expansion",
            dimension="Theta^-1",
            si_unit="1/K",
        ),
        VariableSpec(
            name="delta_T",
            symbol=r"\Delta T",
            description="Temperature change",
            dimension="Theta",
            si_unit="K",
        ),
    ),
    output=VariableSpec(
        name="epsilon_th",
        symbol=r"\epsilon_{th}",
        description="Thermal strain",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes delta_L = alpha L delta_T; strain is delta_L / L.
        openstax_university_physics(2, "1-3-thermal-expansion", "sec. 1.3, eq. (1.2)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"alpha": 1.2e-05, "delta_T": 100.0},
            expected=0.0012,
            rel_tol=1e-12,
            note="Hand calculation: 12e-6 * 100 = 1.2e-3.",
        ),
    ),
    assumptions=(
        "Free expansion: if the body is restrained, stresses develop instead.",
        "alpha treated as constant over the temperature range.",
    ),
    tags=("thermal expansion", "thermal strain", "coefficient of expansion"),
)
