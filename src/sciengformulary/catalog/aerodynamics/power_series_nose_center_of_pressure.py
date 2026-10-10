"""Center of Pressure of a Power-Series Nose: x_cp = L * 2 * n / (2 * n + 1)."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(L: float, n: float) -> float:  # noqa: N803
    positive("L", L)
    positive("n", n)
    return finite_result(L * 2.0 * n / (2.0 * n + 1.0))


power_series_nose_center_of_pressure = FormulaSpec(
    id="aerodynamics.power_series_nose_center_of_pressure",
    name="Center of Pressure of a Power-Series Nose",
    equation="x_cp = L * 2 * n / (2 * n + 1)",
    description=(
        "Center-of-pressure position, measured from the nose tip, of a pointed nose whose "
        "radius grows as the n-th power of the axial coordinate (n = 1 is a cone, "
        "n = 1/2 a parabola), in Barrowman's method."
    ),
    inputs=(
        VariableSpec(
            name="L",
            symbol="L",
            description="Length of the nose",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="n",
            symbol="n",
            description="Power-series exponent of the radius profile r = R (x / L)^n",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="x_cp",
        symbol="x_cp",
        description="Center-of-pressure position measured aft from the nose tip",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # Derived: eq. (3-89) gives X_B = l_0 - V_B / A_B for a body with zero area at its
        # tip. For A(x) = A_B (x / L)^(2n) the volume is V_B = A_B L / (2n + 1), so
        # x_cp = L (1 - 1/(2n + 1)) = 2 n L / (2n + 1). Symbols: l_0 -> L.
        nasa_technical_report(
            "The Practical Calculation of the Aerodynamic Characteristics of Slender Finned "
            "Vehicles",
            ("J. S. Barrowman",),
            "NASA/TM-2001-209983",
            1967,
            "https://ntrs.nasa.gov/citations/20010047838",
            "sec. 3.22, eq. (3-89), p. 29",
            organization=(
                "NASA Goddard Space Flight Center (reissue of a March 1967 Catholic "
                "University of America master's dissertation)"
            ),
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"L": 1.0, "n": 1.0},
            expected=0.6666666666666666,
            rel_tol=1e-11,
            note="Cone, center of pressure at 2L/3; mpmath quadrature of the volume in (3-89).",
        ),
        VerificationCase(
            inputs={"L": 0.4, "n": 0.75},
            expected=0.24000000000000002,
            rel_tol=1e-11,
            note="Exponent 3/4; mpmath quadrature of the volume in eq. (3-89).",
        ),
        VerificationCase(
            inputs={"L": 2.0, "n": 0.5},
            expected=1.0,
            rel_tol=1e-11,
            note="Parabolic nose (n = 1/2), center of pressure at L/2; mpmath quadrature.",
        ),
        VerificationCase(
            inputs={"L": 1.0, "n": 0.001},
            expected=0.001996007984031936,
            rel_tol=1e-11,
            note="Boundary case: exponent near zero puts the center of pressure near the tip.",
        ),
    ),
    assumptions=(
        "Derived result: for A(x) = A_B (x / L)^(2n) the volume is V = A_B L / (2n + 1), and "
        "eq. (3-89), X = l_0 - V / A_B, gives x_cp = L (1 - 1/(2n + 1)) = 2 n L / (2n + 1); "
        "n = 1 gives 2L/3 for a cone.",
        "Barrowman's method: slender-body and thin-airfoil theory, small angle of attack and "
        "a sharp nose tip (source sec. 2.4), in subsonic flow. The nose has zero area at its "
        "tip, A(0) = 0.",
        "Length convention: x_cp is measured aft from the nose tip along the axis; the exponent "
        "n is positive, with typical rocket noses in 0 < n <= 1; any consistent length unit.",
    ),
    tags=("nose", "center of pressure", "power series", "Barrowman", "slender body"),
)
