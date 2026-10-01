"""Orbital Period (Kepler's Third Law): T = 2 * pi * sqrt(a^3 / mu)."""

import math

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(a: float, mu: float) -> float:
    return 2.0 * math.pi * math.sqrt(a**3 / mu)


orbital_period = FormulaSpec(
    id="orbital.orbital_period",
    name="Orbital Period (Kepler's Third Law)",
    equation="T = 2 * pi * sqrt(a^3 / mu)",
    description=(
        "Time for one revolution of a closed two-body orbit; depends only on the semi-major axis "
        "and the central body's gravitational parameter."
    ),
    inputs=(
        VariableSpec(
            name="a",
            symbol="a",
            description="Semi-major axis (radius for a circular orbit)",
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
        name="T",
        symbol="T",
        description="Orbital period",
        dimension="T",
        si_unit="s",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes T^2 = 4 pi^2 a^3 / (G M); mu = G M.
        openstax_university_physics(
            1,
            "13-5-keplers-laws-of-planetary-motion",
            "sec. 13.5, eq. (13.11)",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"a": 42164000.0, "mu": 398600441800000.0},
            expected=86163.57055057828,
            rel_tol=1e-12,
            note=(
                "Independent 40-digit decimal evaluation; about one sidereal day for geostationary "
                "radius."
            ),
        ),
    ),
    assumptions=(
        "Two-body problem: a satellite of negligible mass orbiting a spherically symmetric "
        "central body that is treated as fixed; no drag, thrust or third-body perturbations.",
        "Satellite mass negligible next to the central mass; otherwise mu should include both "
        "masses.",
    ),
    tags=("Kepler's third law", "orbital period", "geostationary", "semi-major axis"),
)
