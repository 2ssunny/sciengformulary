"""Barometric Pressure in a Constant-Gradient Layer."""

import math

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    p_b: float,
    T_b: float,  # noqa: N803
    L: float,  # noqa: N803
    h: float,
    h_b: float,
    g0: float,
    R: float,  # noqa: N803
) -> float:
    positive("p_b", p_b)
    positive("T_b", T_b)
    finite("L", L)
    if L == 0:
        raise ValueError("L must not be zero; use the isothermal-layer formula for L = 0.")
    finite("h", h)
    finite("h_b", h_b)
    positive("g0", g0)
    positive("R", R)
    ratio = 1.0 + L * (h - h_b) / T_b
    if ratio <= 0:
        raise ValueError(
            f"1 + L*(h - h_b)/T_b must be positive (the temperature must stay above zero), "
            f"got {ratio!r}."
        )
    # Written with log1p so that a small gradient does not lose digits in the large exponent.
    return finite_result(p_b * math.exp(-g0 / (R * L) * math.log1p(L * (h - h_b) / T_b)))


barometric_pressure_gradient_layer = FormulaSpec(
    id="aerodynamics.barometric_pressure_gradient_layer",
    name="Barometric Pressure in a Constant-Gradient Layer",
    equation="p = p_b * (1 + L * (h - h_b) / T_b)^(-g0 / (R * L))",
    description=(
        "Static pressure inside an atmospheric layer whose temperature changes linearly with "
        "geopotential altitude, found from hydrostatic balance and the ideal-gas law, given the "
        "pressure and temperature at the base of the layer. The layer base values, the gradient, "
        "g0 and R are all supplied by the caller; for a layer with no temperature change use "
        "aerodynamics.barometric_pressure_isothermal_layer."
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
            description=(
                "Temperature at the base of the layer; above 80 km this must be the "
                "molecular-scale temperature T_M,b"
            ),
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="L",
            symbol="L",
            description="Temperature gradient dT/dh in the layer (negative in the troposphere)",
            dimension="Theta L^-1",
            si_unit="K/m",
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
        # Derived from eq. (33a), which is written with the molecular-scale temperature T_M,b,
        # the molecular weight M0 and the universal gas constant R*:
        #   P = P_b [T_M,b / (T_M,b + L_M,b (H - H_b))]^(g0' M0 / (R* L_M,b)).
        # Below 80 km T_M = T; g0' M0 / R* = g0 / R with R = R*/M0 and g0' numerically equal to
        # g0; and inverting the bracket gives the form shipped here. Symbols: P -> p, H -> h,
        # T_M,b -> T_b, L_M,b -> L.
        nasa_technical_report(
            "U.S. Standard Atmosphere, 1976",
            (),
            "NASA-TM-X-74335; NOAA-S/T-76-1562",
            1976,
            "https://ntrs.nasa.gov/citations/19770009539",
            "sec. 1.3.1, eq. (33a), p. 12; Table 4 (layer base heights and gradients), p. 3; "
            "eq. (23), p. 10",
            organization=(
                "National Oceanic and Atmospheric Administration, National Aeronautics and "
                "Space Administration and U.S. Air Force"
            ),
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={
                "p_b": 101325.0,
                "T_b": 288.15,
                "L": -0.0065,
                "h": 5000.0,
                "h_b": 0.0,
                "g0": 9.80665,
                "R": 287.0530720470647,
            },
            expected=54019.91210376207,
            rel_tol=1e-12,
            note="Troposphere at 5000 m'; 50-digit mpmath evaluation of the reference equation.",
        ),
        VerificationCase(
            inputs={
                "p_b": 101325.0,
                "T_b": 288.15,
                "L": -0.0065,
                "h": 11000.0,
                "h_b": 0.0,
                "g0": 9.80665,
                "R": 287.0530720470647,
            },
            expected=22632.06397346293,
            rel_tol=1e-12,
            note="Top of the troposphere at 11 km'; 50-digit mpmath evaluation.",
        ),
        VerificationCase(
            inputs={
                "p_b": 5474.88866967778,
                "T_b": 216.65,
                "L": 0.001,
                "h": 25000.0,
                "h_b": 20000.0,
                "g0": 9.80665,
                "R": 287.0530720470647,
            },
            expected=2511.023353252595,
            rel_tol=1e-12,
            note="Layer with a positive gradient of 1 K/km' (Table 4); 50-digit mpmath value.",
        ),
        VerificationCase(
            inputs={
                "p_b": 101325.0,
                "T_b": 288.15,
                "L": -0.0065,
                "h": 0.0,
                "h_b": 0.0,
                "g0": 9.80665,
                "R": 287.0530720470647,
            },
            expected=101325.0,
            rel_tol=1e-12,
            note="Boundary case: at the layer base the pressure equals the base pressure.",
        ),
        VerificationCase(
            inputs={
                "p_b": 101325.0,
                "T_b": 288.15,
                "L": -0.0065,
                "h": 4996.070273568692,
                "h_b": 0.0,
                "g0": 9.80665,
                "R": 287.0530720470647,
            },
            expected=54048.0,
            rel_tol=5e-05,
            note=(
                "Table I of the reference prints 540.48 mb at a geometric 5000 m, which is "
                "4996.07 m' of geopotential altitude; the tolerance covers the five printed "
                "digits."
            ),
        ),
    ),
    assumptions=(
        "Derived result: eq. (33a) of the source uses T_M, M0 and R*; with R = R*/M0, g0' "
        "numerically equal to g0 and T_M = T below 80 km, the factor "
        "(T_b / (T_b + L (h - h_b)))^(g0 M0 / (R* L)) becomes "
        "(1 + L (h - h_b) / T_b)^(-g0 / (R L)).",
        "Hydrostatic balance with the ideal-gas law, uniform composition (constant molecular "
        "weight) and temperature linear in geopotential altitude, as in the source's layers up "
        "to 84.852 km'. The kinetic temperature equals the molecular-scale temperature only "
        "below 80 km, so for a layer that extends above 80 km T_b must be the molecular-scale "
        "temperature T_M,b of the layer base. The layer's upper limit is not an input and is "
        "not checked.",
        "No constants are built in: g0, R and the layer base values are inputs. The 1976 "
        "Standard Atmosphere uses g0 = 9.80665 m/s^2, R = R*/M0 = 8.31432e3 / 28.9644 = "
        "287.0531 J/(kg K) (R* in N m/(kmol K), M0 in kg/kmol), and the layer data of Table 4.",
        "Heights are geopotential altitudes in geopotential metres (m'); g0 is the constant "
        "that relates them to geometric metres. Otherwise any consistent units work, with L "
        "per unit of the altitude.",
        "L = 0 is rejected (use the isothermal-layer formula) and so is any h at which the "
        "temperature would reach zero.",
    ),
    tags=("atmosphere", "barometric formula", "hydrostatic", "geopotential altitude"),
)
