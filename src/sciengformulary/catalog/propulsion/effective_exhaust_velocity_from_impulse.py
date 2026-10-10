"""Effective Exhaust Velocity from Total Impulse: c_eff = I_t / m_p."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, nasa_glenn
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(I_t: float, m_p: float) -> float:  # noqa: N803 - symbols as in the source
    positive("I_t", I_t)
    positive("m_p", m_p)
    return finite_result(I_t / m_p)


effective_exhaust_velocity_from_impulse = FormulaSpec(
    id="propulsion.effective_exhaust_velocity_from_impulse",
    name="Effective Exhaust Velocity from Total Impulse",
    equation="c_eff = I_t / m_p",
    description=(
        "Effective exhaust velocity of a rocket firing from its total impulse and the propellant "
        "mass consumed, when the equivalent velocity stays constant over the burn. It is the "
        "same quantity as propulsion.effective_exhaust_velocity, obtained from impulse and "
        "propellant mass rather than from a specific impulse and g0."
    ),
    inputs=(
        VariableSpec(
            name="I_t",
            symbol="I",
            description="Total impulse (integral of thrust over the burn)",
            dimension="M L T^-1",
            si_unit="N s",
        ),
        VariableSpec(
            name="m_p",
            symbol="m",
            description="Propellant mass consumed during the burn",
            dimension="M",
            si_unit="kg",
        ),
    ),
    output=VariableSpec(
        name="c_eff",
        symbol="V_{eq}",
        description="Effective (equivalent) exhaust velocity",
        dimension="L T^-1",
        si_unit="m/s",
    ),
    evaluator=_evaluate,
    references=(
        # Stated: the page defines total impulse as the integral of F dt = integral of
        # mdot * V_eq dt; for a constant V_eq this is I = m * V_eq, solved here for V_eq. The
        # page's typo in the expression for V_eq (see propulsion.effective_exhaust_velocity)
        # is not used.
        nasa_glenn(
            "Specific Impulse",
            "specific-impulse",
            2024,
            locator="Specific Impulse",
            accessed=ENGINEERING_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"I_t": 2500000.0, "m_p": 1000.0},
            expected=2500.0,
            rel_tol=1e-12,
            note="Hand calculation: 2.5e6 N s / 1000 kg = 2500 m/s.",
        ),
        VerificationCase(
            inputs={"I_t": 3000.0, "m_p": 1.2},
            expected=2500.0,
            rel_tol=1e-12,
            note="Hand calculation: 3000 / 1.2 = 2500 m/s (small motor).",
        ),
        VerificationCase(
            inputs={"I_t": 9806.65, "m_p": 1.0},
            expected=9806.65,
            rel_tol=1e-12,
            note="Edge case: I_t / m_p equals 1000 * g0, that is a specific impulse of 1000 s.",
        ),
    ),
    assumptions=(
        "The equivalent velocity is constant in time, so that I = m_p * c_eff; with a varying "
        "velocity the result is the mass-averaged value over the burn.",
        "It equals the true exhaust velocity only for matched expansion (p_e = p_a).",
        "I_t and m_p must be positive and refer to the same burn.",
    ),
    tags=("effective exhaust velocity", "total impulse", "rocket", "propulsion"),
)
