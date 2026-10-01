"""Thermal Diffusivity: alpha = k / (rho * c)."""

from sciengformulary.catalog._sources import lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(k: float, rho: float, c: float) -> float:
    return k / (rho * c)


thermal_diffusivity = FormulaSpec(
    id="heat_transfer.thermal_diffusivity",
    name="Thermal Diffusivity",
    equation="alpha = k / (rho * c)",
    description=(
        "Ratio of thermal conductivity to volumetric heat capacity: how quickly temperature "
        "changes spread through a material."
    ),
    inputs=(
        VariableSpec(
            name="k",
            symbol="k",
            description="Thermal conductivity",
            dimension="M L T^-3 Theta^-1",
            si_unit="W/(m*K)",
        ),
        VariableSpec(
            name="rho",
            symbol=r"\rho",
            description="Density",
            dimension="M L^-3",
            si_unit="kg/m^3",
        ),
        VariableSpec(
            name="c",
            symbol="c",
            description="Specific heat capacity",
            dimension="L^2 T^-2 Theta^-1",
            si_unit="J/(kg*K)",
        ),
    ),
    output=VariableSpec(
        name="alpha",
        symbol=r"\alpha",
        description="Thermal diffusivity",
        dimension="L^2 T^-1",
        si_unit="m^2/s",
    ),
    evaluator=_evaluate,
    references=(
        lienhard_heat_transfer("sec. 1.3"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"k": 237.0, "rho": 2702.0, "c": 903.0},
            expected=9.713488962279695e-05,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation (aluminium-like values).",
        ),
    ),
    assumptions=(
        "Properties at the same temperature; for gases use c_p.",
    ),
    tags=("thermal diffusivity", "conduction", "transient heat transfer"),
)
