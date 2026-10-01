"""Laminar Flat-Plate Local Skin Friction: C_f = 0.664 / sqrt(Re_x)."""

import math

from sciengformulary.catalog._sources import lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(Re_x: float) -> float:  # noqa: N803 - symbols as written in the source
    return 0.664 / math.sqrt(Re_x)


laminar_flat_plate_skin_friction = FormulaSpec(
    id="heat_transfer.laminar_flat_plate_skin_friction",
    name="Laminar Flat-Plate Local Skin Friction",
    equation="C_f = 0.664 / sqrt(Re_x)",
    description=(
        "Local skin-friction coefficient of a laminar boundary layer on a flat plate (Blasius "
        "solution)."
    ),
    inputs=(
        VariableSpec(
            name="Re_x",
            symbol="Re_x",
            description="Reynolds number based on distance from the leading edge",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="C_f",
        symbol="C_f",
        description="Local skin-friction coefficient tau_w / (rho u^2 / 2)",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        lienhard_heat_transfer("sec. 6.2, eq. (6.33)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"Re_x": 100000.0},
            expected=0.002099752366351804,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation of 0.664 / sqrt(1e5).",
        ),
    ),
    assumptions=(
        "Steady, laminar, two-dimensional boundary layer on a flat plate with zero pressure "
        "gradient; local value at distance x from the leading edge. Not valid once the "
        "boundary layer has become turbulent.",
        "Incompressible flow.",
    ),
    tags=("skin friction", "Blasius", "boundary layer", "flat plate", "laminar"),
)
