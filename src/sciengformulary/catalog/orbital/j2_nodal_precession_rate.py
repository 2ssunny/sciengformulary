"""J2 Secular Nodal Precession Rate: dOmega/dt = -(3/2) n J2 (R_e / p)^2 cos(i)."""

import math

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.catalog.orbital._support import borsody_tug_nodal_regression
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(  # noqa: N803 - symbols as in the source
    mu: float, a: float, e: float, i: float, R_e: float, J2: float
) -> float:
    positive("mu", mu)
    positive("a", a)
    if not 0 <= finite("e", e) < 1:
        raise ValueError(f"e must satisfy 0 <= e < 1, got {e!r}.")
    if not 0 <= finite("i", i) <= math.pi:
        raise ValueError(f"i must lie in [0, pi] radians, got {i!r}.")
    positive("R_e", R_e)
    positive("J2", J2)
    # sqrt(mu / a) / a equals sqrt(mu / a^3) but never forms a^3, which would underflow or
    # overflow to 0.0 or inf for extreme lengths.
    mean_motion = math.sqrt(mu / a) / a
    # (1 - e)(1 + e) equals 1 - e^2 without losing precision for small e or e close to 1.
    semi_latus_rectum = a * (1.0 - e) * (1.0 + e)
    if semi_latus_rectum == 0.0:
        raise OverflowError("the semi-latus rectum a * (1 - e^2) underflows to zero.")
    return finite_result(-1.5 * mean_motion * J2 * (R_e / semi_latus_rectum) ** 2 * math.cos(i))


