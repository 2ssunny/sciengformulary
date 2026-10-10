"""Cauchy Probability Density: f = s / (pi * ((x - x0)^2 + s^2))."""

import math

from sciengformulary.catalog._sources import MATH_ACCESSED, mathlib, nist_statistics_handbook
from sciengformulary.catalog.mathematics._domain import finite, positive
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(x: float, x0: float, s: float) -> float:
    finite("x", x)
    finite("x0", x0)
    positive("s", s)
    # Scaled form: squaring (x - x0) / s cannot overflow for moderate inputs, and if it does
    # the true density is below the float range anyway, so 0.0 is returned.
    u = (x - x0) / s
    return 1.0 / (math.pi * s * (1.0 + u * u))


cauchy_probability_density = FormulaSpec(
    id="mathematics.cauchy_probability_density",
    name="Cauchy Probability Density",
    equation="f = s / (pi * ((x - x0)^2 + s^2))",
    description=(
        "Probability density at x of a Cauchy (Lorentzian) distribution centred at x0 with "
        "scale s, the half width at half maximum."
    ),
    inputs=(
        VariableSpec(
            name="x",
            symbol="x",
            description="Value at which the density is evaluated",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="x0",
            symbol="x_0",
            description="Location parameter (median and mode)",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="s",
            symbol="s",
            description="Scale parameter (half width at half maximum), positive",
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
        # Mathlib allows scale 0 (a degenerate point mass); only s > 0 is a density here.
        mathlib(
            "Mathlib/Probability/Distributions/Cauchy.lean#L42",
            "def ProbabilityTheory.cauchyPDFReal",
        ),
        # The handbook writes 1 / (s pi (1 + ((x - t)/s)^2)) with location t; for s > 0 and
        # t = x0 this equals s / (pi ((x - x0)^2 + s^2)).
        nist_statistics_handbook(
            "eda/section3/eda3663.htm",
            "sec. 1.3.6.6.3, Cauchy Distribution: probability density function",
            accessed=MATH_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"x": 0.0, "x0": 0.0, "s": 1.0},
            expected=0.3183098861837907,
            rel_tol=1e-12,
            note="Peak of the standard Cauchy density, 1/pi; 50-digit mpmath, scipy identical.",
        ),
        VerificationCase(
            inputs={"x": 3.0, "x0": 2.0, "s": 0.5},
            expected=0.12732395447351627,
            rel_tol=1e-12,
            note="0.4/pi by hand; 50-digit mpmath, scipy identical.",
        ),
        VerificationCase(
            inputs={"x": -4.0, "x0": 1.0, "s": 2.5},
            expected=0.025464790894703253,
            rel_tol=1e-12,
            note="2.5 / (31.25 pi) = 0.08/pi by hand; 50-digit mpmath, scipy identical.",
        ),
        VerificationCase(
            inputs={"x": 1000000.0, "x0": 0.0, "s": 1.0},
            expected=3.1830988618347235e-13,
            rel_tol=1e-12,
            note="Far tail; 50-digit mpmath, scipy within 1.6e-16.",
        ),
    ),
    assumptions=(
        "s must be finite and > 0, and x and x0 finite; otherwise ValueError is raised.",
        "The support is the whole real line. The distribution has no mean or variance; x0 is "
        "its median and mode.",
        "Very far in the tails the value underflows to 0.0.",
        "x, x0 and s share one unit; the density carries 1/that unit (listed as dimensionless "
        "here).",
    ),
    tags=(
        "Cauchy distribution",
        "Lorentzian",
        "probability density",
        "pdf",
        "heavy tail",
        "statistics",
    ),
)
