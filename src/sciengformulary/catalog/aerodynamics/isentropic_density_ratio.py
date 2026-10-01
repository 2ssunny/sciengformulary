"""Isentropic Static-to-Total Density Ratio."""

from sciengformulary.catalog._sources import naca_report_1135
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(M: float, gamma: float) -> float:  # noqa: N803 - symbols as written in the source
    return (1.0 + 0.5 * (gamma - 1.0) * M**2) ** (-1.0 / (gamma - 1.0))


isentropic_density_ratio = FormulaSpec(
    id="aerodynamics.isentropic_density_ratio",
    name="Isentropic Static-to-Total Density Ratio",
    equation="rho / rho0 = (1 + (gamma - 1) / 2 * M^2)^(-1 / (gamma - 1))",
    description=(
        "Ratio of static to total (stagnation) density at a point in isentropic flow of a perfect "
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
        name="rho_ratio",
        symbol=r"\rho/\rho_0",
        description="Static density divided by total density",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes the total density as rho_t.
        naca_report_1135("eq. (45); Table II, p. 635"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"M": 2.5, "gamma": 1.4},
            expected=0.1317,
            rel_tol=0.0004,
            note=(
                "Published value: NACA Rep. 1135, Table II, M = 2.50 gives rho/rho_t = .1317 (four "
                "significant figures)."
            ),
        ),
        VerificationCase(
            inputs={"M": 0.8, "gamma": 1.4},
            expected=0.739992385508924,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation of 1.128^-2.5.",
        ),
    ),
    assumptions=(
        "Valid only along an isentropic path (adiabatic and reversible flow); do not apply it "
        "across a shock wave.",
        "Calorically perfect gas: constant specific heats, so gamma is constant. The source "
        "treats calorically imperfect (high-temperature) gases separately; do not use this "
        "form for them.",
    ),
    tags=("isentropic flow", "stagnation density", "total density", "compressibility"),
)
