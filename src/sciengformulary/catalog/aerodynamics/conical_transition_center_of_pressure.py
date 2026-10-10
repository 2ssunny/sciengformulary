"""Center of Pressure of a Conical Transition, from Barrowman's method."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(L: float, r_fwd: float, r_aft: float) -> float:  # noqa: N803
    positive("L", L)
    non_negative("r_fwd", r_fwd)
    non_negative("r_aft", r_aft)
    if r_fwd + r_aft == 0:
        raise ValueError("r_fwd and r_aft must not both be zero.")
    if r_fwd == r_aft:
        raise ValueError("r_fwd must differ from r_aft: a cylinder has no normal force.")
    # Divide before multiplying: (L / 3) * (numerator) would underflow for tiny L and radii.
    return finite_result((L / 3.0) * ((2.0 * r_aft + r_fwd) / (r_aft + r_fwd)))


conical_transition_center_of_pressure = FormulaSpec(
    id="aerodynamics.conical_transition_center_of_pressure",
    name="Center of Pressure of a Conical Transition",
    equation="x_cp = (L / 3) * (2 * r_aft + r_fwd) / (r_aft + r_fwd)",
    description=(
        "Position, measured aft from the front of a conical frustum, of the center of "
        "pressure of its slender-body normal force in Barrowman's method. Add the distance "
        "from the nose tip to the front of the transition to get the position from the nose."
    ),
    inputs=(
        VariableSpec(
            name="L",
            symbol="L",
            description="Axial length of the transition",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="r_fwd",
            symbol="r_fwd",
            description="Radius at the forward end of the transition",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="r_aft",
            symbol="r_aft",
            description="Radius at the aft end of the transition",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="x_cp",
        symbol="x_cp",
        description="Center-of-pressure position measured aft from the front of the transition",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # Derived: eqs. (3-77) to (3-88) with (3-65) give the body center of pressure as
        # (l_0 A(l_0) - V_B) / (A(l_0) - A(0)). For a frustum A(x) = pi (r_fwd + (r_aft - r_fwd)
        # x / L)^2 and V_B = (pi L / 3)(r_fwd^2 + r_fwd r_aft + r_aft^2), which the source
        # calls well known but does not print; the quotient simplifies to the form above, equal
        # to (L / 3)(1 + (1 - r)/(1 - r^2)) with r = r_fwd / r_aft. Symbols: l_0 -> L.
        nasa_technical_report(
            "The Practical Calculation of the Aerodynamic Characteristics of Slender Finned "
            "Vehicles",
            ("J. S. Barrowman",),
            "NASA/TM-2001-209983",
            1967,
            "https://ntrs.nasa.gov/citations/20010047838",
            "sec. 3.22, eqs. (3-77)-(3-88), pp. 28-29, with (3-65) p. 20",
            organization=(
                "NASA Goddard Space Flight Center (reissue of a March 1967 Catholic "
                "University of America master's dissertation)"
            ),
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"L": 0.1, "r_fwd": 0.03, "r_aft": 0.05},
            expected=0.05416666666666667,
            rel_tol=1e-11,
            note=(
                "Shoulder with radius ratio 0.6; mpmath quadrature of the integral of "
                "x dA/dx divided by the area change (eqs. 3-83, 3-65)."
            ),
        ),
        VerificationCase(
            inputs={"L": 0.1, "r_fwd": 0.05, "r_aft": 0.04},
            expected=0.04814814814814815,
            rel_tol=1e-11,
            note="Boattail with radius ratio 1.25; mpmath quadrature of the same integral.",
        ),
        VerificationCase(
            inputs={"L": 0.2, "r_fwd": 0.0, "r_aft": 0.05},
            expected=0.13333333333333333,
            rel_tol=1e-11,
            note="Boundary case: a transition from a point is a cone, center of pressure 2L/3.",
        ),
    ),
    assumptions=(
        "Derived result: x_cp = (L A(L) - V) / (A(L) - A(0)) from the source's eqs. (3-65), "
        "(3-85)/(3-87) and (3-88) applied to a frustum, with V = (pi L / 3)(r_fwd^2 + "
        "r_fwd r_aft + r_aft^2); this equals (L / 3)(1 + (1 - r)/(1 - r^2)) with "
        "r = r_fwd / r_aft, that is (L / 3)(2 + r)/(1 + r). The frustum volume is derived "
        "here by integrating the linear radius profile, since the source does not print it.",
        "r_fwd equal to r_aft (a cylinder) has zero normal force and so no center of "
        "pressure; it is rejected.",
        "Barrowman's method: slender-body and thin-airfoil theory with small angle of attack, "
        "steady irrotational flow, a rigid body and a sharp nose tip (source sec. 2.4), in "
        "subsonic flow.",
        "Length convention: x_cp is measured aft from the forward end of the transition, "
        "along the axis; any consistent length unit.",
    ),
    tags=("transition", "center of pressure", "shoulder", "boattail", "Barrowman"),
)
