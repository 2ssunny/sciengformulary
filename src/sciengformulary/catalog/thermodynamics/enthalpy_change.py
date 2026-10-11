"""Enthalpy change from the definition H = U + pV."""

from sciengformulary.catalog._domain import finite, finite_result
from sciengformulary.catalog._sources import (
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(delta_U: float, delta_pV: float) -> float:
    finite("delta_U", delta_U)
    finite("delta_pV", delta_pV)
    return finite_result(delta_U + delta_pV)


enthalpy_change = FormulaSpec(
    id="thermodynamics.enthalpy_change",
    name="Enthalpy Change",
    equation="delta_H = delta_U + delta_pV",
    description="Enthalpy change from the definition H = U + pV.",
    inputs=(
        VariableSpec(
            name="delta_U",
            symbol="delta_U",
            description="Internal energy change",
            dimension="M L^2 T^-2",
            si_unit="J",
        ),
        VariableSpec(
            name="delta_pV",
            symbol="delta_pV",
            description="Final p*V minus initial p*V",
            dimension="M L^2 T^-2",
            si_unit="J",
        ),
    ),
    output=VariableSpec(
        name="delta_H",
        symbol="delta_H",
        description="Enthalpy change",
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
            inputs={"delta_U": 100, "delta_pV": 20},
            expected=120,
            note="100 + 20 = 120 J.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"delta_U": -100, "delta_pV": 20},
            expected=-80,
            note="-100 + 20 = -80 J.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "delta_pV means the change of the product pV, not delta_p times delta_V.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "thermodynamics", "enthalpy change"),
)
