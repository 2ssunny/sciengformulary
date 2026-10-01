"""Normal Shock Total Pressure Ratio."""

from sciengformulary.catalog._sources import naca_report_1135
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(M1: float, gamma: float) -> float:  # noqa: N803 - symbols as written in the source
    density_ratio = (gamma + 1.0) * M1**2 / ((gamma - 1.0) * M1**2 + 2.0)
    pressure_term = (gamma + 1.0) / (2.0 * gamma * M1**2 - (gamma - 1.0))
    return density_ratio ** (gamma / (gamma - 1.0)) * pressure_term ** (1.0 / (gamma - 1.0))


normal_shock_total_pressure_ratio = FormulaSpec(
    id="aerodynamics.normal_shock_total_pressure_ratio",
    name="Normal Shock Total Pressure Ratio",
    equation=(
        "p02 / p01 = ((gamma + 1) M1^2 / ((gamma - 1) M1^2 + 2))^(gamma / (gamma - 1)) * ((gamma + "
        "1) / (2 gamma M1^2 - (gamma - 1)))^(1 / (gamma - 1))"
    ),
    description=(
        "Fraction of total (stagnation) pressure that survives a normal shock. The loss measures "
        "the entropy produced by the shock."
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
        name="pt_ratio",
        symbol="p_{02}/p_{01}",
        description="Downstream over upstream total pressure",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The sheet writes the same ratio as (p2/p1) times a ratio of total-to-static temperature
        # terms; the two forms agree numerically.
        naca_report_1135("eq. (99); Table II, p. 635"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"M1": 2.5, "gamma": 1.4},
            expected=0.499,
            rel_tol=0.0002,
            note=(
                "Published value: NACA Rep. 1135, Table II, M_1 = 2.50 gives p_t2/p_t1 = .4990 "
                "(four significant figures)."
            ),
        ),
        VerificationCase(
            inputs={"M1": 2.0, "gamma": 1.4},
            expected=0.7208738614847453,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation of eq. (99) at M_1 = 2.",
        ),
    ),
    assumptions=(
        "Steady, one-dimensional flow through a stationary normal shock in a calorically "
        "perfect gas; the shock is treated as a discontinuity with no heat addition.",
        "Calorically perfect gas: constant specific heats, so gamma is constant. The source "
        "treats calorically imperfect (high-temperature) gases separately; do not use this "
        "form for them.",
        "M1 must be greater than 1; the ratio is below 1 for every real shock.",
    ),
    tags=(
        "normal shock",
        "total pressure loss",
        "stagnation pressure",
        "Rayleigh pitot",
        "supersonic",
    ),
)
