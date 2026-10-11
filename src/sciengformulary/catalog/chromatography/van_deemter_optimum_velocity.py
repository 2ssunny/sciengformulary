"""Optimum velocity for the simple van Deemter model."""

import math

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import (
    harvey_analytical_chemistry,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(B: float, C: float) -> float:
    positive("B", B)
    positive("C", C)
    return finite_result(math.sqrt(B / C))


van_deemter_optimum_velocity = FormulaSpec(
    id="chromatography.van_deemter_optimum_velocity",
    name="Van Deemter Optimum Velocity",
    equation="u_opt = sqrt(B/C)",
    description="Optimum velocity for the simple van Deemter model.",
    inputs=(
        VariableSpec(
            name="B",
            symbol="B",
            description="Longitudinal-diffusion coefficient",
            dimension="L^2 T^-1",
            si_unit="m^2/s",
        ),
        VariableSpec(
            name="C",
            symbol="C",
            description="Combined mass-transfer coefficient",
            dimension="T",
            si_unit="s",
        ),
    ),
    output=VariableSpec(
        name="u_opt",
        symbol="u_opt",
        description="Velocity minimizing the simple van Deemter expression",
        dimension="L T^-1",
        si_unit="m/s",
    ),
    evaluator=_evaluate,
    references=(
        harvey_analytical_chemistry(
            (
                "12%3A_Chromatographic_and_Electrophoretic_Methods/12.03%3A_Optimizing_Chromatogr"
                "aphic_Separations"
            ),
            "12.3: Optimizing Chromatographic Separations",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"B": 4, "C": 1},
            expected=2,
            note="At u=2, B/u and C*u are equal and their sum is minimal.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"B": 9, "C": 1}, expected=3, note="sqrt(9/1)=3.", rel_tol=1e-12, abs_tol=0.0
        ),
    ),
    assumptions=(
        "Derived result: Set dH/du=-B/u^2+C to zero and check d2H/du2=2B/u^3>0.",
        "Simple H=A+B/u+C*u with constant A, positive B and positive C.",
        "The mathematical optimum must also be achievable within the operating range where the fitted model applies.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chromatography", "van deemter optimum velocity"),
)
