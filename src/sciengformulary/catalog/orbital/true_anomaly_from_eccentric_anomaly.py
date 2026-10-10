"""True Anomaly from Eccentric Anomaly: nu = 2 atan2(sqrt(1 + e) sin(E/2), sqrt(1 - e) cos(E/2))."""

import math

from sciengformulary.catalog._domain import finite, finite_result
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

_TWO_PI = 2.0 * math.pi


def _evaluate(e: float, E: float) -> float:  # noqa: N803
    finite("e", e)
    finite("E", E)
    if not 0 <= e < 1:
        raise ValueError(f"e must satisfy 0 <= e < 1 for an elliptic orbit, got {e!r}.")
    # Reduce E to (-pi, pi], apply the closed form there, and add the whole revolutions back so
    # that nu stays on the revolution of E for every real E (for |E| <= 2 pi this is the
    # plain atan2 expression).
    turns = round(E / _TWO_PI)
    reduced = E - turns * _TWO_PI
    nu = 2.0 * math.atan2(
        math.sqrt(1.0 + e) * math.sin(0.5 * reduced),
        math.sqrt(1.0 - e) * math.cos(0.5 * reduced),
    )
    return finite_result(nu + turns * _TWO_PI)


true_anomaly_from_eccentric_anomaly = FormulaSpec(
    id="orbital.true_anomaly_from_eccentric_anomaly",
    name="True Anomaly from Eccentric Anomaly",
    equation="nu = 2 * atan2(sqrt(1 + e) * sin(E / 2), sqrt(1 - e) * cos(E / 2))",
    description=(
        "True anomaly of an elliptic orbit from the eccentric anomaly. The result is continuous "
        "in E, so it stays on the same revolution as E instead of wrapping to (-pi, pi]."
    ),
    inputs=(
        VariableSpec(
            name="e",
            symbol="e",
            description="Eccentricity, 0 <= e < 1",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="E",
            symbol="E",
            description="Eccentric anomaly",
            dimension="1",
            si_unit="rad",
        ),
    ),
    output=VariableSpec(
        name="nu",
        symbol=r"\nu",
        description="True anomaly, on the same revolution as E",
        dimension="1",
        si_unit="rad",
    ),
    evaluator=_evaluate,
    references=(
        # The tables report prints tan(nu / 2) = sqrt((1 + e) / (1 - e)) tan(E / 2), with nu the
        # angle at the focus from periapsis and E the angle at the centre. The atan2 form
        # implemented here is a quadrant-resolved rearrangement: the positive scale factors
        # keep nu / 2 in the quadrant of E / 2. The report prints only the tangent relation;
        # the branch (continuous with E) is our choice, and libraries differ (some return
        # (-pi, pi], others keep nu on E's revolution).
        nasa_technical_report(
            "Tables for Eccentric and True Anomaly in Elliptic Orbits",
            ("J. T. Kent", "G. B. Taack, Jr.", "D. C. Larson"),
            "NASA TR R-158",
            1963,
            "https://ntrs.nasa.gov/citations/19630006382",
            "eq. (2), p. 3",
        ),
        # The second report (Brunner, not R-158) prints, in its eq. (23), the equivalent inverse
        # relation tan E = sqrt(1 - e^2) sin(nu) / (e + cos(nu)).
        nasa_technical_report(
            "Conceptual Design of a Communications Relay Satellite for a Lunar Sample Return "
            "Mission",
            ("C. W. Brunner",),
            "NASA/CR-2005-213034",
            2005,
            "https://ntrs.nasa.gov/citations/20050232849",
            "eq. (23), p. 20",
            organization="NASA Langley Research Center (The George Washington University, JIAFS)",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"e": 0.5, "E": 1.5707963267948966},
            expected=2.0943951023931953,
            rel_tol=1e-12,
            note="E = 90 degrees with e = 0.5 gives nu = 120 degrees (2 pi / 3) exactly.",
        ),
        VerificationCase(
            inputs={"e": 0.0, "E": 2.4},
            expected=2.4,
            rel_tol=1e-12,
            note="Edge e = 0 (circle): nu = E.",
        ),
        VerificationCase(
            inputs={"e": 0.3, "E": 4.0},
            expected=3.7895822925603033,
            rel_tol=1e-12,
            note="E between pi and 2 pi: nu stays on the same revolution; 50-digit mpmath value.",
        ),
        VerificationCase(
            inputs={"e": 0.8, "E": 3.141592653589793},
            expected=3.141592653589793,
            rel_tol=1e-12,
            note="Apoapsis: E = pi gives nu = pi.",
        ),
    ),
    assumptions=(
        "Derived result: the source prints tan(nu / 2) = sqrt((1 + e) / (1 - e)) tan(E / 2); "
        "the atan2 form used here resolves the quadrant of nu / 2 from the signs of sin(E / 2) "
        "and cos(E / 2).",
        "Branch convention (our choice, not the source's): the result is continuous with the "
        "input angle, so for E in [0, 2 pi] nu lies in [0, 2 pi] and nu - E is periodic in E. "
        "Whole revolutions of E are carried over to nu.",
        "Elliptic orbit only: 0 <= e < 1, otherwise ValueError is raised.",
        "Angles in radians. Floating-point resolution of very large |E| limits the accuracy of "
        "the result in absolute terms.",
    ),
    tags=("true anomaly", "eccentric anomaly", "elliptic orbit"),
)
