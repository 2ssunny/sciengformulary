"""Hohmann Transfer First Impulse: dv1 = sqrt(mu / r1) * (sqrt(2 r2 / (r1 + r2)) - 1)."""

import math

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.catalog.orbital._support import dunning_sp325
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(mu: float, r1: float, r2: float) -> float:
    positive("mu", mu)
    positive("r1", r1)
    positive("r2", r2)
    total = finite_result(r1 + r2)
    # sqrt(2 r2 / total) - 1 = ((r2 - r1) / total) / (sqrt(2 r2 / total) + 1): the algebraically
    # equal right-hand side avoids the cancellation in the bracket when r1 is close to r2.
    bracket = (r2 - r1) / total / (math.sqrt(2.0 * r2 / total) + 1.0)
    return finite_result(math.sqrt(mu / r1) * bracket)


hohmann_first_impulse = FormulaSpec(
    id="orbital.hohmann_first_impulse",
    name="Hohmann Transfer First Impulse",
    equation="dv1 = sqrt(mu / r1) * (sqrt(2 * r2 / (r1 + r2)) - 1)",
    description=(
        "Speed change applied on the initial circular orbit to enter the Hohmann transfer "
        "ellipse toward the final circular orbit."
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
            name="r2",
            symbol="r_2",
            description="Radius of the final circular orbit",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="dv1",
        symbol=r"\Delta v_1",
        description="First tangential impulse (signed speed change along the flight direction)",
        dimension="L T^-1",
        si_unit="m/s",
    ),
    evaluator=_evaluate,
    references=(
        # The report prints the initial circular speed sqrt(mu / r_initial) (eq. 4), the
        # transfer semi-major axis (r_initial + r_final) / 2 (eq. 6), the transfer-ellipse speed
        # at the initial apse sqrt(2 mu / r_initial - mu / a_trans) (eq. 7) and the total
        # delta-v as (v_trans_a - v_initial) + (v_final - v_trans_b) (eq. 9). The shipped form is
        # the first bracket with a_trans substituted. It is the textbook circular-start form;
        # some libraries use the actual current speed instead.
        nasa_technical_report(
            "Conceptual Design of a Communications Relay Satellite for a Lunar Sample Return "
            "Mission",
            ("C. W. Brunner",),
            "NASA/CR-2005-213034",
            2005,
            "https://ntrs.nasa.gov/citations/20050232849",
            "eqs. (4), (6), (7), (9), pp. 15-16",
            organization="NASA Langley Research Center (The George Washington University, JIAFS)",
        ),
        # Derived result (second source supports the ingredients, not the Hohmann result):
        # circular speed sqrt(mu / r) (eq. 1-51), the speed equation V^2 / 2 = H + mu / r
        # (eq. 1-29) and a = -mu / (2 H) for the ellipse (eq. 1-47) with a = (r_a + r_p) / 2.
        dunning_sp325("chap. 1, eqs. (1-29), p. 8, (1-47), p. 13 and (1-51), p. 14"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"mu": 398600441800000.0, "r1": 6678000.0, "r2": 42164000.0},
            expected=2425.769028306859,
            rel_tol=1e-12,
            abs_tol=1e-9,
            note="300 km altitude orbit to geostationary radius; 50-digit mpmath evaluation.",
        ),
        VerificationCase(
            inputs={"mu": 398600441800000.0, "r1": 7000000.0, "r2": 7000000.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-9,
            note="Edge r1 = r2: no transfer is needed, so the impulse is zero.",
        ),
        VerificationCase(
            inputs={"mu": 398600441800000.0, "r1": 42164000.0, "r2": 6678000.0},
            expected=-1466.8387152844527,
            rel_tol=1e-12,
            abs_tol=1e-9,
            note="Lowering from geostationary to 300 km radius (retro burn); 50-digit mpmath.",
        ),
    ),
    assumptions=(
        "Derived result: the report prints the circular speed, the transfer semi-major axis "
        "and the transfer-ellipse speed separately; substituting a_trans = (r1 + r2) / 2 into "
        "the first bracket (v_trans_a - v_initial) of its total delta-v gives the closed form "
        "used here.",
        "Coplanar circular initial and final orbits about the same central body, with "
        "impulsive tangential burns at the apsides of the transfer ellipse.",
        "The result is signed along the flight direction: positive when raising (r2 > r1), "
        "negative when lowering (r2 < r1) and zero for r1 = r2.",
        "mu, r1 and r2 must be finite and positive; otherwise ValueError is raised.",
        "Any consistent units: mu in L^3/T^2 and r1, r2 in L give a speed change in L/T.",
    ),
    tags=("Hohmann transfer", "delta-v", "orbit raising"),
)
