"""Engineering (Nominal) Strain: epsilon_n = delta_L / L0."""

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(delta_L: float, L0: float) -> float:  # noqa: N803 - symbols as written in the source
    return delta_L / L0


engineering_strain = FormulaSpec(
    id="materials.engineering_strain",
    name="Engineering (Nominal) Strain",
    equation="epsilon_n = delta_L / L0",
    description="Change in length divided by original length.",
    inputs=(
        VariableSpec(
            name="delta_L",
            symbol=r"\Delta L",
            description="Change in gauge length",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="L0",
            symbol="L_0",
            description="Original gauge length",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="epsilon_n",
        symbol=r"\epsilon_n",
        description="Engineering strain",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        openstax_university_physics(
            1,
            "12-3-stress-strain-and-elastic-modulus",
            "sec. 12.3, eq. (12.35)",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"delta_L": 0.0018, "L0": 2.0},
            expected=0.0009,
            rel_tol=1e-12,
            note="Hand calculation: 0.0018 / 2 = 9e-4.",
        ),
    ),
    assumptions=(
        "Uniform deformation over the gauge length.",
    ),
    tags=("strain", "nominal strain", "engineering strain", "tensile test"),
)
