"""True Anomaly of the Hyperbolic Asymptote: nu_inf = acos(-1 / e)."""

import math

from sciengformulary.catalog._domain import finite
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.catalog.orbital._support import dunning_sp325
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(e: float) -> float:
    if finite("e", e) <= 1:
        raise ValueError(f"e must exceed 1 for a hyperbolic orbit, got {e!r}.")
    return math.acos(-1.0 / e)


hyperbolic_asymptote_true_anomaly = FormulaSpec(
    id="orbital.hyperbolic_asymptote_true_anomaly",
    name="True Anomaly of the Hyperbolic Asymptote",
    equation="nu_inf = acos(-1 / e)",
    description=(
        "Largest true anomaly reached on a hyperbolic orbit, the direction in which the "
        "distance from the focus grows without bound."
    ),
    inputs=(
        VariableSpec(
            name="e",
            symbol="e",
            description="Eccentricity of the hyperbolic orbit",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="nu_inf",
        symbol=r"\nu_\infty",
        description="True anomaly of the outbound asymptote, between pi/2 and pi",
        dimension="1",
        si_unit="rad",
    ),
    evaluator=_evaluate,
    references=(
        # Derived result: the report gives the conic relation cos(nu) = (p - r) / (e r) in
        # eqs. (21)-(22). Letting r grow without bound turns the right-hand side into -1/e,
        # so cos(nu_inf) = -1/e, and the principal arccosine lies in (pi/2, pi) for e > 1.
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
        # Derived result (second source supports the starting point only): the report states that
        # the conic equation r = p / (1 + e cos(theta - theta_0)) applies to the hyperbola with
        # zero denominators possible; the asymptotes are where 1 + e cos(nu) = 0, giving
        # cos(nu_inf) = -1/e.
        dunning_sp325(
            "chap. 1, eq. (1-38), p. 10, and 'Hyperbolic trajectories', eq. (1-35), p. 16"
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"e": 2.0},
            expected=2.0943951023931957,
            rel_tol=1e-12,
            note="e = 2 gives cos(nu_inf) = -1/2, i.e. 120 degrees; 50-digit mpmath value.",
        ),
        VerificationCase(
            inputs={"e": 1.0001},
            expected=3.1274511071837097,
            rel_tol=1e-12,
            note="e just above 1: the asymptote is almost 180 degrees; 50-digit mpmath value.",
        ),
        VerificationCase(
            inputs={"e": 100.0},
            expected=1.5807964934690637,
            rel_tol=1e-12,
            note="Very large e: just above 90 degrees; 50-digit mpmath value.",
        ),
    ),
    assumptions=(
        "Derived result: the limit r -> infinity of the stated conic relation "
        "cos(nu) = (p - r) / (e r) gives cos(nu_inf) = -1/e.",
        "Hyperbolic orbit, e > 1; values e <= 1 raise ValueError.",
        "The outbound asymptote is at +nu_inf and the inbound one at -nu_inf (principal "
        "branch, result in radians in (pi/2, pi)); the physical true-anomaly range is "
        "(-nu_inf, nu_inf).",
    ),
    tags=("hyperbolic orbit", "asymptote", "true anomaly", "flyby"),
)
