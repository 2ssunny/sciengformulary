"""Bending Stress in a Beam: sigma_x = -M * y / I."""

from sciengformulary.catalog._sources import roylance
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    M: float,  # noqa: N803
    y: float,
    I: float,  # noqa: N803, E741
) -> float:
    return -M * y / I


bending_stress = FormulaSpec(
    id="structures.bending_stress",
    name="Bending Stress in a Beam",
    equation="sigma_x = -M * y / I",
    description=(
        "Normal stress at distance y from the neutral axis of a beam under bending moment M. It "
        "varies linearly across the depth and is zero on the neutral axis."
    ),
    inputs=(
        VariableSpec(
            name="M",
            symbol="M",
            description="Bending moment at the section",
            dimension="M L^2 T^-2",
            si_unit="N*m",
        ),
        VariableSpec(
            name="y",
            symbol="y",
            description="Distance from the neutral axis (positive in the +y direction)",
            dimension="L",
            si_unit="m",
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
        name="sigma_x",
        symbol=r"\sigma_x",
        description="Axial normal stress, tension positive",
        dimension="M L^-1 T^-2",
        si_unit="Pa",
    ),
    evaluator=_evaluate,
    references=(
        roylance("Stresses in Beams", "mit3_11f99_bstress", 2000, "eq. (7)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"M": 2000.0, "y": 0.05, "I": 1e-06},
            expected=-100000000.0,
            rel_tol=1e-12,
            note="Hand calculation: -2000 * 0.05 / 1e-6 = -1e8 Pa.",
        ),
    ),
    assumptions=(
        "Linear elastic, homogeneous, isotropic material; small strains and displacements.",
        "Slender prismatic Euler-Bernoulli beam: plane sections remain plane, shear "
        "deformation neglected, small slopes.",
        "Bending about a principal axis of the section (symmetric bending). The minus sign "
        "follows the source's convention (positive M compresses +y fibres); other texts use "
        "the opposite sign convention.",
    ),
    tags=("bending stress", "flexure formula", "beam", "neutral axis"),
)
