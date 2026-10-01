"""Entropy Change of an Ideal Gas: s2 - s1 = c_p * ln(T2 / T1) - R * ln(p2 / p1)."""

import math

from sciengformulary.catalog._sources import naca_report_1135, nasa_glenn
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    c_p: float,
    R: float,  # noqa: N803
    T1: float,  # noqa: N803
    T2: float,  # noqa: N803
    p1: float,
    p2: float,
) -> float:
    return c_p * math.log(T2 / T1) - R * math.log(p2 / p1)


ideal_gas_entropy_change = FormulaSpec(
    id="thermodynamics.ideal_gas_entropy_change",
    name="Entropy Change of an Ideal Gas",
    equation="s2 - s1 = c_p * ln(T2 / T1) - R * ln(p2 / p1)",
    description=(
        "Specific entropy change of an ideal gas between two states, from temperatures and "
        "pressures."
    ),
    inputs=(
        VariableSpec(
            name="c_p",
            symbol="c_p",
            description="Specific heat at constant pressure",
            dimension="L^2 T^-2 Theta^-1",
            si_unit="J/(kg*K)",
        ),
        VariableSpec(
            name="R",
            symbol="R",
            description="Specific gas constant (287 J/(kg K) for dry air)",
            dimension="L^2 T^-2 Theta^-1",
            si_unit="J/(kg*K)",
        ),
        VariableSpec(
            name="T1",
            symbol="T_1",
            description="Initial absolute temperature",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="T2",
            symbol="T_2",
            description="Final absolute temperature",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="p1",
            symbol="p_1",
            description="Initial absolute pressure",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="p2",
            symbol="p_2",
            description="Final absolute pressure",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
    ),
    output=VariableSpec(
        name="delta_s",
        symbol=r"\Delta s",
        description="Specific entropy change s2 - s1",
        dimension="L^2 T^-2 Theta^-1",
        si_unit="J/(kg*K)",
    ),
    evaluator=_evaluate,
    references=(
        nasa_glenn("Entropy of a Gas", "entropy-of-a-gas", 2024),
        naca_report_1135("eq. (23a)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={
                "c_p": 1005.0,
                "R": 287.0,
                "T1": 300.0,
                "T2": 600.0,
                "p1": 100000.0,
                "p2": 500000.0,
            },
            expected=234.70423559415823,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation of 1005 ln 2 - 287 ln 5.",
        ),
    ),
    assumptions=(
        "Ideal (thermally perfect) gas: p = rho R T holds; not near condensation or at very "
        "high pressure.",
        "Calorically perfect gas: constant specific heats, so gamma is constant over the "
        "temperature range.",
        "Path-independent: valid for any process between the two equilibrium states, "
        "reversible or not.",
    ),
    tags=("entropy", "ideal gas", "second law", "state change"),
)
