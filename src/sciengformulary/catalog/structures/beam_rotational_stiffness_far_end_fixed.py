"""Beam Rotational Stiffness, Far End Fixed: k_theta = 4 * E * I / L."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, roylance
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    E: float,  # noqa: N803
    I: float,  # noqa: N803, E741
    L: float,  # noqa: N803
) -> float:
    positive("E", E)
    positive("I", I)
    positive("L", L)
    return finite_result(4.0 * E * I / L)


beam_rotational_stiffness_far_end_fixed = FormulaSpec(
    id="structures.beam_rotational_stiffness_far_end_fixed",
    name="Beam Rotational Stiffness, Far End Fixed",
    equation="k_theta = 4 * E * I / L",
    description=(
        "Moment needed at one end of a prismatic beam to rotate that end by one radian, with "
        "no translation, while the other end is clamped."
    ),
    inputs=(
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
            description="Second moment of area of the cross-section about the bending axis",
            dimension="L^4",
            si_unit="m^4",
        ),
        VariableSpec(
            name="L",
            symbol="L",
            description="Beam length",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="k_theta",
        symbol=r"k_\theta",
        description="Rotational stiffness at the rotated end (moment per radian)",
        dimension="M L^2 T^-2",
        si_unit="N*m/rad",
    ),
    evaluator=_evaluate,
    references=(
        # The notes integrate the load to shear and moment and then v'' = M / (E I) twice more,
        # fixing the constants from boundary conditions on slope and deflection (eqs. (1)-(4));
        # Fig. 6 gives the cantilever curve for a point load, and p. 9 states that separate
        # loads superpose. The stiffness itself is not printed. Derived two ways: (a) solve
        # E I v'' = M with v(0) = 0, v'(0) = theta, v(L) = 0, v'(L) = 0, giving
        # v = theta * x * (1 - x / L)^2; (b) superpose a tip load and a tip couple on a
        # cantilever so that the tip deflection is zero and the tip rotation is theta.
        roylance(
            "Beam Displacements",
            "mit3_11f99_bdisp",
            2000,
            "eqs. (1)-(4), pp. 1-2; Fig. 6 and the superposition paragraph, p. 9",
            accessed=ENGINEERING_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"E": 200000000000.0, "I": 8e-06, "L": 4.0},
            expected=1600000.0,
            rel_tol=1e-12,
            note="Hand calculation: 4 * 200e9 * 8e-6 / 4 = 1.6e6 N*m/rad.",
        ),
        VerificationCase(
            inputs={"E": 70000000000.0, "I": 1.2e-06, "L": 0.5},
            expected=672000.0,
            rel_tol=1e-12,
            note="Hand calculation: 4 * 70e9 * 1.2e-6 / 0.5 = 6.72e5 N*m/rad.",
        ),
    ),
    assumptions=(
        "Prismatic, linear elastic Euler-Bernoulli beam: small deflections and slopes, shear "
        "deformation neglected, constant E I.",
        "The rotated end cannot translate, and the far end is fully clamped (no translation, "
        "no rotation).",
        "The moment carried over to the clamped far end is half of k_theta times the rotation "
        "(carry-over factor 1/2).",
        "E, I and L must be finite and positive; otherwise ValueError is raised.",
        "Derived result: obtained from E I v'' = M with the stated boundary conditions and "
        "checked by superposing a tip load and a tip couple on a cantilever; the source does "
        "not print this stiffness.",
        "Homogeneous in any consistent unit set (moment per radian; the radian is dimensionless).",
    ),
    tags=("stiffness", "moment distribution", "beam", "carry-over"),
)
