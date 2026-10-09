"""Wind Speed Power-Law Profile: U = U_ref * (z / z_ref)^alpha."""

import math

from sciengformulary.catalog._domain import finite, finite_result, non_negative, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(U_ref: float, z: float, z_ref: float, alpha: float) -> float:  # noqa: N803
    # alpha is empirical and site dependent, so any finite real exponent is accepted.
    non_negative("U_ref", U_ref)
    positive("z", z)
    positive("z_ref", z_ref)
    finite("alpha", alpha)
    # Powers of the height ratio are taken through logarithms, so that a ratio beyond the float
    # range (with a small exponent) neither overflows nor underflows spuriously.
    return finite_result(U_ref * math.exp(alpha * (math.log(z) - math.log(z_ref))))


wind_shear_power_law = FormulaSpec(
    id="fluids.wind_shear_power_law",
    name="Wind Speed Power-Law Profile",
    equation="U = U_ref * (z / z_ref)^alpha",
    description=(
        "Steady mean wind speed at height z over level terrain, extrapolated from the speed at "
        "a reference height with a power law whose exponent is determined from measurements. "
        "It describes the vertical wind profile of the atmospheric boundary layer; it is not a "
        "pipe or channel velocity profile such as fluids.manning_velocity."
    ),
    inputs=(
        VariableSpec(
            name="U_ref",
            symbol="V_1",
            description="Wind speed at the reference height",
            dimension="L T^-1",
            si_unit="m/s",
        ),
        VariableSpec(
            name="z",
            symbol="z_2",
            description="Height at which the wind speed is wanted",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="z_ref",
            symbol="z_1",
            description="Reference height of the known wind speed",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="alpha",
            symbol=r"\alpha",
            description="Power-law exponent (empirical; 1/7 is the classical value)",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="U",
        symbol="V_2",
        description="Wind speed at height z",
        dimension="L T^-1",
        si_unit="m/s",
    ),
    evaluator=_evaluate,
    references=(
        # Stated: V_2 = V_1 * (z_2 / z_1)^alpha for simultaneous steady winds over level
        # terrain; the report notes that alpha is found experimentally and quotes 1/7 for
        # certain conditions. Symbols: V_1 -> U_ref, V_2 -> U, z_1 -> z_ref, z_2 -> z.
        nasa_technical_report(
            "Modified Power Law Equations for Vertical Wind Profiles",
            ("D. A. Spera", "T. R. Richards"),
            "NASA TM-79275; DOE/NASA/1059-79/4",
            1979,
            "https://ntrs.nasa.gov/citations/19800005367",
            "Introduction, eq. (1) (p. 1 of the paper)",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"U_ref": 8.0, "z": 100.0, "z_ref": 10.0, "alpha": 0.14285714285714285},
            expected=11.115963954985101,
            rel_tol=1e-12,
            note="50-digit mpmath evaluation of 8 * 10^(1/7), the 1/7 law from 10 m to 100 m.",
        ),
        VerificationCase(
            inputs={"U_ref": 6.5, "z": 80.0, "z_ref": 50.0, "alpha": 0.2},
            expected=7.140643531489766,
            rel_tol=1e-12,
            note="50-digit mpmath evaluation of 6.5 * 1.6^0.2.",
        ),
        VerificationCase(
            inputs={"U_ref": 7.0, "z": 10.0, "z_ref": 10.0, "alpha": 0.14},
            expected=7.0,
            rel_tol=1e-12,
            note="Edge case: at the reference height the speed equals the reference speed.",
        ),
    ),
    assumptions=(
        "Empirical: the exponent depends on height, time of day, season, terrain, wind speed "
        "and temperature, and must be supplied from data; it is not restricted to a typical "
        "range here.",
        "Simultaneous, steady (non-gusting) mean winds over level terrain; the law is an "
        "interpolation or extrapolation between heights, with no stated range of validity "
        "in height.",
        "z and z_ref must be positive and in the same length unit; U_ref must not be negative.",
    ),
    tags=("wind profile", "wind shear", "power law", "atmospheric boundary layer", "wind"),
)
