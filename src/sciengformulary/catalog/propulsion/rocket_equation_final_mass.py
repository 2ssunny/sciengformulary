"""Rocket Equation (Final Mass): m_f = m0 * exp(-dv / u_e)."""

import math

from sciengformulary.catalog._domain import non_negative, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(m0: float, dv: float, u_e: float) -> float:
    positive("m0", m0)
    non_negative("dv", dv)
    positive("u_e", u_e)
    final_mass = m0 * math.exp(-dv / u_e)
    if final_mass <= 0.0:
        raise ValueError(
            f"the final mass underflows to zero for dv/u_e = {dv / u_e!r}; "
            "the mass ratio is outside the floating-point range."
        )
    return final_mass


rocket_equation_final_mass = FormulaSpec(
    id="propulsion.rocket_equation_final_mass",
    name="Rocket Equation (Final Mass)",
    equation="m_f = m0 * exp(-dv / u_e)",
    description=(
        "Mass of a rocket after a velocity change dv at constant effective exhaust speed, in "
        "the absence of external forces."
    ),
    inputs=(
        VariableSpec(
            name="m0",
            symbol="m_0",
            description="Initial mass including propellant",
            dimension="M",
            si_unit="kg",
        ),
        VariableSpec(
            name="dv",
            symbol=r"\Delta v",
            description="Velocity change achieved",
            dimension="L T^-1",
            si_unit="m/s",
        ),
        VariableSpec(
            name="u_e",
            symbol="u_e",
            description="Effective exhaust speed relative to the rocket",
            dimension="L T^-1",
            si_unit="m/s",
        ),
    ),
    output=VariableSpec(
        name="m_f",
        symbol="m_f",
        description="Final mass, in the unit of m0",
        dimension="M",
        si_unit="kg",
    ),
    evaluator=_evaluate,
    references=(
        # Derived result: the report states the final-to-initial mass ratio as e^(-Delta v / c)
        # with c the effective exhaust speed (text before its eq. (3)) and the propellant fraction
        # 1 - e^(-Delta v / c) in eq. (5). Multiplying the stated ratio by the initial mass gives
        # the final mass here, which is the algebraic inverse of Delta v = c ln(m0 / m_f).
        nasa_technical_report(
            "An Analytical Optimization of Electric Propulsion Orbit Transfer Vehicles",
            ("S. R. Oleson",),
            "NASA CR-191129",
            1993,
            "https://ntrs.nasa.gov/citations/19930017871",
            "p. 3 (text before eq. 3) and eq. (5)",
            organization="NASA Lewis Research Center (Sverdrup Technology)",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"m0": 1000.0, "dv": 0.0, "u_e": 3000.0},
            expected=1000.0,
            rel_tol=1e-12,
            note="Hand calculation at dv = 0: exp(0) = 1, so no propellant is used.",
        ),
        VerificationCase(
            inputs={"m0": 5000.0, "dv": 5860.0, "u_e": 29419.95},
            expected=4096.9932273956065,
            rel_tol=1e-12,
            note=(
                "Ion-thruster-like exhaust speed (specific impulse 3000 s) and dv = 5.86 km/s; "
                "independent 50-digit mpmath evaluation."
            ),
        ),
        VerificationCase(
            inputs={"m0": 2000.0, "dv": 3000.0, "u_e": 3500.0},
            expected=848.7456913538999,
            rel_tol=1e-12,
            note="Chemical-rocket-like case; independent 50-digit mpmath evaluation.",
        ),
    ),
    assumptions=(
        "Derived result: the stated mass ratio exp(-dv / u_e) multiplied by the initial mass; "
        "equivalently the inverse of the rocket equation dv = u_e ln(m0 / m_f).",
        "No gravity, drag or other external force, and a constant effective exhaust speed; dv "
        "is the velocity change the rocket actually achieves.",
        "Inputs must satisfy m0 > 0, dv >= 0 and u_e > 0, so the result lies in (0, m0]. A "
        "ratio dv / u_e so large that the result underflows to zero (about 745 or more) raises "
        "ValueError.",
        "dv and u_e must use the same speed unit; the result has the unit of m0.",
    ),
    tags=("rocket equation", "Tsiolkovsky", "propellant mass", "final mass", "propulsion"),
)
