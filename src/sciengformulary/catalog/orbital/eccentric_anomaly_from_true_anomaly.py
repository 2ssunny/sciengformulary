"""Eccentric Anomaly from True Anomaly:
E = 2 atan2(sqrt(1 - e) sin(nu/2), sqrt(1 + e) cos(nu/2)).
"""

import math

from sciengformulary.catalog._domain import finite, finite_result
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

_TWO_PI = 2.0 * math.pi


def _evaluate(e: float, nu: float) -> float:
    finite("e", e)
    finite("nu", nu)
    if not 0 <= e < 1:
        raise ValueError(f"e must satisfy 0 <= e < 1 for an elliptic orbit, got {e!r}.")
    # Same branch handling as orbital.true_anomaly_from_eccentric_anomaly: reduce nu to
    # (-pi, pi], apply the closed form, and add the whole revolutions back.
    turns = round(nu / _TWO_PI)
    reduced = nu - turns * _TWO_PI
    big_e = 2.0 * math.atan2(
        math.sqrt(1.0 - e) * math.sin(0.5 * reduced),
        math.sqrt(1.0 + e) * math.cos(0.5 * reduced),
    )
    return finite_result(big_e + turns * _TWO_PI)


eccentric_anomaly_from_true_anomaly = FormulaSpec(
    id="orbital.eccentric_anomaly_from_true_anomaly",
    name="Eccentric Anomaly from True Anomaly",
    equation="E = 2 * atan2(sqrt(1 - e) * sin(nu / 2), sqrt(1 + e) * cos(nu / 2))",
    description=(
        "Eccentric anomaly of an elliptic orbit from the true anomaly. The result is continuous "
        "in nu, so it stays on the same revolution as nu instead of wrapping to (-pi, pi]."
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
            name="nu",
            symbol=r"\nu",
            description="True anomaly, measured from periapsis",
            dimension="1",
            si_unit="rad",
        ),
    ),
    output=VariableSpec(
        name="E",
        symbol="E",
        description="Eccentric anomaly, on the same revolution as nu",
        dimension="1",
        si_unit="rad",
    ),
    evaluator=_evaluate,
    references=(
        # Inverting the printed tan(nu / 2) = sqrt((1 + e) / (1 - e)) tan(E / 2) gives
        # tan(E / 2) = sqrt((1 - e) / (1 + e)) tan(nu / 2); the atan2 form resolves the quadrant
        # (positive scale factors keep E / 2 in the quadrant of nu / 2). The branch (continuous
        # with nu) is our choice, not the source's.
        nasa_technical_report(
            "Tables for Eccentric and True Anomaly in Elliptic Orbits",
            ("J. T. Kent", "G. B. Taack, Jr.", "D. C. Larson"),
            "NASA TR R-158",
            1963,
            "https://ntrs.nasa.gov/citations/19630006382",
            "eq. (2), p. 3",
        ),
        # The second report (Brunner, not R-158) prints, in its eq. (23), tan E = sqrt(1 - e^2)
        # sin(nu) / (e + cos(nu)), consistent with the inverse used here.
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
            inputs={"e": 0.5, "nu": 2.0943951023931953},
            expected=1.5707963267948963,
            rel_tol=1e-12,
            note="Inverse of the E = 90 degrees case: nu = 120 degrees, e = 0.5.",
        ),
        VerificationCase(
            inputs={"e": 0.0, "nu": 2.4},
            expected=2.4,
            rel_tol=1e-12,
            note="Edge e = 0 (circle): E = nu.",
        ),
        VerificationCase(
            inputs={"e": 0.3, "nu": 5.0},
            expected=5.280319491381671,
            rel_tol=1e-12,
            note="nu between pi and 2 pi: E stays on the same revolution; 50-digit mpmath value.",
        ),
        VerificationCase(
            inputs={"e": 0.9, "nu": 0.1},
            expected=0.02295970185248208,
            rel_tol=1e-12,
            note="High eccentricity near periapsis; 50-digit mpmath value.",
        ),
    ),
    assumptions=(
        "Derived result: the source prints tan(nu / 2) = sqrt((1 + e) / (1 - e)) tan(E / 2); "
        "inverting it gives tan(E / 2) = sqrt((1 - e) / (1 + e)) tan(nu / 2), and the atan2 "
        "form used here resolves the quadrant.",
        "Branch convention (our choice, not the source's): the result is continuous with the "
        "input angle, so for nu in [0, 2 pi] E lies in [0, 2 pi]. Whole revolutions of nu are "
        "carried over to E, as in orbital.true_anomaly_from_eccentric_anomaly.",
        "Elliptic orbit only: 0 <= e < 1, otherwise ValueError is raised.",
        "Angles in radians. Floating-point resolution of very large |nu| limits the accuracy "
        "of the result in absolute terms.",
    ),
    tags=("eccentric anomaly", "true anomaly", "elliptic orbit"),
)
