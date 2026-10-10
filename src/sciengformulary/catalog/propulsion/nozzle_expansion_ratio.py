"""Ideal Nozzle Expansion Ratio from Pressure Ratio:
eps = A_e / A_t = 1 / (((gamma + 1) / 2)^(1 / (gamma - 1)) * (p_e / p_c)^(1 / gamma)
                       * sqrt((gamma + 1) / (gamma - 1) * (1 - (p_e / p_c)^((gamma - 1) / gamma))))
"""

import dataclasses
import math

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import (
    ENGINEERING_ACCESSED,
    naca_report_1135,
    nasa_technical_report,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

# The critical pressure ratio is reproduced to a few ulps by the floating-point power below;
# a ratio within this relative margin of it is accepted as "at the throat" (eps = 1).
_CRITICAL_MARGIN = 1e-12


def _evaluate(gamma: float, p_e: float, p_c: float) -> float:
    if positive("gamma", gamma) <= 1:
        raise ValueError(f"gamma must be greater than 1, got {gamma!r}.")
    positive("p_e", p_e)
    positive("p_c", p_c)
    if p_e >= p_c:
        raise ValueError(f"p_e must be below p_c, got p_e={p_e!r}, p_c={p_c!r}.")
    ratio = p_e / p_c
    critical = (2.0 / (gamma + 1.0)) ** (gamma / (gamma - 1.0))
    if ratio > critical * (1.0 + _CRITICAL_MARGIN):
        raise ValueError(
            "p_e / p_c must not exceed the critical pressure ratio "
            f"(2 / (gamma + 1))^(gamma / (gamma - 1)) = {critical!r} (supersonic exit), "
            f"got {ratio!r}."
        )
    momentum = math.sqrt((gamma + 1.0) / (gamma - 1.0) * (1.0 - ratio ** ((gamma - 1.0) / gamma)))
    denominator = ((gamma + 1.0) / 2.0) ** (1.0 / (gamma - 1.0)) * ratio ** (1.0 / gamma) * momentum
    if denominator == 0.0:
        raise OverflowError("the result is outside the floating-point range (inf).")
    return finite_result(1.0 / denominator)


nozzle_expansion_ratio = FormulaSpec(
    id="propulsion.nozzle_expansion_ratio",
    name="Ideal Nozzle Expansion Ratio from Pressure Ratio",
    equation=(
        "A_e / A_t = 1 / (((gamma + 1) / 2)^(1 / (gamma - 1)) * (p_e / p_c)^(1 / gamma) "
        "* sqrt((gamma + 1) / (gamma - 1) * (1 - (p_e / p_c)^((gamma - 1) / gamma))))"
    ),
    description=(
        "Exit-to-throat area ratio of an ideal convergent-divergent nozzle that expands "
        "isentropically from the chamber stagnation pressure to the exit static pressure. It "
        "takes a pressure ratio and returns an area ratio, with no Mach number involved. The "
        "result is a consistent expansion-ratio input for propulsion.thrust_coefficient."
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
            description="Stagnation pressure at the nozzle inlet",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
    ),
    output=VariableSpec(
        name="eps",
        symbol=r"\epsilon",
        description="Nozzle area expansion ratio A_e / A_t",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Stated up to rewriting: the report prints eps = (2/(gamma+1))^(1/(gamma-1))
        # * (p_c/p_e)^(1/gamma) / sqrt((gamma+1)/(gamma-1) * [1 - (p_e/p_c)^((gamma-1)/gamma)]).
        # The prefactor (2/(gamma+1))^(1/(gamma-1)) * (p_c/p_e)^(1/gamma) is written here as the
        # reciprocal of ((gamma+1)/2)^(1/(gamma-1)) * (p_e/p_c)^(1/gamma). Symbols: the report
        # writes (p_c)_ns for the nozzle-inlet stagnation pressure.
        nasa_technical_report(
            "Design of Liquid Propellant Rocket Engines",
            ("D. K. Huzel", "D. H. Huang"),
            "NASA SP-125",
            1967,
            "https://ntrs.nasa.gov/citations/19710019929",
            "sec. 1.2, eq. (1-20), p. 7 (sample calculation 1-2, pp. 8-10)",
        ),
        # Independent route: p/p_t = (1 + (gamma-1)/2 M^2)^(-gamma/(gamma-1)) gives the exit
        # Mach number, and the area ratio follows from the isentropic area-Mach relation. The
        # shared builder records the access date of the other formulas, so it is replaced
        # with the date this page was opened for this formula.
        dataclasses.replace(
            naca_report_1135("eqs. (44) and (80), pp. 616 and 618"),
            accessed=ENGINEERING_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"gamma": 1.2, "p_e": 0.009852216748768473, "p_c": 1.0},
            expected=12.006365875398286,
            rel_tol=1e-10,
            note=(
                "Sample calculation 1-2 of the first reference (gamma 1.2, p_c/p_e = 101.5, "
                "printed eps = 12); expected value from a 50-digit mpmath evaluation through "
                "the second reference (exit Mach number from eq. (44), area ratio from "
                "eq. (80))."
            ),
        ),
        VerificationCase(
            inputs={"gamma": 1.4, "p_e": 0.01, "p_c": 1.0},
            expected=8.116468977058233,
            rel_tol=1e-10,
            note="mpmath through the exit Mach number and area-Mach relation of the second "
            "reference, gamma 1.4 and p_e / p_c = 0.01.",
        ),
        VerificationCase(
            inputs={"gamma": 1.4, "p_e": 0.5282817877171742, "p_c": 1.0},
            expected=1.0,
            rel_tol=1e-10,
            note="Edge case: the critical pressure ratio (2/2.4)^3.5 puts the exit at the "
            "throat, so the area ratio is exactly 1.",
        ),
        VerificationCase(
            inputs={"gamma": 1.25, "p_e": 0.0005, "p_c": 1.0},
            expected=102.9617873957671,
            rel_tol=1e-10,
            note="mpmath through the exit Mach number and area-Mach relation of the second "
            "reference, gamma 1.25 and a high expansion.",
        ),
        VerificationCase(
            inputs={"gamma": 1.2, "p_e": 9.85, "p_c": 1000.0},
            expected=12.0,
            rel_tol=0.004,
            note=(
                "Printed values of sample calculation 1-2 (9.85 and 1000 psia, eps = 12); the "
                "ratio is dimensionless. The tolerance covers the rounding of the printed "
                "inputs and result."
            ),
        ),
    ),
    assumptions=(
        "Derived result: the cited equation is rewritten with the reciprocal prefactor "
        "((gamma + 1) / 2)^(1 / (gamma - 1)) * (p_e / p_c)^(1 / gamma); this is checked "
        "against the independent route through the exit Mach number and the isentropic "
        "area-Mach relation.",
        "Ideal, one-dimensional, isentropic flow of a perfect gas with constant gamma, "
        "sonic at the throat.",
        "gamma must be greater than 1, p_e and p_c positive with p_e < p_c, and p_e / p_c must "
        "not exceed the critical ratio (2 / (gamma + 1))^(gamma / (gamma - 1)); at the critical "
        "ratio the result is 1, and a larger ratio (subsonic exit) is rejected.",
        "p_e and p_c in the same pressure unit.",
    ),
    tags=("nozzle", "expansion ratio", "area ratio", "rocket", "isentropic", "propulsion"),
)
