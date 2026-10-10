"""Schmidt Number: Sc = nu / D_AB."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    nu: float,
    D_AB: float,  # noqa: N803
) -> float:
    positive("nu", nu)
    positive("D_AB", D_AB)
    return finite_result(nu / D_AB)


schmidt_number = FormulaSpec(
    id="heat_transfer.schmidt_number",
    name="Schmidt Number",
    equation="Sc = nu / D_AB",
    description="Ratio of momentum diffusivity to mass diffusivity of a fluid mixture.",
    inputs=(
        VariableSpec(
            name="nu",
            symbol=r"\nu",
            description="Kinematic viscosity",
            dimension="L^2 T^-1",
            si_unit="m^2/s",
        ),
        VariableSpec(
            name="D_AB",
            symbol="D_{AB}",
            description="Binary mass diffusivity of species A in B",
            dimension="L^2 T^-1",
            si_unit="m^2/s",
        ),
    ),
    output=VariableSpec(
        name="Sc",
        symbol="Sc",
        description="Schmidt number",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes the binary diffusion coefficient as D_12 for a binary mixture.
        lienhard_heat_transfer("sec. 11.3, eq. (11.27), p. 632", accessed=ENGINEERING_ACCESSED),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"nu": 6e-07, "D_AB": 1e-09},
            expected=600.0,
            rel_tol=1e-12,
            note="Liquid-like values; hand calculation 6e-7 / 1e-9 = 600, exact in mpmath.",
        ),
        VerificationCase(
            inputs={"nu": 1.5e-05, "D_AB": 2.5e-05},
            expected=0.6,
            rel_tol=1e-12,
            note="Gas-like values; hand calculation 1.5e-5 / 2.5e-5 = 0.6.",
        ),
    ),
    assumptions=(
        "D_AB is the binary diffusion coefficient (or an effective one) of the diffusing "
        "species in the mixture, at the same temperature and pressure as nu.",
        "nu and D_AB must be finite and positive; otherwise ValueError is raised.",
        "Dimensionally homogeneous: nu and D_AB in the same units.",
    ),
    tags=("Schmidt number", "dimensionless group", "mass transfer", "diffusivity"),
)
