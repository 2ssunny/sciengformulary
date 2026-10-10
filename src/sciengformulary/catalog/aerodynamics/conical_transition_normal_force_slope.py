"""Normal-Force Slope of a Conical Transition (shoulder or boattail), Barrowman."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(r_fwd: float, r_aft: float, r_ref: float) -> float:
    non_negative("r_fwd", r_fwd)
    non_negative("r_aft", r_aft)
    positive("r_ref", r_ref)
    return finite_result(2.0 * ((r_aft / r_ref) ** 2 - (r_fwd / r_ref) ** 2))


conical_transition_normal_force_slope = FormulaSpec(
    id="aerodynamics.conical_transition_normal_force_slope",
    name="Normal-Force Slope of a Conical Transition (Shoulder or Boattail)",
    equation="CN_alpha = 2 * ((r_aft / r_ref)^2 - (r_fwd / r_ref)^2)",
    description=(
        "Additional normal-force slope from a conical frustum between two circular sections "
        "in Barrowman's method. It depends only on the change in cross-section area across "
        "the frustum, and is negative for a boattail."
    ),
    inputs=(
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
        VariableSpec(
            name="r_ref",
            symbol="r_ref",
            description="Radius of the circular reference area",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="CN_alpha",
        symbol="C_{N alpha}",
        description=(
            "Normal-force coefficient slope of the transition, positive for a shoulder and "
            "negative for a boattail"
        ),
        dimension="1",
        si_unit="1/rad",
    ),
    evaluator=_evaluate,
    references=(
        # Derived: eq. (3-65) gives C_N,alpha = (2 / A_r) [A(l_0) - A(0)] for a body component,
        # independent of its shape. For a frustum A(l_0) = pi r_aft^2 and A(0) = pi r_fwd^2,
        # and A_r = pi r_ref^2. Symbols: l_0 -> frustum length (does not appear in the result).
        nasa_technical_report(
            "The Practical Calculation of the Aerodynamic Characteristics of Slender Finned "
            "Vehicles",
            ("J. S. Barrowman",),
            "NASA/TM-2001-209983",
            1967,
            "https://ntrs.nasa.gov/citations/20010047838",
            "sec. 3.21, eq. (3-65), p. 20",
            organization=(
                "NASA Goddard Space Flight Center (reissue of a March 1967 Catholic "
                "University of America master's dissertation)"
            ),
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"r_fwd": 0.05, "r_aft": 0.04, "r_ref": 0.05},
            expected=-0.72,
            rel_tol=1e-12,
            note="Boattail from 0.05 m to 0.04 m radius, reference radius 0.05 m; exact value.",
        ),
        VerificationCase(
            inputs={"r_fwd": 0.03, "r_aft": 0.05, "r_ref": 0.05},
            expected=1.28,
            rel_tol=1e-12,
            note="Shoulder from 0.03 m to 0.05 m radius, reference radius 0.05 m; exact value.",
        ),
        VerificationCase(
            inputs={"r_fwd": 0.05, "r_aft": 0.05, "r_ref": 0.05},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Boundary case: a cylinder adds no normal force.",
        ),
    ),
    assumptions=(
        "Derived result: eq. (3-65), C_N,alpha = (2 / A_r) [A(l_0) - A(0)], holds for a body "
        "component whose area is continuous with its neighbours; for a frustum A(l_0) = "
        "pi r_aft^2 and A(0) = pi r_fwd^2, and A_r = pi r_ref^2.",
        "Barrowman's method: slender-body and thin-airfoil theory with small angle of attack, "
        "steady irrotational flow, a rigid body and a sharp nose tip (source sec. 2.4), in "
        "subsonic flow.",
        "The reference area is the circle of radius r_ref, the area the coefficient is "
        "referred to; radii are in one consistent length unit, with r_fwd the radius at the "
        "forward end of the transition and r_aft at its aft end.",
    ),
    tags=("transition", "shoulder", "boattail", "normal force", "Barrowman", "slender body"),
)
