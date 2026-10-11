"""Activity-based water autoionization product."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import (
    harvey_analytical_chemistry,
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(a_H: float, a_OH: float) -> float:
    positive("a_H", a_H)
    positive("a_OH", a_OH)
    return finite_result(a_H * a_OH)


water_ion_product = FormulaSpec(
    id="chemical_equilibrium.water_ion_product",
    name="Water Ion Product",
    equation="Kw = a_H * a_OH",
    description="Activity-based water autoionization product.",
    inputs=(
        VariableSpec(
            name="a_H",
            symbol="a_H",
            description="Dimensionless hydrogen-ion activity",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="a_OH",
            symbol="a_OH",
            description="Dimensionless hydroxide-ion activity",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="Kw", symbol="Kw", description="Water ion product", dimension="1", si_unit="-"
    ),
    evaluator=_evaluate,
    references=(
        openstax_section(
            "chemistry-2e",
            "14-3-relative-strengths-of-acids-and-bases",
            "14.3 Relative Strengths of Acids and Bases",
            accessed="2026-10-10",
        ),
        harvey_analytical_chemistry(
            "06%3A_Equilibrium_Chemistry/6.09%3A_Activity_Effects",
            "6.9: Activity Effects",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"a_H": 1e-07, "a_OH": 1e-07},
            expected=1e-14,
            note="At a representative neutral condition 1e-7 times 1e-7 = 1e-14.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"a_H": 0.001, "a_OH": 1e-11},
            expected=1e-14,
            note="1e-3 times 1e-11 = 1e-14.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Aqueous solution with solvent-water activity included in the conventional constant.",
        "Use equilibrium activities; Kw varies with temperature and is not universally 1e-14.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemical equilibrium", "water ion product"),
)
