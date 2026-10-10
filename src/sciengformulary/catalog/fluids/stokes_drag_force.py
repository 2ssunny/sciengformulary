"""Stokes Drag on a Sphere: F_D = 3 * pi * mu * D * v_rel."""

import math

from sciengformulary.catalog._sources import (
    lienhard_heat_transfer,
    openstax_university_physics,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    mu: float,
    D: float,  # noqa: N803
    v_rel: float,
) -> float:
    return 3.0 * math.pi * mu * D * v_rel


stokes_drag_force = FormulaSpec(
    id="fluids.stokes_drag_force",
    name="Stokes Drag on a Sphere",
    equation="F_D = 3 * pi * mu * D * v_rel",
    description=(
        "Viscous drag on a small sphere moving slowly through a fluid, proportional to the "
        "relative speed."
    ),
    inputs=(
        VariableSpec(
            name="mu",
            symbol=r"\mu",
            description="Dynamic viscosity of the fluid",
            dimension="M L^-1 T^-1",
            si_unit="Pa*s",
        ),
        VariableSpec(
            name="D",
            symbol="D",
            description="Sphere (particle) diameter",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="v_rel",
            symbol="v_{rel}",
            description="Speed of the fluid relative to the sphere",
            dimension="L T^-1",
            si_unit="m/s",
        ),
    ),
    output=VariableSpec(
        name="F_D",
        symbol="F_D",
        description="Drag force, along the relative velocity",
        dimension="M L T^-2",
        si_unit="N",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes F_s = 6 pi r eta v with sphere radius r = D / 2.
        openstax_university_physics(1, "6-4-drag-force-and-terminal-speed", "sec. 6.4, eq. (6.6)"),
        # The book prints F = 6 pi mu v R for a sphere of radius R at Re_D < 1 (footnote); R = D / 2
        # gives 3 pi mu D v.
        lienhard_heat_transfer("sec. 11.10, footnote 24, p. 692"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"mu": 1.8e-05, "D": 1e-05, "v_rel": 0.1},
            expected=1.6964600329384883e-10,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation of 6 * pi * 5e-6 * 1.8e-5 * 0.1.",
        ),
    ),
    assumptions=(
        "Holds for small spheres, low relative speeds or highly viscous fluids, where drag "
        "scales linearly with speed. Larger or faster bodies instead see drag that scales with "
        "the square of the speed.",
        "Rigid sphere far from walls and other particles, in a continuum fluid.",
    ),
    tags=("Stokes drag", "creeping flow", "particle", "sphere", "viscous drag"),
)
