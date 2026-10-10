"""Hyperbolic Eccentric Anomaly from True Anomaly.

H = asinh(sqrt(e^2 - 1) * sin(nu) / (1 + e * cos(nu))).
"""

import math

from sciengformulary.catalog._domain import finite, finite_result
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(e: float, nu: float) -> float:
    if finite("e", e) <= 1:
        raise ValueError(f"e must exceed 1 for a hyperbolic orbit, got {e!r}.")
    finite("nu", nu)
    nu_inf = math.acos(-1.0 / e)
    if abs(nu) >= nu_inf:
        raise ValueError(
            f"nu must satisfy |nu| < acos(-1/e) = {nu_inf!r} on a hyperbolic orbit, got {nu!r}."
        )
    denominator = 1.0 + e * math.cos(nu)
    if denominator <= 0.0:
        raise ValueError(f"1 + e cos(nu) must be positive, got {denominator!r}.")
    # (e - 1)(e + 1) equals e^2 - 1 but keeps full precision when e is close to 1.
    root = math.sqrt((e - 1.0) * (e + 1.0))
    return finite_result(math.asinh(root * math.sin(nu) / denominator))


hyperbolic_eccentric_anomaly_from_true_anomaly = FormulaSpec(
    id="orbital.hyperbolic_eccentric_anomaly_from_true_anomaly",
    name="Hyperbolic Eccentric Anomaly from True Anomaly",
    equation="H = asinh(sqrt(e^2 - 1) * sin(nu) / (1 + e * cos(nu)))",
    description=(
        "Hyperbolic eccentric anomaly of a hyperbolic orbit from the true anomaly, with the "
        "same sign as nu."
    ),
    inputs=(
        VariableSpec(
            name="e",
            symbol="e",
            description="Eccentricity of the hyperbolic orbit",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="nu",
            symbol=r"\nu",
            description="True anomaly, within the open interval (-nu_inf, nu_inf)",
            dimension="1",
            si_unit="rad",
        ),
    ),
    output=VariableSpec(
        name="H",
        symbol="H",
        description="Hyperbolic eccentric anomaly",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Derived result: the preprint defines H through the hyperbolic Kepler equation
        # sqrt(mu / |a|^3) (t - T) = e sinh H - H. Taking the conic r = p / (1 + e cos nu), the
        # areal law r^2 dnu/dt = sqrt(mu p) and |a| = p / (e^2 - 1), the function e sinh H - H
        # with H = asinh(sqrt(e^2 - 1) sin nu / (1 + e cos nu)) vanishes at nu = 0 and has the
        # derivative n r^2 / h with respect to nu, so it equals n (t - T). The preprint itself
        # does not print H as a function of nu.
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
            inputs={"e": 2.0, "nu": 1.35},
            expected=1.0000213593109137,
            rel_tol=1e-12,
            note="e = 2 and nu = 1.35 rad; independent 50-digit mpmath evaluation.",
        ),
        VerificationCase(
            inputs={"e": 2.0, "nu": 0.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Periapsis: sin(0) = 0 so H = 0 exactly.",
        ),
        VerificationCase(
            inputs={"e": 1.5, "nu": -1.9},
            expected=-1.4675706294660553,
            rel_tol=1e-12,
            note=(
                "Inbound leg close to the asymptote at -acos(-1/1.5), about -2.30 rad; "
                "50-digit mpmath value."
            ),
        ),
    ),
    assumptions=(
        "Derived result: the relation follows from the stated hyperbolic Kepler equation, the "
        "conic equation and the areal law, as checked by differentiating e sinh H - H with "
        "respect to nu.",
        "Hyperbolic orbit, e > 1; values e <= 1 raise ValueError.",
        "Branch convention (our choice, not the source's): nu must lie strictly inside "
        "(-nu_inf, nu_inf) with nu_inf = acos(-1/e), the angles actually reached on the "
        "hyperbola; other angles raise ValueError instead of being wrapped. H has the sign of "
        "nu and H = 0 at periapsis.",
        "Angles in radians.",
    ),
    tags=("hyperbolic orbit", "hyperbolic anomaly", "true anomaly", "anomaly conversion"),
)
