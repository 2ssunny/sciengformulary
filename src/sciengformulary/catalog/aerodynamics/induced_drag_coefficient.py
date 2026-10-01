"""Induced Drag Coefficient: C_Di = C_L^2 / (pi * AR * e)."""

import math

from sciengformulary.catalog._sources import nasa_glenn
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    C_L: float,  # noqa: N803
    AR: float,  # noqa: N803
    e: float,
) -> float:
    return C_L**2 / (math.pi * AR * e)


induced_drag_coefficient = FormulaSpec(
    id="aerodynamics.induced_drag_coefficient",
    name="Induced Drag Coefficient",
    equation="C_Di = C_L^2 / (pi * AR * e)",
    description=(
        "Drag coefficient caused by the trailing vortices of a finite lifting wing. It grows with "
        "the square of the lift coefficient and falls as the wing becomes more slender (higher "
        "aspect ratio) or its lift distribution closer to elliptic."
    ),
    inputs=(
        VariableSpec(
            name="C_L",
            symbol="C_L",
            description="Wing lift coefficient",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="AR",
            symbol="AR",
            description="Wing aspect ratio, span squared over planform area",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="e",
            symbol="e",
            description="Span efficiency factor (1 for an elliptic lift distribution)",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="C_Di",
        symbol="C_{D_i}",
        description="Induced drag coefficient",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The sheet writes k C_L^2 / (pi AR) with k = 1/e, the same expression.
        nasa_glenn("Induced Drag Coefficient", "induced-drag-coefficient", 2023),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"C_L": 0.5, "AR": 8.0, "e": 0.8},
            expected=0.012433979929054323,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation of 0.5^2 / (pi * 8 * 0.8).",
        ),
    ),
    assumptions=(
        "Finite wing in subsonic attached flow; the relation comes from lifting-line theory "
        "and does not describe stalled wings.",
        "e is at most 1; 1 corresponds to an elliptic lift distribution, other planforms have "
        "lower values that must be supplied for the actual wing.",
        "Gives only the lift-dependent (induced) part of drag, not total drag.",
    ),
    tags=("induced drag", "drag due to lift", "span efficiency", "Oswald", "lifting line"),
)
