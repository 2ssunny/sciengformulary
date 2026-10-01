"""Mach Number: M = V / a."""

from sciengformulary.catalog._sources import naca_report_1135, nasa_glenn
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(V: float, a: float) -> float:  # noqa: N803 - symbols as written in the source
    return V / a


mach_number = FormulaSpec(
    id="aerodynamics.mach_number",
    name="Mach Number",
    equation="M = V / a",
    description="Flow speed divided by the local speed of sound.",
    inputs=(
        VariableSpec(
            name="V",
            symbol="V",
            description="Flow speed",
            dimension="L T^-1",
            si_unit="m/s",
        ),
        VariableSpec(
            name="a",
            symbol="a",
            description="Local speed of sound at the same point",
            dimension="L T^-1",
            si_unit="m/s",
        ),
    ),
    output=VariableSpec(
        name="M",
        symbol="M",
        description="Mach number",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        naca_report_1135("eq. (30)"),
        nasa_glenn("Similarity Parameters", "similarity-parameters", 2024),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"V": 170.15, "a": 340.3},
            expected=0.5,
            rel_tol=1e-12,
            note="Hand calculation: 170.15 / 340.3 = 0.5.",
        ),
    ),
    assumptions=(
        "V and a must be taken at the same point; the local speed of sound depends on the "
        "local static temperature, not the freestream value.",
    ),
    tags=("mach number", "M", "compressibility", "similarity parameter"),
)
