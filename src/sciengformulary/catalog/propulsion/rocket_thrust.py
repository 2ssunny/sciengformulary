"""Rocket Thrust: F = mdot * v_e + (p_e - p_a) * A_e."""

from sciengformulary.catalog._sources import nasa_glenn
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    mdot: float,
    v_e: float,
    p_e: float,
    p_a: float,
    A_e: float,  # noqa: N803
) -> float:
    return mdot * v_e + (p_e - p_a) * A_e


rocket_thrust = FormulaSpec(
    id="propulsion.rocket_thrust",
    name="Rocket Thrust",
    equation="F = mdot * v_e + (p_e - p_a) * A_e",
    description=(
        "Net thrust of a rocket engine: momentum flux of the exhaust plus the pressure force from "
        "any mismatch between nozzle-exit and ambient pressure acting over the exit area."
    ),
    inputs=(
        VariableSpec(
            name="mdot",
            symbol=r"\dot{m}",
            description="Propellant mass flow rate through the nozzle",
            dimension="M T^-1",
            si_unit="kg/s",
        ),
        VariableSpec(
            name="v_e",
            symbol="v_e",
            description="Exhaust velocity at the nozzle exit, relative to the vehicle",
            dimension="L T^-1",
            si_unit="m/s",
        ),
        VariableSpec(
            name="p_e",
            symbol="p_e",
            description="Static pressure in the exhaust at the nozzle exit plane",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="p_a",
            symbol="p_a",
            description="Ambient (free-stream) static pressure",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="A_e",
            symbol="A_e",
            description="Nozzle exit area",
            dimension="L^2",
            si_unit="m^2",
        ),
    ),
    output=VariableSpec(
        name="F",
        symbol="F",
        description="Thrust",
        dimension="M L T^-2",
        si_unit="N",
    ),
    evaluator=_evaluate,
    references=(
        # The source names the ambient pressure p_0 and the exit quantities with subscript e.
        nasa_glenn("Rocket Thrust Equation", "rocket-thrust-equation", 2024),
        nasa_glenn("Specific Impulse", "specific-impulse", 2024),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"mdot": 100.0, "v_e": 2500.0, "p_e": 50000.0, "p_a": 101325.0, "A_e": 1.0},
            expected=198675.0,
            rel_tol=1e-12,
            note=(
                "Hand calculation: 100 * 2500 + (50000 - 101325) * 1 = 198675 N (an over-expanded "
                "nozzle, so the pressure term is negative)."
            ),
        ),
    ),
    assumptions=(
        "Steady operation; the exhaust leaves uniformly through the exit plane.",
        "All the working fluid is carried on board (no air intake); for air-breathing engines "
        "the inlet momentum flux must also be subtracted.",
        "The pressure term vanishes for a perfectly expanded nozzle (p_e = p_a) and is "
        "negative for an over-expanded one.",
    ),
    tags=("thrust", "rocket", "nozzle", "pressure thrust", "propulsion"),
)
