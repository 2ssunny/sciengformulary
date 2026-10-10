"""Laplace Sphere of Influence Radius: r_SOI = a * (m / M)^(2/5)."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.catalog.orbital._support import burrows_sphere_of_influence, positive_result
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(a: float, m: float, M: float) -> float:  # noqa: N803 - symbols as in the source
    positive("a", a)
    positive("m", m)
    positive("M", M)
    if m > M:
        raise ValueError(f"m must not exceed M, got m={m!r} and M={M!r}.")
    # Raising m and M to the 2/5 power separately keeps the ratio representable (at least about
    # 1e-252 for any positive floats), where m / M itself can underflow to zero first.
    ratio = (m**0.4) / (M**0.4)
    return positive_result(finite_result(a * ratio))


laplace_sphere_of_influence_radius = FormulaSpec(
    id="orbital.laplace_sphere_of_influence_radius",
    name="Laplace Sphere of Influence Radius",
    equation="r_SOI = a * (m / M)^(2 / 5)",
    description=(
        "Radius of the region around a secondary body inside which, in the patched-conic "
        "approximation, its gravity is treated as dominant over the primary's."
    ),
    inputs=(
        VariableSpec(
            name="a",
            symbol="a",
            description="Distance between the secondary body and the primary body",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="m",
            symbol="m",
            description="Mass of the secondary body (or its gravitational parameter)",
            dimension="M",
            si_unit="kg",
        ),
        VariableSpec(
            name="M",
            symbol="M",
            description="Mass of the primary body, in the same kind and unit as m",
            dimension="M",
            si_unit="kg",
        ),
    ),
    output=VariableSpec(
        name="r_SOI",
        symbol="r_{SOI}",
        description="Sphere-of-influence radius, in the unit of a",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # The report writes R_s = D (mu_Moon / mu_Earth)^(2/5) for the Moon's sphere of influence
        # with D the Earth-Moon distance; a is the secondary-primary distance and the mass ratio
        # equals the ratio of the gravitational parameters (mu = G m). A JPL Descanso chapter that
        # states the same relation is not cited because its authors and year are not verified.
        nasa_technical_report(
            "Conceptual Design of a Communications Relay Satellite for a Lunar Sample Return "
            "Mission",
            ("C. W. Brunner",),
            "NASA/CR-2005-213034",
            2005,
            "https://ntrs.nasa.gov/citations/20050232849",
            "eq. (11), p. 19",
            organization="NASA Langley Research Center (The George Washington University, JIAFS)",
        ),
        # Stated, with the symbols renamed: rho = (m_1 / M)^(2/5) r_1, where rho is the radius of
        # the sphere of influence of the body m_1 (the secondary) with respect to the perturbing
        # mass M (the primary) at distance r_1. The memorandum calls it the frequently seen
        # expression and compares it with its own approximations of the exact definition.
        burrows_sphere_of_influence("eq. (11), p. 6"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"a": 149597870.7, "m": 7.34722101e22, "M": 1.98879724e30},
            expected=159198.30893582272,
            rel_tol=1e-12,
            note=(
                "Moon about the Sun with a = 1 AU expressed in km, so the result is in km; "
                "independent 50-digit mpmath evaluation."
            ),
        ),
        VerificationCase(
            inputs={"a": 149597870700.0, "m": 5.9722e24, "M": 1.98847e30},
            expected=924637562.0510032,
            rel_tol=1e-12,
            note="Earth about the Sun in metres (about 9.25e8 m); 50-digit mpmath evaluation.",
        ),
        VerificationCase(
            inputs={"a": 384400000.0, "m": 1.0, "M": 1.0},
            expected=384400000.0,
            rel_tol=1e-12,
            note=(
                "Numerical edge m = M, outside the m << M regime but allowed by the input "
                "domain: the ratio is 1 and the result equals a."
            ),
        ),
    ),
    assumptions=(
        "Patched-conic approximation with m << M; the radius is a conventional boundary for "
        "switching the dominant attractor, not a sharp physical limit.",
        "m and M must be the same kind of quantity in the same unit (both masses or both "
        "gravitational parameters); only their ratio enters.",
        "a is the distance between secondary and primary; the result has the unit of a.",
        "Inputs must satisfy a > 0 and 0 < m <= M; other values raise ValueError. A result "
        "outside the float range, including one that underflows to zero, raises OverflowError.",
    ),
    tags=("sphere of influence", "patched conic", "Laplace", "interplanetary"),
)
