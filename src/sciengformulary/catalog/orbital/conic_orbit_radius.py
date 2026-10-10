"""Conic Orbit Radius: r = p / (1 + e * cos(nu))."""

import math

from sciengformulary.catalog._domain import finite, finite_result, non_negative, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.catalog.orbital._support import dunning_sp325
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(p: float, e: float, nu: float) -> float:
    positive("p", p)
    non_negative("e", e)
    finite("nu", nu)
    denominator = 1.0 + e * math.cos(nu)
    if denominator <= 0:
        raise ValueError(
            "1 + e * cos(nu) must be positive (nu lies on or beyond an asymptote), "
            f"got e={e!r}, nu={nu!r}."
        )
    return finite_result(p / denominator)


conic_orbit_radius = FormulaSpec(
    id="orbital.conic_orbit_radius",
    name="Conic Orbit Radius",
    equation="r = p / (1 + e * cos(nu))",
    description=(
        "Distance from the focus to a point on a Kepler conic, from the semi-latus rectum, the "
        "eccentricity and the true anomaly."
    ),
    inputs=(
        VariableSpec(
            name="p",
            symbol="p",
            description="Semi-latus rectum of the conic",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="e",
            symbol="e",
            description="Eccentricity",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="nu",
            symbol=r"\nu",
            description="True anomaly, measured from periapsis",
            dimension="1",
            si_unit="rad",
        ),
    ),
    output=VariableSpec(
        name="r",
        symbol="r",
        description="Distance from the focus",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # The report gives cos(nu) = (p - r) / (e r) with p = h^2 / mu (eqs. 21-22); solving
        # for r gives r = p / (1 + e cos(nu)).
        nasa_technical_report(
            "Conceptual Design of a Communications Relay Satellite for a Lunar Sample Return "
            "Mission",
            ("C. W. Brunner",),
            "NASA/CR-2005-213034",
            2005,
            "https://ntrs.nasa.gov/citations/20050232849",
            "eqs. (21)-(22), p. 20",
            organization="NASA Langley Research Center (The George Washington University, JIAFS)",
        ),
        # Stated, with the symbols renamed: the report writes the conic as r = p / (1 + eps
        # cos(theta - theta_0)) with eps the eccentricity and theta - theta_0 the true anomaly.
        dunning_sp325("chap. 1, 'Equation of a Conic Section', eq. (1-38), p. 10"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"p": 6930000.0, "e": 0.1, "nu": 0.0},
            expected=6300000.0,
            rel_tol=1e-12,
            note="Periapsis of an ellipse, p / (1 + e) = 6.93e6 / 1.1; exact arithmetic.",
        ),
        VerificationCase(
            inputs={"p": 6930000.0, "e": 0.1, "nu": 3.141592653589793},
            expected=7700000.0,
            rel_tol=1e-12,
            note="Apoapsis of an ellipse, p / (1 - e) = 6.93e6 / 0.9; exact arithmetic.",
        ),
        VerificationCase(
            inputs={"p": 10000000.0, "e": 2.0, "nu": 1.0},
            expected=4806295.219952881,
            rel_tol=1e-12,
            note="Hyperbola inside its asymptotes (1 + e cos nu > 0); 50-digit mpmath value.",
        ),
        VerificationCase(
            inputs={"p": 10000000.0, "e": 1.0, "nu": 1.5707963267948966},
            expected=10000000.0,
            rel_tol=1e-12,
            note="Parabola at nu = 90 degrees, where r = p.",
        ),
        VerificationCase(
            inputs={"p": 7000000.0, "e": 0.0, "nu": 2.2},
            expected=7000000.0,
            rel_tol=1e-12,
            note="Edge e = 0 (circle): r = p for any true anomaly.",
        ),
    ),
    assumptions=(
        "Derived result: the cited report states cos(nu) = (p - r) / (e r); solving this for r "
        "gives the polar form r = p / (1 + e cos(nu)), which is the one implemented here.",
        "Two-body Keplerian conic: circle, ellipse, parabola and hyperbola are all covered "
        "because the form uses the semi-latus rectum rather than the semi-major axis.",
        "p must be positive and e >= 0. For e >= 1 only angles inside the asymptotes are "
        "physical, so 1 + e cos(nu) <= 0 raises ValueError.",
        "nu is in radians and is not wrapped; any finite value is accepted for e < 1.",
        "Any consistent length unit: r has the unit of p.",
    ),
    tags=("orbit equation", "true anomaly", "conic section", "polar form"),
)
