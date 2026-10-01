"""Normal Shock Static Pressure Ratio: p2 / p1 = (2 * gamma * M1^2 - (gamma - 1)) / (gamma + 1)."""

from sciengformulary.catalog._sources import naca_report_1135
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(M1: float, gamma: float) -> float:  # noqa: N803 - symbols as written in the source
    return (2.0 * gamma * M1**2 - (gamma - 1.0)) / (gamma + 1.0)


normal_shock_pressure_ratio = FormulaSpec(
    id="aerodynamics.normal_shock_pressure_ratio",
    name="Normal Shock Static Pressure Ratio",
    equation="p2 / p1 = (2 * gamma * M1^2 - (gamma - 1)) / (gamma + 1)",
    description=(
        "Jump in static pressure across a stationary normal shock wave, as a function of the "
        "upstream Mach number."
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
        name="p_ratio",
        symbol="p_2/p_1",
        description="Downstream over upstream static pressure",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        naca_report_1135("eq. (93); Table II, p. 635"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"M1": 2.5, "gamma": 1.4},
            expected=7.125,
            rel_tol=1e-12,
            note=(
                "Exact arithmetic: (2.8 * 6.25 - 0.4) / 2.4 = 7.125, matching NACA Rep. 1135, "
                "Table II at M_1 = 2.50."
            ),
        ),
        VerificationCase(
            inputs={"M1": 2.0, "gamma": 1.4},
            expected=4.5,
            rel_tol=1e-12,
            note="Exact arithmetic: (2.8 * 4 - 0.4) / 2.4 = 4.5.",
        ),
    ),
    assumptions=(
        "Steady, one-dimensional flow through a stationary normal shock in a calorically "
        "perfect gas; the shock is treated as a discontinuity with no heat addition.",
        "Calorically perfect gas: constant specific heats, so gamma is constant. The source "
        "treats calorically imperfect (high-temperature) gases separately; do not use this "
        "form for them.",
        "M1 must be greater than 1; for M1 <= 1 there is no shock and the formula has no "
        "physical meaning.",
    ),
    tags=("normal shock", "shock wave", "Rankine-Hugoniot", "pressure ratio", "supersonic"),
)
