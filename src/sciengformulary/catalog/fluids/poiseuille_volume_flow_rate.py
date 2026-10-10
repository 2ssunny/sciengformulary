"""Poiseuille Volume Flow Rate: Q = pi * R^4 * delta_p / (8 * mu * L)."""

import math

from sciengformulary.catalog._sources import (
    lienhard_heat_transfer,
    openstax_university_physics,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    R: float,  # noqa: N803
    delta_p: float,
    mu: float,
    L: float,  # noqa: N803
) -> float:
    return math.pi * R**4 * delta_p / (8.0 * mu * L)


poiseuille_volume_flow_rate = FormulaSpec(
    id="fluids.poiseuille_volume_flow_rate",
    name="Poiseuille Volume Flow Rate",
    equation="Q = pi * R^4 * delta_p / (8 * mu * L)",
    description=(
        "Volume flow rate of fully developed laminar flow through a circular pipe driven by a "
        "pressure drop (Hagen-Poiseuille law). The mean velocity is Q / (pi R^2)."
    ),
    inputs=(
        VariableSpec(
            name="R",
            symbol="R",
            description="Pipe inner radius",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="delta_p",
            symbol=r"\Delta p",
            description="Pressure drop over the length L (upstream minus downstream)",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="mu",
            symbol=r"\mu",
            description="Dynamic viscosity of the fluid",
            dimension="M L^-1 T^-1",
            si_unit="Pa*s",
        ),
        VariableSpec(
            name="L",
            symbol="L",
            description="Pipe length over which delta_p acts",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="Q",
        symbol="Q",
        description="Volume flow rate",
        dimension="L^3 T^-1",
        si_unit="m^3/s",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes Q = (p2 - p1) pi r^4 / (8 eta l). The sheet's mean speed D^2 (-dp/dx) /
        # (32 mu) equals Q / (pi R^2).
        openstax_university_physics(1, "14-7-viscosity-and-turbulence", "sec. 14.7, eq. (14.19)"),
        # The book prints the parabolic profile of fully developed laminar pipe flow; the mean speed
        # is half the centreline speed, and Q = pi R^2 times the mean speed.
        lienhard_heat_transfer("sec. 7.2, eqs. (7.14)-(7.15), p. 358"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"R": 0.01, "delta_p": 100.0, "mu": 0.001, "L": 1.0},
            expected=0.00039269908169872416,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation: pi * 1e-8 * 100 / 8e-3.",
        ),
    ),
    assumptions=(
        "Steady, incompressible, fully developed laminar flow of a Newtonian fluid in a "
        "straight rigid circular pipe; not valid in the entrance region.",
        "Valid for laminar flow only. Based on pipe diameter, a Reynolds number under about "
        "2000 is laminar and one over about 3000 is turbulent.",
        "Derived result: obtained by integrating the cited parabolic velocity profile over the "
        "pipe cross-section; the source prints the profile, not the flow-rate formula.",
    ),
    tags=("Poiseuille", "Hagen-Poiseuille", "pipe flow", "laminar", "viscous flow"),
)
