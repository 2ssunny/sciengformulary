"""Keplerian Mean Motion: n = sqrt(mu / |a|^3)."""

import math

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.catalog.orbital._support import dunning_sp325, positive_result
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(mu: float, a: float) -> float:
    positive("mu", mu)
    finite("a", a)
    if a == 0:
        raise ValueError("a must not be zero (mean motion is undefined for a = 0).")
    size = abs(a)
    # sqrt(mu / size) / size equals sqrt(mu / size^3) but never forms size^3, which would
    # overflow or underflow for extreme lengths.
    return positive_result(finite_result(math.sqrt(mu / size) / size))


keplerian_mean_motion = FormulaSpec(
    id="orbital.keplerian_mean_motion",
    name="Keplerian Mean Motion",
    equation="n = sqrt(mu / abs(a)^3)",
    description=(
        "Average angular rate of a body on a two-body Kepler orbit, equal to 2 pi over the "
        "period for an ellipse. The absolute value lets the same expression serve a hyperbola, "
        "whose semi-major axis is negative."
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
            name="a",
            symbol="a",
            description="Semi-major axis (negative for a hyperbola)",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="n",
        symbol="n",
        description="Mean motion",
        dimension="T^-1",
        si_unit="rad/s",
    ),
    evaluator=_evaluate,
    references=(
        # The preprint writes Kepler's equation in Gauss form with the periapsis distance q:
        # sqrt(mu) (t - T) = q^(3/2) (1 - e)^(-3/2) (E - e sin E) for e < 1, and with
        # q^(3/2) (e - 1)^(-3/2) (e sinh H - H) for e > 1. With |a| = q / |1 - e| the factor in
        # front of the anomaly bracket is |a|^(3/2), so the anomaly grows at the rate
        # sqrt(mu / |a|^3), which is the mean motion n.
        nasa_technical_report(
            "A Numerical Solution of Kepler's Problem in Universal Variables",
            ("R. C. Blanchard", "P. E. Zadunaisky"),
            "X-643-67-627",
            1967,
            "https://ntrs.nasa.gov/citations/19680004301",
            "eq. (1.1), p. 1",
            organization="NASA Goddard Space Flight Center",
        ),
        # Stated for an ellipse, with g_e r_e^2 playing the role of mu: n = sqrt(g_e r_e^2 / a^3).
        dunning_sp325("chap. 1, 'Mean and Eccentric Anomaly', eq. (1-66), p. 16"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"mu": 398600441800000.0, "a": 7000000.0},
            expected=0.001078007612872506,
            rel_tol=1e-12,
            note="LEO-like semi-major axis of 7000 km; 50-digit mpmath evaluation.",
        ),
        VerificationCase(
            inputs={"mu": 398600441800000.0, "a": 42164000.0},
            expected=7.292159861796045e-05,
            rel_tol=1e-12,
            note="Geostationary radius, rate close to Earth's rotation; 50-digit mpmath value.",
        ),
        VerificationCase(
            inputs={"mu": 398600441800000.0, "a": -7000000.0},
            expected=0.001078007612872506,
            rel_tol=1e-12,
            note="Hyperbolic branch (a < 0) uses |a|; 50-digit mpmath value.",
        ),
    ),
    assumptions=(
        "Derived result: the source gives Kepler's equation in Gauss form with the periapsis "
        "distance q; substituting |a| = q / |1 - e| turns the coefficient of the anomaly "
        "bracket into |a|^(3/2) and gives n = sqrt(mu / |a|^3).",
        "Two-body Keplerian motion about a point or spherically symmetric central mass; no J2 or "
        "other perturbation correction.",
        "Elliptic (a > 0) and hyperbolic (a < 0) orbits only; the parabola (a infinite) is "
        "excluded, and a = 0 raises ValueError.",
        "mu must be finite and positive and a finite and non-zero; otherwise ValueError is "
        "raised. A result outside the float range, including one that underflows to zero, raises "
        "OverflowError.",
        "Any consistent units: mu in L^3/T^2 and a in L give n in radians per unit time.",
    ),
    tags=("mean motion", "Kepler", "orbit rate", "elliptic", "hyperbolic"),
)
