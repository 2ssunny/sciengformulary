"""Inverse of Barker's Equation: D = tan(nu / 2) from the normalised mean anomaly M_p."""

import math

from sciengformulary.catalog._domain import finite, finite_result
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(M_p: float) -> float:  # noqa: N803 - symbol as in the source
    finite("M_p", M_p)
    # The cubic is odd in D, so solve for |M_p| and restore the sign; this avoids cancellation
    # between B and sqrt(1 + B^2) when B is large and negative.
    b = 1.5 * abs(M_p)
    root = finite_result(b + math.hypot(1.0, b))
    a = root ** (2.0 / 3.0)
    # D = 2 A B / (1 + A + A^2), written as 2 B / (1/A + 1 + A) so that A^2 cannot overflow
    # and no near-equal terms are subtracted for small M_p.
    d = 2.0 * b / (1.0 / a + 1.0 + a)
    return finite_result(math.copysign(d, M_p))


barker_parabolic_anomaly_from_mean_anomaly = FormulaSpec(
    id="orbital.barker_parabolic_anomaly_from_mean_anomaly",
    name="Parabolic Anomaly from Normalised Mean Anomaly (Barker's Equation Inverse)",
    equation="D = 2 * A * B / (1 + A + A^2), B = 3 * M_p / 2, A = (B + sqrt(1 + B^2))^(2 / 3)",
    description=(
        "Closed-form solution of Barker's cubic for D = tan(nu / 2) given the normalised mean "
        "anomaly, with no iteration needed."
    ),
    inputs=(
        VariableSpec(
            name="M_p",
            symbol="M_p",
            description="Normalised parabolic mean anomaly sqrt(mu / (2 q^3)) (t - T)",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="D",
        symbol="D",
        description="Parabolic anomaly tan(nu / 2)",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Derived result: Barker's equation D + D^3 / 3 = M_p follows from the preprint's
        # parabolic Kepler equation, eqs. (1.1) and (1.2); see
        # orbital.barker_parabolic_mean_anomaly.
        # The depressed cubic D^3 + 3 D - 3 M_p = 0 has a positive discriminant and so a single
        # real root, D = u - 1/u with u = (B + sqrt(1 + B^2))^(1/3) and B = 3 M_p / 2 (Cardano).
        # With A = u^2 this is D = (A - 1) / sqrt(A), which equals 2 A B / (1 + A + A^2) because
        # A - 1/A = 2 B. The second form is the one evaluated, since it does not cancel for
        # small M_p.
        nasa_technical_report(
            "A Numerical Solution of Kepler's Problem in Universal Variables",
            ("R. C. Blanchard", "P. E. Zadunaisky"),
            "X-643-67-627",
            1967,
            "https://ntrs.nasa.gov/citations/19680004301",
            "eqs. (1.1) second line and (1.2), p. 1",
            organization="NASA Goddard Space Flight Center",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"M_p": 1.3333333333333333},
            expected=1.0,
            rel_tol=1e-12,
            note="Hand calculation: M_p = 4/3 gives D = 1 (D + D^3 / 3 = 4/3), up to rounding.",
        ),
        VerificationCase(
            inputs={"M_p": 0.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Periapsis: the only real root of D + D^3 / 3 = 0 is D = 0.",
        ),
        VerificationCase(
            inputs={"M_p": -10.0},
            expected=-2.7866708131026976,
            rel_tol=1e-12,
            note="Negative M_p: the solution is odd in M_p; independent 50-digit mpmath value.",
        ),
        VerificationCase(
            inputs={"M_p": 1000000.0},
            expected=144.21802341800267,
            rel_tol=1e-12,
            note="Very large M_p, where D grows like the cube root; 50-digit mpmath value.",
        ),
    ),
    assumptions=(
        "Derived result: the Cardano closed form of the cubic in Barker's equation; the cubic "
        "has exactly one real root for every real M_p.",
        "Parabolic orbit. Normalisation fixed by the source: M_p = sqrt(mu / (2 q^3)) (t - T) "
        "with q the periapsis distance, so M_p = 4/3 at nu = 90 degrees.",
        "The true anomaly is nu = 2 atan(D), which lies strictly between -pi and pi.",
        "Magnitudes of M_p near the floating-point limit (about 6e307) raise OverflowError.",
    ),
    tags=("Barker's equation", "parabolic orbit", "cubic", "true anomaly"),
)
