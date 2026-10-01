"""Isentropic Static-to-Total Pressure Ratio."""

from sciengformulary.catalog._sources import naca_report_1135
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(M: float, gamma: float) -> float:  # noqa: N803 - symbols as written in the source
    return (1.0 + 0.5 * (gamma - 1.0) * M**2) ** (-gamma / (gamma - 1.0))


isentropic_pressure_ratio = FormulaSpec(
    id="aerodynamics.isentropic_pressure_ratio",
    name="Isentropic Static-to-Total Pressure Ratio",
    equation="p / p0 = (1 + (gamma - 1) / 2 * M^2)^(-gamma / (gamma - 1))",
    description=(
        "Ratio of static to total (stagnation) pressure at a point in isentropic flow of a perfect "
        "gas, as a function of the local Mach number."
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
        name="p_ratio",
        symbol="p/p_0",
        description="Static pressure divided by total pressure",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes the total pressure as p_t.
        naca_report_1135("eq. (44); Table II, p. 635"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"M": 2.5, "gamma": 1.4},
            expected=0.05853,
            rel_tol=0.0002,
            note=(
                "Published value: NACA Rep. 1135, Table II, M = 2.50 gives p/p_t = .5853 x 10^-1 "
                "(four significant figures)."
            ),
        ),
        VerificationCase(
            inputs={"M": 0.8, "gamma": 1.4},
            expected=0.6560216183589752,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation of 1.128^-3.5.",
        ),
    ),
    assumptions=(
        "Valid only along an isentropic path (adiabatic and reversible flow); do not apply it "
        "across a shock wave.",
        "Calorically perfect gas: constant specific heats, so gamma is constant. The source "
        "treats calorically imperfect (high-temperature) gases separately; do not use this "
        "form for them.",
    ),
    tags=("isentropic flow", "stagnation pressure", "total pressure", "p/p0", "pitot"),
)
