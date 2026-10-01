"""Biot Number: Bi = h * L / k_body."""

from sciengformulary.catalog._sources import lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    h: float,
    L: float,  # noqa: N803
    k_body: float,
) -> float:
    return h * L / k_body


biot_number = FormulaSpec(
    id="heat_transfer.biot_number",
    name="Biot Number",
    equation="Bi = h * L / k_body",
    description=(
        "Ratio of internal conduction resistance to external convection resistance of a body; "
        "small values justify a uniform-temperature (lumped) model."
    ),
    inputs=(
        VariableSpec(
            name="h",
            symbol="h",
            description="Convective heat transfer coefficient",
            dimension="M T^-3 Theta^-1",
            si_unit="W/(m^2*K)",
        ),
        VariableSpec(
            name="L",
            symbol="L",
            description=(
                "Characteristic length of the body (often volume over surface area, or the "
                "source's stated dimension)"
            ),
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="k_body",
            symbol="k_b",
            description="Thermal conductivity of the solid body",
            dimension="M L T^-3 Theta^-1",
            si_unit="W/(m*K)",
        ),
    ),
    output=VariableSpec(
        name="Bi",
        symbol="Bi",
        description="Biot number",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The sheet writes the length as r0 (the body's characteristic dimension).
        lienhard_heat_transfer("sec. 1.3"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"h": 250.0, "L": 0.0005, "k_body": 45.0},
            expected=0.002777777777777778,
            rel_tol=1e-12,
            note=(
                "Worked example in the cited section: thermocouple bead with h = 250, L = 0.001/2 "
                "m, k = 45 gives Bi = 0.00278."
            ),
        ),
    ),
    assumptions=(
        "k is the solid's conductivity, unlike the Nusselt number.",
        "The threshold for lumping (commonly 0.1) depends on the length chosen.",
    ),
    tags=("Biot number", "lumped capacitance", "dimensionless group", "conduction"),
)
