"""Mean-Motion Sensitivity to Semi-Major Axis: dn/da = -(3/2) n / a."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(n: float, a: float) -> float:
    positive("n", n)
    positive("a", a)
    return finite_result(-1.5 * n / a)


mean_motion_semi_major_axis_sensitivity = FormulaSpec(
    id="orbital.mean_motion_semi_major_axis_sensitivity",
    name="Mean-Motion Sensitivity to Semi-Major Axis",
    equation="dn_da = -(3 / 2) * n / a",
    description=(
        "Rate at which the mean motion changes with the semi-major axis of a Kepler orbit, the "
        "derivative of n = sqrt(mu / a^3) at constant mu."
    ),
    inputs=(
        VariableSpec(
            name="n",
            symbol="n",
            description="Mean motion at that semi-major axis",
            dimension="T^-1",
            si_unit="rad/s",
        ),
        VariableSpec(
            name="a",
            symbol="a",
            description="Semi-major axis",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="dn_da",
        symbol=r"\partial n / \partial a",
        description="Derivative of the mean motion with respect to the semi-major axis",
        dimension="L^-1 T^-1",
        si_unit="rad/s/m",
    ),
    evaluator=_evaluate,
    references=(
        # Derived result: the preprint's Kepler equation (1.1) has the time coefficient
        # q^(3/2) (1 - e)^(-3/2) = a^(3/2), so n = sqrt(mu / a^3) = mu^(1/2) a^(-3/2).
        # Differentiating with respect to a at fixed mu gives
        # -(3/2) mu^(1/2) a^(-5/2) = -(3/2) n / a.
        nasa_technical_report(
            "A Numerical Solution of Kepler's Problem in Universal Variables",
            ("R. C. Blanchard", "P. E. Zadunaisky"),
            "X-643-67-627",
            1967,
            "https://ntrs.nasa.gov/citations/19680004301",
            "eq. (1.1) (time coefficient sqrt(mu / a^3))",
            organization="NASA Goddard Space Flight Center",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"n": 0.001078007612872506, "a": 7000000.0},
            expected=-2.310016313298227e-10,
            rel_tol=1e-12,
            note="-(3/2) n / a at a = 7e6 m; independent 50-digit mpmath evaluation.",
        ),
        VerificationCase(
            inputs={"n": 7.292159861796045e-05, "a": 42164000.0},
            expected=-2.5942130235969234e-12,
            rel_tol=1e-12,
            note="-(3/2) n / a at the geostationary radius; 50-digit mpmath evaluation.",
        ),
    ),
    assumptions=(
        "Derived result: the derivative of n = sqrt(mu / a^3) with respect to a at constant "
        "mu, which is -(3/2) n / a.",
        "Elliptic Kepler orbit with constant mu; n and a must belong to the same orbit, "
        "n = sqrt(mu / a^3). The formula does not check that consistency.",
        "The result is negative: a larger orbit has a lower mean motion. It is a local "
        "linearisation, accurate for small changes in a.",
        "Homogeneous in any consistent units: the result is in 1 / (time * length).",
    ),
    tags=("mean motion", "sensitivity", "orbit drift", "derivative", "semi-major axis"),
)
