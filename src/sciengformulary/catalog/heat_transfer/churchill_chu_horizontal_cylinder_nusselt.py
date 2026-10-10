"""Churchill-Chu Horizontal Cylinder Natural Convection.

Nu_D = (0.60 + 0.387 Ra_D^(1/6) / (1 + (0.559/Pr)^(9/16))^(8/27))^2.
"""

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

_RA_MIN = 1.0e-6


def _evaluate(Ra_D: float, Pr: float) -> float:  # noqa: N803 - symbols as written in the source
    if finite("Ra_D", Ra_D) < _RA_MIN:
        raise ValueError(f"Ra_D must be at least {_RA_MIN:g} for this correlation, got {Ra_D!r}.")
    positive("Pr", Pr)
    # The source form is [Ra / (1 + (0.559/Pr)^(9/16))^(16/9)]^(1/6); taking the sixth root
    # inside gives the exponent 8/27 on the denominator, used here.
    denominator = (1.0 + (0.559 / Pr) ** (9.0 / 16.0)) ** (8.0 / 27.0)
    return finite_result((0.60 + 0.387 * Ra_D ** (1.0 / 6.0) / denominator) ** 2)


churchill_chu_horizontal_cylinder_nusselt = FormulaSpec(
    id="heat_transfer.churchill_chu_horizontal_cylinder_nusselt",
    name="Churchill-Chu Horizontal Cylinder Natural Convection",
    equation="Nu_D = (0.60 + 0.387 * Ra_D^(1/6) / (1 + (0.559 / Pr)^(9/16))^(8/27))^2",
    description=(
        "Average Nusselt number for natural convection from a long horizontal isothermal "
        "cylinder in an extensive quiescent fluid, over laminar and turbulent conditions. It "
        "differs from the vertical-plate form in its constants and applies only for "
        "Ra_D >= 1e-6."
    ),
    inputs=(
        VariableSpec(
            name="Ra_D",
            symbol="Ra_D",
            description="Rayleigh number based on the cylinder diameter, at least 1e-6",
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
        name="Nu_D",
        symbol="Nu_D",
        description="Average Nusselt number h D / k based on the cylinder diameter",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Derived rearrangement, not a new result: the source prints
        # {0.60 + 0.387 [Ra_D / (1 + (0.559/Pr)^(9/16))^(16/9)]^(1/6)}^2. Pulling the sixth
        # root through the quotient turns the exponent 16/9 into 8/27 (checked symbolically).
        lienhard_heat_transfer("sec. 8.4, eq. (8.29), pp. 430-431", accessed=ENGINEERING_ACCESSED),
        # Example 8.4 evaluates the correlation at Pr = 0.707 with film-temperature properties.
        lienhard_heat_transfer("sec. 8.4, Example 8.4, p. 431", accessed=ENGINEERING_ACCESSED),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"Ra_D": 0.0005762, "Pr": 0.707},
            expected=0.4797602017289283,
            rel_tol=1e-12,
            note=(
                "Rayleigh and Prandtl numbers of the textbook's Example 8.4 at its lowest "
                "gravity level (printed result 0.480); value from 50-digit arithmetic (mpmath)."
            ),
        ),
        VerificationCase(
            inputs={"Ra_D": 5.762, "Pr": 0.707},
            expected=1.0609626321876542,
            rel_tol=1e-12,
            note=(
                "Example 8.4 at a gravity level 10^4 times larger (printed result 1.061); "
                "value from 50-digit arithmetic (mpmath)."
            ),
        ),
        VerificationCase(
            inputs={"Ra_D": 1e-06, "Pr": 0.7},
            expected=0.39954060545245246,
            rel_tol=1e-12,
            note="Lower limit of the stated Rayleigh range; 50-digit arithmetic (mpmath).",
        ),
        VerificationCase(
            inputs={"Ra_D": 1814700000.0, "Pr": 0.69},
            expected=139.13493970073606,
            rel_tol=1e-12,
            note="High Rayleigh number; 50-digit arithmetic; an independent library agrees.",
        ),
    ),
    assumptions=(
        "Long horizontal isothermal cylinder in an extensive quiescent fluid; average Nusselt "
        "number over the circumference.",
        "Valid for Ra_D >= 1e-6 (laminar and turbulent); the evaluator raises ValueError below "
        "that. The source states no limit on Pr, so only Pr > 0 is required.",
        "Derived result: the evaluator uses the algebraically rearranged form with exponent "
        "8/27, equal to the source's bracketed form with exponent 16/9 inside the sixth root.",
        "All properties are evaluated at the film temperature, the mean of the wall and "
        "ambient temperatures. Dimensionless; valid in any consistent unit system.",
    ),
    tags=("Nusselt number", "natural convection", "horizontal cylinder", "Churchill-Chu"),
)
