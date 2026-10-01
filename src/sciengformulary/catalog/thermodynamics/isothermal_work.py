"""Isothermal Expansion Work of an Ideal Gas: W = m * R * T * ln(V2 / V1)."""

import math

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    m: float,
    R: float,  # noqa: N803
    T: float,  # noqa: N803
    V1: float,  # noqa: N803
    V2: float,  # noqa: N803
) -> float:
    return m * R * T * math.log(V2 / V1)


isothermal_work = FormulaSpec(
    id="thermodynamics.isothermal_work",
    name="Isothermal Expansion Work of an Ideal Gas",
    equation="W = m * R * T * ln(V2 / V1)",
    description=(
        "Work done by a fixed mass of ideal gas expanding reversibly at constant temperature from "
        "volume V1 to V2."
    ),
    inputs=(
        VariableSpec(
            name="m",
            symbol="m",
            description="Mass of gas",
            dimension="M",
            si_unit="kg",
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
        VariableSpec(
            name="V1",
            symbol="V_1",
            description="Initial volume",
            dimension="L^3",
            si_unit="m^3",
        ),
        VariableSpec(
            name="V2",
            symbol="V_2",
            description="Final volume",
            dimension="L^3",
            si_unit="m^3",
        ),
    ),
    output=VariableSpec(
        name="W",
        symbol="W",
        description="Work done by the gas (positive for expansion)",
        dimension="M L^2 T^-2",
        si_unit="J",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes W = n R T ln(V2 / V1) with n moles and the universal gas constant; n
        # R_universal = m R_specific.
        openstax_university_physics(2, "3-2-work-heat-and-internal-energy", "sec. 3.2"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"m": 1.0, "R": 287.0, "T": 300.0, "V1": 1.0, "V2": 2.0},
            expected=59679.97224621129,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation of 287 * 300 * ln 2.",
        ),
    ),
    assumptions=(
        "Ideal (thermally perfect) gas: p = rho R T holds; not near condensation or at very "
        "high pressure.",
        "Quasi-static (reversible) process at constant temperature.",
    ),
    tags=("isothermal process", "boundary work", "expansion work", "ideal gas"),
)
