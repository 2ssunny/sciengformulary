"""Gibbs energy change at a common temperature."""

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import (
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(delta_H: float, T: float, delta_S: float) -> float:
    finite("delta_H", delta_H)
    positive("T", T)
    finite("delta_S", delta_S)
    return finite_result(delta_H - T * delta_S)


gibbs_energy_change = FormulaSpec(
    id="thermodynamics.gibbs_energy_change",
    name="Gibbs Energy Change",
    equation="delta_G = delta_H - T * delta_S",
    description="Gibbs energy change at a common temperature.",
    inputs=(
        VariableSpec(
            name="delta_H",
            symbol="delta_H",
            description="Molar reaction or transition enthalpy change",
            dimension="M L^2 T^-2 N^-1",
            si_unit="J/mol",
        ),
        VariableSpec(
            name="T",
            symbol="T",
            description="Common absolute temperature of both states",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="delta_S",
            symbol="delta_S",
            description="Molar reaction or transition entropy change",
            dimension="M L^2 T^-2 N^-1 Theta^-1",
            si_unit="J/(mol*K)",
        ),
    ),
    output=VariableSpec(
        name="delta_G",
        symbol="delta_G",
        description="Molar Gibbs energy change",
        dimension="M L^2 T^-2 N^-1",
        si_unit="J/mol",
    ),
    evaluator=_evaluate,
    references=(
        openstax_section(
            "chemistry-2e",
            "16-4-free-energy",
            "16.4 Free Energy",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"delta_H": 10000, "T": 300, "delta_S": 20},
            expected=4000,
            note="10000 - 300 times 20 = 4000 J/mol.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"delta_H": -10000, "T": 300, "delta_S": 0},
            expected=-10000,
            note="Zero entropy change leaves delta_H.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "States are compared at the same temperature.",
        "Use consistent reaction normalization for enthalpy and entropy; spontaneity inference from delta_G applies at fixed T and p.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "thermodynamics", "gibbs energy change"),
)
