"""Effective Exhaust Velocity from Specific Impulse: v_e = g0 * I_sp."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import (
    ENGINEERING_ACCESSED,
    nasa_glenn,
    nasa_technical_report,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(I_sp: float, g0: float) -> float:  # noqa: N803 - symbols as written in the source
    positive("I_sp", I_sp)
    positive("g0", g0)
    return finite_result(g0 * I_sp)


effective_exhaust_velocity = FormulaSpec(
    id="propulsion.effective_exhaust_velocity",
    name="Effective Exhaust Velocity from Specific Impulse",
    equation="v_e = g0 * I_sp",
    description=(
        "Effective (equivalent) exhaust velocity of a rocket, the thrust per unit propellant "
        "mass flow, recovered from a specific impulse given in seconds. It is the inverse view "
        "of propulsion.specific_impulse, which gets I_sp from thrust and mass flow, and here "
        "g0 is an input. propulsion.effective_exhaust_velocity_from_impulse gives the same "
        "quantity from total impulse and propellant mass instead."
    ),
    inputs=(
        VariableSpec(
            name="I_sp",
            symbol="I_{sp}",
            description="Specific impulse (thrust per unit weight flow of propellant)",
            dimension="T",
            si_unit="s",
        ),
        VariableSpec(
            name="g0",
            symbol="g_0",
            description="Standard gravity used to define the specific impulse (9.80665 m/s^2)",
            dimension="L T^-2",
            si_unit="m/s^2",
        ),
    ),
    output=VariableSpec(
        name="v_e",
        symbol="V_{eq}",
        description="Effective (equivalent) exhaust velocity, F / mdot",
        dimension="L T^-1",
        si_unit="m/s",
    ),
    evaluator=_evaluate,
    references=(
        # Stated: the page prints I_sp = V_eq / g0 (with F = mdot * V_eq); solving for V_eq
        # gives the equation above. The page also prints an expression for V_eq in terms of the
        # exit velocity, exit area and pressures that drops the factor mdot on V_e (a typo; it
        # is not dimensionally consistent). That expression is not used here. The page quotes
        # g0 as 9.8 m/s^2 or 32.2 ft/s^2; g0 is an input, so any consistent value can be passed.
        nasa_glenn(
            "Specific Impulse",
            "specific-impulse",
            2024,
            locator="Specific Impulse",
            accessed=ENGINEERING_ACCESSED,
        ),
        # Stated: c = g * I_s with c the effective exhaust velocity.
        nasa_technical_report(
            "Design of Liquid Propellant Rocket Engines",
            ("D. K. Huzel", "D. H. Huang"),
            "NASA SP-125",
            1967,
            "https://ntrs.nasa.gov/citations/19710019929",
            "sec. 1.3, eqs. (1-31) and (1-31a), p. 11",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"I_sp": 300.0, "g0": 9.80665},
            expected=2941.995,
            rel_tol=1e-12,
            note="Hand calculation: 300 * 9.80665 = 2941.995 m/s (50-digit mpmath agrees).",
        ),
        VerificationCase(
            inputs={"I_sp": 450.0, "g0": 9.80665},
            expected=4412.9925,
            rel_tol=1e-12,
            note="Hand calculation: 450 * 9.80665 = 4412.9925 m/s.",
        ),
        VerificationCase(
            inputs={"I_sp": 1.0, "g0": 9.80665},
            expected=9.80665,
            rel_tol=1e-12,
            note="Edge case: a specific impulse of 1 s gives exactly g0 in m/s.",
        ),
    ),
    assumptions=(
        "The effective velocity includes the pressure-thrust contribution; it equals the true "
        "exit velocity only for matched expansion (p_e = p_a).",
        "g0 is the standard gravity used to define the specific impulse so that I_sp keeps its "
        "conventional meaning, not the local gravitational acceleration. Pass it in the length "
        "unit wanted for v_e (9.80665 m/s^2 for m/s).",
        "I_sp and g0 must be positive.",
    ),
    tags=("exhaust velocity", "equivalent velocity", "specific impulse", "rocket", "propulsion"),
)
