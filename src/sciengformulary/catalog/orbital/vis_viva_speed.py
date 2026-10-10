"""Vis-Viva Orbital Speed: v = sqrt(mu * (2 / r - 1 / a))."""

import math

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.catalog.orbital._support import dunning_sp325
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(mu: float, r: float, a: float) -> float:
    positive("mu", mu)
    positive("r", r)
    finite("a", a)
    if a == 0:
        raise ValueError("a must not be zero.")
    two_a = 2.0 * a
    if math.isfinite(two_a):
        # 2 / r - 1 / a = (2 a - r) / (r a). The difference 2 a - r is computed exactly when r is
        # within a factor of two of 2 a, so the radicand stays accurate as r approaches 2 a.
        radicand = finite_result((mu / r) * ((two_a - r) / a))
    else:
        radicand = finite_result(mu * (2.0 / r - 1.0 / a))
    if radicand < 0:
        raise ValueError(
            "mu * (2 / r - 1 / a) must not be negative (r cannot exceed 2 a), "
            f"got r={r!r}, a={a!r}."
        )
    return math.sqrt(radicand)


vis_viva_speed = FormulaSpec(
    id="orbital.vis_viva_speed",
    name="Vis-Viva Orbital Speed",
    equation="v = sqrt(mu * (2 / r - 1 / a))",
    description=(
        "Speed of a body at distance r on a conic orbit of semi-major axis a (negative for a "
        "hyperbola), obtained from conservation of energy: it expresses v^2 / 2 - mu / r = "
        "-mu / (2 a), the relation between the specific energy and the semi-major axis."
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
            description="Current distance from the centre of the central body",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="a",
            symbol="a",
            description="Semi-major axis (negative for a hyperbola)",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="v",
        symbol="v",
        description="Orbital speed",
        dimension="L T^-1",
        si_unit="m/s",
    ),
    evaluator=_evaluate,
    references=(
        # The report prints sqrt(2 mu / r - mu / a) for the speed at the apsides of its transfer
        # ellipse (eqs. 7, 8, 37) and the energy relations xi = v^2 / 2 - mu / r (eq. 15) and
        # a = -mu / (2 xi) (eq. 19). Eliminating xi between the last two gives the general form
        # here, which also holds for a hyperbola (xi > 0, a < 0).
        nasa_technical_report(
            "Conceptual Design of a Communications Relay Satellite for a Lunar Sample Return "
            "Mission",
            ("C. W. Brunner",),
            "NASA/CR-2005-213034",
            2005,
            "https://ntrs.nasa.gov/citations/20050232849",
            "eqs. (7), (8), (37), p. 16 and p. 23; eqs. (12), (15), (19), pp. 19-20",
            organization="NASA Langley Research Center (The George Washington University, JIAFS)",
        ),
        # The energy equation V^2 / 2 = H + g_e r_e^2 / r is printed for all orbits (eq. 1-29)
        # and a = -g_e r_e^2 / (2 H) for an ellipse (eq. 1-47), with g_e r_e^2 playing the role
        # of mu. Eliminating H gives the form here; the extension to a < 0 (hyperbola, H > 0)
        # is the same algebra, since the report gives H > 0 for the hyperbola.
        dunning_sp325("chap. 1, eq. (1-29), p. 8, and eq. (1-47), p. 13"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"mu": 398600441800000.0, "r": 6678000.0, "a": 24421000.0},
            expected=10151.608507443249,
            rel_tol=1e-12,
            note="Geostationary transfer orbit, perigee speed; 50-digit mpmath evaluation.",
        ),
        VerificationCase(
            inputs={"mu": 398600441800000.0, "r": 42164000.0, "a": 24421000.0},
            expected=1607.8275688432316,
            rel_tol=1e-12,
            note="Geostationary transfer orbit, apogee speed; 50-digit mpmath evaluation.",
        ),
        VerificationCase(
            inputs={"mu": 398600441800000.0, "r": 7000000.0, "a": 7000000.0},
            expected=7546.053290107542,
            rel_tol=1e-12,
            note="Edge r = a reproduces the circular speed; 50-digit mpmath evaluation.",
        ),
        VerificationCase(
            inputs={"mu": 398600441800000.0, "r": 7000000.0, "a": -20000000.0},
            expected=11567.880644451934,
            rel_tol=1e-12,
            note="Hyperbolic branch (a < 0); 50-digit mpmath evaluation.",
        ),
    ),
    assumptions=(
        "Derived result: the cited report prints the vis-viva speed at the apsides of its "
        "transfer ellipse together with the energy relations; eliminating the specific energy "
        "between v^2 / 2 - mu / r = xi and a = -mu / (2 xi) gives the general form used here.",
        "Two-body Keplerian motion about a point or spherically symmetric central mass.",
        "Needs mu * (2 / r - 1 / a) >= 0, which for an ellipse means r <= 2 a; a negative "
        "value raises ValueError instead of being clamped.",
        "The parabola (1 / a = 0) is outside the input domain: a = 0 raises ValueError.",
        "mu and r must be finite and positive, and a finite and non-zero; otherwise "
        "ValueError is raised.",
        "Any consistent units: mu in L^3/T^2, r and a in L give a speed in L/T.",
    ),
    tags=("vis-viva", "orbital speed", "energy", "Hohmann"),
)
