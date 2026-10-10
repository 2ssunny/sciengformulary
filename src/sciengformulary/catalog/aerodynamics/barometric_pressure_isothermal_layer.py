"""Barometric Pressure in an Isothermal Layer."""

import math

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    p_b: float,
    T_b: float,  # noqa: N803
    h: float,
    h_b: float,
    g0: float,
    R: float,  # noqa: N803
) -> float:
    positive("p_b", p_b)
    positive("T_b", T_b)
    finite("h", h)
    finite("h_b", h_b)
    positive("g0", g0)
    positive("R", R)
    # math.exp raises OverflowError for a huge negative altitude difference, so no inf is returned.
    return finite_result(p_b * math.exp(-g0 * (h - h_b) / (R * T_b)))


barometric_pressure_isothermal_layer = FormulaSpec(
    id="aerodynamics.barometric_pressure_isothermal_layer",
    name="Barometric Pressure in an Isothermal Layer",
    equation="p = p_b * exp(-g0 * (h - h_b) / (R * T_b))",
    description=(
        "Static pressure inside an atmospheric layer of constant temperature, found from "
        "hydrostatic balance and the ideal-gas law, given the pressure at the base of the layer. "
        "It is the zero-gradient companion of aerodynamics.barometric_pressure_gradient_layer; "
        "g0 and R are supplied by the caller."
    ),
    inputs=(
        VariableSpec(
            name="p_b",
            symbol="p_b",
            description="Pressure at the base of the layer",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="T_b",
            symbol="T_b",
            description="Constant temperature of the layer",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="h",
            symbol="h",
            description="Geopotential altitude of the evaluation point",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="h_b",
            symbol="h_b",
            description="Geopotential altitude of the layer base",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="g0",
            symbol="g_0",
            description="Standard gravity that defines the geopotential altitude scale",
            dimension="L T^-2",
            si_unit="m/s^2",
        ),
        VariableSpec(
            name="R",
            symbol="R",
            description="Specific gas constant of the air, R*/M0",
            dimension="L^2 T^-2 Theta^-1",
            si_unit="J/(kg K)",
        ),
    ),
    output=VariableSpec(
        name="p",
        symbol="p",
        description="Static pressure at altitude h",
        dimension="M L^-1 T^-2",
        si_unit="Pa",
    ),
    evaluator=_evaluate,
    references=(
        # Derived from eq. (33b): P = P_b exp[-g0' M0 (H - H_b) / (R* T_M,b)] for a layer with
        # zero gradient. With R = R*/M0, g0' numerically equal to g0 and T_M,b = T_b below 80 km
        # only the symbols change. Symbols: P -> p, H -> h, T_M,b -> T_b.
        nasa_technical_report(
            "U.S. Standard Atmosphere, 1976",
            (),
            "NASA-TM-X-74335; NOAA-S/T-76-1562",
            1976,
            "https://ntrs.nasa.gov/citations/19770009539",
            "sec. 1.3.1, eq. (33b), p. 12; Table 4, p. 3",
            organization=(
                "National Oceanic and Atmospheric Administration, National Aeronautics and "
                "Space Administration and U.S. Air Force"
            ),
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={
                "p_b": 22632.06397346293,
                "T_b": 216.65,
                "h": 15000.0,
                "h_b": 11000.0,
                "g0": 9.80665,
                "R": 287.0530720470647,
            },
            expected=12044.570862423208,
            rel_tol=1e-12,
            note="Isothermal layer from 11 km' to 15 km'; 50-digit mpmath evaluation.",
        ),
        VerificationCase(
            inputs={
                "p_b": 22632.06397346293,
                "T_b": 216.65,
                "h": 20000.0,
                "h_b": 11000.0,
                "g0": 9.80665,
                "R": 287.0530720470647,
            },
            expected=5474.88866967778,
            rel_tol=1e-12,
            note="Top of the isothermal layer at 20 km'; 50-digit mpmath evaluation.",
        ),
        VerificationCase(
            inputs={
                "p_b": 22632.06397346293,
                "T_b": 216.65,
                "h": 11000.0,
                "h_b": 11000.0,
                "g0": 9.80665,
                "R": 287.0530720470647,
            },
            expected=22632.06397346293,
            rel_tol=1e-12,
            note="Boundary case: at the layer base the pressure equals the base pressure.",
        ),
        VerificationCase(
            inputs={
                "p_b": 22632.06397346293,
                "T_b": 216.65,
                "h": 14964.687968767215,
                "h_b": 11000.0,
                "g0": 9.80665,
                "R": 287.0530720470647,
            },
            expected=12111.0,
            rel_tol=0.0001,
            note=(
                "Table I of the reference prints 121.11 mb at a geometric 15000 m, which is "
                "14965 m' of geopotential altitude. The source table truncates rather than "
                "rounds on this row, so the computed 121.118 mb is 6.8e-5 (relative) above the "
                "printed value; the tolerance of 1e-4 allows for that truncation."
            ),
        ),
    ),
    assumptions=(
        "Derived result: eq. (33b) of the source uses M0, R* and T_M,b; with R = R*/M0, g0' "
        "numerically equal to g0 and T_M = T below 80 km it becomes "
        "p_b exp(-g0 (h - h_b) / (R T_b)).",
        "Hydrostatic balance with the ideal-gas law and constant composition and temperature; "
        "the 1976 Standard Atmosphere has isothermal layers at 11 to 20 km' and 47 to 51 km'. "
        "The layer's upper limit is not an input and is not checked.",
        "No constants are built in: g0, R and the layer base values are inputs. The 1976 "
        "Standard Atmosphere uses g0 = 9.80665 m/s^2 and R = R*/M0 = 8.31432e3 / 28.9644 = "
        "287.0531 J/(kg K) (R* in N m/(kmol K), M0 in kg/kmol).",
        "Heights are geopotential altitudes in geopotential metres (m'); g0 is the constant "
        "that relates them to geometric metres. Otherwise any consistent units work.",
    ),
    tags=("atmosphere", "barometric formula", "isothermal layer", "geopotential altitude"),
)
