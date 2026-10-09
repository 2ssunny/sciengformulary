"""Circular Orbit Speed: v_c = sqrt(mu / r)."""

import math

from sciengformulary.catalog._domain import positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.catalog.orbital._support import dunning_sp325
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(mu: float, r: float) -> float:
    positive("mu", mu)
    positive("r", r)
    return math.sqrt(mu / r)


circular_orbit_speed = FormulaSpec(
    id="orbital.circular_orbit_speed",
    name="Circular Orbit Speed",
    equation="v_c = sqrt(mu / r)",
    description=(
        "Speed of a body in a circular orbit of radius r about a central body with "
        "gravitational parameter mu."
    ),
    inputs=(
        VariableSpec(
            name="mu",
            symbol=r"\mu",
            description="Standard gravitational parameter G M of the central body",
            dimension="L^3 T^-2",
            si_unit="m^3/s^2",
        ),
        VariableSpec(
            name="r",
            symbol="r",
            description="Orbit radius, measured from the centre of the central body",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="v_c",
        symbol="v_c",
        description="Circular orbit speed",
        dimension="L T^-1",
        si_unit="m/s",
    ),
    evaluator=_evaluate,
    references=(
        # Stated: the report gives the speeds of the initial and final circular orbits as
        # sqrt(mu / r_initial) and sqrt(mu / r_final); each of those radii is this r.
        nasa_technical_report(
            "Conceptual Design of a Communications Relay Satellite for a Lunar Sample Return "
            "Mission",
            ("C. W. Brunner",),
            "NASA/CR-2005-213034",
            2005,
            "https://ntrs.nasa.gov/citations/20050232849",
            "eqs. (4)-(5), p. 15",
            organization="NASA Langley Research Center (The George Washington University, JIAFS)",
        ),
        # Stated, with the symbols renamed: the circular-orbit speed is V_cir = sqrt(g_e r_e^2 /
        # r_cir), where the report's g_e r_e^2 (eq. 1-18) plays the role of mu.
        dunning_sp325("chap. 1, 'Circular orbit', eq. (1-51), p. 14 (and eq. 1-18, p. 7)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"mu": 398600441800000.0, "r": 6778000.0},
            expected=7668.635675197651,
            rel_tol=1e-12,
            note="400 km altitude circular orbit; 50-digit mpmath evaluation.",
        ),
        VerificationCase(
            inputs={"mu": 398600441800000.0, "r": 42164000.0},
            expected=3074.6662841276843,
            rel_tol=1e-12,
            note="Geostationary radius; 50-digit mpmath evaluation.",
        ),
        VerificationCase(
            inputs={"mu": 397532000000000.0, "r": 6760000.0},
            expected=7668.54020500249,
            rel_tol=1e-12,
            note="Low orbit with a rounded Earth mu; 50-digit mpmath evaluation of sqrt(mu / r).",
        ),
    ),
    assumptions=(
        "Two-body motion on a circular orbit about a point or spherically symmetric central "
        "mass; no drag, thrust or third-body perturbations.",
        "Satellite mass negligible next to the central mass; otherwise mu includes both masses.",
        "mu and r must be finite and positive; otherwise ValueError is raised.",
        "Any consistent units: mu in L^3/T^2 and r in L give a speed in L/T.",
    ),
    tags=("circular orbit", "orbital speed", "satellite"),
)
