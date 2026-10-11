"""Mass concentration of a solute."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import (
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(m_solute: float, V: float) -> float:
    non_negative("m_solute", m_solute)
    positive("V", V)
    return finite_result(m_solute / V)


mass_concentration = FormulaSpec(
    id="chemistry.mass_concentration",
    name="Mass Concentration",
    equation="rho_solute = m_solute / V",
    description="Mass concentration of a solute.",
    inputs=(
        VariableSpec(
            name="m_solute",
            symbol="m_solute",
            description="Mass of solute",
            dimension="M",
            si_unit="kg",
        ),
        VariableSpec(
            name="V",
            symbol="V",
            description="Final volume of solution",
            dimension="L^3",
            si_unit="m^3",
        ),
    ),
    output=VariableSpec(
        name="rho_solute",
        symbol="rho_solute",
        description="Solute mass concentration",
        dimension="M L^-3",
        si_unit="kg/m^3",
    ),
    evaluator=_evaluate,
    references=(
        openstax_section(
            "chemistry-2e",
            "3-4-other-units-for-solution-concentrations",
            "3.4 Other Units for Solution Concentrations",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"m_solute": 0.002, "V": 0.001},
            expected=2,
            note="2 g per L equals 2 kg/m^3.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"m_solute": 0, "V": 1},
            expected=0,
            note="No solute gives zero mass concentration.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "Derived result: Combine the mass-per-volume concentration definition with SI volume units.",
        "This is solute mass per solution volume, not the density of the entire solution.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemistry", "mass concentration"),
)
