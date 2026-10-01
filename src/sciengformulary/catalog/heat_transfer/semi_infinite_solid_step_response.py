"""Semi-Infinite Solid After a Step Change in Surface Temperature."""

import math

from sciengformulary.catalog._sources import lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(x: float, alpha: float, t: float) -> float:
    return math.erf(x / (2.0 * math.sqrt(alpha * t)))


semi_infinite_solid_step_response = FormulaSpec(
    id="heat_transfer.semi_infinite_solid_step_response",
    name="Semi-Infinite Solid After a Step Change in Surface Temperature",
    equation="(T - T_s) / (T_i - T_s) = erf(x / (2 * sqrt(alpha * t)))",
    description=(
        "Dimensionless temperature inside a thick solid, initially uniform, at depth x and time t "
        "after its surface is suddenly held at a new temperature."
    ),
    inputs=(
        VariableSpec(
            name="x",
            symbol="x",
            description="Depth below the surface",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="alpha",
            symbol=r"\alpha",
            description="Thermal diffusivity of the solid",
            dimension="L^2 T^-1",
            si_unit="m^2/s",
        ),
        VariableSpec(
            name="t",
            symbol="t",
            description="Time since the surface temperature changed",
            dimension="T",
            si_unit="s",
        ),
    ),
    output=VariableSpec(
        name="theta",
        symbol=r"\Theta",
        description="Dimensionless temperature (T - T_s) / (T_i - T_s)",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes the surface temperature as T_inf and the similarity variable as zeta =
        # x / sqrt(alpha t), with Theta = erf(zeta / 2).
        lienhard_heat_transfer("sec. 5.6, eqs. (5.44), (5.50)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"x": 0.01, "alpha": 1e-05, "t": 10.0},
            expected=0.5204998778130465,
            rel_tol=1e-12,
            note="Independent evaluation of erf(0.5) by its Maclaurin series in 40-digit decimal.",
        ),
    ),
    assumptions=(
        "Semi-infinite solid: the temperature change has not yet reached the far side of the body.",
        "Uniform initial temperature, constant properties, no heat generation; surface "
        "temperature held exactly constant.",
    ),
    tags=("transient conduction", "error function", "semi-infinite solid", "diffusion"),
)
