"""Fourier's Law (One-Dimensional): q = -k * dT/dx."""

from sciengformulary.catalog._sources import lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(k: float, dTdx: float) -> float:  # noqa: N803 - symbols as written in the source
    return -k * dTdx


fourier_conduction_heat_flux = FormulaSpec(
    id="heat_transfer.fourier_conduction_heat_flux",
    name="Fourier's Law (One-Dimensional)",
    equation="q = -k * dT/dx",
    description=(
        "Conductive heat flux in a solid or stationary fluid, proportional to the temperature "
        "gradient and directed down it."
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
            name="dTdx",
            symbol="dT/dx",
            description="Temperature gradient along x",
            dimension="Theta L^-1",
            si_unit="K/m",
        ),
    ),
    output=VariableSpec(
        name="q",
        symbol="q",
        description="Heat flux in the +x direction",
        dimension="M T^-3",
        si_unit="W/m^2",
    ),
    evaluator=_evaluate,
    references=(
        # The sheet writes the rate Qdot = -k A dT/dx; this is the same law per unit area.
        lienhard_heat_transfer("sec. 1.3, eq. (1.8)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"k": 34.0, "dTdx": -2000.0},
            expected=68000.0,
            rel_tol=1e-12,
            note=(
                "Worked example in the cited section: lead slab, k = 34 W/(m K), 110 C to 50 C "
                "across 0.03 m gives q = 68000 W/m^2."
            ),
        ),
    ),
    assumptions=(
        "Isotropic material; for anisotropic solids conductivity is a tensor.",
        "Continuum conduction; not for rarefied gases or nanoscale structures.",
    ),
    tags=("Fourier's law", "conduction", "heat flux", "thermal conductivity"),
)
