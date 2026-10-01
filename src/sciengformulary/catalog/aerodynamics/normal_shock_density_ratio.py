"""Normal Shock Density Ratio: rho2 / rho1 = (gamma + 1) * M1^2 / ((gamma - 1) * M1^2 + 2)."""

from sciengformulary.catalog._sources import naca_report_1135
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(M1: float, gamma: float) -> float:  # noqa: N803 - symbols as written in the source
    return (gamma + 1.0) * M1**2 / ((gamma - 1.0) * M1**2 + 2.0)


normal_shock_density_ratio = FormulaSpec(
    id="aerodynamics.normal_shock_density_ratio",
    name="Normal Shock Density Ratio",
    equation="rho2 / rho1 = (gamma + 1) * M1^2 / ((gamma - 1) * M1^2 + 2)",
    description=(
        "Jump in density (equal to the drop in normal velocity, u1/u2) across a stationary normal "
        "shock wave."
    ),
    inputs=(
        VariableSpec(
            name="M1",
            symbol="M_1",
            description="Mach number just upstream of the normal shock (must exceed 1)",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="gamma",
            symbol=r"\gamma",
            description="Ratio of specific heats c_p / c_v of the gas",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="rho_ratio",
        symbol=r"\rho_2/\rho_1",
        description="Downstream over upstream density",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        naca_report_1135("eq. (94); Table II, p. 635"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"M1": 2.5, "gamma": 1.4},
            expected=3.333,
            rel_tol=0.0002,
            note=(
                "Published value: NACA Rep. 1135, Table II, M_1 = 2.50 gives rho_2/rho_1 = 3.333 "
                "(four significant figures)."
            ),
        ),
        VerificationCase(
            inputs={"M1": 2.0, "gamma": 1.4},
            expected=2.6666666666666665,
            rel_tol=1e-12,
            note="Exact arithmetic: 2.4 * 4 / (0.4 * 4 + 2) = 9.6 / 3.6 = 8/3.",
        ),
    ),
    assumptions=(
        "Steady, one-dimensional flow through a stationary normal shock in a calorically "
        "perfect gas; the shock is treated as a discontinuity with no heat addition.",
        "Calorically perfect gas: constant specific heats, so gamma is constant. The source "
        "treats calorically imperfect (high-temperature) gases separately; do not use this "
        "form for them.",
        "M1 must be greater than 1. The ratio approaches (gamma + 1)/(gamma - 1), 6 for air, "
        "as M1 grows.",
    ),
    tags=("normal shock", "shock wave", "Rankine-Hugoniot", "density ratio", "supersonic"),
)
