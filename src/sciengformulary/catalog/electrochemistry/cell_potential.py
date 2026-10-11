"""Cell potential from compatible reduction potentials."""

from sciengformulary.catalog._domain import finite, finite_result
from sciengformulary.core import (
    FormulaSpec,
    ReferenceSpec,
    VariableSpec,
    VerificationCase,
)


def _evaluate(E_cathode: float, E_anode: float) -> float:
    finite("E_cathode", E_cathode)
    finite("E_anode", E_anode)
    return finite_result(E_cathode - E_anode)


cell_potential = FormulaSpec(
    id="electrochemistry.cell_potential",
    name="Cell Potential",
    equation="E_cell = E_cathode - E_anode",
    description="Cell potential from compatible reduction potentials.",
    inputs=(
        VariableSpec(
            name="E_cathode",
            symbol="E_cathode",
            description="Cathode reduction potential",
            dimension="M L^2 T^-3 I^-1",
            si_unit="V",
        ),
        VariableSpec(
            name="E_anode",
            symbol="E_anode",
            description="Anode reduction potential",
            dimension="M L^2 T^-3 I^-1",
            si_unit="V",
        ),
    ),
    output=VariableSpec(
        name="E_cell",
        symbol="E_cell",
        description="Cell potential",
        dimension="M L^2 T^-3 I^-1",
        si_unit="V",
    ),
    evaluator=_evaluate,
    references=(
        ReferenceSpec(
            source_type="official_web",
            title="17.3 Electrode and Cell Potentials",
            organization="OpenStax",
            url="https://openstax.org/books/chemistry-2e/pages/17-3-electrode-and-cell-potentials",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"E_cathode": 0.34, "E_anode": -0.76},
            expected=1.1,
            note="0.34 - (-0.76) = 1.10 V.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"E_cathode": 0.2, "E_anode": 0.2},
            expected=0,
            note="Identical reduction potentials give zero difference.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "Both potentials are reduction potentials on the same reference scale.",
        "Standard cell potential requires standard half-cell potentials; nonstandard half-cells require their actual potentials.",
        "Do not multiply potentials by stoichiometric coefficients.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "electrochemistry", "cell potential"),
)
