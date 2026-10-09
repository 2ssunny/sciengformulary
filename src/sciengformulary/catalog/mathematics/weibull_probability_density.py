"""Weibull Probability Density (Two-Parameter, Shape-Scale):
f = (k / lam) * (x / lam)^(k - 1) * exp(-(x / lam)^k) for x >= 0; f = 0 for x < 0.
"""

import math
import sys

from sciengformulary.catalog._sources import nist_statistics_handbook
from sciengformulary.catalog.mathematics._domain import finite, finite_result, positive
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

# exp(k ln u) overflows a float above about 709.78; past this point exp(-(x/lam)^k) is far
# below the smallest float, so the density is returned as 0.0.
_EXP_LIMIT = 709.0


def _evaluate(x: float, k: float, lam: float) -> float:
    finite("x", x)
    positive("k", k)
    positive("lam", lam)
    if x < 0:
        return 0.0
    if x == 0:
        if k < 1:
            raise ValueError(f"The Weibull density is unbounded at x = 0 when k < 1, got k={k!r}.")
        return 1.0 / lam if k == 1 else 0.0
    u = x / lam
    # ln(x/lam) from the quotient when it is a normal float; if the quotient over- or
    # underflows, from the difference of logs instead.
    if sys.float_info.min <= u <= sys.float_info.max:
        log_u = math.log(u)
    else:
        log_u = math.log(x) - math.log(lam)
    k_log_u = k * log_u
    if k_log_u > _EXP_LIMIT:
        return 0.0
    # Log space keeps k/lam and (x/lam)^(k - 1) from overflowing on their own.
    log_f = math.log(k) - math.log(lam) + (k - 1.0) * log_u - math.exp(k_log_u)
    return finite_result(math.exp(log_f))


weibull_probability_density = FormulaSpec(
    id="mathematics.weibull_probability_density",
    name="Weibull Probability Density (Two-Parameter, Shape-Scale)",
    equation="f = (k / lam) * (x / lam)^(k - 1) * exp(-(x / lam)^k) for x >= 0; f = 0 for x < 0",
    description=(
        "Probability density at x of the two-parameter Weibull distribution (location 0) with "
        "shape k and scale lam, the characteristic life at which the CDF reaches 1 - 1/e. "
        "k = 1 gives the exponential density with rate 1/lam."
    ),
    inputs=(
        VariableSpec(
            name="x",
            symbol="x",
            description="Value (e.g. time to failure) at which the density is evaluated",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="k",
            symbol="k",
            description="Shape parameter (Weibull slope; NIST gamma), positive",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="lam",
            symbol=r"\lambda",
            description=(
                "Scale parameter (characteristic life; NIST alpha), positive; a scale, not a rate"
            ),
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="f",
        symbol="f(x)",
        description="Probability density at x (per unit of x)",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The handbook writes shape gamma, location mu and scale alpha, and names the mu = 0
        # case the 2-parameter Weibull; gamma = k, alpha = lam.
        nist_statistics_handbook(
            "eda/section3/eda3668.htm",
            "sec. 1.3.6.6.8, Weibull Distribution: probability density function",
            accessed="2026-10-09",
        ),
        # The reliability chapter states the two-parameter density in t with shape gamma and
        # characteristic life alpha, and works the example reproduced in case 2 below.
        nist_statistics_handbook(
            "apr/section1/apr162.htm",
            "sec. 8.1.6.2, Weibull: Weibull formulas and worked example",
            accessed="2026-10-09",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"x": 2.0, "k": 2.0, "lam": 2.0},
            expected=0.36787944117144233,
            rel_tol=1e-12,
            note="u = 1 gives (k/lam) exp(-1) = exp(-1) by hand; scipy weibull_min identical.",
        ),
        VerificationCase(
            inputs={"x": 1000.0, "k": 1.5, "lam": 5000.0},
            expected=0.00012268508642966375,
            rel_tol=1e-12,
            note=(
                "NIST sec. 8.1.6.2 worked example (printed as 0.000123); 50-digit mpmath "
                "value, scipy within 2.2e-16."
            ),
        ),
        VerificationCase(
            inputs={"x": 0.4, "k": 0.5, "lam": 1.5},
            expected=0.38514624943214093,
            rel_tol=1e-12,
            note="Shape below 1 (decreasing density); 50-digit mpmath, scipy within 1.4e-16.",
        ),
        VerificationCase(
            inputs={"x": 3.1, "k": 3.6, "lam": 2.2},
            expected=0.12836539916480855,
            rel_tol=1e-12,
            note="Shape above 1; 50-digit mpmath, scipy within 4.3e-16.",
        ),
        VerificationCase(
            inputs={"x": 0.0, "k": 1.0, "lam": 4.0},
            expected=0.25,
            rel_tol=1e-12,
            note="Edge x = 0 with k = 1 (exponential case): 1/lam.",
        ),
        VerificationCase(
            inputs={"x": 0.0, "k": 2.0, "lam": 1.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Edge x = 0 with k > 1, where (x/lam)^(k - 1) vanishes.",
        ),
        VerificationCase(
            inputs={"x": -1.0, "k": 2.0, "lam": 1.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="x < 0 lies outside the support, where the density is zero.",
        ),
    ),
    assumptions=(
        "Two-parameter form: location (NIST mu) fixed at 0, shape k (NIST gamma), scale lam "
        "(NIST alpha). For a location mu evaluate at x - mu.",
        "lam is a scale (characteristic life), unlike lam in the gamma and exponential "
        "densities, where it is a rate.",
        "k and lam must be finite and > 0, and x finite; otherwise ValueError is raised.",
        "Returns 0.0 for x < 0, where the density is genuinely zero.",
        "At x = 0 the density is 1/lam for k = 1 and 0 for k > 1; for k < 1 it is unbounded, "
        "so x = 0 raises ValueError.",
        "Evaluated in log space. Relative error measured against 50-digit mpmath for "
        "0.1 <= k <= 20 and 1e-3 <= lam <= 1e4: below 3e-14 for 1e-6 <= (x/lam)^k <= 30 and "
        "below 1.2e-12 for (x/lam)^k <= 700 (deep in the tail the rounding of x/lam is "
        "amplified by k (x/lam)^k); outside that range accuracy is not characterised. A "
        "finite input whose density exceeds the float range raises OverflowError.",
        "x and lam share one unit; the density carries 1/that unit (listed as dimensionless here).",
    ),
    tags=(
        "Weibull distribution",
        "probability density",
        "pdf",
        "reliability",
        "shape",
        "scale",
        "characteristic life",
        "statistics",
    ),
)
