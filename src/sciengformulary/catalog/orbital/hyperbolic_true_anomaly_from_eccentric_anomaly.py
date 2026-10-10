"""True Anomaly from Hyperbolic Eccentric Anomaly.

nu = 2 * atan(sqrt((e + 1) / (e - 1)) * tanh(H / 2)).
"""

import math

from sciengformulary.catalog._domain import finite, finite_result
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(e: float, H: float) -> float:  # noqa: N803 - symbols as in the source
    if finite("e", e) <= 1:
        raise ValueError(f"e must exceed 1 for a hyperbolic orbit, got {e!r}.")
    finite("H", H)
    return finite_result(2.0 * math.atan(math.sqrt((e + 1.0) / (e - 1.0)) * math.tanh(0.5 * H)))


hyperbolic_true_anomaly_from_eccentric_anomaly = FormulaSpec(
    id="orbital.hyperbolic_true_anomaly_from_eccentric_anomaly",
    name="True Anomaly from Hyperbolic Eccentric Anomaly",
    equation="nu = 2 * atan(sqrt((e + 1) / (e - 1)) * tanh(H / 2))",
    description=(
        "True anomaly of a hyperbolic orbit from the hyperbolic eccentric anomaly; it tends to "
        "the asymptote value as H grows."
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
        name="nu",
        symbol=r"\nu",
        description="True anomaly, within (-nu_inf, nu_inf)",
        dimension="1",
        si_unit="rad",
    ),
    evaluator=_evaluate,
    references=(
        # Derived result: the preprint defines H only through the hyperbolic Kepler equation,
        # eq. (1.1). Inverting the derived relation H = asinh(sqrt(e^2 - 1) sin(nu) /
        # (1 + e cos(nu))) gives tan(nu / 2) = sqrt((e + 1) / (e - 1)) tanh(H / 2); this is
        # consistent with cosh H = (e + cos nu) / (1 + e cos nu) and r = |a| (e cosh H - 1).
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
            inputs={"e": 2.0, "H": 1.0},
            expected=1.3499822664876797,
            rel_tol=1e-12,
            note="e = 2 and H = 1 (about 1.35 rad); independent 50-digit mpmath evaluation.",
        ),
        VerificationCase(
            inputs={"e": 2.0, "H": 0.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Periapsis: tanh(0) = 0 so nu = 0 exactly.",
        ),
        VerificationCase(
            inputs={"e": 2.0, "H": 12.0},
            expected=2.094384460272533,
            rel_tol=1e-12,
            note="Large H approaches the asymptote 2 pi / 3 from below; 50-digit mpmath value.",
        ),
    ),
    assumptions=(
        "Derived result: this is the inverse of the derived relation H(nu), obtained from the "
        "stated hyperbolic Kepler equation together with the conic and areal laws.",
        "Hyperbolic orbit, e > 1; values e <= 1 raise ValueError.",
        "Branch convention (our choice, not the source's): the result lies in the open interval "
        "(-nu_inf, nu_inf), nu_inf = acos(-1/e), with the sign of H and nu = 0 at periapsis; "
        "no angle wrapping is applied.",
        "Angles in radians.",
    ),
    tags=("hyperbolic orbit", "true anomaly", "hyperbolic anomaly", "anomaly conversion"),
)
