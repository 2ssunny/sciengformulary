"""Specific Energy of an Elliptical Orbit: epsilon = -mu / (2 * a)."""

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(mu: float, a: float) -> float:
    return -mu / (2.0 * a)


elliptical_orbit_specific_energy = FormulaSpec(
    id="orbital.elliptical_orbit_specific_energy",
    name="Specific Energy of an Elliptical Orbit",
    equation="epsilon = -mu / (2 * a)",
    description="Specific orbital energy of a closed orbit depends only on its semi-major axis.",
    inputs=(
        VariableSpec(
            name="mu",
            symbol=r"\mu",
            description="Standard gravitational parameter G M of the central body",
            dimension="L^3 T^-2",
            si_unit="m^3/s^2",
        ),
        VariableSpec(
            name="a",
            symbol="a",
            description="Semi-major axis of the orbit (radius for a circle)",
            dimension="L",
            si_unit="m",
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
        # The source gives E = -G m M / (2a) for the satellite of mass m; per unit mass with mu = G
        # M.
        openstax_university_physics(1, "13-5-keplers-laws-of-planetary-motion", "sec. 13.5"),
        openstax_university_physics(1, "13-4-satellite-orbits-and-energy", "sec. 13.4, eq. (13.9)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"mu": 398600441800000.0, "a": 24000000.0},
            expected=-8304175.870833334,
            rel_tol=1e-12,
            note="Hand calculation: -3.986004418e14 / 4.8e7.",
        ),
    ),
    assumptions=(
        "Two-body problem: a satellite of negligible mass orbiting a spherically symmetric "
        "central body that is treated as fixed; no drag, thrust or third-body perturbations.",
        "Closed orbits only (circle or ellipse); a > 0.",
    ),
    tags=("orbital energy", "semi-major axis", "ellipse", "two-body"),
)
