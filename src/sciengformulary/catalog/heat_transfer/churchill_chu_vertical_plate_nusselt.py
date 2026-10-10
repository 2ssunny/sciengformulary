"""Churchill-Chu Vertical Plate Natural Convection.

Nu_L = (0.825 + 0.387 Ra_L^(1/6) / (1 + (0.492/Pr)^(9/16))^(8/27))^2.
"""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(Ra_L: float, Pr: float) -> float:  # noqa: N803 - symbols as written in the source
    positive("Ra_L", Ra_L)
    positive("Pr", Pr)
    # The source states no lower or upper limit on Ra_L or Pr for this form.
    denominator = (1.0 + (0.492 / Pr) ** (9.0 / 16.0)) ** (8.0 / 27.0)
    return finite_result((0.825 + 0.387 * Ra_L ** (1.0 / 6.0) / denominator) ** 2)


churchill_chu_vertical_plate_nusselt = FormulaSpec(
    id="heat_transfer.churchill_chu_vertical_plate_nusselt",
    name="Churchill-Chu Vertical Plate Natural Convection",
    equation="Nu_L = (0.825 + 0.387 * Ra_L^(1/6) / (1 + (0.492 / Pr)^(9/16))^(8/27))^2",
    description=(
        "Average Nusselt number for natural convection on a vertical isothermal or uniform-flux "
        "plate, one expression spanning laminar, transitional and turbulent boundary layers "
        "and all Prandtl numbers. A separate laminar-only form is more accurate when the "
        "boundary layer is known to be laminar."
    ),
    inputs=(
        VariableSpec(
            name="Ra_L",
            symbol="Ra_L",
            description="Rayleigh number based on the plate height, positive",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="Pr",
            symbol="Pr",
            description="Prandtl number, positive",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="Nu_L",
        symbol="Nu_L",
        description="Average Nusselt number h L / k based on the plate height",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        lienhard_heat_transfer("sec. 8.3, eq. (8.13b), p. 420", accessed=ENGINEERING_ACCESSED),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"Ra_L": 1814700000.0, "Pr": 0.69},
            expected=147.16185223770617,
            rel_tol=1e-12,
            note="Ra = 2.63e9 * 0.69; evaluated with 50-digit arithmetic (mpmath).",
        ),
        VerificationCase(
            inputs={"Ra_L": 1000000000000.0, "Pr": 7.0},
            expected=1389.0728802931085,
            rel_tol=1e-12,
            note="Turbulent regime, water-like Prandtl number; 50-digit arithmetic.",
        ),
        VerificationCase(
            inputs={"Ra_L": 1.0, "Pr": 0.71},
            expected=1.3211667381810492,
            rel_tol=1e-12,
            note="Very small Rayleigh number; 50-digit arithmetic (mpmath).",
        ),
    ),
    assumptions=(
        "Vertical plate (or vertical surface) in a large quiescent fluid, with either a uniform "
        "wall temperature or a uniform wall heat flux.",
        "The source states the expression for all Ra_L and Pr, so the evaluator only requires "
        "both to be positive. In the laminar range a separate laminar relation of the source "
        "is more accurate.",
        "All properties are evaluated at the film temperature, the mean of the wall and "
        "ambient temperatures.",
        "Dimensionless; valid in any consistent unit system.",
    ),
    tags=("Nusselt number", "natural convection", "vertical plate", "Churchill-Chu"),
)
