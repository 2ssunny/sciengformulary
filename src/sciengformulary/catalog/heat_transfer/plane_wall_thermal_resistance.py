"""Thermal Resistance of a Plane Wall: R_t = L / (k * A)."""

from sciengformulary.catalog._sources import lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    L: float,  # noqa: N803
    k: float,
    A: float,  # noqa: N803
) -> float:
    return L / (k * A)


plane_wall_thermal_resistance = FormulaSpec(
    id="heat_transfer.plane_wall_thermal_resistance",
    name="Thermal Resistance of a Plane Wall",
    equation="R_t = L / (k * A)",
    description=(
        "Conductive thermal resistance of a flat slab; layers in series add their resistances like "
        "electrical resistors."
    ),
    inputs=(
        VariableSpec(
            name="L",
            symbol="L",
            description="Wall thickness",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="k",
            symbol="k",
            description="Thermal conductivity",
            dimension="M L T^-3 Theta^-1",
            si_unit="W/(m*K)",
        ),
        VariableSpec(
            name="A",
            symbol="A",
            description="Wall area normal to the heat flow",
            dimension="L^2",
            si_unit="m^2",
        ),
    ),
    output=VariableSpec(
        name="R_t",
        symbol="R_t",
        description="Thermal resistance",
        dimension="M^-1 L^-2 T^3 Theta",
        si_unit="K/W",
    ),
    evaluator=_evaluate,
    references=(
        # The sheet's per-area resistance dx/k equals A times this value.
        lienhard_heat_transfer("sec. 2.3, eq. (2.16)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"L": 0.03, "k": 34.0, "A": 0.4},
            expected=0.0022058823529411764,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation of 0.03 / (34 * 0.4).",
        ),
    ),
    assumptions=(
        "Steady state; constant thermal conductivity.",
        "One-dimensional conduction with no internal heat generation.",
    ),
    tags=("thermal resistance", "R-value", "conduction", "electrical analogy"),
)
