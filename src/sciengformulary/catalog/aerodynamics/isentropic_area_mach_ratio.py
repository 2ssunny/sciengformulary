"""Isentropic Area-Mach Number Relation: A / A* as a function of M and gamma."""

import dataclasses

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, naca_report_1135
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(M: float, gamma: float) -> float:  # noqa: N803
    positive("M", M)
    if positive("gamma", gamma) <= 1:
        raise ValueError(f"gamma must be greater than 1, got {gamma!r}.")
    exponent = (gamma + 1.0) / (2.0 * (gamma - 1.0))
    return finite_result((2.0 / (gamma + 1.0) * (1.0 + 0.5 * (gamma - 1.0) * M**2)) ** exponent / M)


isentropic_area_mach_ratio = FormulaSpec(
    id="aerodynamics.isentropic_area_mach_ratio",
    name="Isentropic Area-Mach Number Relation",
    equation="A / A_star = (1 / M) * ((2 / (gamma + 1)) * (1 + (gamma - 1) / 2 * M^2))"
    "^((gamma + 1) / (2 * (gamma - 1)))",
    description=(
        "Ratio of the local stream-tube cross-section to the cross-section where the Mach "
        "number is 1, for steady one-dimensional isentropic flow of a calorically perfect gas. "
        "It fixes how the area must change for the Mach number to change; the companion "
        "relations aerodynamics.isentropic_pressure_ratio, isentropic_temperature_ratio and "
        "isentropic_density_ratio give the static-to-total property ratios at the same Mach "
        "number. The relation is single valued in M but not in A / A_star."
    ),
    inputs=(
        VariableSpec(
            name="M",
            symbol="M",
            description="Local Mach number",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="gamma",
            symbol=r"\gamma",
            description="Ratio of specific heats c_p / c_v of the gas",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="A_over_Astar",
        symbol="A/A^*",
        description="Ratio of the local stream-tube area to the area at the sonic section",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Stated up to the reciprocal: eq. (80) prints A*/A = ((gamma+1)/2)^((gamma+1)/(2(gamma-1)))
        # M (1 + (gamma-1)/2 M^2)^(-(gamma+1)/(2(gamma-1))); the shipped A/A* is its inverse.
        # Table II prints A/A* for gamma = 7/5. The shared builder carries the access date of the
        # other formulas, so it is replaced with the date this report was opened for this one.
        dataclasses.replace(
            naca_report_1135("eq. (80); Tables I and II"),
            accessed=ENGINEERING_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"M": 2.0, "gamma": 1.4},
            expected=1.6875,
            rel_tol=1e-12,
            note="Exact fraction 27/16 from the reciprocal of eq. (80).",
        ),
        VerificationCase(
            inputs={"M": 1.0, "gamma": 1.4},
            expected=1.0,
            rel_tol=1e-12,
            note="Boundary case: the sonic section has A / A_star = 1.",
        ),
        VerificationCase(
            inputs={"M": 0.5, "gamma": 1.4},
            expected=1.33984375,
            rel_tol=1e-12,
            note="Subsonic branch; exact fraction 343/256 from the reciprocal of eq. (80).",
        ),
        VerificationCase(
            inputs={"M": 3.0, "gamma": 1.4},
            expected=4.234567901234569,
            rel_tol=1e-12,
            note="Supersonic branch; mpmath evaluation of the reciprocal of eq. (80).",
        ),
        VerificationCase(
            inputs={"M": 2.0, "gamma": 1.2},
            expected=1.8837116867500996,
            rel_tol=1e-12,
            note="gamma = 1.2; mpmath evaluation of the reciprocal of eq. (80).",
        ),
        VerificationCase(
            inputs={"M": 2.5, "gamma": 1.4},
            expected=2.637,
            rel_tol=0.0002,
            note="Table II prints A/A* = 2.637 at M = 2.50 for gamma = 7/5; four printed digits.",
        ),
        VerificationCase(
            inputs={"M": 3.0, "gamma": 1.4},
            expected=4.235,
            rel_tol=0.0002,
            note="Table II prints A/A* = 4.235 at M = 3.00 for gamma = 7/5; four printed digits.",
        ),
    ),
    assumptions=(
        "Steady, one-dimensional, adiabatic and reversible flow of a thermally and calorically "
        "perfect gas.",
        "Derived result: eq. (80) of the source prints the reciprocal A_star / A; the "
        "shipped A / A_star is its inverse.",
        "Valid on both the subsonic (M < 1) and supersonic (M > 1) branches; the result is "
        "never below 1. Inverting for M from a given area ratio is not done here and has two "
        "solutions.",
        "M must be positive and gamma greater than 1.",
    ),
    tags=("isentropic flow", "area ratio", "nozzle", "compressible flow"),
)
