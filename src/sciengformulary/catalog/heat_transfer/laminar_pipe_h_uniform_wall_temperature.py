"""Laminar Pipe Heat Transfer Coefficient (Uniform Wall Temperature): h = 3.657 * k / D."""

from sciengformulary.catalog._sources import lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(k: float, D: float) -> float:  # noqa: N803 - symbols as written in the source
    return 3.657 * k / D


laminar_pipe_h_uniform_wall_temperature = FormulaSpec(
    id="heat_transfer.laminar_pipe_h_uniform_wall_temperature",
    name="Laminar Pipe Heat Transfer Coefficient (Uniform Wall Temperature)",
    equation="h = 3.657 * k / D",
    description=(
        "Heat transfer coefficient for fully developed laminar flow in a circular pipe with "
        "uniform wall temperature, from Nu_D = 3.657."
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
        lienhard_heat_transfer("sec. 7.2, eq. (7.23)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"k": 0.6, "D": 0.01},
            expected=219.42,
            rel_tol=1e-12,
            note="Hand calculation: 3.657 * 0.6 / 0.01 = 219.42 W/(m^2 K).",
        ),
    ),
    assumptions=(
        "Fully developed laminar flow in a smooth circular pipe (hydrodynamically and "
        "thermally developed); not valid in the entrance region or for turbulent flow.",
        "Uniform wall temperature (for example condensing steam outside).",
    ),
    tags=("laminar flow", "pipe flow", "Nusselt number", "isothermal wall", "internal flow"),
)
