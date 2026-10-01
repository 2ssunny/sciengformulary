"""Mode I Stress Intensity Factor: K_I = Y * sigma * sqrt(pi * a)."""

import math

from sciengformulary.catalog._sources import roylance
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    Y: float,  # noqa: N803
    sigma: float,
    a: float,
) -> float:
    return Y * sigma * math.sqrt(math.pi * a)


mode_i_stress_intensity_factor = FormulaSpec(
    id="materials.mode_i_stress_intensity_factor",
    name="Mode I Stress Intensity Factor",
    equation="K_I = Y * sigma * sqrt(pi * a)",
    description=(
        "Strength of the stress singularity at the tip of a crack opened by a remote tensile "
        "stress; fracture is predicted when it reaches the fracture toughness."
    ),
    inputs=(
        VariableSpec(
            name="Y",
            symbol="Y",
            description=(
                "Dimensionless geometry factor for the crack and specimen (1 for a centre crack in "
                "an infinite plate, 1.12 for a shallow edge crack)"
            ),
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="sigma",
            symbol=r"\sigma",
            description="Remote applied tensile stress",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="a",
            symbol="a",
            description="Crack length (edge crack) or half-length (centre crack)",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="K_I",
        symbol="K_I",
        description="Mode I stress intensity factor",
        dimension="M L^-1/2 T^-2",
        si_unit="Pa*m^(1/2)",
    ),
    evaluator=_evaluate,
    references=(
        # The module writes the geometry factor as alpha.
        roylance("Introduction to Fracture Mechanics", "mit3_11f99_frac", 2001, "eq. (5); Table 1"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"Y": 1.12, "sigma": 100000000.0, "a": 0.01},
            expected=19851483.13014178,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation of 1.12 * 1e8 * sqrt(pi * 0.01).",
        ),
    ),
    assumptions=(
        "Linear elastic fracture mechanics: plastic zone small compared with crack length and "
        "specimen dimensions.",
        "Y must come from a solution for the actual crack and specimen geometry.",
    ),
    tags=("fracture mechanics", "stress intensity factor", "crack", "LEFM", "toughness"),
)
