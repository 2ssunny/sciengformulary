"""NASA 7-Coefficient Polynomial, Enthalpy: H/(RT) = a1 + a2 T/2 + ... + a5 T^4/5 + a6/T."""

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import nasa_rp_1311
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    a1: float,
    a2: float,
    a3: float,
    a4: float,
    a5: float,
    a6: float,
    T: float,  # noqa: N803
) -> float:
    for name, value in (("a1", a1), ("a2", a2), ("a3", a3), ("a4", a4), ("a5", a5), ("a6", a6)):
        finite(name, value)
    positive("T", T)
    poly = a1 + T * (a2 / 2 + T * (a3 / 3 + T * (a4 / 4 + T * (a5 / 5))))
    return finite_result(poly + a6 / T)


nasa7_enthalpy = FormulaSpec(
    id="thermodynamics.nasa7_enthalpy",
    name="NASA 7-Coefficient Polynomial: Enthalpy",
    equation="h_over_RT = a1 + a2*T/2 + a3*T^2/3 + a4*T^3/4 + a5*T^4/5 + a6/T",
    description=(
        "Dimensionless standard-state molar enthalpy H/(RT) from the NASA 7-coefficient form, "
        "including the enthalpy integration constant a6, evaluated with caller-supplied "
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
            name="a6",
            symbol="a_6",
            description="Enthalpy integration constant (an enthalpy divided by R)",
            dimension="Theta",
            si_unit="K",
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
        name="h_over_RT",
        symbol=r"H^\circ / (R T)",
        description="Standard-state molar enthalpy divided by R T",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Stated up to index naming: RP-1311 numbers the coefficients a1 to a6 as used here
        # (eq. 4.7, the integral of cp/R dT divided by T); libraries counting from zero map
        # a0 to a1, and so on.
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
                "a6": -1050.0,
                "T": 300.0,
            },
            expected=-0.116502,
            rel_tol=1e-12,
            note=(
                "Exact rational evaluation at 300 K; the coefficients are invented test "
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
                "a6": -9000.0,
                "T": 1000.0,
            },
            expected=-5.524,
            rel_tol=1e-12,
            note="Exact rational evaluation at 1000 K; invented test coefficients.",
        ),
        VerificationCase(
            inputs={
                "a1": 3.5,
                "a2": -0.0012,
                "a3": 2.5e-06,
                "a4": -1.8e-09,
                "a5": 4e-13,
                "a6": -1050.0,
                "T": 200.0,
            },
            expected=-1.8401386666666666,
            rel_tol=1e-12,
            note="Exact rational evaluation at 200 K; invented test coefficients.",
        ),
    ),
    assumptions=(
        "Use the same coefficient set, for the same species and temperature interval, as for "
        "the heat-capacity polynomial; a1 to a5 are the same coefficients and a6 is the "
        "enthalpy integration constant of that interval. No coefficient set is shipped here.",
        "Coefficient sets are fitted over a stated temperature interval (RP-1311 gas fits "
        "cover 200-1000 K and 1000-6000 K, one set each). The evaluator cannot check that T "
        "lies in the interval of the set supplied: outside it the result is not characterised "
        "and must not be used.",
        "Ideal-gas standard-state property. Coefficient units hold only for T in kelvin: a_k "
        "carries K^-(k-1) for k = 1..5 and a6 carries K.",
        "T must be positive and finite and each coefficient finite, otherwise ValueError is "
        "raised.",
    ),
    tags=("NASA polynomials", "enthalpy", "thermodynamic data", "ideal gas", "NASA"),
)
