"""NASA 9-Coefficient Polynomial, Heat Capacity: cp/R = a1/T^2 + a2/T + a3 + a4 T + ... + a7 T^4."""

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
    a7: float,
    T: float,  # noqa: N803
) -> float:
    for name, value in (
        ("a1", a1),
        ("a2", a2),
        ("a3", a3),
        ("a4", a4),
        ("a5", a5),
        ("a6", a6),
        ("a7", a7),
    ):
        finite(name, value)
    positive("T", T)
    inverse_t = 1.0 / T
    low = (a1 * inverse_t + a2) * inverse_t
    high = T * (a4 + T * (a5 + T * (a6 + T * a7)))
    return finite_result(low + a3 + high)


nasa9_heat_capacity = FormulaSpec(
    id="thermodynamics.nasa9_heat_capacity",
    name="NASA 9-Coefficient Polynomial: Heat Capacity",
    equation="cp_over_R = a1/T^2 + a2/T + a3 + a4*T + a5*T^2 + a6*T^3 + a7*T^4",
    description=(
        "Dimensionless ideal-gas heat capacity cp/R from the seven heat-capacity terms of the "
        "NASA 9-coefficient form (called the new form in RP-1311; its two further "
        "coefficients are integration constants for enthalpy and entropy), evaluated with "
        "caller-supplied coefficients."
    ),
    inputs=(
        VariableSpec(
            name="a1",
            symbol="a_1",
            description="Coefficient of T^-2",
            dimension="Theta^2",
            si_unit="K^2",
        ),
        VariableSpec(
            name="a2",
            symbol="a_2",
            description="Coefficient of T^-1",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="a3",
            symbol="a_3",
            description="Constant term (dimensionless)",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="a4",
            symbol="a_4",
            description="Coefficient of T",
            dimension="Theta^-1",
            si_unit="1/K",
        ),
        VariableSpec(
            name="a5",
            symbol="a_5",
            description="Coefficient of T^2",
            dimension="Theta^-2",
            si_unit="1/K^2",
        ),
        VariableSpec(
            name="a6",
            symbol="a_6",
            description="Coefficient of T^3",
            dimension="Theta^-3",
            si_unit="1/K^3",
        ),
        VariableSpec(
            name="a7",
            symbol="a_7",
            description="Coefficient of T^4",
            dimension="Theta^-4",
            si_unit="1/K^4",
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
        name="cp_over_R",
        symbol=r"c_p^\circ / R",
        description="Standard-state molar heat capacity at constant pressure divided by R",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Stated up to index naming: RP-1311 numbers the seven heat-capacity coefficients a1 to
        # a7 (eq. 4.9) as used here; libraries counting from zero map a0 to a1, and so on. The
        # id says "9-coefficient" because the full set adds the enthalpy and entropy constants
        # (a8, a9), which this heat-capacity relation does not use.
        nasa_rp_1311("eq. (4.9), p. 20 (PDF p. 26)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={
                "a1": 100000.0,
                "a2": -1500.0,
                "a3": 4.2,
                "a4": -0.002,
                "a5": 1.4e-06,
                "a6": -3e-10,
                "a7": 2e-14,
                "T": 500.0,
            },
            expected=0.91375,
            rel_tol=1e-12,
            note=(
                "Exact rational evaluation at 500 K; the coefficients are invented test "
                "numbers, not data for any species."
            ),
        ),
        VerificationCase(
            inputs={
                "a1": -50000.0,
                "a2": 800.0,
                "a3": 3.0,
                "a4": 0.001,
                "a5": -4e-07,
                "a6": 9e-11,
                "a7": -6e-15,
                "T": 1000.0,
            },
            expected=4.434,
            rel_tol=1e-12,
            note="Exact rational evaluation at 1000 K; invented test coefficients.",
        ),
        VerificationCase(
            inputs={
                "a1": 100000.0,
                "a2": -1500.0,
                "a3": 4.2,
                "a4": -0.002,
                "a5": 1.4e-06,
                "a6": -3e-10,
                "a7": 2e-14,
                "T": 200.0,
            },
            expected=-1.146368,
            rel_tol=1e-12,
            note="Exact rational evaluation at 200 K; invented test coefficients.",
        ),
    ),
    assumptions=(
        "The coefficients are data for one species and one temperature interval (RP-1311 gas "
        "fits cover 200-1000 K and 1000-6000 K, and 6000-20000 K for some gases, one set per "
        "interval); no coefficient set is shipped here. The evaluator cannot check that T lies "
        "inside the interval of the set supplied: outside it the polynomial is not "
        "characterised and the result must not be used.",
        "Ideal-gas standard-state property; it does not depend on pressure.",
        "Coefficient units follow from a dimensionless cp/R: a_k carries K^(3-k) with T in "
        "kelvin, so the coefficients are valid only for T in kelvin.",
        "T must be positive and finite and each coefficient finite, otherwise ValueError is "
        "raised.",
    ),
    tags=("NASA polynomials", "heat capacity", "thermodynamic data", "ideal gas", "NASA"),
)
