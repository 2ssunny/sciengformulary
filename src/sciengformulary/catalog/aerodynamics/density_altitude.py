"""Density Altitude in the Standard Troposphere."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


# Troposphere branch accepted by this module, in geopotential metres: from the Z = -5000 m row of
# Table I (H = -5004 m') to the base H_b = 11 km' of the next layer in Table 4. A density
# altitude outside this interval is not a troposphere altitude, and the formula does not apply.
_LOWEST_ALTITUDE = -5004.0
_HIGHEST_ALTITUDE = 11000.0


def _evaluate(
    p: float,
    T: float,  # noqa: N803
    p0: float,
    T0: float,  # noqa: N803
    Gamma: float,  # noqa: N803
    g0: float,
    R: float,  # noqa: N803
) -> float:
    positive("p", p)
    positive("T", T)
    positive("p0", p0)
    positive("T0", T0)
    positive("Gamma", Gamma)
    positive("g0", g0)
    positive("R", R)
    n = g0 / (R * Gamma) - 1.0
    if n == 0:
        raise ValueError("g0 / (R * Gamma) must not equal 1; the density profile is then flat.")
    density_ratio = (p / p0) / (T / T0)
    altitude = finite_result(T0 / Gamma * (1.0 - density_ratio ** (1.0 / n)))
    if not _LOWEST_ALTITUDE <= altitude <= _HIGHEST_ALTITUDE:
        raise ValueError(
            f"the density altitude {altitude!r} m' lies outside the standard troposphere "
            f"({_LOWEST_ALTITUDE} to {_HIGHEST_ALTITUDE} m'), where this formula applies."
        )
    return altitude


density_altitude = FormulaSpec(
    id="aerodynamics.density_altitude",
    name="Density Altitude (Standard Troposphere)",
    equation="h_d = (T0 / Gamma) * (1 - ((p / p0) / (T / T0))^(1 / (g0 / (R * Gamma) - 1)))",
    description=(
        "Geopotential altitude in the standard troposphere at which the air density equals the "
        "density of the actual air, whose pressure p and temperature T are measured. The "
        "standard sea-level values and the lapse rate are supplied by the caller. The result is an "
        "altitude, not a density or a pressure altitude."
    ),
    inputs=(
        VariableSpec(
            name="p",
            symbol="p",
            description="Static pressure of the actual air",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="T",
            symbol="T",
            description="Static temperature of the actual air",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="p0",
            symbol="p_0",
            description="Standard sea-level pressure (101325 Pa in the standard atmosphere)",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="T0",
            symbol="T_0",
            description="Standard sea-level temperature (288.15 K in the standard atmosphere)",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="Gamma",
            symbol=r"\Gamma",
            description="Standard tropospheric lapse rate (0.0065 K/m in the standard atmosphere)",
            dimension="Theta L^-1",
            si_unit="K/m",
        ),
        VariableSpec(
            name="g0",
            symbol="g_0",
            description="Standard gravity (9.80665 m/s^2 in the standard atmosphere)",
            dimension="L T^-2",
            si_unit="m/s^2",
        ),
        VariableSpec(
            name="R",
            symbol="R",
            description="Specific gas constant of the air, R*/M0 (287.0531 J/(kg K) in the "
            "standard atmosphere)",
            dimension="L^2 T^-2 Theta^-1",
            si_unit="J/(kg K)",
        ),
    ),
    output=VariableSpec(
        name="h_d",
        symbol="h_d",
        description="Density altitude (geopotential)",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # Derived from the standard-troposphere relations: T = T0 - Gamma h (eq. (23) with
        # T_M = T below 80 km and L = -Gamma, Table 4), p = p0 (T/T0)^(g0/(R Gamma)) (eq. (33a)),
        # and rho = p / (R T) (eq. (42) with eq. (22)). Eliminating p and T gives
        # rho/rho0 = (T/T0)^(g0/(R Gamma) - 1) = (1 - Gamma h/T0)^(g0/(R Gamma) - 1); setting that
        # equal to the density ratio (p/p0)/(T/T0) of the actual air and solving for h gives the
        # shipped form.
        nasa_technical_report(
            "U.S. Standard Atmosphere, 1976",
            (),
            "NASA-TM-X-74335; NOAA-S/T-76-1562",
            1976,
            "https://ntrs.nasa.gov/citations/19770009539",
            "sec. 1.2.5, eqs. (22), (23), p. 9-10; sec. 1.3.1, eq. (33a), p. 12; sec. 1.3.4, "
            "eq. (42), p. 15; Table 4, p. 3 (b = 0: H_b = 0, L = -6.5 K/km', T_M,0 = 288.15 K); "
            "Table 10, p. 20; Table I, p. 51 (row Z = -5000 m, H = -5004 m')",
            organization=(
                "National Oceanic and Atmospheric Administration, National Aeronautics and "
                "Space Administration and U.S. Air Force"
            ),
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={
                "p": 101325.0,
                "T": 288.15,
                "p0": 101325.0,
                "T0": 288.15,
                "Gamma": 0.0065,
                "g0": 9.80665,
                "R": 287.0530720470647,
            },
            expected=-8.219357077538994e-13,
            rel_tol=1e-11,
            abs_tol=1e-09,
            note="Standard sea-level air gives zero; mpmath root-finding on the forward model.",
        ),
        VerificationCase(
            inputs={
                "p": 101325.0,
                "T": 303.15,
                "p0": 101325.0,
                "T0": 288.15,
                "Gamma": 0.0065,
                "g0": 9.80665,
                "R": 287.0530720470647,
            },
            expected=525.4557961194042,
            rel_tol=1e-11,
            abs_tol=1e-09,
            note="Hot day at standard sea-level pressure; mpmath root of the forward model.",
        ),
        VerificationCase(
            inputs={
                "p": 54048.0,
                "T": 255.676,
                "p0": 101325.0,
                "T0": 288.15,
                "Gamma": 0.0065,
                "g0": 9.80665,
                "R": 287.0530720470647,
            },
            expected=4996.13571767492,
            rel_tol=1e-11,
            abs_tol=1e-09,
            note=(
                "Standard-atmosphere state of Table I at a geometric 5000 m, which corresponds "
                "to about 4996 m'; mpmath root of the forward model."
            ),
        ),
        VerificationCase(
            inputs={
                "p": 70000.0,
                "T": 270.0,
                "p0": 101325.0,
                "T0": 288.15,
                "Gamma": 0.0065,
                "g0": 9.80665,
                "R": 287.0530720470647,
            },
            expected=3063.677290652884,
            rel_tol=1e-11,
            abs_tol=1e-09,
            note="Mixed state, 70 kPa and 270 K; mpmath root of the forward model.",
        ),
    ),
    assumptions=(
        "Derived result: in the standard troposphere T = T0 - Gamma h, p = p0 (T/T0)^(g0/(R "
        "Gamma)) and rho = p/(R T), so rho/rho0 = (T/T0)^(g0/(R Gamma) - 1); equating this to "
        "(p/p0)/(T/T0) of the actual air and solving for h gives the shipped form.",
        "The result is the altitude at which the standard-atmosphere density equals the actual "
        "density. It is meaningful only on the troposphere branch of the standard atmosphere, "
        "from -5004 m' (the Z = -5000 m row of the source's Table I, the lower limit accepted "
        "here) to the 11 km' base of the next layer in Table 4. A density altitude outside "
        "that interval raises ValueError, because the layer formula changes there.",
        "The actual air is an ideal gas with the same specific gas constant R as the standard air.",
        "The constants p0, T0, Gamma, g0 and R are inputs; only the altitude limits of the "
        "troposphere branch just described are fixed in the code. The 1976 Standard "
        "Atmosphere values are p0 = 101325 Pa, T0 = 288.15 K, Gamma = 6.5 K/km', g0 = 9.80665 "
        "m/s^2 and R = R*/M0 = 8.31432e3 / 28.9644 = 287.0531 J/(kg K).",
        "g0 / (R Gamma) = 1 is rejected, since the exponent is then undefined.",
    ),
    tags=("density altitude", "ISA", "atmosphere", "troposphere"),
)
