"""Simply Supported Beam Centre Deflection Under a Central Load: delta = P * L^3 / (48 * E * I)."""

from sciengformulary.catalog._sources import roylance
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    P: float,  # noqa: N803
    L: float,  # noqa: N803
    E: float,  # noqa: N803
    I: float,  # noqa: N803, E741
) -> float:
    return P * L**3 / (48.0 * E * I)


simply_supported_center_deflection = FormulaSpec(
    id="structures.simply_supported_center_deflection",
    name="Simply Supported Beam Centre Deflection Under a Central Load",
    equation="delta = P * L^3 / (48 * E * I)",
    description=(
        "Mid-span deflection of a simply supported beam carrying a point load at the centre "
        "(three-point bending)."
    ),
    inputs=(
        VariableSpec(
            name="P",
            symbol="P",
            description="Point load at mid-span",
            dimension="M L T^-2",
            si_unit="N",
        ),
        VariableSpec(
            name="L",
            symbol="L",
            description="Span between supports",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="E",
            symbol="E",
            description="Young's modulus of the material",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="I",
            symbol="I",
            description=(
                "Second moment of area of the cross-section about the bending (neutral) axis"
            ),
            dimension="L^4",
            si_unit="m^4",
        ),
    ),
    output=VariableSpec(
        name="delta",
        symbol=r"\delta",
        description="Mid-span deflection magnitude",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        roylance("Beam Displacements", "mit3_11f99_bdisp", 2000, "eq. (7)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"P": 1000.0, "L": 4.0, "E": 200000000000.0, "I": 1e-06},
            expected=0.006666666666666667,
            rel_tol=1e-12,
            note="Hand calculation: 1000 * 64 / (48 * 200e9 * 1e-6) = 0.0066667 m.",
        ),
    ),
    assumptions=(
        "Linear elastic, homogeneous, isotropic material; small strains and displacements.",
        "Slender prismatic Euler-Bernoulli beam: plane sections remain plane, shear "
        "deformation neglected, small slopes.",
        "Pinned (simple) supports at both ends; constant E I.",
        "Shear deflection is neglected; it matters for short, deep beams.",
    ),
    tags=("three-point bending", "deflection", "simply supported beam", "flexural test"),
)
