"""Stagnation (Total) Temperature: T0 = T + V^2 / (2 * c_p)."""

from sciengformulary.catalog._sources import naca_report_1135
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    T: float,  # noqa: N803
    V: float,  # noqa: N803
    c_p: float,
) -> float:
    return T + V**2 / (2.0 * c_p)


stagnation_temperature = FormulaSpec(
    id="thermodynamics.stagnation_temperature",
    name="Stagnation (Total) Temperature",
    equation="T0 = T + V^2 / (2 * c_p)",
    description=(
        "Temperature a moving gas would reach if brought to rest adiabatically, from the static "
        "temperature and flow speed."
    ),
    inputs=(
        VariableSpec(
            name="T",
            symbol="T",
            description="Static temperature",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="V",
            symbol="V",
            description="Flow speed",
            dimension="L T^-1",
            si_unit="m/s",
        ),
        VariableSpec(
            name="c_p",
            symbol="c_p",
            description="Specific heat at constant pressure",
            dimension="L^2 T^-2 Theta^-1",
            si_unit="J/(kg*K)",
        ),
    ),
    output=VariableSpec(
        name="T0",
        symbol="T_0",
        description="Stagnation temperature",
        dimension="Theta",
        si_unit="K",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes c_p T + V^2/2 = c_p T_t; T_t = T0.
        naca_report_1135("eq. (32b)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"T": 250.0, "V": 300.0, "c_p": 1005.0},
            expected=294.7761194029851,
            rel_tol=1e-12,
            note="Exact arithmetic: 250 + 90000 / 2010.",
        ),
    ),
    assumptions=(
        "Adiabatic deceleration with no shaft work; it need not be reversible.",
        "Calorically perfect gas: constant specific heats, so gamma is constant over the "
        "temperature range.",
    ),
    tags=("stagnation temperature", "total temperature", "ram temperature", "compressible flow"),
)
