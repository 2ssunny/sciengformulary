"""Hyperbolic Kepler Equation: M_h = e * sinh(H) - H."""

import math

from sciengformulary.catalog._domain import finite, finite_result
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _sinh_minus_x(x: float) -> float:
    """sinh(x) - x without the cancellation for small |x| (series x^3/3! + x^5/5! + ...)."""
    if abs(x) >= 0.5:
        return math.sinh(x) - x
    total = 0.0
    term = x * x * x / 6.0
    k = 3
    while True:
        total += term
        term *= x * x / ((k + 1.0) * (k + 2.0))
        k += 2
        if abs(term) <= 1e-18 * abs(total):
            return total + term


def _evaluate(e: float, H: float) -> float:  # noqa: N803 - symbols as in the source
    if finite("e", e) <= 1:
        raise ValueError(f"e must exceed 1 for a hyperbolic orbit, got {e!r}.")
    finite("H", H)
    try:
        sinh_h = math.sinh(H)
        small_part = _sinh_minus_x(H)
    except OverflowError:
        raise OverflowError(f"sinh(H) is outside the floating-point range for H={H!r}.") from None
    # e sinh H - H = (e - 1) sinh H + (sinh H - H). Both terms have the sign of H, so nothing
    # cancels when e is close to 1 or H is small, where the direct difference loses digits.
    return finite_result((e - 1.0) * sinh_h + small_part)


hyperbolic_kepler_mean_anomaly = FormulaSpec(
    id="orbital.hyperbolic_kepler_mean_anomaly",
    name="Hyperbolic Kepler Equation (Mean Anomaly from Hyperbolic Anomaly)",
    equation="M_h = e * sinh(H) - H",
    description=(
        "Explicit side of Kepler's equation for a hyperbolic orbit: the hyperbolic mean anomaly, "
        "which grows linearly in time, for a given hyperbolic eccentric anomaly."
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
            name="H",
            symbol="H",
            description="Hyperbolic eccentric anomaly",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="M_h",
        symbol="M_h",
        description="Hyperbolic mean anomaly, sqrt(mu / |a|^3) (t - T)",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The preprint writes Kepler's equation in Gauss form with q the periapsis distance; for
        # e > 1 its third line is sqrt(mu) (t - T) = q^(3/2) (e - 1)^(-3/2) (e sinh H - H). With
        # |a| = q / (e - 1) this is sqrt(mu / |a|^3) (t - T) = e sinh H - H, which defines M_h.
        nasa_technical_report(
            "A Numerical Solution of Kepler's Problem in Universal Variables",
            ("R. C. Blanchard", "P. E. Zadunaisky"),
            "X-643-67-627",
            1967,
            "https://ntrs.nasa.gov/citations/19680004301",
            "eq. (1.1), third line, p. 1",
            organization="NASA Goddard Space Flight Center",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"e": 2.0, "H": 1.0},
            expected=1.350402387287603,
            rel_tol=1e-12,
            note="Independent 50-digit mpmath evaluation of 2 sinh(1) - 1.",
        ),
        VerificationCase(
            inputs={"e": 2.0, "H": 0.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Periapsis: both terms vanish, so M_h = 0 exactly.",
        ),
        VerificationCase(
            inputs={"e": 1.2, "H": -2.5},
            expected=-4.760245377247744,
            rel_tol=1e-12,
            note="Inbound leg (H < 0), where the function is odd in H; 50-digit mpmath value.",
        ),
    ),
    assumptions=(
        "Hyperbolic two-body orbit, e > 1; values e <= 1 raise ValueError.",
        "Time is measured from periapsis passage, so M_h = 0 at H = 0; M_h is negative before "
        "periapsis.",
        "|H| beyond roughly 710 overflows sinh and raises OverflowError.",
        "Only this explicit direction is provided; finding H from M_h needs an iteration.",
    ),
    tags=("hyperbolic orbit", "Kepler's equation", "hyperbolic anomaly", "mean anomaly"),
)
