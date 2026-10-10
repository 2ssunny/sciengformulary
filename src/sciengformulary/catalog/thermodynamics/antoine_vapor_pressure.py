"""Antoine Vapor Pressure Equation: p_sat = 10^(A - B / (T + C)), log10, bar, kelvin."""

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, ReferenceSpec, VariableSpec, VerificationCase


def _evaluate(
    A: float,  # noqa: N803
    B: float,  # noqa: N803
    C: float,  # noqa: N803
    T: float,  # noqa: N803
) -> float:
    finite("A", A)
    finite("B", B)
    finite("C", C)
    positive("T", T)
    denominator = T + C
    if denominator <= 0:
        raise ValueError(f"T + C must be positive, got T={T!r} and C={C!r}.")
    exponent = A - B / denominator
    try:
        pressure = 10.0**exponent
    except OverflowError:
        raise OverflowError(
            f"the result is outside the floating-point range (log10 p = {exponent!r})."
        ) from None
    if pressure == 0.0:
        raise ValueError(f"The vapor pressure underflows to zero (log10 p = {exponent!r}).")
    return finite_result(pressure)


antoine_vapor_pressure = FormulaSpec(
    id="thermodynamics.antoine_vapor_pressure",
    name="Antoine Vapor Pressure Equation",
    equation="p_sat = 10^(A - B / (T + C))",
    description=(
        "Empirical correlation of the saturation vapor pressure of a pure substance with "
        "absolute temperature, using three fitted constants (base-10 logarithm, pressure in "
        "bar and temperature in kelvin for the NIST WebBook form)."
    ),
    inputs=(
        VariableSpec(
            name="A",
            symbol="A",
            description="Antoine constant, dimensionless; fixes the pressure unit of the result",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="B",
            symbol="B",
            description="Antoine constant with temperature units (kelvin)",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="C",
            symbol="C",
            description="Antoine constant with temperature units (kelvin); often negative",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="T",
            symbol="T",
            description=(
                "Absolute temperature, which must lie inside the fitted interval of the "
                "coefficient set"
            ),
            dimension="Theta",
            si_unit="K",
        ),
    ),
    output=VariableSpec(
        name="p_sat",
        symbol=r"p_{sat}",
        description=(
            "Saturation vapor pressure, in the pressure unit the coefficient set was fitted to "
            "(bar for the NIST WebBook sets)"
        ),
        dimension="M L^-1 T^-2",
        si_unit="bar",
    ),
    evaluator=_evaluate,
    references=(
        # The WebBook prints the form log10(P) = A - B / (T + C) with P in bar and T in kelvin,
        # and lists coefficient sets, each with its own temperature interval. Only the form and
        # units are used here; no coefficient values are taken from the page.
        ReferenceSpec(
            source_type="official_web",
            title="NIST Chemistry WebBook, NIST Standard Reference Database Number 69",
            organization="National Institute of Standards and Technology",
            url="https://webbook.nist.gov/cgi/cbook.cgi?ID=C7732185&Mask=4",
            accessed=ENGINEERING_ACCESSED,
            locator="'Phase change data', block 'Antoine Equation Parameters'",
        ),
        # Lienhard writes the same correlation with the natural logarithm,
        # ln p = A - B / (C + T), and names it the Antoine equation in footnote 8, saying that
        # it also applies to the vapor pressure of liquids. Converting to base 10 divides A and
        # B by ln 10 (A_10 = A_ln / ln 10, B_10 = B_ln / ln 10); C is unchanged.
        lienhard_heat_transfer(
            "eq. (11.49), p. 645; fn. 8, p. 646",
            accessed=ENGINEERING_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"A": 5.0, "B": 1700.0, "C": -40.0, "T": 350.0},
            expected=0.3281927872511474,
            rel_tol=1e-12,
            note=(
                "Synthetic coefficients (not a real substance): 10^(5 - 1700 / 310); value from "
                "50-digit mpmath arithmetic."
            ),
        ),
        VerificationCase(
            inputs={"A": 5.0, "B": 1000.0, "C": -50.0, "T": 250.0},
            expected=1.0,
            rel_tol=1e-12,
            note="Hand calculation: B / (T + C) = 1000 / 200 = 5 = A, so log10 p = 0 and p = 1.",
        ),
        VerificationCase(
            inputs={"A": 4.2, "B": 1200.0, "C": 35.0, "T": 300.0},
            expected=4.148684872471824,
            rel_tol=1e-12,
            note="Synthetic coefficients with C > 0: 10^(4.2 - 1200 / 335); 50-digit mpmath value.",
        ),
    ),
    assumptions=(
        "Unit convention: base-10 logarithm, T in kelvin, B and C in kelvin, and p in bar for "
        "coefficient sets taken from the NIST Chemistry WebBook. A set from another source may "
        "use the natural logarithm or another pressure unit and must be converted first "
        "(A_ln = A_10 * ln 10, B_ln = B_10 * ln 10, C unchanged), or the result is in that "
        "set's own pressure unit.",
        "Coefficient sets are data with their own stated temperature ranges: each (A, B, C) set "
        "is valid only inside the interval it was fitted over, and the evaluator cannot check "
        "that interval, so extrapolation is the caller's responsibility. This item supplies no "
        "coefficient data.",
        "The equation is an empirical fit, not a thermodynamic law. The constant C = 0 case "
        "follows from the Clausius-Clapeyron equation for an enthalpy of phase change that "
        "does not vary with temperature.",
        "A, B and C must be finite, T finite and positive, and T + C positive (T + C = 0 is "
        "the pole of the equation, and T + C < 0 lies on its unphysical side, where the "
        "result is meaningless); otherwise ValueError is raised. A result that exceeds the "
        "floating-point range raises OverflowError, and one that underflows to zero raises "
        "ValueError.",
        "The output si_unit is listed as bar because the coefficient convention fixes the "
        "unit: A, B and C are unit-specific fitted constants, and the NIST WebBook sets give "
        "p in bar for T in kelvin. The evaluator does no unit conversion, so a set fitted to "
        "another pressure unit (Pa, kPa, mmHg) returns the result in that unit, and the "
        "caller must convert.",
        "Not dimensionally homogeneous in the usual sense: A is dimensionless, B and C carry "
        "temperature units, and the pressure unit is fixed by the coefficient set.",
    ),
    tags=("Antoine equation", "vapor pressure", "saturation pressure", "empirical"),
)
