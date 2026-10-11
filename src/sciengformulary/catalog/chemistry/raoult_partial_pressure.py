"""Raoult law component vapor pressure."""

from sciengformulary.catalog._domain import finite, finite_result, non_negative
from sciengformulary.catalog._sources import (
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(x: float, p_pure: float) -> float:
    finite("x", x)
    if not 0 <= x <= 1:
        raise ValueError("x must be between zero and one")
    non_negative("p_pure", p_pure)
    return finite_result(x * p_pure)


raoult_partial_pressure = FormulaSpec(
    id="chemistry.raoult_partial_pressure",
    name="Raoult Partial Pressure",
    equation="p = x * p_pure",
    description="Raoult law component vapor pressure.",
    inputs=(
        VariableSpec(
            name="x",
            symbol="x",
            description="Liquid-phase mole fraction of the volatile component",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="p_pure",
            symbol="p_pure",
            description="Pure-component saturation vapor pressure at the same temperature",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
    ),
    output=VariableSpec(
        name="p",
        symbol="p",
        description="Component partial pressure",
        dimension="M L^-1 T^-2",
        si_unit="Pa",
    ),
    evaluator=_evaluate,
    references=(
        openstax_section(
            "chemistry-2e",
            "11-4-colligative-properties",
            "11.4 Colligative Properties",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"x": 0.5, "p_pure": 3000},
            expected=1500,
            note="Half the liquid mole fraction gives half the pure vapor pressure.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"x": 1, "p_pure": 3000},
            expected=3000,
            note="Pure liquid recovers its saturation vapor pressure.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Ideal liquid solution and vapor-phase behavior appropriate to Raoult law.",
        "Use liquid composition, not vapor composition.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemistry", "raoult partial pressure"),
)
