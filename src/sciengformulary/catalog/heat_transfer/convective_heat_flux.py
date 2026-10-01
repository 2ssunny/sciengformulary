"""Newton's Law of Cooling: q = h * (T_s - T_inf)."""

from sciengformulary.catalog._sources import lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    h: float,
    T_s: float,  # noqa: N803
    T_inf: float,  # noqa: N803
) -> float:
    return h * (T_s - T_inf)


convective_heat_flux = FormulaSpec(
    id="heat_transfer.convective_heat_flux",
    name="Newton's Law of Cooling",
    equation="q = h * (T_s - T_inf)",
    description="Convective heat flux from a surface to the surrounding fluid.",
    inputs=(
        VariableSpec(
            name="h",
            symbol="h",
            description="Convective heat transfer coefficient",
            dimension="M T^-3 Theta^-1",
            si_unit="W/(m^2*K)",
        ),
        VariableSpec(
            name="T_s",
            symbol="T_s",
            description="Surface temperature",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="T_inf",
            symbol=r"T_\infty",
            description="Fluid temperature away from the surface",
            dimension="Theta",
            si_unit="K",
        ),
    ),
    output=VariableSpec(
        name="q",
        symbol="q",
        description="Heat flux from the surface into the fluid",
        dimension="M T^-3",
        si_unit="W/m^2",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes q = h (T_body - T_inf). The sheet's q = h (T_f - T_w) is the same law
        # with the opposite sign convention (flux into the wall).
        lienhard_heat_transfer("sec. 1.3, eq. (1.17)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"h": 25.0, "T_s": 80.0, "T_inf": 20.0},
            expected=1500.0,
            rel_tol=1e-12,
            note="Hand calculation: 25 * (80 - 20) = 1500 W/m^2.",
        ),
    ),
    assumptions=(
        "h is an empirical or correlated coefficient for the actual flow; it is not a material "
        "property.",
        "Valid for forced or natural convection once h is known; for natural convection h "
        "itself depends on the temperature difference.",
    ),
    tags=("convection", "Newton's law of cooling", "heat transfer coefficient", "film"),
)
