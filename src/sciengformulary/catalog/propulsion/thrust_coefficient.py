"""Rocket Nozzle Thrust Coefficient (Ideal, Any Altitude):
C_F = sqrt(2 gamma^2 / (gamma - 1) * (2 / (gamma + 1))^((gamma + 1) / (gamma - 1))
           * (1 - (p_e / p_c)^((gamma - 1) / gamma))) + eps * (p_e - p_a) / p_c
"""

import math

from sciengformulary.catalog._domain import finite, finite_result, non_negative, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


# The critical pressure ratio is reproduced to a few ulps by the floating-point power below;
# a ratio within this relative margin of it is accepted as "at the throat".
_CRITICAL_MARGIN = 1e-12


def _evaluate(gamma: float, p_e: float, p_c: float, p_a: float, eps: float) -> float:
    if positive("gamma", gamma) <= 1:
        raise ValueError(f"gamma must be greater than 1, got {gamma!r}.")
    positive("p_e", p_e)
    positive("p_c", p_c)
    if p_e >= p_c:
        raise ValueError(f"p_e must be below p_c, got p_e={p_e!r}, p_c={p_c!r}.")
    critical = (2.0 / (gamma + 1.0)) ** (gamma / (gamma - 1.0))
    if p_e / p_c > critical * (1.0 + _CRITICAL_MARGIN):
        raise ValueError(
            "p_e / p_c must not exceed the critical pressure ratio "
            f"(2 / (gamma + 1))^(gamma / (gamma - 1)) = {critical!r}: the formula assumes a "
            f"sonic throat and a supersonic exit, got {p_e / p_c!r}."
        )
    non_negative("p_a", p_a)
    if finite("eps", eps) < 1:
        raise ValueError(f"eps must be at least 1, got {eps!r}.")
    momentum = math.sqrt(
        2.0
        * gamma**2
        / (gamma - 1.0)
        * (2.0 / (gamma + 1.0)) ** ((gamma + 1.0) / (gamma - 1.0))
        * (1.0 - (p_e / p_c) ** ((gamma - 1.0) / gamma))
    )
    return finite_result(momentum + eps * (p_e - p_a) / p_c)


thrust_coefficient = FormulaSpec(
    id="propulsion.thrust_coefficient",
    name="Rocket Nozzle Thrust Coefficient (Ideal, Any Altitude)",
    equation=(
        "C_F = sqrt((2 * gamma^2 / (gamma - 1)) * (2 / (gamma + 1))^((gamma + 1) / (gamma - 1)) "
        "* (1 - (p_e / p_c)^((gamma - 1) / gamma))) + eps * (p_e - p_a) / p_c"
    ),
    description=(
        "Thrust coefficient C_F = F / (A_t * p_c) of an ideal rocket nozzle: a momentum term "
        "fixed by gamma and the exit-to-chamber pressure ratio, plus a pressure-thrust term "
        "at the given ambient pressure. It is a dimensionless nozzle figure of merit, not a "
        "force: propulsion.rocket_thrust gives the thrust itself from mass flow, exhaust "
        "velocity and exit conditions, and propulsion.nozzle_expansion_ratio gives the eps that "
        "is consistent with p_e / p_c."
    ),
    inputs=(
        VariableSpec(
            name="gamma",
            symbol=r"\gamma",
            description="Ratio of specific heats of the exhaust gas",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="p_e",
            symbol="p_e",
            description="Static pressure at the nozzle exit",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="p_c",
            symbol="(p_c)_{ns}",
            description="Nozzle stagnation (chamber) pressure",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="p_a",
            symbol="p_a",
            description="Ambient pressure (zero in vacuum)",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="eps",
            symbol=r"\epsilon",
            description="Nozzle area expansion ratio A_e / A_t",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="C_F",
        symbol="C_f",
        description="Thrust coefficient F / (A_t * p_c)",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Stated: the report defines C_f = F / (A_t * (p_c)_ns) in eq. (1-33) and prints the
        # ideal form in eq. (1-33a). It writes (p_c)_ns for the nozzle stagnation pressure and
        # C_f for the thrust coefficient.
        nasa_technical_report(
            "Design of Liquid Propellant Rocket Engines",
            ("D. K. Huzel", "D. H. Huang"),
            "NASA SP-125",
            1967,
            "https://ntrs.nasa.gov/citations/19710019929",
            "sec. 1.3, eq. (1-33a), p. 12 (definition (1-33) C_f = F/(A_t (p_c)_ns))",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"gamma": 1.2, "p_e": 1.0, "p_c": 101.5, "p_a": 1.0, "eps": 12.006365875398286},
            expected=1.6462855673870371,
            rel_tol=1e-11,
            note="50-digit mpmath evaluation of the cited equation; gamma 1.2, optimum "
            "expansion (p_a = p_e), eps consistent with eq. (1-20) of the same report.",
        ),
        VerificationCase(
            inputs={"gamma": 1.2, "p_e": 1.0, "p_c": 101.5, "p_a": 0.0, "eps": 12.006365875398286},
            expected=1.7645748863564783,
            rel_tol=1e-11,
            note="50-digit mpmath evaluation of the cited equation for the same nozzle in vacuum.",
        ),
        VerificationCase(
            inputs={"gamma": 1.2, "p_e": 1.0, "p_c": 101.5, "p_a": 2.0, "eps": 12.006365875398286},
            expected=1.527996248417596,
            rel_tol=1e-11,
            note="50-digit mpmath evaluation of the cited equation, over-expanded with "
            "p_a = 2 p_e (negative pressure term).",
        ),
        VerificationCase(
            inputs={"gamma": 1.4, "p_e": 1.0, "p_c": 50.0, "p_a": 1.0, "eps": 5.158477790334015},
            expected=1.4861717353486505,
            rel_tol=1e-11,
            note="50-digit mpmath evaluation of the cited equation; gamma 1.4, optimum expansion.",
        ),
    ),
    assumptions=(
        "Ideal, one-dimensional, isentropic nozzle flow of a perfect gas with constant gamma; "
        "no friction, divergence or flow-separation losses.",
        "eps and p_e / p_c are linked through the ideal expansion-ratio relation "
        "(propulsion.nozzle_expansion_ratio). The evaluator does not enforce the link, so "
        "pass a consistent pair.",
        "Matched expansion (p_a = p_e) drops the pressure term of the sum.",
        "gamma must be greater than 1, p_e and p_c positive with p_e / p_c at most the critical "
        "pressure ratio (2 / (gamma + 1))^(gamma / (gamma - 1)) (sonic throat, supersonic exit; "
        "larger values raise ValueError), p_a not negative and eps at least 1; all pressures in "
        "the same unit.",
    ),
    tags=("thrust coefficient", "C_F", "nozzle", "rocket", "propulsion"),
)
