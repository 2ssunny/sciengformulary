"""Laminar Flat-Plate Local Nusselt Number: Nu_x = 0.332 * Re_x^(1/2) * Pr^(1/3)."""

from sciengformulary.catalog._sources import lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(Re_x: float, Pr: float) -> float:  # noqa: N803 - symbols as written in the source
    return 0.332 * Re_x**0.5 * Pr ** (1.0 / 3.0)


laminar_flat_plate_local_nusselt = FormulaSpec(
    id="heat_transfer.laminar_flat_plate_local_nusselt",
    name="Laminar Flat-Plate Local Nusselt Number",
    equation="Nu_x = 0.332 * Re_x^(1/2) * Pr^(1/3)",
    description="Local Nusselt number of a laminar boundary layer on an isothermal flat plate.",
    inputs=(
        VariableSpec(
            name="Re_x",
            symbol="Re_x",
            description="Reynolds number based on distance x from the leading edge",
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
        name="Nu_x",
        symbol="Nu_x",
        description="Local Nusselt number h x / k",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        lienhard_heat_transfer("sec. 6.5, eq. (6.58)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"Re_x": 100000.0, "Pr": 0.7},
            expected=93.2189264376131,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation of 0.332 sqrt(1e5) 0.7^(1/3).",
        ),
    ),
    assumptions=(
        "Steady, laminar, two-dimensional boundary layer on a flat plate with zero pressure "
        "gradient; local value at distance x from the leading edge. Not valid once the "
        "boundary layer has become turbulent.",
        "Uniform wall temperature; Pr of at least about 0.6 (within 2 % of the exact solution "
        "there). Not for liquid metals.",
        "Unheated starting lengths and uniform heat flux need other forms.",
    ),
    tags=("Nusselt number", "flat plate", "boundary layer", "laminar", "Pohlhausen"),
)
