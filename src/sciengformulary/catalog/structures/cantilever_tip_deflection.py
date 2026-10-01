"""Cantilever Tip Deflection Under an End Load: delta = F * L^3 / (3 * E * I)."""

from sciengformulary.catalog._sources import roylance
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    F: float,  # noqa: N803
    L: float,  # noqa: N803
    E: float,  # noqa: N803
    I: float,  # noqa: N803, E741
) -> float:
    return F * L**3 / (3.0 * E * I)


cantilever_tip_deflection = FormulaSpec(
    id="structures.cantilever_tip_deflection",
    name="Cantilever Tip Deflection Under an End Load",
    equation="delta = F * L^3 / (3 * E * I)",
    description=(
        "Deflection of the free end of a cantilever with a transverse point load at that end."
    ),
    inputs=(
        VariableSpec(
            name="F",
            symbol="F",
            description="Transverse load at the free end",
            dimension="M L T^-2",
            si_unit="N",
        ),
        VariableSpec(
            name="L",
            symbol="L",
            description="Cantilever length",
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
        description="Tip deflection magnitude, in the load direction",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # Fig. 6 gives the cantilever deflection curve for a point load at x = a; evaluating it at
        # x = a = L gives this result.
        roylance("Beam Displacements", "mit3_11f99_bdisp", 2000, "Fig. 6"),
        # Example 3 uses the same result for each arm of a double-cantilever specimen.
        roylance("Introduction to Fracture Mechanics", "mit3_11f99_frac", 2001, "Example 3"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"F": 1000.0, "L": 2.0, "E": 200000000000.0, "I": 1e-06},
            expected=0.013333333333333334,
            rel_tol=1e-12,
            note="Hand calculation: 1000 * 8 / (3 * 200e9 * 1e-6) = 0.013333 m.",
        ),
    ),
    assumptions=(
        "Linear elastic, homogeneous, isotropic material; small strains and displacements.",
        "Slender prismatic Euler-Bernoulli beam: plane sections remain plane, shear "
        "deformation neglected, small slopes.",
        "Rigidly clamped root; constant E I along the length.",
    ),
    tags=("cantilever", "deflection", "beam", "tip load"),
)
