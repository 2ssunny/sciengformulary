"""Specific Orbital Energy: epsilon = v^2 / 2 - mu / r."""

from sciengformulary.catalog._sources import (
    nasa_cr_2005_213034,
    openstax_university_physics,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(v: float, r: float, mu: float) -> float:
    return 0.5 * v**2 - mu / r


specific_orbital_energy = FormulaSpec(
    id="orbital.specific_orbital_energy",
    name="Specific Orbital Energy",
    equation="epsilon = v^2 / 2 - mu / r",
    description=(
        "Sum of kinetic and gravitational potential energy divided by the satellite's mass. The "
        "value does not change as the satellite moves along a two-body orbit, and a negative "
        "value indicates a bound, elliptical orbit."
    ),
    inputs=(
        VariableSpec(
            name="v",
            symbol="v",
            description="Orbital speed",
            dimension="L T^-1",
            si_unit="m/s",
        ),
        VariableSpec(
            name="r",
            symbol="r",
            description="Distance from the centre of the central body",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="mu",
            symbol=r"\mu",
            description="Standard gravitational parameter G M of the central body",
            dimension="L^3 T^-2",
            si_unit="m^3/s^2",
        ),
    ),
    output=VariableSpec(
        name="epsilon",
        symbol=r"\epsilon",
        description="Specific orbital energy",
        dimension="L^2 T^-2",
        si_unit="J/kg",
    ),
    evaluator=_evaluate,
    references=(
        # The source conserves K + U = m v^2/2 - G M m / r; dividing by the satellite mass m gives
        # this per-mass form with mu = G M.
        openstax_university_physics(
            1,
            "13-3-gravitational-potential-energy-and-total-energy",
            "sec. 13.3, eq. (13.5)",
        ),
        # The report writes the energy per unit mass at departure as v0^2 / 2 - mu / r0.
        nasa_cr_2005_213034("eq. (12), p. 19"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"v": 7500.0, "r": 7000000.0, "mu": 398600441800000.0},
            expected=-28817920.257142857,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation of 7500^2/2 - 3.986004418e14 / 7.0e6.",
        ),
    ),
    assumptions=(
        "Two-body problem: a satellite of negligible mass orbiting a spherically symmetric "
        "central body that is treated as fixed; no drag, thrust or third-body perturbations.",
        "Potential energy is zero at infinite separation.",
    ),
    tags=("orbital energy", "vis-viva", "two-body", "specific energy"),
)
