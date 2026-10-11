"""Integrated Clausius-Clapeyron vapor pressure estimate."""

import math

from sciengformulary.catalog._constants import (
    MOLAR_GAS_CONSTANT,
)
from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import bipm_si_defining_constants
from sciengformulary.core import (
    FormulaSpec,
    ReferenceSpec,
    VariableSpec,
    VerificationCase,
)


def _evaluate(p1: float, T1: float, T2: float, delta_H_vap: float) -> float:
    positive("p1", p1)
    positive("T1", T1)
    positive("T2", T2)
    positive("delta_H_vap", delta_H_vap)
    return finite_result(p1 * math.exp(-delta_H_vap / MOLAR_GAS_CONSTANT * (1 / T2 - 1 / T1)))


clausius_clapeyron_pressure = FormulaSpec(
    id="thermodynamics.clausius_clapeyron_pressure",
    name="Clausius Clapeyron Pressure",
    equation="p2 = p1 * exp[-delta_H_vap/R_u * (1/T2 - 1/T1)]",
    description="Integrated Clausius-Clapeyron vapor pressure estimate.",
    inputs=(
        VariableSpec(
            name="p1",
            symbol="p1",
            description="Saturation vapor pressure at T1",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="T1",
            symbol="T1",
            description="First absolute temperature",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="T2",
            symbol="T2",
            description="Second absolute temperature",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="delta_H_vap",
            symbol="delta_H_vap",
            description="Molar enthalpy of vaporization",
            dimension="M L^2 T^-2 N^-1",
            si_unit="J/mol",
        ),
    ),
    output=VariableSpec(
        name="p2",
        symbol="p2",
        description="Estimated saturation vapor pressure at T2",
        dimension="M L^-1 T^-2",
        si_unit="Pa",
    ),
    evaluator=_evaluate,
    references=(
        ReferenceSpec(
            source_type="official_web",
            title="10.3 Phase Transitions",
            organization="OpenStax",
            url="https://openstax.org/books/chemistry-2e/pages/10-3-phase-transitions",
            accessed="2026-10-10",
        ),
        bipm_si_defining_constants(),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"p1": 1000, "T1": 300, "T2": 300, "delta_H_vap": 40000},
            expected=1000,
            note="Equal temperatures preserve saturation pressure.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"p1": 1000, "T1": 300, "T2": 600, "delta_H_vap": 4988.677570891944},
            expected=2718.2818284590453,
            note="Algebraic case: exponent equals one, independently evaluated as 1000 exp(1).",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Derived result: Rearrange the two-temperature integrated Clausius-Clapeyron relation.",
        "Ideal vapor; liquid molar volume negligible relative to vapor.",
        "Enthalpy of vaporization approximately constant over the interval; remain within one liquid-vapor coexistence regime.",
        "Wide algebraic verification cases are mathematical checks, not recommendations for a real fluid.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "thermodynamics", "clausius clapeyron pressure"),
)
