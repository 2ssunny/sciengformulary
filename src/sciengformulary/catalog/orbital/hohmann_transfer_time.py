"""Hohmann Transfer Time of Flight: t_H = pi * sqrt(((r1 + r2) / 2)^3 / mu)."""

import math

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.catalog.orbital._support import dunning_sp325
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(mu: float, r1: float, r2: float) -> float:
    positive("mu", mu)
    positive("r1", r1)
    positive("r2", r2)
    a_trans = 0.5 * finite_result(r1 + r2)
    # pi * a * sqrt(a / mu) equals pi * sqrt(a^3 / mu) without forming a^3, which could overflow.
    return finite_result(math.pi * a_trans * math.sqrt(a_trans / mu))


hohmann_transfer_time = FormulaSpec(
    id="orbital.hohmann_transfer_time",
    name="Hohmann Transfer Time of Flight",
    equation="t_H = pi * sqrt(((r1 + r2) / 2)^3 / mu)",
    description=(
        "Time to travel from one apse of the Hohmann transfer ellipse to the other, which is "
        "half the period of that ellipse."
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
            description="Radius of the initial circular orbit (one apse of the transfer ellipse)",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="r2",
            symbol="r_2",
            description="Radius of the final circular orbit (other apse of the transfer ellipse)",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="t_H",
        symbol="t_H",
        description="Transfer time",
        dimension="T",
        si_unit="s",
    ),
    evaluator=_evaluate,
    references=(
        # The report prints the transfer semi-major axis a_trans = (r_initial + r_final) / 2
        # (eq. 6) and the transfer time tau_trans = pi sqrt(a_trans^3 / mu) (eq. 10), half the
        # transfer-ellipse period. The shipped form substitutes a_trans.
        nasa_technical_report(
            "Conceptual Design of a Communications Relay Satellite for a Lunar Sample Return "
            "Mission",
            ("C. W. Brunner",),
            "NASA/CR-2005-213034",
            2005,
            "https://ntrs.nasa.gov/citations/20050232849",
            "eqs. (6), (10), p. 16",
            organization="NASA Langley Research Center (The George Washington University, JIAFS)",
        ),
        # Stated, with a = (r_a + r_p) / 2 (eq. 1-47, p. 13) and the period P = 2 pi sqrt(a^3 /
        # mu) of an ellipse (eq. 1-48, p. 13); half the period is the time between the apsides.
        dunning_sp325("chap. 1, eqs. (1-47) and (1-48), p. 13"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"mu": 398600441800000.0, "r1": 6678000.0, "r2": 42164000.0},
            expected=18990.051838481286,
            rel_tol=1e-12,
            note="300 km altitude orbit to geostationary radius; 50-digit mpmath evaluation.",
        ),
        VerificationCase(
            inputs={"mu": 398600441800000.0, "r1": 7000000.0, "r2": 7000000.0},
            expected=2914.2583188430076,
            rel_tol=1e-12,
            note="Edge r1 = r2: half the period of the circular orbit; 50-digit mpmath value.",
        ),
        VerificationCase(
            inputs={"mu": 398600441800000.0, "r1": 42164000.0, "r2": 6678000.0},
            expected=18990.051838481286,
            rel_tol=1e-12,
            note="Radii swapped: the time is symmetric in r1 and r2; 50-digit mpmath value.",
        ),
    ),
    assumptions=(
        "Derived result: the report prints the transfer semi-major axis and the transfer time "
        "in terms of it; substituting a_trans = (r1 + r2) / 2 into pi sqrt(a_trans^3 / mu) "
        "gives the two-radius form used here.",
        "Transfer ellipse with apsides r1 and r2, travelled for half a revolution under "
        "two-body motion.",
        "The result is symmetric in r1 and r2 and positive; it does not depend on whether the "
        "transfer raises or lowers the orbit.",
        "mu, r1 and r2 must be finite and positive; otherwise ValueError is raised.",
        "Any consistent units: mu in L^3/T^2 and r1, r2 in L give a time in T.",
    ),
    tags=("Hohmann transfer", "time of flight", "transfer ellipse"),
)
