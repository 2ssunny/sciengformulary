"""Center of Pressure of a Slender Body from its Volume: x_cp = L - V / A_base."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(L: float, V: float, A_base: float) -> float:  # noqa: N803
    positive("L", L)
    non_negative("V", V)
    positive("A_base", A_base)
    return finite_result(L - V / A_base)


slender_body_center_of_pressure_from_volume = FormulaSpec(
    id="aerodynamics.slender_body_center_of_pressure_from_volume",
    name="Center of Pressure of a Slender Body from its Volume",
    equation="x_cp = L - V / A_base",
    description=(
        "Center-of-pressure position of a slender pointed body in subsonic flow, from its "
        "length, volume and base area, measured from the nose tip, as used in Barrowman's "
        "method."
    ),
    inputs=(
        VariableSpec(
            name="L",
            symbol="L",
            description="Body length",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="V",
            symbol="V",
            description="Body volume",
            dimension="L^3",
            si_unit="m^3",
        ),
        VariableSpec(
            name="A_base",
            symbol="A_B",
            description="Base area of the body",
            dimension="L^2",
            si_unit="m^2",
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
        # Stated: eq. (3-89) prints X_B = l_0 - V_B / A_B for a body whose area is zero at
        # its tip. Symbols: l_0 -> L, V_B -> V, A_B -> A_base.
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
            inputs={"L": 1.0, "V": 0.2617993877991493, "A_base": 0.785398163397448},
            expected=0.6666666666666667,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Cone with V = A L / 3, center of pressure at 2L/3; exact arithmetic.",
        ),
        VerificationCase(
            inputs={"L": 2.0, "V": 0.75, "A_base": 0.75},
            expected=1.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Volume A L / 2 (parabolic body), center of pressure at L/2; exact arithmetic.",
        ),
        VerificationCase(
            inputs={"L": 1.0, "V": 0.2, "A_base": 0.2},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Boundary case: volume A L (cylinder) puts the center of pressure at the tip.",
        ),
    ),
    assumptions=(
        "Barrowman's method: slender-body and thin-airfoil theory, small angle of attack and "
        "a sharp nose tip (source sec. 2.4), in subsonic flow. The body has zero area at its "
        "tip, A(0) = 0; the supersonic body center of pressure uses a different integral "
        "(eq. 3-92) and is not included.",
        "Length convention: x_cp is measured aft from the nose tip along the axis, L is the "
        "body length and A_base is the cross-section area at its aft end; V is not negative "
        "and A_base is positive; any consistent unit system.",
    ),
    tags=("center of pressure", "slender body", "volume", "Barrowman", "rocket aerodynamics"),
)
