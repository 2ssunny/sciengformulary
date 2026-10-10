"""Rayleigh Number: Ra_L = Gr_L * Pr."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    Gr_L: float,  # noqa: N803
    Pr: float,  # noqa: N803
) -> float:
    non_negative("Gr_L", Gr_L)
    positive("Pr", Pr)
    return finite_result(Gr_L * Pr)


rayleigh_number = FormulaSpec(
    id="heat_transfer.rayleigh_number",
    name="Rayleigh Number",
    equation="Ra_L = Gr_L * Pr",
    description=(
        "Product of the Grashof and Prandtl numbers, the main independent variable of "
        "natural-convection correlations."
    ),
    inputs=(
        VariableSpec(
            name="Gr_L",
            symbol="Gr_L",
            description="Grashof number based on the length L",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="Pr",
            symbol="Pr",
            description="Prandtl number of the fluid",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="Ra_L",
        symbol="Ra_L",
        description="Rayleigh number based on the length L",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The source also gives the equivalent g beta dT L^3 / (alpha nu).
        lienhard_heat_transfer("sec. 8.3, eq. (8.11), p. 419", accessed=ENGINEERING_ACCESSED),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"Gr_L": 4600000000.0, "Pr": 1.2},
            expected=5520000000.0,
            rel_tol=1e-12,
            note="Hand calculation: 4.6e9 * 1.2 = 5.52e9; 50-digit mpmath agrees.",
        ),
        VerificationCase(
            inputs={"Gr_L": 0.0, "Pr": 0.7},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Zero Grashof number gives zero.",
        ),
    ),
    assumptions=(
        "Gr_L and Pr must use the same characteristic length and fluid property temperature, "
        "so that the product is the Rayleigh number of one correlation.",
        "Gr_L must be finite and not negative; Pr must be finite and positive; otherwise "
        "ValueError is raised.",
        "Dimensionless: no unit system enters.",
    ),
    tags=("Rayleigh number", "dimensionless group", "natural convection", "buoyancy"),
)
