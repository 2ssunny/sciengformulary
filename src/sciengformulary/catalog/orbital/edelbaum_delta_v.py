"""Edelbaum Low-Thrust Transfer Delta-V.

dV = sqrt(V0^2 - 2 V0 V1 cos(pi di / 2) + V1^2), V0 = sqrt(mu / a0), V1 = sqrt(mu / a1).
"""

import math

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(mu: float, a0: float, a1: float, di: float) -> float:
    positive("mu", mu)
    positive("a0", a0)
    positive("a1", a1)
    non_negative("di", di)
    if di > math.pi:
        raise ValueError(
            f"di must not exceed pi radians (a plane change cannot be larger), got {di!r}."
        )
    v0 = math.sqrt(mu / a0)
    v1 = math.sqrt(mu / a1)
    # V0^2 - 2 V0 V1 cos(x) + V1^2 = (V0 - V1)^2 + 4 V0 V1 sin^2(x / 2) with x = pi di / 2.
    # The second form is the same quantity (1 - cos x = 2 sin^2(x / 2)) and cannot go negative
    # through rounding. V0 - V1 itself cancels when the radii are close, so it is evaluated as
    # (V0^2 - V1^2) / (V0 + V1) = V0^2 (a1 - a0) / (a1 (V0 + V1)), which is exact in a1 - a0.
    speed_difference = v0 * v0 * ((a1 - a0) / a1) / (v0 + v1)
    half_angle = 0.25 * math.pi * di
    return finite_result(math.sqrt(speed_difference**2 + 4.0 * v0 * v1 * math.sin(half_angle) ** 2))


edelbaum_delta_v = FormulaSpec(
    id="orbital.edelbaum_delta_v",
    name="Edelbaum Low-Thrust Transfer Delta-V",
    equation=(
        "dV = sqrt(V0^2 - 2 * V0 * V1 * cos(pi * di / 2) + V1^2), "
        "V0 = sqrt(mu / a0), V1 = sqrt(mu / a1)"
    ),
    description=(
        "Approximate total velocity increment for a continuous low-thrust transfer between "
        "circular orbits of different radius and inclination, from Edelbaum's analysis."
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
            name="a0",
            symbol="a_0",
            description="Radius of the initial circular orbit",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="a1",
            symbol="a_1",
            description="Radius of the final circular orbit",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="di",
            symbol=r"\Delta i",
            description="Total inclination (plane) change",
            dimension="1",
            si_unit="rad",
        ),
    ),
    output=VariableSpec(
        name="dV",
        symbol=r"\Delta V",
        description="Low-thrust velocity increment",
        dimension="L T^-1",
        si_unit="m/s",
    ),
    evaluator=_evaluate,
    references=(
        # Stated, with the symbols renamed: the report gives
        # Delta V = [V0^2 + V^2 - 2 V V0 cos(pi/2 * theta)]^(1/2) with V0 and V the circular
        # velocities of the original and desired orbits and theta the plane change in radians;
        # here V = V1 and theta = di, with circular speed sqrt(mu / a). The evaluator uses the
        # equal form (V0 - V1)^2 + 4 V0 V1 sin^2(pi di / 4). The report's LEO-to-GEO example
        # (500 km, 28.7 deg to a 35683 km altitude) prints 5.86 km/s.
        nasa_technical_report(
            "An Analytical Optimization of Electric Propulsion Orbit Transfer Vehicles",
            ("S. R. Oleson",),
            "NASA CR-191129",
            1993,
            "https://ntrs.nasa.gov/citations/19930017871",
            "p. 3, eq. (3), and p. 5 verification example",
            organization="NASA Lewis Research Center (Sverdrup Technology)",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={
                "mu": 398600441800000.0,
                "a0": 6878137.0,
                "a1": 42061137.0,
                "di": 0.5009094953223726,
            },
            expected=5859.523707431074,
            rel_tol=1e-12,
            note=(
                "The example transfer of the report: 500 km altitude at 28.7 degrees to a "
                "35683 km altitude orbit at 0 degrees; independent 50-digit mpmath evaluation."
            ),
        ),
        VerificationCase(
            inputs={
                "mu": 398600441800000.0,
                "a0": 6878137.0,
                "a1": 42061137.0,
                "di": 0.5009094953223726,
            },
            expected=5860.0,
            rel_tol=0.001,
            note=(
                "The report prints a required low-thrust delta-v of 5.86 km/s for this same "
                "transfer; the tolerance covers its three-figure rounding."
            ),
        ),
        VerificationCase(
            inputs={"mu": 398600441800000.0, "a0": 7000000.0, "a1": 7000000.0, "di": 0.5},
            expected=5775.499147736466,
            rel_tol=1e-12,
            note="Pure plane change (a0 = a1), where the result is 2 V sin(pi di / 4); mpmath.",
        ),
        VerificationCase(
            inputs={"mu": 398600441800000.0, "a0": 7000000.0, "a1": 42164000.0, "di": 0.0},
            expected=4471.387005979857,
            rel_tol=1e-12,
            note="No plane change: the result is |V0 - V1|; independent 50-digit mpmath value.",
        ),
    ),
    assumptions=(
        "Circular-to-circular, quasi-circular transfer with constant thrust magnitude, constant "
        "thrust angle within each revolution and a small thrust-to-weight ratio (the source "
        "states about 1e-2 or less).",
        "The plane change di is in radians and enters as pi/2 times di. The source states no "
        "upper bound on di; only the geometric limit di <= pi is enforced (larger values raise "
        "ValueError). For a0 = a1 the evaluated delta-v 2 V sin(pi di / 4) peaks at di = 2 rad "
        "and decreases beyond it, so results for di above 2 rad should not be trusted.",
        "Inputs must satisfy mu > 0, a0 > 0, a1 > 0 and 0 <= di <= pi; other values raise "
        "ValueError.",
        "Homogeneous in any consistent units: the result has the units of the circular speed.",
    ),
    tags=("Edelbaum", "low thrust", "electric propulsion", "plane change", "orbit transfer"),
)
