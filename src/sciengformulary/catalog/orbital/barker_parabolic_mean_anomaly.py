"""Barker's Equation: M_p = tan(nu / 2) + tan(nu / 2)^3 / 3."""

import math

from sciengformulary.catalog._domain import finite, finite_result
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(nu: float) -> float:
    if abs(finite("nu", nu)) >= math.pi:
        raise ValueError(f"nu must satisfy |nu| < pi on a parabolic orbit, got {nu!r}.")
    d = math.tan(0.5 * nu)
    return finite_result(d + d**3 / 3.0)


barker_parabolic_mean_anomaly = FormulaSpec(
    id="orbital.barker_parabolic_mean_anomaly",
    name="Barker's Equation (Normalised Parabolic Mean Anomaly)",
    equation="M_p = tan(nu / 2) + tan(nu / 2)^3 / 3",
    description=(
        "Normalised time since periapsis on a parabolic orbit, sqrt(mu / (2 q^3)) (t - T), "
        "expressed through the true anomaly."
    ),
    inputs=(
        VariableSpec(
            name="nu",
            symbol=r"\nu",
            description="True anomaly, strictly between -pi and pi",
            dimension="1",
            si_unit="rad",
        ),
    ),
    output=VariableSpec(
        name="M_p",
        symbol="M_p",
        description="Normalised parabolic mean anomaly sqrt(mu / (2 q^3)) (t - T)",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Derived result: the preprint writes the parabolic case of Kepler's equation as
        # sqrt(mu) (t - T) = q beta + beta^3 / 6 with beta = sqrt(2 q) tan(nu / 2) (eqs. (1.1) and
        # (1.2)). Substituting beta gives sqrt(mu) (t - T) = sqrt(2) q^(3/2) (D + D^3 / 3) with
        # D = tan(nu / 2), so sqrt(mu / (2 q^3)) (t - T) = D + D^3 / 3. The normalisation is
        # the one fixed by this source; other texts scale the time differently.
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
            inputs={"nu": 1.5707963267948966},
            expected=1.3333333333333333,
            rel_tol=1e-12,
            note="Hand calculation at nu = 90 degrees: tan(45 deg) = 1, so M_p = 1 + 1/3 = 4/3.",
        ),
        VerificationCase(
            inputs={"nu": 0.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Periapsis: tan(0) = 0 so M_p = 0 exactly.",
        ),
        VerificationCase(
            inputs={"nu": -2.0},
            expected=-2.8165816405991544,
            rel_tol=1e-12,
            note="Inbound leg: the function is odd in nu; independent 50-digit mpmath value.",
        ),
        VerificationCase(
            inputs={"nu": 3.0},
            expected=948.7907480744601,
            rel_tol=1e-12,
            note="Close to the asymptote nu -> pi, where M_p is very large; 50-digit mpmath value.",
        ),
    ),
    assumptions=(
        "Derived result: algebra on the stated Gauss form of the parabolic Kepler equation, "
        "with D = tan(nu / 2) substituted for beta.",
        "Parabolic orbit (e = 1). The true anomaly must satisfy |nu| < pi, where tan(nu / 2) "
        "is finite; other values raise ValueError. Angles in radians, with no wrapping applied.",
        "Normalisation fixed by the source: M_p = sqrt(mu / (2 q^3)) (t - T) with q the "
        "periapsis distance, so M_p = 4/3 at nu = 90 degrees. The caller applies the time "
        "scaling; M_p is dimensionless.",
    ),
    tags=("Barker's equation", "parabolic orbit", "mean anomaly", "true anomaly"),
)
