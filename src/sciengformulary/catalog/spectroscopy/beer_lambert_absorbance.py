"""Beer-Lambert absorbance in SI reference units."""

from sciengformulary.catalog._domain import finite_result, non_negative
from sciengformulary.catalog._sources import (
    harvey_analytical_chemistry,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(epsilon: float, l: float, c: float) -> float:  # noqa: E741 - symbols as written in the source
    non_negative("epsilon", epsilon)
    non_negative("l", l)
    non_negative("c", c)
    return finite_result(epsilon * l * c)


beer_lambert_absorbance = FormulaSpec(
    id="spectroscopy.beer_lambert_absorbance",
    name="Beer Lambert Absorbance",
    equation="A = epsilon*l*c",
    description="Beer-Lambert absorbance in SI reference units.",
    inputs=(
        VariableSpec(
            name="epsilon",
            symbol="epsilon",
            description="Decadic molar absorption coefficient",
            dimension="L^2 N^-1",
            si_unit="m^2/mol",
        ),
        VariableSpec(
            name="l", symbol="l", description="Absorption path length", dimension="L", si_unit="m"
        ),
        VariableSpec(
            name="c",
            symbol="c",
            description="Absorber concentration",
            dimension="N L^-3",
            si_unit="mol/m^3",
        ),
    ),
    output=VariableSpec(
        name="A", symbol="A", description="Decadic absorbance", dimension="1", si_unit="-"
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
            inputs={"epsilon": 10, "l": 0.01, "c": 2},
            expected=0.2,
            note="100 L/(mol cm), 1 cm, 0.002 mol/L converted to SI gives 0.2.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"epsilon": 10, "l": 0.01, "c": 0},
            expected=0,
            note="No absorber gives zero ideal absorbance.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "Homogeneous absorbing medium and suitably narrow spectral bandwidth.",
        "No significant scattering, stray light or concentration-dependent chemical changes.",
        "epsilon is decadic, not Napierian; use a consistent coefficient and concentration convention.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "spectroscopy", "beer lambert absorbance"),
)
