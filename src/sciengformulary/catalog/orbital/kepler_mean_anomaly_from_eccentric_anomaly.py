"""Kepler's Equation, Mean Anomaly from Eccentric Anomaly: M = E - e * sin(E)."""

import math

from sciengformulary.catalog._domain import finite, finite_result
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _x_minus_sin_x(x: float) -> float:
    """x - sin(x) without the cancellation for small |x| (Taylor series x^3/3! - x^5/5! + ...)."""
    if abs(x) >= 0.5:
        return x - math.sin(x)
    total = 0.0
    term = x * x * x / 6.0
    k = 3
    while True:
        total += term
        term *= -x * x / ((k + 1.0) * (k + 2.0))
        k += 2
        if abs(term) <= 1e-18 * abs(total):
            return total + term


def _evaluate(e: float, E: float) -> float:  # noqa: N803
    finite("e", e)
    finite("E", E)
    if not 0 <= e < 1:
        raise ValueError(f"e must satisfy 0 <= e < 1 for an elliptic orbit, got {e!r}.")
    # E - e sin E = (1 - e) E + e (E - sin E). Both terms have the sign of E, so nothing cancels
    # when e is close to 1 or E is small, where the direct difference loses digits.
    return finite_result((1.0 - e) * E + e * _x_minus_sin_x(E))


kepler_mean_anomaly_from_eccentric_anomaly = FormulaSpec(
    id="orbital.kepler_mean_anomaly_from_eccentric_anomaly",
    name="Kepler's Equation (Mean Anomaly from Eccentric Anomaly)",
    equation="M = E - e * sin(E)",
    description=(
        "Explicit direction of Kepler's equation for an elliptic orbit: the mean anomaly that "
        "belongs to a given eccentric anomaly. The reverse direction has no closed form."
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
        name="M",
        symbol="M",
        description="Mean anomaly",
        dimension="1",
        si_unit="rad",
    ),
    evaluator=_evaluate,
    references=(
        # Stated: the tables report prints E - e sin E = M, with M the mean anomaly.
        nasa_technical_report(
            "Tables for Eccentric and True Anomaly in Elliptic Orbits",
            ("J. T. Kent", "G. B. Taack, Jr.", "D. C. Larson"),
            "NASA TR R-158",
            1963,
            "https://ntrs.nasa.gov/citations/19630006382",
            "eq. (1), p. 3 (printed page 3)",
        ),
        # Time of flight written as sqrt(a^3 / mu) [(E1 - e sin E1) - (E0 - e sin E0)], which
        # confirms that the mean anomaly is E - e sin E.
        nasa_technical_report(
            "Conceptual Design of a Communications Relay Satellite for a Lunar Sample Return "
            "Mission",
            ("C. W. Brunner",),
            "NASA/CR-2005-213034",
            2005,
            "https://ntrs.nasa.gov/citations/20050232849",
            "eq. (25), p. 20",
            organization="NASA Langley Research Center (The George Washington University, JIAFS)",
        ),
        # The same relation with the time scaling written out: sqrt(mu / a^3) (t - T) =
        # E - e sin E.
        nasa_technical_report(
            "A Numerical Solution of Kepler's Problem in Universal Variables",
            ("R. C. Blanchard", "P. E. Zadunaisky"),
            "X-643-67-627",
            1967,
            "https://ntrs.nasa.gov/citations/19680004301",
            "eq. (1.1), p. 1",
            organization="NASA Goddard Space Flight Center",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"e": 0.5, "E": 1.5707963267948966},
            expected=1.0707963267948966,
            rel_tol=1e-12,
            note="E = 90 degrees: pi/2 - 0.5 = 1.0707963... by hand; matches 50-digit mpmath.",
        ),
        VerificationCase(
            inputs={"e": 0.0, "E": 1.7},
            expected=1.7,
            rel_tol=1e-12,
            note="Edge e = 0 (circle): M = E.",
        ),
        VerificationCase(
            inputs={"e": 0.9, "E": 3.5},
            expected=3.8157049049206577,
            rel_tol=1e-12,
            note="Highly eccentric orbit with E beyond pi, no wrapping; 50-digit mpmath value.",
        ),
        VerificationCase(
            inputs={"e": 0.3, "E": 0.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Periapsis: M = 0 when E = 0.",
        ),
    ),
    assumptions=(
        "Elliptic orbit only: 0 <= e < 1, otherwise ValueError is raised. The hyperbolic "
        "counterpart has a different equation.",
        "No angle normalisation: M changes by 2 pi whenever E does, and any finite E (radians) "
        "is accepted.",
        "This is the explicit direction only; finding E from M needs an iterative solution of "
        "this equation and is not provided.",
        "E and M are in radians; the equation is not valid for angles in degrees.",
    ),
    tags=("Kepler's equation", "mean anomaly", "eccentric anomaly", "elliptic orbit"),
)
