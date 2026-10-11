"""NASA 7-Coefficient Polynomial, Entropy: S/R = a1 ln T + a2 T + ... + a5 T^4/4 + a7."""

import math

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import nasa_rp_1311
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    a1: float,
    a2: float,
    a3: float,
    a4: float,
    a5: float,
    a7: float,
    T: float,  # noqa: N803
) -> float:
    for name, value in (("a1", a1), ("a2", a2), ("a3", a3), ("a4", a4), ("a5", a5), ("a7", a7)):
        finite(name, value)
    positive("T", T)
    poly = T * (a2 + T * (a3 / 2 + T * (a4 / 3 + T * (a5 / 4))))
    return finite_result(a1 * math.log(T) + poly + a7)


nasa7_entropy = FormulaSpec(
    id="thermodynamics.nasa7_entropy",
    name="NASA 7-Coefficient Polynomial: Entropy",
    equation="s_over_R = a1*ln(T) + a2*T + a3*T^2/2 + a4*T^3/3 + a5*T^4/4 + a7",
    description=(
        "Dimensionless standard-state molar entropy S/R from the NASA 7-coefficient form, "
        "including the entropy integration constant a7, evaluated with caller-supplied "
        "coefficients."
    ),
    inputs=(
        VariableSpec(
            name="a1",
            symbol="a_1",
            description="Constant coefficient of the heat-capacity polynomial (dimensionless)",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="a2",
            symbol="a_2",
            description="Coefficient of T in the heat-capacity polynomial",
            dimension="Theta^-1",
            si_unit="1/K",
        ),
        VariableSpec(
            name="a3",
            symbol="a_3",
            description="Coefficient of T^2 in the heat-capacity polynomial",
            dimension="Theta^-2",
            si_unit="1/K^2",
        ),
        VariableSpec(
            name="a4",
            symbol="a_4",
            description="Coefficient of T^3 in the heat-capacity polynomial",
            dimension="Theta^-3",
            si_unit="1/K^3",
        ),
        VariableSpec(
            name="a5",
            symbol="a_5",
            description="Coefficient of T^4 in the heat-capacity polynomial",
            dimension="Theta^-4",
            si_unit="1/K^4",
        ),
        VariableSpec(
            name="a7",
            symbol="a_7",
            description="Entropy integration constant (dimensionless)",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="T",
            symbol="T",
            description="Absolute temperature, inside the fit interval of the coefficient set",
            dimension="Theta",
            si_unit="K",
        ),
    ),
    output=VariableSpec(
        name="s_over_R",
        symbol=r"S^\circ / R",
        description="Standard-state molar entropy divided by R",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Stated up to index naming: RP-1311 numbers the coefficients a1 to a5 and a7 as used
        # here (eq. 4.8, the integral of cp/(R T) dT, with a6 belonging to the enthalpy);
        # libraries counting from zero map a0 to a1, and so on.
        nasa_rp_1311("eq. (4.6)-(4.8), p. 20 (PDF p. 26)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={
                "a1": 3.5,
                "a2": -0.0012,
                "a3": 2.5e-06,
                "a4": -1.8e-09,
                "a5": 4e-13,
                "a7": 3.2,
                "T": 300.0,
            },
            expected=22.900348661296704,
            rel_tol=1e-12,
            note=(
                "50-digit mpmath evaluation at 300 K; the coefficients are invented test "
                "numbers, not data for any species."
            ),
        ),
        VerificationCase(
            inputs={
                "a1": 2.9,
                "a2": 0.0015,
                "a3": -6e-07,
                "a4": 1.1e-10,
                "a5": -7.5e-15,
                "a7": 6.5,
                "T": 1000.0,
            },
            expected=27.767281975714866,
            rel_tol=1e-12,
            note="50-digit mpmath evaluation at 1000 K; invented test coefficients.",
        ),
        VerificationCase(
            inputs={
                "a1": 3.5,
                "a2": -0.0012,
                "a3": 2.5e-06,
                "a4": -1.8e-09,
                "a5": 4e-13,
                "a7": 3.2,
                "T": 200.0,
            },
            expected=21.549470782918128,
            rel_tol=1e-12,
            note="50-digit mpmath evaluation at 200 K; invented test coefficients.",
        ),
    ),
    assumptions=(
        "Use the same coefficient set, for the same species and temperature interval, as for "
        "the heat-capacity polynomial; a1 to a5 are the same coefficients and a7 is the "
        "entropy integration constant of that interval. No coefficient set is shipped here.",
        "Coefficient sets are fitted over a stated temperature interval (RP-1311 gas fits "
        "cover 200-1000 K and 1000-6000 K, one set each). The evaluator cannot check that T "
        "lies in the interval of the set supplied: outside it the result is not characterised "
        "and must not be used.",
        "Ideal-gas standard-state property. The logarithm takes the numeric value of T in "
        "kelvin, and a7 absorbs that choice and the standard-state pressure convention of the "
        "data set, so the relation holds only for T in kelvin with coefficients whose pressure "
        "convention matches the one the entropy is used with.",
        "T must be positive and finite and each coefficient finite, otherwise ValueError is "
        "raised.",
    ),
    tags=("NASA polynomials", "entropy", "thermodynamic data", "ideal gas", "NASA"),
)
