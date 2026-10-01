"""Isentropic Static-to-Total Temperature Ratio: T / T0 = (1 + (gamma - 1) / 2 * M^2)^-1."""

from sciengformulary.catalog._sources import naca_report_1135
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(M: float, gamma: float) -> float:  # noqa: N803 - symbols as written in the source
    return 1.0 / (1.0 + 0.5 * (gamma - 1.0) * M**2)


isentropic_temperature_ratio = FormulaSpec(
    id="aerodynamics.isentropic_temperature_ratio",
    name="Isentropic Static-to-Total Temperature Ratio",
    equation="T / T0 = (1 + (gamma - 1) / 2 * M^2)^-1",
    description=(
        "Ratio of static to total (stagnation) temperature at a point in steady adiabatic flow of "
        "a perfect gas, as a function of the local Mach number."
    ),
    inputs=(
        VariableSpec(
            name="M",
            symbol="M",
            description="Local Mach number",
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
        name="T_ratio",
        symbol="T/T_0",
        description="Static temperature divided by total temperature",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes the total temperature as T_t and labels this ratio [adiab, perf]; Table
        # II tabulates it for gamma = 7/5.
        naca_report_1135("eq. (43); Table II, p. 635"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"M": 2.5, "gamma": 1.4},
            expected=0.4444,
            rel_tol=0.0002,
            note=(
                "Published value: NACA Rep. 1135, Table II, M = 2.50 gives T/T_t = .4444 (four "
                "significant figures, hence the tolerance)."
            ),
        ),
        VerificationCase(
            inputs={"M": 0.5, "gamma": 1.4},
            expected=0.9523809523809523,
            rel_tol=1e-12,
            note="Hand calculation: 1 / (1 + 0.2 * 0.25) = 1 / 1.05.",
        ),
    ),
    assumptions=(
        "Steady adiabatic flow of a calorically perfect gas with no shaft work; the relation "
        "also holds across shocks because total temperature is conserved.",
        "Calorically perfect gas: constant specific heats, so gamma is constant. The source "
        "treats calorically imperfect (high-temperature) gases separately; do not use this "
        "form for them.",
    ),
    tags=("isentropic flow", "stagnation temperature", "total temperature", "T/T0"),
)
