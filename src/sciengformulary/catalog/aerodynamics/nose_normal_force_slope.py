"""Subsonic Normal-Force Slope of a Pointed Nose: CN_alpha = 2 * (r_base / r_ref)^2."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(r_base: float, r_ref: float) -> float:
    non_negative("r_base", r_base)
    positive("r_ref", r_ref)
    return finite_result(2.0 * (r_base / r_ref) ** 2)


nose_normal_force_slope = FormulaSpec(
    id="aerodynamics.nose_normal_force_slope",
    name="Subsonic Normal-Force Slope of a Pointed Nose",
    equation="CN_alpha_nose = 2 * (r_base / r_ref)^2",
    description=(
        "Slope of the normal-force coefficient with angle of attack contributed by a pointed "
        "nose in Barrowman's method. It depends only on the base area of the nose relative "
        "to the reference area, not on the nose shape."
    ),
    inputs=(
        VariableSpec(
            name="r_base",
            symbol="r_base",
            description="Radius of the circular base of the nose",
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
        description="Normal-force coefficient slope of the nose, referred to the reference area",
        dimension="1",
        si_unit="1/rad",
    ),
    evaluator=_evaluate,
    references=(
        # Derived: eq. (3-66), from (3-65), states (C_N,alpha)_B = 2 A_BN / A_r for a body
        # component with zero area at its front, A_BN being the base area of the nose. With
        # circular sections A = pi r^2, so the area ratio is (r_base / r_ref)^2.
        # Symbols: A_BN -> pi r_base^2, A_r -> pi r_ref^2.
        nasa_technical_report(
            "The Practical Calculation of the Aerodynamic Characteristics of Slender Finned "
            "Vehicles",
            ("J. S. Barrowman",),
            "NASA/TM-2001-209983",
            1967,
            "https://ntrs.nasa.gov/citations/20010047838",
            "sec. 3.21, eq. (3-66) (from (3-65)), p. 20-21",
            organization=(
                "NASA Goddard Space Flight Center (reissue of a March 1967 Catholic "
                "University of America master's dissertation)"
            ),
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"r_base": 0.05, "r_ref": 0.05},
            expected=2.0,
            rel_tol=1e-12,
            note="Base radius equal to the reference radius gives 2; exact arithmetic.",
        ),
        VerificationCase(
            inputs={"r_base": 0.03, "r_ref": 0.0635},
            expected=0.4464008928017856,
            rel_tol=1e-12,
            note="Base radius 0.03 m, reference radius 0.0635 m; 50-digit mpmath evaluation.",
        ),
        VerificationCase(
            inputs={"r_base": 0.0, "r_ref": 0.05},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Boundary case: zero base area gives no normal force.",
        ),
    ),
    assumptions=(
        "Derived result: the source states (C_N,alpha)_B = 2 A_BN / A_r for a component whose "
        "front area is zero, with A_BN the nose base area; for circular sections A = pi r^2, "
        "so the ratio is (r_base / r_ref)^2.",
        "Barrowman's method: slender-body and thin-airfoil theory with small angle of attack, "
        "steady irrotational flow, a rigid body and a sharp nose tip (source sec. 2.4), in "
        "subsonic flow.",
        "The reference area is the circle of radius r_ref, the area the coefficient is "
        "referred to; r_base and r_ref are radii in one consistent length unit.",
    ),
    tags=("nose", "normal force", "slender body", "Barrowman", "rocket aerodynamics"),
)
