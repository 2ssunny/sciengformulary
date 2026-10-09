"""Ohm's Law: V = I * R."""

from sciengformulary.catalog._sources import (
    lienhard_heat_transfer,
    openstax_university_physics,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(I: float, R: float) -> float:  # noqa: N803, E741 - symbols as written in the source
    return I * R


ohms_law_voltage = FormulaSpec(
    id="electrical.ohms_law_voltage",
    name="Ohm's Law",
    equation="V = I * R",
    description="Voltage across an ohmic resistor carrying a current.",
    inputs=(
        VariableSpec(
            name="I",
            symbol="I",
            description="Current through the resistor",
            dimension="I",
            si_unit="A",
        ),
        VariableSpec(
            name="R",
            symbol="R",
            description="Resistance",
            dimension="M L^2 T^-3 I^-2",
            si_unit="ohm",
        ),
    ),
    output=VariableSpec(
        name="V",
        symbol="V",
        description="Voltage (potential difference) across the resistor",
        dimension="M L^2 T^-3 I^-1",
        si_unit="V",
    ),
    evaluator=_evaluate,
    references=(
        openstax_university_physics(2, "9-4-ohms-law", "sec. 9.4, eq. (9.11)"),
        # The book prints I = V / R and R = L / (gamma A); V = I R is its rearrangement.
        lienhard_heat_transfer("sec. 2.3, eq. (2.18), p. 63"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"I": 2.0, "R": 5.0},
            expected=10.0,
            rel_tol=1e-12,
            note="Hand calculation: 2 * 5 = 10 V.",
        ),
    ),
    assumptions=(
        "Ohmic (linear) element at fixed temperature; diodes, lamps with heating filaments and "
        "similar devices do not obey it.",
    ),
    tags=("Ohm's law", "resistance", "voltage", "current", "circuit"),
)
