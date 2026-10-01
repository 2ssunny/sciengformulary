"""Gravitational Potential Energy Near a Surface: U = m * g * h."""

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(m: float, g: float, h: float) -> float:
    return m * g * h


gravitational_potential_energy = FormulaSpec(
    id="mechanics.gravitational_potential_energy",
    name="Gravitational Potential Energy Near a Surface",
    equation="U = m * g * h",
    description=(
        "Change in gravitational potential energy of a mass raised a height h above a chosen datum "
        "in uniform gravity."
    ),
    inputs=(
        VariableSpec(
            name="m",
            symbol="m",
            description="Mass of the body",
            dimension="M",
            si_unit="kg",
        ),
        VariableSpec(
            name="g",
            symbol="g",
            description="Local gravitational acceleration (about 9.81 m/s^2 near Earth's surface)",
            dimension="L T^-2",
            si_unit="m/s^2",
        ),
        VariableSpec(
            name="h",
            symbol="h",
            description="Height above the chosen datum (negative below it)",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="U",
        symbol="U",
        description="Potential energy relative to the datum",
        dimension="M L^2 T^-2",
        si_unit="J",
    ),
    evaluator=_evaluate,
    references=(
        # The source gives U = m g y + const; the constant is zero at the datum.
        openstax_university_physics(1, "8-1-potential-energy-of-a-system", "sec. 8.1, eq. (8.5)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"m": 75.0, "g": 9.8, "h": 147.0},
            expected=108045.0,
            rel_tol=1e-12,
            note=(
                "Worked example in the cited section: (75 * 9.8 N)(147 m) = 108 kJ (108045 J "
                "before rounding)."
            ),
        ),
    ),
    assumptions=(
        "Uniform gravitational field: h small compared with the planet's radius.",
        "Only differences in U are physical; the datum is arbitrary.",
    ),
    tags=("potential energy", "gravity", "energy", "height"),
)
