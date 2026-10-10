"""Isentropic Mass Flow Rate from Mach number and stagnation conditions."""

import dataclasses
import math

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, naca_report_1135
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    A: float,  # noqa: N803
    p0: float,
    T0: float,  # noqa: N803
    gamma: float,
    R: float,  # noqa: N803
    M: float,  # noqa: N803
) -> float:
    positive("A", A)
    positive("p0", p0)
    positive("T0", T0)
    if positive("gamma", gamma) <= 1:
        raise ValueError(f"gamma must be greater than 1, got {gamma!r}.")
    positive("R", R)
    non_negative("M", M)
    factor = 1.0 + 0.5 * (gamma - 1.0) * M**2
    exponent = -(gamma + 1.0) / (2.0 * (gamma - 1.0))
    return finite_result(A * p0 * math.sqrt(gamma / (R * T0)) * M * factor**exponent)


isentropic_mass_flow_rate = FormulaSpec(
    id="aerodynamics.isentropic_mass_flow_rate",
    name="Isentropic Mass Flow Rate from Mach Number and Stagnation Conditions",
    equation="mdot = A * p0 * sqrt(gamma / (R * T0)) * M * "
    "(1 + (gamma - 1) / 2 * M^2)^(-(gamma + 1) / (2 * (gamma - 1)))",
    description=(
        "Mass flow rate through a stream-tube cross-section of a steady isentropic flow of a "
        "perfect gas, from the local Mach number and the stagnation pressure and temperature. "
        "It differs from fluids.mass_flow_rate (density times velocity times area) in using "
        "stagnation conditions and Mach number instead of the local density and speed. At "
        "M = 1 it is the choked mass flow of the section."
    ),
    inputs=(
        VariableSpec(
            name="A",
            symbol="A",
            description="Local cross-sectional area of the stream tube",
            dimension="L^2",
            si_unit="m^2",
        ),
        VariableSpec(
            name="p0",
            symbol="p_0",
            description="Stagnation (total) pressure",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="T0",
            symbol="T_0",
            description="Stagnation (total) temperature",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="gamma",
            symbol=r"\gamma",
            description="Ratio of specific heats c_p / c_v of the gas",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="R",
            symbol="R",
            description="Specific gas constant of the gas",
            dimension="L^2 T^-2 Theta^-1",
            si_unit="J/(kg K)",
        ),
        VariableSpec(
            name="M",
            symbol="M",
            description="Local Mach number at the cross-section",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="mdot",
        symbol=r"\dot{m}",
        description="Mass flow rate",
        dimension="M T^-1",
        si_unit="kg/s",
    ),
    evaluator=_evaluate,
    references=(
        # Derived: the report prints p/rho = R T (26), a = sqrt(gamma R T) (29b), M = V/a (30),
        # T/T_t (43) and p/p_t (44) as functions of M, and rho V A = constant (79); the text
        # after the area relation says these give the mass flow per unit area as a function of
        # Mach number, total temperature and total pressure, without printing the product. The
        # product is formed here: mdot = rho V A with rho = p/(R T), V = M a, and the powers of
        # (1 + (gamma-1)/2 M^2) combined. The shared builder carries the access date of the
        # other formulas, so it is replaced with the date this report was opened for this one.
        dataclasses.replace(
            naca_report_1135(
                "eqs. (26), (29b), (30), (43), (44), (46), pp. 615-616; eq. (79) and text, p. 618"
            ),
            accessed=ENGINEERING_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={
                "A": 0.01,
                "p0": 500000.0,
                "T0": 300.0,
                "gamma": 1.4,
                "R": 287.0530720470647,
                "M": 1.0,
            },
            expected=11.66671414836129,
            rel_tol=1e-11,
            note=(
                "Choked flow; mpmath evaluation of rho * V * A built separately from the "
                "reference relations (26), (29b), (30), (43) and (44)."
            ),
        ),
        VerificationCase(
            inputs={
                "A": 0.01,
                "p0": 500000.0,
                "T0": 300.0,
                "gamma": 1.4,
                "R": 287.0530720470647,
                "M": 0.5,
            },
            expected=8.70751843143,
            rel_tol=1e-11,
            note="Subsonic station; same independent mpmath construction of rho * V * A.",
        ),
        VerificationCase(
            inputs={
                "A": 0.002,
                "p0": 101325.0,
                "T0": 288.15,
                "gamma": 1.4,
                "R": 287.0530720470647,
                "M": 2.0,
            },
            expected=0.28591220493316727,
            rel_tol=1e-11,
            note="Supersonic station; same independent mpmath construction of rho * V * A.",
        ),
        VerificationCase(
            inputs={
                "A": 0.01,
                "p0": 500000.0,
                "T0": 300.0,
                "gamma": 1.4,
                "R": 287.0530720470647,
                "M": 0.0,
            },
            expected=0.0,
            rel_tol=1e-11,
            abs_tol=1e-15,
            note="Boundary case: at M = 0 nothing flows.",
        ),
    ),
    assumptions=(
        "Derived result: mdot = rho V A with V = M a, a = sqrt(gamma R T), rho = p / (R T), "
        "p = p0 (1 + (gamma-1)/2 M^2)^(-gamma/(gamma-1)) and T = T0 / (1 + (gamma-1)/2 M^2); "
        "collecting the powers gives the shipped form. The source describes this result in "
        "words but does not print the product.",
        "Steady, one-dimensional isentropic flow of a thermally and calorically perfect gas; "
        "valid on the subsonic and supersonic branches. A, p0, T0, gamma and R are consistent "
        "with the Mach number given at the section.",
        "SI units (or any consistent set); sqrt(gamma / (R T0)) carries s/m.",
    ),
    tags=("mass flow", "isentropic flow", "choked flow", "compressible flow"),
)
