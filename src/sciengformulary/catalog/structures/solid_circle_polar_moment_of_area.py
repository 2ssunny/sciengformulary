"""Polar Second Moment of a Solid Circle: J = pi * c^4 / 2."""

import math

from sciengformulary.catalog._sources import roylance
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(c: float) -> float:
    return math.pi * c**4 / 2.0


solid_circle_polar_moment_of_area = FormulaSpec(
    id="structures.solid_circle_polar_moment_of_area",
    name="Polar Second Moment of a Solid Circle",
    equation="J = pi * c^4 / 2",
    description="Polar second moment of area of a solid circular cross-section.",
    inputs=(
        VariableSpec(
            name="c",
            symbol="c",
            description="Outer radius of the section",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="J",
        symbol="J",
        description="Polar second moment of area",
        dimension="L^4",
        si_unit="m^4",
    ),
    evaluator=_evaluate,
    references=(
        # The source gives J = pi (R_o^4 - R_i^4) / 2 for a hollow shaft; R_i = 0 for a solid one.
        roylance("Shear and Torsion", "mit3_11f99_torsion", 2000, "eq. (12)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"c": 0.025},
            expected=6.135923151542565e-07,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation of pi * 0.025^4 / 2.",
        ),
    ),
    assumptions=(
        "Solid circular section; for a tube subtract the bore's J.",
    ),
    tags=("polar moment", "torsion", "shaft", "circular section"),
)
