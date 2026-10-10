"""Student t Probability Density (Standard):
f = Gamma((nu + 1) / 2) / (sqrt(nu * pi) * Gamma(nu / 2)) * (1 + x^2 / nu)^(-(nu + 1) / 2).
"""

import math

from sciengformulary.catalog._sources import nist_statistics_handbook
from sciengformulary.catalog._domain import finite, integer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

# Below this the gamma functions are formed directly (no overflow: Gamma(25) ~ 6e23);
# from here on the asymptotic series below is accurate to well under one rounding.
_SERIES_FROM_NU = 50
_HALF_LOG_2PI = 0.5 * math.log(2.0 * math.pi)


def _log_normaliser(nu: int) -> float:
    """ln(Gamma((nu + 1)/2) / (sqrt(nu pi) Gamma(nu/2))) for nu >= _SERIES_FROM_NU.

    Subtracting two log-gamma values of size ~ nu ln(nu) / 2 would lose about log10(nu)
    digits, so the difference is taken from the Stirling series instead: with n = 1/nu,
    ln(normaliser) = -ln(2 pi)/2 - n/4 + n^3/24 - n^5/20 + 17 n^7/112 - 31 n^9/36 + O(n^11).
    """
    n = 1.0 / nu
    n2 = n * n
    series = n * (-0.25 + n2 * (1.0 / 24.0 + n2 * (-0.05 + n2 * (17.0 / 112.0 - n2 * 31.0 / 36.0))))
    return -_HALF_LOG_2PI + series


def _evaluate(x: float, nu: float) -> float:
    finite("x", x)
    dof = integer("nu", nu, minimum=1)
    # (1 + x^2/nu)^(-(nu + 1)/2) through log1p, so a small x^2/nu keeps its digits; if x^2
    # overflows, the kernel is exp(-inf) = 0.0, matching a true value below the float range.
    log_kernel = -0.5 * (dof + 1) * math.log1p(x * x / dof)
    if dof < _SERIES_FROM_NU:
        normaliser = math.gamma(0.5 * (dof + 1)) / (
            math.gamma(0.5 * dof) * math.sqrt(dof * math.pi)
        )
        return normaliser * math.exp(log_kernel)
    return math.exp(_log_normaliser(dof) + log_kernel)


student_t_probability_density = FormulaSpec(
    id="mathematics.student_t_probability_density",
    name="Student t Probability Density (Standard)",
    equation=(
        "f = Gamma((nu + 1) / 2) / (sqrt(nu * pi) * Gamma(nu / 2)) * (1 + x^2 / nu)^(-(nu + 1) / 2)"
    ),
    description=(
        "Probability density at x of the standard Student t distribution with nu degrees of "
        "freedom (location 0, scale 1). nu = 1 gives the standard Cauchy density; as nu grows "
        "the density approaches the standard normal."
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
            name="nu",
            symbol=r"\nu",
            description="Degrees of freedom (whole number, at least 1)",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="f",
        symbol="f(x)",
        description="Probability density at x",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Derived result. The handbook states f = (1 + x^2/nu)^(-(nu + 1)/2) / (B(0.5, 0.5 nu)
        # sqrt(nu)) with nu a positive integer. With B(a, b) = Gamma(a) Gamma(b) / Gamma(a + b)
        # (the identity cited for mathematics.beta_function) and Gamma(1/2) = sqrt(pi),
        # 1 / (sqrt(nu) B(1/2, nu/2)) = Gamma((nu + 1)/2) / (sqrt(nu pi) Gamma(nu/2)).
        nist_statistics_handbook(
            "eda/section3/eda3664.htm",
            "sec. 1.3.6.6.4, t Distribution: probability density function",
            accessed="2026-10-09",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"x": 0.0, "nu": 1},
            expected=0.3183098861837907,
            rel_tol=1e-12,
            note="nu = 1 is the standard Cauchy law, peak 1/pi; 50-digit mpmath, scipy 1.7e-16.",
        ),
        VerificationCase(
            inputs={"x": 0.0, "nu": 2},
            expected=0.3535533905932738,
            rel_tol=1e-12,
            note="Peak for nu = 2: 1/(2 sqrt(2)) by hand; 50-digit mpmath, scipy identical.",
        ),
        VerificationCase(
            inputs={"x": 1.3, "nu": 5},
            expected=0.15847673572898244,
            rel_tol=1e-12,
            note="50-digit mpmath; the gamma and the handbook's beta forms agree; scipy equal.",
        ),
        VerificationCase(
            inputs={"x": -2.5, "nu": 30},
            expected=0.021057019220621632,
            rel_tol=1e-12,
            note="Larger nu; 50-digit mpmath (scipy differs by its own 2e-15).",
        ),
        VerificationCase(
            inputs={"x": 1.0, "nu": 1},
            expected=0.15915494309189535,
            rel_tol=1e-12,
            note="1/(2 pi), the standard Cauchy density at x = 1; 50-digit mpmath.",
        ),
    ),
    assumptions=(
        "Standard form (location 0, scale 1). For location m and scale s evaluate at "
        "(x - m) / s and divide the result by s.",
        "nu is restricted to whole numbers >= 1, as in the cited source; non-integral or "
        "smaller nu raises ValueError, as does a non-finite x. Integral floats such as 5.0 "
        "are accepted.",
        "Derived result: the gamma-function normaliser replaces the source's beta function "
        "B(1/2, nu/2) through B(a, b) = Gamma(a) Gamma(b) / Gamma(a + b) and Gamma(1/2) = "
        "sqrt(pi); checked symbolically and numerically (both forms agree to 40 digits).",
        "For nu < 50 the gamma functions are formed directly; for nu >= 50 the log of the "
        "normaliser comes from its Stirling series, since subtracting two large log-gamma values "
        "would lose digits. Relative error measured against 50-digit mpmath of the source's beta "
        "form for 1 <= nu <= 1e8 on random points: below 3e-14 for |x| <= 10 (more than 5000 "
        "points, largest observed 1.6e-14) and below 2.5e-13 for |x| <= 1e100 wherever the density "
        "is within the float range (825 points, largest observed 1.4e-13); outside that range "
        "accuracy is not characterised.",
        "The support is the whole real line; far in the tails the value underflows to 0.0.",
    ),
    tags=(
        "Student t distribution",
        "t distribution",
        "probability density",
        "pdf",
        "degrees of freedom",
        "statistics",
    ),
)
