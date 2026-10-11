"""Titrant volume at reaction equivalence."""

from sciengformulary.catalog._domain import (
    finite_result,
    integer,
    non_negative,
    positive,
)
from sciengformulary.core import (
    FormulaSpec,
    ReferenceSpec,
    VariableSpec,
    VerificationCase,
)


def _evaluate(
    c_analyte: float, V_analyte: float, c_titrant: float, nu_titrant: float, nu_analyte: float
) -> float:
    non_negative("c_analyte", c_analyte)
    positive("V_analyte", V_analyte)
    positive("c_titrant", c_titrant)
    nu_titrant = integer("nu_titrant", nu_titrant, minimum=1)
    nu_analyte = integer("nu_analyte", nu_analyte, minimum=1)
    return finite_result((c_analyte / c_titrant) * V_analyte * (nu_titrant / nu_analyte))


titration_equivalence_volume = FormulaSpec(
    id="chemistry.titration_equivalence_volume",
    name="Titration Equivalence Volume",
    equation="V_titrant = c_analyte*V_analyte*nu_titrant/(c_titrant*nu_analyte)",
    description="Titrant volume at reaction equivalence.",
    inputs=(
        VariableSpec(
            name="c_analyte",
            symbol="c_analyte",
            description="Formal analyte concentration",
            dimension="N L^-3",
            si_unit="mol/m^3",
        ),
        VariableSpec(
            name="V_analyte",
            symbol="V_analyte",
            description="Analyte aliquot volume",
            dimension="L^3",
            si_unit="m^3",
        ),
        VariableSpec(
            name="c_titrant",
            symbol="c_titrant",
            description="Titrant concentration",
            dimension="N L^-3",
            si_unit="mol/m^3",
        ),
        VariableSpec(
            name="nu_titrant",
            symbol="nu_titrant",
            description="Titrant coefficient in the balanced reaction",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="nu_analyte",
            symbol="nu_analyte",
            description="Analyte coefficient in the balanced reaction",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="V_titrant",
        symbol="V_titrant",
        description="Theoretical titrant volume at stoichiometric equivalence",
        dimension="L^3",
        si_unit="m^3",
    ),
    evaluator=_evaluate,
    references=(
        ReferenceSpec(
            source_type="official_web",
            title="14.7 Acid-Base Titrations",
            organization="OpenStax",
            url="https://openstax.org/books/chemistry-2e/pages/14-7-acid-base-titrations",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={
                "c_analyte": 100,
                "V_analyte": 2.5e-05,
                "c_titrant": 100,
                "nu_titrant": 1,
                "nu_analyte": 1,
            },
            expected=2.5e-05,
            note="Equal concentrations and 1:1 stoichiometry require equal volumes.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={
                "c_analyte": 100,
                "V_analyte": 2.5e-05,
                "c_titrant": 100,
                "nu_titrant": 2,
                "nu_analyte": 1,
            },
            expected=5e-05,
            note="Two titrant units per analyte require twice the volume.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Derived result: Combine amount concentration with the balanced-reaction molar ratio.",
        "A defined quantitative titration reaction with known stoichiometry and no interfering reactions.",
        "Stoichiometric equivalence volume is not necessarily the experimental indicator endpoint.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemistry", "titration equivalence volume"),
)