j2_nodal_precession_rate = FormulaSpec(
    id="orbital.j2_nodal_precession_rate",
    name="J2 Secular Nodal Precession Rate",
    equation=(
        "dOmega_dt = -(3 / 2) * n * J2 * (R_e / p)^2 * cos(i), n = sqrt(mu / a^3), "
        "p = a * (1 - e^2)"
    ),
    description=(
        "First-order secular drift rate of the longitude of the ascending node caused by the "
        "oblateness of the central body; negative (westward) for prograde orbits and positive "
        "for retrograde ones."
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
            name="a",
            symbol="a",
            description="Semi-major axis",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="e",
            symbol="e",
            description="Eccentricity of the elliptic orbit",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="i",
            symbol="i",
            description="Inclination",
            dimension="1",
            si_unit="rad",
        ),
        VariableSpec(
            name="R_e",
            symbol="R_e",
            description="Equatorial reference radius of the J2 model",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="J2",
            symbol="J_2",
            description="Second zonal harmonic coefficient (unnormalised, positive when oblate)",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="dOmega_dt",
        symbol=r"\dot{\Omega}",
        description="Secular rate of the right ascension of the ascending node",
        dimension="T^-1",
        si_unit="rad/s",
    ),
    evaluator=_evaluate,
    references=(
        # Stated, with the symbols renamed. Eq. (1) of the memorandum is the total node change
        # over a trip time T_D: dOmega = -(J sqrt(G) / R_E^(3/2)) T_D (R_E / p)^(7/2)
        # (1 - e^2)^(3/2) cos i, with G the gravitational parameter of the Earth, p the
        # semi-latus rectum and J its "oblateness parameter". Dividing by T_D gives the rate
        # -J sqrt(mu) R_E^2 p^(-7/2) (1 - e^2)^(3/2) cos i; with p = a (1 - e^2) this is
        # -J n (R_E / p)^2 cos i for n = sqrt(mu / a^3), i.e. the shipped form with J = (3/2) J2.
        # The list of symbols (p. 11) gives J only as "oblateness parameter (1.624e-3)", and
        # 1.5 * 1.08263e-3 = 1.6239e-3 rounds to that value; the paper does not write J = (3/2) J2
        # in words, so the identification rests on this numerical match (and on the lumped
        # constant of TN D-1045 below being 1.5 J2 as well). The eccentricity factor (1 - e^2)^-2
        # at fixed a is taken from this memorandum.
        borsody_tug_nodal_regression(
            "analysis item (4), eq. (1), p. 2; oblateness parameter J (value 1.624e-3) and "
            "semilatus rectum p in the list of symbols, p. 11"
        ),
        # Corroboration of the relation for a circular orbit (e = 0): the note gives a nodal
        # regression rate proportional to cos i, to (a / r)^2 and to the mean motion, with the
        # coefficient written through a lumped quadrupole constant (6 mu = 1.637e-3 for the
        # note's constant). The note does not print how that constant relates to J2, so the
        # worked example is used only as a rough consistency check with J2 = 1.637e-3 / 1.5.
        nasa_technical_report(
            "Earth Oblateness and Relative Sun Motion Considerations in the Determination of an "
            "Ideal Orbit for the Nimbus Meteorological Satellite",
            ("W. R. Bandeen",),
            "NASA TN D-1045",
            1961,
            "https://ntrs.nasa.gov/citations/19980231088",
            "p. 2, eq. (1) and the 'ideal orbit' example, pp. 2-4",
            organization="NASA Goddard Space Flight Center",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={
                "mu": 398600441800000.0,
                "a": 7078000.0,
                "e": 0.0,
                "i": 1.7139133254584316,
                "R_e": 6378137.0,
                "J2": 0.00108263,
            },
            expected=1.9941075262375987e-07,
            rel_tol=1e-12,
            note=(
                "Near sun-synchronous low orbit (about +0.9856 degrees per day, eastward because "
                "cos i < 0); independent 50-digit mpmath evaluation."
            ),
        ),
        VerificationCase(
            inputs={
                "mu": 398600441800000.0,
                "a": 26554000.0,
                "e": 0.7,
                "i": 1.106538745764405,
                "R_e": 6378137.0,
                "J2": 0.00108263,
            },
            expected=-2.3532990527964748e-08,
            rel_tol=1e-12,
            note="Molniya-like eccentric prograde orbit; 50-digit mpmath evaluation.",
        ),
        VerificationCase(
            inputs={
                "mu": 398600441800000.0,
                "a": 7000000.0,
                "e": 0.001,
                "i": 1.5707963267948966,
                "R_e": 6378137.0,
                "J2": 0.00108263,
            },
            expected=-8.899517796278093e-23,
            rel_tol=1e-12,
            abs_tol=1e-20,
            note=(
                "Polar orbit: cos(i) is zero except for the rounding of pi/2, so the rate "
                "vanishes to within the absolute tolerance; 50-digit mpmath evaluation."
            ),
        ),
        VerificationCase(
            inputs={
                "mu": 398600441800000.0,
                "a": 7000000.0,
                "e": 0.0,
                "i": 0.0,
                "R_e": 6378137.0,
                "J2": 0.00108263,
            },
            expected=-1.4533986457887414e-06,
            rel_tol=1e-12,
            note="Equatorial prograde circular orbit, -3/2 n J2 (R_e/a)^2; 50-digit mpmath value.",
        ),
        VerificationCase(
            inputs={
                "mu": 398632900000000.0,
                "a": 7483200.0,
                "e": 0.0,
                "i": 1.743409389817136,
                "R_e": 6378388.0,
                "J2": 0.0010913333333333333,
            },
            expected=1.9909681837564945e-07,
            rel_tol=0.002,
            note=(
                "Inputs follow the 600 n.mi. ideal-orbit example of NASA TN D-1045 (i = 99.89 "
                "deg, which regresses about +0.9856 deg/day); the paper's inputs are rounded and "
                "J2 = 1.637e-3 / 1.5 is inferred. The expected value is a 50-digit mpmath "
                "evaluation (0.98629 deg/day), within 7e-4 of the printed rate, so the "
                "tolerance is loosened to 2e-3."
            ),
        ),
    ),
    assumptions=(
        "First-order secular J2 theory, orbit-averaged: no J2-squared, J4 or other terms, and "
        "no short-period oscillation.",
        "The cited memorandum prints the rate with a lumped oblateness parameter J whose "
        "listed value (1.624e-3, p. 11) equals 1.5 * 1.08263e-3; J = (3/2) J2 rests on that "
        "numerical match, since the paper does not name J2.",
        "n is the Keplerian mean motion sqrt(mu / a^3); the J2 correction to n is second order "
        "and is not included.",
        "Elliptic orbit with 0 <= e < 1; inclination 0 <= i <= pi in radians; J2 is unnormalised "
        "and must be positive (an oblate body).",
        "mu, a and R_e must be in one consistent unit system; the rate is per unit of that "
        "system's time in radians.",
    ),
    tags=("J2 perturbation", "nodal regression", "sun-synchronous", "precession", "oblateness"),
)
