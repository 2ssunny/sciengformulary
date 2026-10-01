"""Normal Shock Downstream Mach Number."""

import math

from sciengformulary.catalog._sources import naca_report_1135
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(M1: float, gamma: float) -> float:  # noqa: N803 - symbols as written in the source
    return math.sqrt(((gamma - 1.0) * M1**2 + 2.0) / (2.0 * gamma * M1**2 - (gamma - 1.0)))


normal_shock_downstream_mach = FormulaSpec(
    id="aerodynamics.normal_shock_downstream_mach",
    name="Normal Shock Downstream Mach Number",
    equation="M2 = sqrt(((gamma - 1) * M1^2 + 2) / (2 * gamma * M1^2 - (gamma - 1)))",
    description="Mach number just downstream of a stationary normal shock wave.",
    inputs=(
        VariableSpec(
            name="M1",
            symbol="M_1",
            description="Mach number just upstream of the normal shock (must exceed 1)",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="gamma",
            symbol=r"\gamma",
            description="Ratio of specific heats c_p / c_v of the gas",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="M2",
        symbol="M_2",
        description="Downstream Mach number (subsonic for M1 > 1)",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The source gives M2 squared; this is its positive root.
        naca_report_1135("eq. (96); Table II, p. 635"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"M1": 2.5, "gamma": 1.4},
            expected=0.513,
            rel_tol=0.0002,
            note=(
                "Published value: NACA Rep. 1135, Table II, M_1 = 2.50 gives M_2 = .5130 (four "
                "significant figures)."
            ),
        ),
        VerificationCase(
            inputs={"M1": 2.0, "gamma": 1.4},
            expected=0.5773502691896257,
            rel_tol=1e-12,
            note="Hand calculation: sqrt(3.6 / 10.8) = sqrt(1/3).",
        ),
    ),
    assumptions=(
        "Steady, one-dimensional flow through a stationary normal shock in a calorically "
        "perfect gas; the shock is treated as a discontinuity with no heat addition.",
        "Calorically perfect gas: constant specific heats, so gamma is constant. The source "
        "treats calorically imperfect (high-temperature) gases separately; do not use this "
        "form for them.",
        "M1 must be greater than 1.",
    ),
    tags=("normal shock", "shock wave", "downstream Mach", "supersonic"),
)
