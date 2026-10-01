"""Ideal Gas Law (Density Form): p = rho * R * T."""

from sciengformulary.catalog._sources import naca_report_1135, nasa_glenn
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    rho: float,
    R: float,  # noqa: N803
    T: float,  # noqa: N803
) -> float:
    return rho * R * T


ideal_gas_pressure = FormulaSpec(
    id="thermodynamics.ideal_gas_pressure",
    name="Ideal Gas Law (Density Form)",
    equation="p = rho * R * T",
    description="Pressure of an ideal gas from its density and absolute temperature.",
    inputs=(
        VariableSpec(
            name="rho",
            symbol=r"\rho",
            description="Gas density",
            dimension="M L^-3",
            si_unit="kg/m^3",
        ),
        VariableSpec(
            name="R",
            symbol="R",
            description="Specific gas constant (287 J/(kg K) for dry air)",
            dimension="L^2 T^-2 Theta^-1",
            si_unit="J/(kg*K)",
        ),
        VariableSpec(
            name="T",
            symbol="T",
            description="Absolute temperature",
            dimension="Theta",
            si_unit="K",
        ),
    ),
    output=VariableSpec(
        name="p",
        symbol="p",
        description="Absolute static pressure",
        dimension="M L^-1 T^-2",
        si_unit="Pa",
    ),
    evaluator=_evaluate,
    references=(
        nasa_glenn("Equation of State", "equation-of-state", 2024),
        naca_report_1135("eq. (26)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"rho": 1.225, "R": 287.05, "T": 288.15},
            expected=101323.9854375,
            rel_tol=1e-12,
            note="Hand calculation: 1.225 * 287.05 * 288.15 = 101323.985 Pa.",
        ),
    ),
    assumptions=(
        "Ideal (thermally perfect) gas: p = rho R T holds; not near condensation or at very "
        "high pressure.",
        "R is the specific gas constant of the particular gas (universal constant divided by "
        "molar mass), not 8.314.",
        "Absolute pressure and temperature.",
    ),
    tags=("ideal gas", "equation of state", "gas law", "density"),
)
