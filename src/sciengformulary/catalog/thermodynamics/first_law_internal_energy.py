"""First law with the chemistry work convention."""

from sciengformulary.catalog._domain import finite, finite_result
from sciengformulary.catalog._sources import (
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(q: float, w: float) -> float:
    finite("q", q)
    finite("w", w)
    return finite_result(q + w)


first_law_internal_energy = FormulaSpec(
    id="thermodynamics.first_law_internal_energy",
    name="First Law Internal Energy",
    equation="delta_U = q + w",
    description="First law with the chemistry work convention.",
    inputs=(
        VariableSpec(
            name="q",
            symbol="q",
            description="Heat transferred into the system",
            dimension="M L^2 T^-2",
            si_unit="J",
        ),
        VariableSpec(
            name="w",
            symbol="w",
            description="Work done on the system",
            dimension="M L^2 T^-2",
            si_unit="J",
        ),
    ),
    output=VariableSpec(
        name="delta_U",
        symbol="delta_U",
        description="Internal energy change",
        dimension="M L^2 T^-2",
        si_unit="J",
    ),
    evaluator=_evaluate,
    references=(
        openstax_section(
            "chemistry-2e",
            "5-3-enthalpy",
            "5.3 Enthalpy",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"q": 100, "w": -30},
            expected=70,
            note="100 J absorbed minus 30 J expansion work = 70 J.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"q": 0, "w": -50},
            expected=-50,
            note="Adiabatic work of -50 J gives delta_U = -50 J.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Closed system and chemistry sign convention: heat in and work on are positive.",
        "Macroscopic kinetic and potential energy changes are excluded from delta_U.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "thermodynamics", "first law internal energy"),
)
