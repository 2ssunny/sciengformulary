"""Additive two-species absorbance."""

from sciengformulary.catalog._domain import finite_result, non_negative
from sciengformulary.catalog._sources import (
    harvey_analytical_chemistry,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(l: float, epsilon_1: float, c1: float, epsilon_2: float, c2: float) -> float:  # noqa: E741 - symbols as written in the source
    non_negative("l", l)
    non_negative("epsilon_1", epsilon_1)
    non_negative("c1", c1)
    non_negative("epsilon_2", epsilon_2)
    non_negative("c2", c2)
    return finite_result(l * (epsilon_1 * c1 + epsilon_2 * c2))


two_component_absorbance = FormulaSpec(
    id="spectroscopy.two_component_absorbance",
    name="Two Component Absorbance",
    equation="A = l*(epsilon_1*c1 + epsilon_2*c2)",
    description="Additive two-species absorbance.",
    inputs=(
        VariableSpec(
            name="l",
            symbol="l",
            description="Common absorption path length",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="epsilon_1",
            symbol="epsilon_1",
            description="Decadic molar coefficient of species 1",
            dimension="L^2 N^-1",
            si_unit="m^2/mol",
        ),
        VariableSpec(
            name="c1",
            symbol="c1",
            description="Concentration of species 1",
            dimension="N L^-3",
            si_unit="mol/m^3",
        ),
        VariableSpec(
            name="epsilon_2",
            symbol="epsilon_2",
            description="Decadic molar coefficient of species 2",
            dimension="L^2 N^-1",
            si_unit="m^2/mol",
        ),
        VariableSpec(
            name="c2",
            symbol="c2",
            description="Concentration of species 2",
            dimension="N L^-3",
            si_unit="mol/m^3",
        ),
    ),
    output=VariableSpec(
        name="A", symbol="A", description="Total decadic absorbance", dimension="1", si_unit="-"
    ),
    evaluator=_evaluate,
    references=(
        harvey_analytical_chemistry(
            "10%3A_Spectroscopic_Methods/10.02%3A_Spectroscopy_Based_on_Absorption",
            "10.2: Spectroscopy Based on Absorption",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"l": 0.01, "epsilon_1": 10, "c1": 2, "epsilon_2": 20, "c2": 1},
            expected=0.4,
            note="Independent absorbances 0.2+0.2=0.4.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"l": 0.01, "epsilon_1": 10, "c1": 0, "epsilon_2": 20, "c2": 0},
            expected=0,
            note="Absent absorbers give zero total absorbance.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "Two independent absorbers at the same wavelength, each within Beer-Lambert conditions.",
        "Concentrations are actual absorbing-species concentrations after any equilibrium reaction.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "spectroscopy", "two component absorbance"),
)
