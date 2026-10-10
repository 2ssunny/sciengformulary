"""Specific Angular Momentum from the Semi-Latus Rectum: h = sqrt(mu * p)."""

import math

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.catalog.orbital._support import dunning_sp325
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(mu: float, p: float) -> float:
    positive("mu", mu)
    non_negative("p", p)
    return math.sqrt(finite_result(mu * p))


specific_angular_momentum = FormulaSpec(
    id="orbital.specific_angular_momentum",
    name="Specific Angular Momentum from Semi-Latus Rectum",
    equation="h = sqrt(mu * p)",
    description=(
        "Magnitude of the angular momentum per unit mass of a Kepler orbit with semi-latus "
        "rectum p."
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
            name="p",
            symbol="p",
            description="Semi-latus rectum of the orbit",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="h",
        symbol="h",
        description="Specific angular momentum magnitude",
        dimension="L^2 T^-1",
        si_unit="m^2/s",
    ),
    evaluator=_evaluate,
    references=(
        # The report defines h through the flight-path angle, h = r v cos(phi) (eq. 13), and
        # prints the semi-parameter as p = h^2 / mu (eq. 18); solving the latter for h gives
        # h = sqrt(mu p).
        nasa_technical_report(
            "Conceptual Design of a Communications Relay Satellite for a Lunar Sample Return "
            "Mission",
            ("C. W. Brunner",),
            "NASA/CR-2005-213034",
            2005,
            "https://ntrs.nasa.gov/citations/20050232849",
            "eqs. (13), (18), pp. 19-20",
            organization="NASA Langley Research Center (The George Washington University, JIAFS)",
        ),
        # Stated, with the symbols renamed: the semilatus rectum is p = h^2 / (g_e r_e^2)
        # (eq. 1-36) with h the angular momentum per unit mass (eq. 1-23); g_e r_e^2 plays the
        # role of mu. Solving for h gives h = sqrt(mu p).
        dunning_sp325("chap. 1, eq. (1-23), p. 7, and eq. (1-36), p. 9"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"mu": 398600441800000.0, "p": 7000000.0},
            expected=52822373030.75279,
            rel_tol=1e-12,
            note="Circular orbit of radius 7000 km; 50-digit mpmath evaluation.",
        ),
        VerificationCase(
            inputs={"mu": 398600441800000.0, "p": 6930000.0},
            expected=52557597563.75856,
            rel_tol=1e-12,
            note="Ellipse with p = 6930 km; 50-digit mpmath evaluation.",
        ),
        VerificationCase(
            inputs={"mu": 398600441800000.0, "p": 0.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Edge p = 0, the rectilinear orbit with zero angular momentum.",
        ),
    ),
    assumptions=(
        "Derived result: the source prints p = h^2 / mu; solving for the non-negative root "
        "gives h = sqrt(mu p).",
        "Two-body Keplerian motion; h is the magnitude of the angular momentum per unit mass.",
        "p = 0 is the degenerate radial (rectilinear) orbit and gives h = 0.",
        "mu must be finite and positive and p finite and not negative; otherwise ValueError is "
        "raised. A result outside the float range raises OverflowError.",
        "Any consistent units: mu in L^3/T^2 and p in L give h in L^2/T.",
    ),
    tags=("specific angular momentum", "semi-latus rectum", "orbit"),
)
