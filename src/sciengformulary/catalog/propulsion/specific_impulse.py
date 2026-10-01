"""Specific Impulse: I_sp = F / (mdot * g0)."""

from sciengformulary.catalog._constants import (
    STANDARD_ACCELERATION_OF_GRAVITY,
    STANDARD_GRAVITY_REFERENCE,
)
from sciengformulary.catalog._sources import nasa_glenn
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(F: float, mdot: float) -> float:  # noqa: N803 - symbols as written in the source
    return F / (mdot * STANDARD_ACCELERATION_OF_GRAVITY)


specific_impulse = FormulaSpec(
    id="propulsion.specific_impulse",
    name="Specific Impulse",
    equation="I_sp = F / (mdot * g0)",
    description=(
        "Thrust produced per unit weight flow rate of propellant, expressed in seconds by dividing "
        "by standard gravity. Higher values mean less propellant for the same impulse."
    ),
    inputs=(
        VariableSpec(
            name="F",
            symbol="F",
            description="Thrust",
            dimension="M L T^-2",
            si_unit="N",
        ),
        VariableSpec(
            name="mdot",
            symbol=r"\dot{m}",
            description="Propellant mass flow rate",
            dimension="M T^-1",
            si_unit="kg/s",
        ),
    ),
    output=VariableSpec(
        name="I_sp",
        symbol="I_{sp}",
        description="Specific impulse",
        dimension="T",
        si_unit="s",
    ),
    evaluator=_evaluate,
    references=(
        # g0 is the standard acceleration of gravity, 9.80665 m/s^2 by definition.
        nasa_glenn("Specific Impulse", "specific-impulse", 2024),
        STANDARD_GRAVITY_REFERENCE,
    ),
    verification_cases=(
        VerificationCase(
            inputs={"F": 9806.65, "mdot": 4.0},
            expected=250.0,
            rel_tol=1e-12,
            note="Hand calculation: 9806.65 / (4 * 9.80665) = 250 s.",
        ),
        VerificationCase(
            inputs={"F": 1000.0, "mdot": 1.0},
            expected=101.97162129779282,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation of 1000 / 9.80665.",
        ),
    ),
    assumptions=(
        "g0 is the fixed standard gravity used only to convert to seconds; it is not the local "
        "gravitational acceleration.",
        "F and mdot must refer to the same operating point.",
    ),
    tags=("specific impulse", "Isp", "rocket", "propellant efficiency", "propulsion"),
)
