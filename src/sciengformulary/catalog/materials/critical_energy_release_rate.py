"""Critical Energy Release Rate (Plane Stress): G_c = K_c^2 / E."""

from sciengformulary.catalog._sources import roylance
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(K_c: float, E: float) -> float:  # noqa: N803 - symbols as written in the source
    return K_c**2 / E


critical_energy_release_rate = FormulaSpec(
    id="materials.critical_energy_release_rate",
    name="Critical Energy Release Rate (Plane Stress)",
    equation="G_c = K_c^2 / E",
    description=(
        "Critical strain energy release rate corresponding to a critical stress intensity factor."
    ),
    inputs=(
        VariableSpec(
            name="K_c",
            symbol="K_c",
            description="Critical (mode I) stress intensity factor, fracture toughness",
            dimension="M L^-1/2 T^-2",
            si_unit="Pa*m^(1/2)",
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
        name="G_c",
        symbol=r"\mathcal{G}_c",
        description="Critical energy release rate",
        dimension="M T^-2",
        si_unit="J/m^2",
    ),
    evaluator=_evaluate,
    references=(
        roylance("Introduction to Fracture Mechanics", "mit3_11f99_frac", 2001, "p. 9"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"K_c": 41000000.0, "E": 69000000000.0},
            expected=24362.318840579712,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation of (41e6)^2 / 69e9.",
        ),
    ),
    assumptions=(
        "Plane stress. In plane strain the source gives K_c^2 = E G_c (1 - nu^2) instead.",
        "Linear elastic fracture mechanics.",
    ),
    tags=("fracture mechanics", "energy release rate", "Griffith", "toughness"),
)
