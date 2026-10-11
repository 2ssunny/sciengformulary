"""Pressure-volume work at constant external pressure."""

from sciengformulary.catalog._domain import finite, finite_result, non_negative
from sciengformulary.catalog._sources import (
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(p_external: float, delta_V: float) -> float:
    non_negative("p_external", p_external)
    finite("delta_V", delta_V)
    return finite_result(-p_external * delta_V)


constant_external_pressure_work = FormulaSpec(
    id="thermodynamics.constant_external_pressure_work",
    name="Constant External Pressure Work",
    equation="w = -p_external * delta_V",
    description="Pressure-volume work at constant external pressure.",
    inputs=(
        VariableSpec(
            name="p_external",
            symbol="p_external",
            description="Constant external pressure",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="delta_V",
            symbol="delta_V",
            description="Final volume minus initial volume",
            dimension="L^3",
            si_unit="m^3",
        ),
    ),
    output=VariableSpec(
        name="w",
        symbol="w",
        description="Work done on the system",
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
            inputs={"p_external": 100000, "delta_V": 0.001},
            expected=-100,
            note="Expansion by 1 L against 100 kPa gives -100 J.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"p_external": 100000, "delta_V": -0.001},
            expected=100,
            note="Compression reverses the work sign.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Derived result: Integrate pressure-volume work at constant external pressure.",
        "Only pressure-volume work against a constant external pressure.",
        "This is not the existing reversible isothermal work law.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "thermodynamics", "constant external pressure work"),
)
