"""Hooke's Law (Uniaxial): sigma = E * epsilon."""

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(E: float, epsilon: float) -> float:  # noqa: N803 - symbols as written in the source
    return E * epsilon


uniaxial_hookes_law = FormulaSpec(
    id="materials.uniaxial_hookes_law",
    name="Hooke's Law (Uniaxial)",
    equation="sigma = E * epsilon",
    description="Stress proportional to strain in the elastic range of uniaxial loading.",
    inputs=(
        VariableSpec(
            name="E",
            symbol="E",
            description="Young's modulus of the material",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="epsilon",
            symbol=r"\epsilon",
            description="Axial strain",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="sigma",
        symbol=r"\sigma",
        description="Axial stress",
        dimension="M L^-1 T^-2",
        si_unit="Pa",
    ),
    evaluator=_evaluate,
    references=(
        # The source defines Young's modulus Y as tensile stress over tensile strain.
        openstax_university_physics(
            1,
            "12-3-stress-strain-and-elastic-modulus",
            "sec. 12.3, eq. (12.36)",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"E": 200000000000.0, "epsilon": 0.001},
            expected=200000000.0,
            rel_tol=1e-12,
            note="Hand calculation: 200e9 * 1e-3 = 2e8 Pa.",
        ),
    ),
    assumptions=(
        "Linear elastic, homogeneous, isotropic material; small strains and displacements.",
        "Uniaxial stress only; for multiaxial states use the generalised Hooke's law with "
        "Poisson coupling.",
        "Below the proportional limit (no yielding).",
    ),
    tags=("Hooke's law", "Young's modulus", "elasticity", "stress-strain"),
)
