"""Bi-Elliptic Transfer Total Delta-V: sum of the three tangential burns."""

import math

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.catalog.orbital._support import dunning_sp325
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(mu: float, r1: float, rb: float, r2: float) -> float:
    positive("mu", mu)
    positive("r1", r1)
    positive("rb", rb)
    positive("r2", r2)
    if rb < max(r1, r2):
        raise ValueError(f"rb must be at least max(r1, r2) = {max(r1, r2)!r}, got {rb!r}.")
    # Vis-viva at the tangent points, written for an ellipse with periapsis radius r_p and
    # apoapsis radius r_a so that no near-equal terms are subtracted:
    # v_p = sqrt(2 mu r_a / (r_p (r_p + r_a))) and v_a = sqrt(2 mu r_p / (r_a (r_p + r_a))).
    # This equals sqrt(2 mu / r - mu / a) with a = (r_p + r_a) / 2 at r = r_p or r = r_a.
    v_peri_1 = math.sqrt(2.0 * mu * rb / (r1 * (r1 + rb)))
    v_apo_1 = math.sqrt(2.0 * mu * r1 / (rb * (r1 + rb)))
    v_peri_2 = math.sqrt(2.0 * mu * rb / (r2 * (r2 + rb)))
    v_apo_2 = math.sqrt(2.0 * mu * r2 / (rb * (r2 + rb)))
    first = abs(v_peri_1 - math.sqrt(mu / r1))
    second = abs(v_apo_2 - v_apo_1)
    third = abs(math.sqrt(mu / r2) - v_peri_2)
    return finite_result(first + second + third)


bielliptic_total_delta_v = FormulaSpec(
    id="orbital.bielliptic_total_delta_v",
    name="Bi-Elliptic Transfer Total Delta-V",
    equation=(
        "dv = abs(sqrt(2*mu/r1 - mu/a1) - sqrt(mu/r1)) "
        "+ abs(sqrt(2*mu/rb - mu/a2) - sqrt(2*mu/rb - mu/a1)) "
        "+ abs(sqrt(mu/r2) - sqrt(2*mu/r2 - mu/a2)), a1 = (r1 + rb)/2, a2 = (rb + r2)/2"
    ),
    description=(
        "Total impulsive speed change of a three-burn transfer between two coplanar circular "
        "orbits through an intermediate apoapsis radius rb."
    ),
    inputs=(
        VariableSpec(
            name="mu",
            symbol=r"\mu",
            description="Standard gravitational parameter G M of the central body",
            dimension="L^3 T^-2",
            si_unit="m^3/s^2",
        ),
        VariableSpec(
            name="r1",
            symbol="r_1",
            description="Radius of the initial circular orbit",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="rb",
            symbol="r_b",
            description="Intermediate apoapsis radius shared by both transfer ellipses",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="r2",
            symbol="r_2",
            description="Radius of the final circular orbit",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="dv",
        symbol=r"\Delta v",
        description="Total delta-v, the sum of the three burn magnitudes",
        dimension="L T^-1",
        si_unit="m/s",
    ),
    evaluator=_evaluate,
    references=(
        # Derived result: the report describes the bi-elliptic transfer as two Hohmann-type
        # ellipses with three speed changes (perigee burn, burn at the intermediate apoapsis, burn
        # at the periapsis of the second ellipse) and reuses its vis-viva relations, eqs. (4)-(9).
        # It does not print the summed total. Here vis-viva gives the speed on each ellipse at
        # the tangent points, and the total is the sum of the three speed-change magnitudes.
        nasa_technical_report(
            "Conceptual Design of a Communications Relay Satellite for a Lunar Sample Return "
            "Mission",
            ("C. W. Brunner",),
            "NASA/CR-2005-213034",
            2005,
            "https://ntrs.nasa.gov/citations/20050232849",
            "sec. 2.3.1, p. 16 (text after eq. 10) with eqs. (4)-(9)",
            organization="NASA Langley Research Center (The George Washington University, JIAFS)",
        ),
        # Derived result (second source supports the ingredients, not the bi-elliptic total):
        # circular speed (eq. 1-51), the speed equation V^2 / 2 = H + mu / r (eq. 1-29) and
        # a = -mu / (2 H) for the ellipse (eq. 1-47) with a = (r_a + r_p) / 2.
        dunning_sp325("chap. 1, eqs. (1-29), p. 8, (1-47), p. 13 and (1-51), p. 14"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"mu": 398600441800000.0, "r1": 7000000.0, "rb": 420000000.0, "r2": 140000000.0},
            expected=3929.5249342942725,
            rel_tol=1e-12,
            note=(
                "Radius ratio 20 with rb = 3 r2, where the transfer costs less than a Hohmann "
                "transfer; independent 50-digit mpmath evaluation of the vis-viva sums."
            ),
        ),
        VerificationCase(
            inputs={"mu": 398600441800000.0, "r1": 7000000.0, "rb": 140000000.0, "r2": 140000000.0},
            expected=4035.111342228118,
            rel_tol=1e-12,
            note=(
                "Edge rb = r2: the third burn vanishes and the total equals the two Hohmann "
                "burns; independent 50-digit mpmath evaluation."
            ),
        ),
        VerificationCase(
            inputs={"mu": 398600441800000.0, "r1": 6678000.0, "rb": 100000000.0, "r2": 42164000.0},
            expected=4256.0538139104865,
            rel_tol=1e-12,
            note=(
                "Low orbit to geostationary radius through rb = 1e8 m, which costs more than a "
                "Hohmann transfer at this ratio; independent 50-digit mpmath evaluation."
            ),
        ),
    ),
    assumptions=(
        "Derived result: the three tangential burns follow from vis-viva on the two transfer "
        "ellipses; the source describes the burns but does not print their sum, and the total "
        "adds the burn magnitudes.",
        "Coplanar circular start and end orbits, impulsive tangential burns, two-body motion "
        "around a central body of fixed gravitational parameter mu.",
        "rb must be at least max(r1, r2) so that rb is the apoapsis of both ellipses; smaller "
        "values raise ValueError. The third burn is retrograde when rb > r2.",
        "Whether this beats a Hohmann transfer depends on r2/r1 and rb; the formula does not "
        "decide that.",
        "Homogeneous in any consistent units (radii in length units, mu in length^3/time^2).",
    ),
    tags=("bi-elliptic transfer", "delta-v", "orbit transfer", "Hohmann alternative"),
)
