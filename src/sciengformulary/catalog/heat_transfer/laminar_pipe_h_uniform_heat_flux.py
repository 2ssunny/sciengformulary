"""Laminar Pipe Heat Transfer Coefficient (Uniform Wall Heat Flux): h = (48 / 11) * k / D."""

from sciengformulary.catalog._sources import lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(k: float, D: float) -> float:  # noqa: N803 - symbols as written in the source
    return 48.0 / 11.0 * k / D


laminar_pipe_h_uniform_heat_flux = FormulaSpec(
    id="heat_transfer.laminar_pipe_h_uniform_heat_flux",
    name="Laminar Pipe Heat Transfer Coefficient (Uniform Wall Heat Flux)",
    equation="h = (48 / 11) * k / D",
    description=(
        "Heat transfer coefficient for fully developed laminar flow in a circular pipe with "
        "uniform wall heat flux, from Nu_D = 48/11 (about 4.364)."
    ),
    inputs=(
        VariableSpec(
            name="k",
            symbol="k",
            description="Thermal conductivity of the fluid",
            dimension="M L T^-3 Theta^-1",
            si_unit="W/(m*K)",
        ),
        VariableSpec(
            name="D",
            symbol="D",
            description="Pipe inner diameter",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="h",
        symbol="h",
        description="Heat transfer coefficient based on wall minus bulk temperature",
        dimension="M T^-3 Theta^-1",
        si_unit="W/(m^2*K)",
    ),
    evaluator=_evaluate,
    references=(
        lienhard_heat_transfer("sec. 7.2, eq. (7.22)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"k": 0.6396, "D": 0.001},
            expected=2790.981818181818,
            rel_tol=1e-12,
            note=(
                "Worked example in the cited section: water in a 1 mm tube gives h = 2791 W/(m^2 "
                "K) (2790.98 before rounding)."
            ),
        ),
    ),
    assumptions=(
        "Fully developed laminar flow in a smooth circular pipe (hydrodynamically and "
        "thermally developed); not valid in the entrance region or for turbulent flow.",
        "Uniform heat flux at the wall (for example electric heating).",
    ),
    tags=("laminar flow", "pipe flow", "Nusselt number", "uniform heat flux", "internal flow"),
)
