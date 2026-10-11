"""NASA 7-Coefficient Polynomial, Heat Capacity: cp/R = a1 + a2 T + a3 T^2 + a4 T^3 + a5 T^4."""

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import nasa_rp_1311
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    a1: float,
    a2: float,
    a3: float,
    a4: float,
    a5: float,
    T: float,  # noqa: N803
) -> float:
    for name, value in (("a1", a1), ("a2", a2), ("a3", a3), ("a4", a4), ("a5", a5)):
        finite(name, value)
    positive("T", T)
    return finite_result((((a5 * T + a4) * T + a3) * T + a2) * T + a1)


nasa7_heat_capacity = FormulaSpec(
    id="thermodynamics.nasa7_heat_capacity",
    name="NASA 7-Coefficient Polynomial: Heat Capacity",
    equation="cp_over_R = a1 + a2*T + a3*T^2 + a4*T^3 + a5*T^4",
    description=(
        "Dimensionless ideal-gas heat capacity cp/R from the fourth-order polynomial of the "
        "NASA 7-coefficient form (called the old form in RP-1311), evaluated with caller-supplied "
        "coefficients."
    ),
    inputs=(
        VariableSpec(
            name="a1",
            symbol="a_1",
            description="Constant coefficient of the polynomial (dimensionless)",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="a2",
            symbol="a_2",
            description="Coefficient of T",
            dimension="Theta^-1",
            si_unit="1/K",
        ),
        VariableSpec(
            name="a3",
            symbol="a_3",
            description="Coefficient of T^2",
            dimension="Theta^-2",
            si_unit="1/K^2",
        ),
        VariableSpec(
            name="a4",
            symbol="a_4",
            description="Coefficient of T^3",
            dimension="Theta^-3",
            si_unit="1/K^3",
        ),
        VariableSpec(
            name="a5",
            symbol="a_5",
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
        # Stated up to index naming: RP-1311 numbers the coefficients a1 to a5 (eq. 4.6) as used
        # here; libraries that count from zero (a0 to a4) map a0 to a1, and so on.
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
                "T": 300.0,
            },
            expected=3.31964,
            rel_tol=1e-12,
            note=(
                "Exact rational evaluation of the polynomial at 300 K; the coefficients are "
                "invented test numbers, not data for any species."
            ),
        ),
        VerificationCase(
            inputs={
                "a1": 2.9,
                "a2": 0.0015,
                "a3": -6e-07,
                "a4": 1.1e-10,
                "a5": -7.5e-15,
                "T": 1000.0,
            },
            expected=3.9025,
            rel_tol=1e-12,
            note=(
                "Exact rational evaluation at 1000 K, the joint of the two usual gas intervals; "
                "invented test coefficients."
            ),
        ),
        VerificationCase(
            inputs={
                "a1": 3.5,
                "a2": -0.0012,
                "a3": 2.5e-06,
                "a4": -1.8e-09,
                "a5": 4e-13,
                "T": 200.0,
            },
            expected=3.34624,
            rel_tol=1e-12,
            note=(
                "Exact rational evaluation at 200 K, the lower edge of the usual gas interval; "
                "invented test coefficients."
            ),
        ),
    ),
    assumptions=(
        "The coefficients are data for one species and one temperature interval (RP-1311 gas "
        "fits cover 200-1000 K and 1000-6000 K, with a separate coefficient set for each); no "
        "coefficient set is shipped here. The evaluator cannot check that T lies inside the "
        "interval of the set supplied: outside it the polynomial is not characterised and the "
        "result must not be used.",
        "Ideal-gas standard-state property; it does not depend on pressure.",
        "Coefficient units follow from a dimensionless cp/R: a_k carries K^-(k-1) with T in "
        "kelvin, so the coefficients are valid only for T in kelvin.",
        "T must be positive and finite and each coefficient finite, otherwise ValueError is "
        "raised.",
    ),
    tags=("NASA polynomials", "heat capacity", "thermodynamic data", "ideal gas", "NASA"),
)
