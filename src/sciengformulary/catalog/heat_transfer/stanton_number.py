"""Stanton Number: St = Nu / (Re * Pr)."""

from sciengformulary.catalog._sources import lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    Nu: float,  # noqa: N803
    Re: float,  # noqa: N803
    Pr: float,  # noqa: N803
) -> float:
    return Nu / (Re * Pr)


stanton_number = FormulaSpec(
    id="heat_transfer.stanton_number",
    name="Stanton Number",
    equation="St = Nu / (Re * Pr)",
    description=(
        "Dimensionless heat transfer coefficient that compares the actual heat flux with the "
        "enthalpy flux carried by the stream."
    ),
    inputs=(
        VariableSpec(
            name="Nu",
            symbol="Nu",
            description="Nusselt number",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="Re",
            symbol="Re",
            description="Reynolds number (same length scale as Nu)",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="Pr",
            symbol="Pr",
            description="Prandtl number",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="St",
        symbol="St",
        description="Stanton number",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The source also writes St = h / (rho c_p u_inf).
        lienhard_heat_transfer("sec. 6.6, eq. (6.75)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"Nu": 100.0, "Re": 100000.0, "Pr": 0.7},
            expected=0.0014285714285714286,
            rel_tol=1e-12,
            note="Hand calculation: 100 / (1e5 * 0.7).",
        ),
    ),
    assumptions=(
        "Nu and Re based on the same length.",
    ),
    tags=("Stanton number", "dimensionless group", "Reynolds analogy"),
)
