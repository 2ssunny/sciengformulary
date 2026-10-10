"""Sutherland Dynamic Viscosity: mu = beta * T^(3/2) / (T + S)."""

import math

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(T: float, beta: float, S: float) -> float:  # noqa: N803
    positive("T", T)
    positive("beta", beta)
    positive("S", S)
    return finite_result(beta * T * math.sqrt(T) / (T + S))


sutherland_viscosity_air = FormulaSpec(
    id="fluids.sutherland_viscosity_air",
    name="Sutherland Dynamic Viscosity of Air",
    equation="mu = beta * T^(3/2) / (T + S)",
    description=(
        "Dynamic viscosity of a gas as a function of absolute temperature from Sutherland's "
        "two-constant form, with the constants supplied by the caller (for air in the standard "
        "atmosphere beta = 1.458e-6 kg/(s m K^0.5) and S = 110.4 K). It gives mu only; divide "
        "by density, as in fluids.kinematic_viscosity, to obtain the kinematic viscosity."
    ),
    inputs=(
        VariableSpec(
            name="T",
            symbol="T",
            description="Absolute temperature",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="beta",
            symbol=r"\beta",
            description="Sutherland coefficient (1.458e-6 kg/(s m K^0.5) for air)",
            dimension="M L^-1 T^-1 Theta^-1/2",
            si_unit="kg/(s m K^0.5)",
        ),
        VariableSpec(
            name="S",
            symbol="S",
            description="Sutherland constant (110.4 K for air)",
            dimension="Theta",
            si_unit="K",
        ),
    ),
    output=VariableSpec(
        name="mu",
        symbol=r"\mu",
        description="Dynamic viscosity",
        dimension="M L^-1 T^-1",
        si_unit="Pa s",
    ),
    evaluator=_evaluate,
    references=(
        # Stated: eq. (51), mu = beta T^(3/2) / (T + S), with beta = 1.458e-6 kg/(s m K^0.5) and
        # S = 110.4 K for air; T is the kinetic temperature, equal to the molecular-scale
        # temperature below 80 km. The source is inconsistent about S: Table 2B (p. 2) and the
        # Category II text (p. 4) print S = 110 K, while the text of eq. (51) (p. 19) prints
        # 110.4 K. The value 110.4 K is used because it reproduces the sea-level viscosity
        # mu0 = 1.7894e-5 kg/(m s) printed in Table 10 (p. 20); S = 110 K would give 1.7912e-5.
        nasa_technical_report(
            "U.S. Standard Atmosphere, 1976",
            (),
            "NASA-TM-X-74335; NOAA-S/T-76-1562",
            1976,
            "https://ntrs.nasa.gov/citations/19770009539",
            "sec. 1.3.11, eq. (51), p. 19; Table 2B (constants, p. 2) and p. 4 (S = 110 K, "
            "see comment above); Table 10 (sea-level mu0), p. 20",
            organization=(
                "National Oceanic and Atmospheric Administration, National Aeronautics and "
                "Space Administration and U.S. Air Force"
            ),
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"T": 288.15, "beta": 1.458e-06, "S": 110.4},
            expected=1.7893802780775828e-05,
            rel_tol=1e-12,
            note="Standard sea-level temperature; 50-digit mpmath evaluation.",
        ),
        VerificationCase(
            inputs={"T": 216.65, "beta": 1.458e-06, "S": 110.4},
            expected=1.4216130796413358e-05,
            rel_tol=1e-12,
            note="Tropopause temperature; 50-digit mpmath evaluation.",
        ),
        VerificationCase(
            inputs={"T": 180.65, "beta": 1.458e-06, "S": 110.4},
            expected=1.2163172589607777e-05,
            rel_tol=1e-12,
            note="Cold case at 180.65 K; 50-digit mpmath evaluation.",
        ),
        VerificationCase(
            inputs={"T": 288.15, "beta": 1.458e-06, "S": 110.4},
            expected=1.7894e-05,
            rel_tol=0.0001,
            note=(
                "Table 10 of the reference prints a sea-level viscosity of 1.7894e-5 kg/(m s); "
                "the tolerance covers its five printed digits."
            ),
        ),
    ),
    assumptions=(
        "Empirical relation whose two constants are fitted to measurements. For air the "
        "source gives beta = 1.458e-6 kg/(s m K^0.5) and S = 110.4 K in the text of eq. (51); "
        "they are inputs and are not built in. The source is not consistent about S: its "
        "Table 2B and p. 4 print 110 K. Only 110.4 K reproduces its Table 10 value of mu0, "
        "so that is the value recommended here.",
        "The source states that the expression fails at very high and very low temperatures "
        "and uses it only up to 86 km. No numeric temperature limit is stated, so none is "
        "enforced here.",
        "Units: beta carries K^-1/2. With T in kelvin, beta in kg/(s m K^0.5) and S in kelvin "
        "the result is in kg/(m s) = Pa s.",
    ),
    tags=("viscosity", "Sutherland", "air", "standard atmosphere"),
)
