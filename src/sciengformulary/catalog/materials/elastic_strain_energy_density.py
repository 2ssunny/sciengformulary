"""Elastic Strain Energy Density: u = sigma^2 / (2 * E)."""

from sciengformulary.catalog._sources import roylance
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(sigma: float, E: float) -> float:  # noqa: N803 - symbols as written in the source
    return sigma**2 / (2.0 * E)


elastic_strain_energy_density = FormulaSpec(
    id="materials.elastic_strain_energy_density",
    name="Elastic Strain Energy Density",
    equation="u = sigma^2 / (2 * E)",
    description="Strain energy stored per unit volume in a uniaxially stressed elastic solid.",
    inputs=(
        VariableSpec(
            name="sigma",
            symbol=r"\sigma",
            description="Uniaxial stress",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="E",
            symbol="E",
            description="Young's modulus of the material",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
    ),
    output=VariableSpec(
        name="u",
        symbol="u",
        description="Strain energy per unit volume",
        dimension="M L^-1 T^-2",
        si_unit="J/m^3",
    ),
    evaluator=_evaluate,
    references=(
        # The module writes U* = sigma^2 / 2E. The sheet's U = V sigma^2 / (2E) is this density
        # times the volume.
        roylance("Stresses in Beams", "mit3_11f99_bstress", 2000, "p. 6"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"sigma": 200000000.0, "E": 200000000000.0},
            expected=100000.0,
            rel_tol=1e-12,
            note="Hand calculation: (200e6)^2 / (2 * 200e9) = 1e5 J/m^3.",
        ),
    ),
    assumptions=(
        "Linear elastic, homogeneous, isotropic material; small strains and displacements.",
        "Uniaxial stress state.",
    ),
    tags=("strain energy", "resilience", "elastic energy"),
)
