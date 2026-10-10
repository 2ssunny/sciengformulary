"""Flight-Path Angle on a Conic Orbit: gamma = atan2(e * sin(nu), 1 + e * cos(nu))."""

import math

from sciengformulary.catalog._domain import finite, non_negative
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.catalog.orbital._support import dunning_sp325
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(e: float, nu: float) -> float:
    non_negative("e", e)
    finite("nu", nu)
    denominator = 1.0 + e * math.cos(nu)
    if denominator <= 0:
        raise ValueError(
            "1 + e * cos(nu) must be positive (nu lies on or beyond an asymptote), "
            f"got e={e!r}, nu={nu!r}."
        )
    return math.atan2(e * math.sin(nu), denominator)


flight_path_angle = FormulaSpec(
    id="orbital.flight_path_angle",
    name="Flight-Path Angle on a Conic Orbit",
    equation="gamma = atan2(e * sin(nu), 1 + e * cos(nu))",
    description=(
        "Angle between the velocity vector and the local horizontal (the direction "
        "perpendicular to the radius) at true anomaly nu; positive while the body moves away "
        "from the focus."
    ),
    inputs=(
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
        name="gamma",
        symbol=r"\gamma",
        description="Flight-path angle from the local horizontal, in (-pi/2, pi/2)",
        dimension="1",
        si_unit="rad",
    ),
    evaluator=_evaluate,
    references=(
        # The report gives cos(phi) = h / (r v) from h = r v cos(phi) (eqs. 13, 16), where phi
        # is the flight-path angle, and so fixes only its magnitude. With h = sqrt(mu p),
        # r = p / (1 + e cos nu) and v^2 = (mu / p) (1 + 2 e cos nu + e^2) this becomes
        # cos(gamma) = (1 + e cos nu) / sqrt(1 + 2 e cos nu + e^2) and the matching
        # sin(gamma) = e sin(nu) / sqrt(...), which the atan2 form combines. The sign (positive
        # outbound) is our convention for the angle above the local horizontal. Some libraries
        # cite Vallado for the same relation; that book was not opened here.
        nasa_technical_report(
            "Conceptual Design of a Communications Relay Satellite for a Lunar Sample Return "
            "Mission",
            ("C. W. Brunner",),
            "NASA/CR-2005-213034",
            2005,
            "https://ntrs.nasa.gov/citations/20050232849",
            "eqs. (13), (16), p. 19",
            organization="NASA Langley Research Center (The George Washington University, JIAFS)",
        ),
        # Derived result (second source supports the ingredients only): with h = r^2 theta_dot
        # (eq. 1-23), r_dot = (h / r^2) dr/dtheta (eq. 1-31) and r = p / (1 + e cos(theta))
        # (eq. 1-38), r_dot / (r theta_dot) = (1 / r) dr/dtheta = e sin(theta) / (1 + e cos(theta)),
        # the tangent of the angle between the velocity and the local horizontal. The report
        # does not name that angle in chapter 1.
        dunning_sp325("chap. 1, eqs. (1-23), (1-31), (1-38), pp. 7-10"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"e": 0.0, "nu": 1.3},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Circular orbit: the flight-path angle is zero for any true anomaly.",
        ),
        VerificationCase(
            inputs={"e": 0.5, "nu": 1.5707963267948966},
            expected=0.4636476090008061,
            rel_tol=1e-12,
            note="e = 0.5 at nu = 90 degrees gives atan(0.5); 50-digit mpmath value.",
        ),
        VerificationCase(
            inputs={"e": 0.3, "nu": -2.0},
            expected=-0.3021591249043568,
            rel_tol=1e-12,
            note="Inbound leg (nu < 0) gives a negative angle; 50-digit mpmath value.",
        ),
        VerificationCase(
            inputs={"e": 2.0, "nu": 2.0},
            expected=1.478838878440151,
            rel_tol=1e-12,
            note="Hyperbola with nu close to its asymptote; 50-digit mpmath value.",
        ),
        VerificationCase(
            inputs={"e": 0.3, "nu": 3.141592653589793},
            expected=5.248486282060085e-17,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Apoapsis: zero up to the rounding of sin(pi); 50-digit mpmath value.",
        ),
    ),
    assumptions=(
        "Derived result: the cited report fixes only cos(phi) = h / (r v). Substituting "
        "h = sqrt(mu p), r = p / (1 + e cos nu) and v^2 = (mu / p) (1 + 2 e cos nu + e^2) gives "
        "tan(gamma) = e sin(nu) / (1 + e cos(nu)), and the atan2 form carries the sign.",
        "Two-body Keplerian conic of any eccentricity e >= 0 (circle, ellipse, parabola or "
        "hyperbola).",
        "The angle is measured from the local horizontal, positive outward, not from the local "
        "vertical; the sign convention is ours, not the report's.",
        "For e >= 1 only true anomalies inside the asymptotes are physical, so "
        "1 + e cos(nu) <= 0 raises ValueError; e < 0 or non-finite inputs also raise "
        "ValueError.",
        "nu is in radians; the result is in radians and always lies in (-pi/2, pi/2).",
    ),
    tags=("flight-path angle", "true anomaly", "eccentricity"),
)
