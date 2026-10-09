"""Semi-Latus Rectum from Semi-Major Axis and Eccentricity: p = a * (1 - e^2)."""

from sciengformulary.catalog._domain import finite, finite_result, non_negative
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.catalog.orbital._support import dunning_sp325
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(a: float, e: float) -> float:
    finite("a", a)
    non_negative("e", e)
    if a == 0:
        raise ValueError("a must not be zero.")
    if e == 1:
        raise ValueError(
            "e = 1 (parabola) has no finite semi-major axis; give the periapsis distance q "
            "and use p = 2 q instead."
        )
    # (1 - e)(1 + e) equals 1 - e^2 but keeps its accuracy when e is close to 1, where 1 - e * e
    # would subtract two nearly equal numbers.
    p = finite_result(a * (1.0 - e) * (1.0 + e))
    if p <= 0:
        raise ValueError(
            "a * (1 - e^2) must be positive: an ellipse needs a > 0 and e < 1, a hyperbola "
            f"needs a < 0 and e > 1, got a={a!r}, e={e!r}."
        )
    return p


semi_latus_rectum = FormulaSpec(
    id="orbital.semi_latus_rectum",
    name="Semi-Latus Rectum from Semi-Major Axis and Eccentricity",
    equation="p = a * (1 - e^2)",
    description=(
        "Semi-latus rectum of a Kepler conic: the distance from the focus to the conic, "
        "measured perpendicular to the major axis."
    ),
    inputs=(
        VariableSpec(
            name="a",
            symbol="a",
            description="Semi-major axis (negative for a hyperbola)",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="e",
            symbol="e",
            description="Eccentricity (not equal to 1)",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="p",
        symbol="p",
        description="Semi-latus rectum",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # The report calls p the semi-parameter, prints e = sqrt(1 - p / a) (eq. 20) and
        # p = h^2 / mu (eq. 18); squaring eq. 20 and solving for p gives p = a (1 - e^2).
        nasa_technical_report(
            "Conceptual Design of a Communications Relay Satellite for a Lunar Sample Return "
            "Mission",
            ("C. W. Brunner",),
            "NASA/CR-2005-213034",
            2005,
            "https://ntrs.nasa.gov/citations/20050232849",
            "eq. (20), p. 20 (and p = h^2 / mu, eq. 18)",
            organization="NASA Langley Research Center (The George Washington University, JIAFS)",
        ),
        # Stated for an ellipse: p = h^2 / (g_e r_e^2) (eq. 1-36, p. 9) and p = a (1 - eps^2)
        # (printed after eq. 1-36a, p. 13). The hyperbolic branch (a < 0, e > 1) is the same
        # algebra and is the form Brunner's e = sqrt(1 - p / a) already covers.
        dunning_sp325("chap. 1, eq. (1-36), p. 9, and 'p = a(1 - eps^2)' after eq. (1-36a), p. 13"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"a": 7000000.0, "e": 0.1},
            expected=6930000.0,
            rel_tol=1e-12,
            note="Ellipse with e = 0.1: 7e6 * (1 - 0.01) = 6.93e6 by hand.",
        ),
        VerificationCase(
            inputs={"a": 7000000.0, "e": 0.0},
            expected=7000000.0,
            rel_tol=1e-12,
            note="Edge e = 0 (circle): p = a.",
        ),
        VerificationCase(
            inputs={"a": -10000000.0, "e": 2.0},
            expected=30000000.0,
            rel_tol=1e-12,
            note="Hyperbola (a < 0, e > 1): -1e7 * (1 - 4) = 3e7 by hand.",
        ),
    ),
    assumptions=(
        "Derived result: the source gives e = sqrt(1 - p / a); squaring and solving for p "
        "gives p = a (1 - e^2).",
        "Two-body Keplerian conic. An ellipse needs a > 0 and e < 1, a hyperbola needs a < 0 "
        "and e > 1, so that p > 0; any other sign combination raises ValueError.",
        "The parabola (e = 1, a infinite) is excluded and raises ValueError: take p = 2 q from "
        "its periapsis distance q instead.",
        "a must be finite and non-zero and e finite and non-negative; otherwise ValueError is "
        "raised.",
        "Any consistent length unit: p has the unit of a.",
    ),
    tags=("semi-latus rectum", "semi-parameter", "conic section"),
)
