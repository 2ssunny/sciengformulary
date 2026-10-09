"""Shared reference builders and a result guard for the NASA-sourced orbital formulas."""

from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import ReferenceSpec


def positive_result(value: float) -> float:
    """Return ``value`` if a strictly positive true result did not underflow to zero.

    Raises:
        OverflowError: If ``value`` is zero or negative although the true result is positive,
            so no misleading ``0.0`` is returned.
    """
    if not value > 0.0:
        raise OverflowError(
            f"the positive result underflows to {value!r}: it is outside the floating-point range."
        )
    return value


def dunning_sp325(locator: str) -> ReferenceSpec:
    """NASA SP-325, ``The Orbital Mechanics of Flight Mechanics`` (R. S. Dunning, 1973).

    NTRS record 19740004369 carries the rights determination ``GOV_PUBLIC_USE_PERMITTED``.
    Pass only the section, equation and page checked in the printed pages.
    """
    return nasa_technical_report(
        "The Orbital Mechanics of Flight Mechanics",
        ("R. S. Dunning",),
        "NASA SP-325",
        1973,
        "https://ntrs.nasa.gov/citations/19740004369",
        locator,
        organization="NASA Langley Research Center",
    )


def burrows_sphere_of_influence(locator: str) -> ReferenceSpec:
    """NASA TM X-53485, ``The Classical "Sphere-of-Influence"`` (R. R. Burrows, 1966).

    NTRS record 19660025930 carries the rights determination ``GOV_PUBLIC_USE_PERMITTED``.
    """
    return nasa_technical_report(
        'The Classical "Sphere-of-Influence"',
        ("R. R. Burrows",),
        "NASA TM X-53485",
        1966,
        "https://ntrs.nasa.gov/citations/19660025930",
        locator,
        organization="NASA George C. Marshall Space Flight Center",
    )


def borsody_tug_nodal_regression(locator: str) -> ReferenceSpec:
    """NASA TM X-73433, Borsody's reusable-Tug paper with nodal-regression corrections (1976).

    NTRS record 19760020249 carries the rights determination ``GOV_PUBLIC_USE_PERMITTED``.
    """
    return nasa_technical_report(
        "Performance of a Recoverable Tug for Planetary Missions Including Use of Perigee "
        "Propulsion and Corrections for Nodal Regression",
        ("J. Borsody",),
        "NASA TM X-73433",
        1976,
        "https://ntrs.nasa.gov/citations/19760020249",
        locator,
        organization="NASA Lewis Research Center",
    )
