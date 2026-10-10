"""Fixed-Guided Beam Lateral Stiffness: k_v = 12 * E * I / L^3."""

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
    return finite_result(12.0 * E * I / L**3)


fixed_guided_beam_lateral_stiffness = FormulaSpec(
    id="structures.fixed_guided_beam_lateral_stiffness",
    name="Fixed-Guided Beam Lateral Stiffness",
    equation="k_v = 12 * E * I / L^3",
    description=(
        "Transverse force per unit relative end displacement of a prismatic beam whose two "
        "ends cannot rotate: one end clamped, the other sliding transversely."
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
        name="k_v",
        symbol="k_v",
        description="Lateral stiffness (force per unit transverse displacement)",
        dimension="M T^-2",
        si_unit="N/m",
    ),
    evaluator=_evaluate,
    references=(
        # The notes give the integration procedure (eqs. (1)-(4)), the cantilever curve for a
        # point load (Fig. 6) and the superposition statement (p. 9); the stiffness itself is
        # not printed. Derived two ways: (a) a tip load plus a tip couple on a cantilever chosen
        # so the tip rotation is zero give F = 12 E I Delta / L^3 for a tip displacement Delta;
        # (b) v = Delta * (3 x^2 / L^2 - 2 x^3 / L^3) meets the four end conditions and has
        # |E I v'''| = 12 E I Delta / L^3.
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
            expected=300000.0,
            rel_tol=1e-12,
            note="Hand calculation: 12 * 200e9 * 8e-6 / 64 = 3.0e5 N/m.",
        ),
        VerificationCase(
            inputs={"E": 70000000000.0, "I": 1.2e-06, "L": 0.5},
            expected=8064000.0,
            rel_tol=1e-12,
            note="Hand calculation: 12 * 70e9 * 1.2e-6 / 0.125 = 8.064e6 N/m.",
        ),
    ),
    assumptions=(
        "Prismatic, linear elastic Euler-Bernoulli beam: small deflections, shear deformation "
        "neglected, constant E I.",
        "Both end rotations are prevented, and one end is displaced transversely relative to "
        "the other (the classical stiffness of a column in a rigid frame). This is not the "
        "cantilever value 3 E I / L^3.",
        "E, I and L must be finite and positive; otherwise ValueError is raised.",
        "Derived result: obtained from E I v'' = M with the stated boundary conditions and "
        "checked by superposition on a cantilever; the source does not print this stiffness.",
        "Homogeneous in any consistent unit set (force per length).",
    ),
    tags=("stiffness", "beam", "guided end", "storey column"),
)
