"""Angle of Twist of a Circular Shaft: phi = T * L / (G * J)."""

from sciengformulary.catalog._sources import roylance
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    T: float,  # noqa: N803
    L: float,  # noqa: N803
    G: float,  # noqa: N803
    J: float,  # noqa: N803
) -> float:
    return T * L / (G * J)


angle_of_twist = FormulaSpec(
    id="structures.angle_of_twist",
    name="Angle of Twist of a Circular Shaft",
    equation="phi = T * L / (G * J)",
    description="Relative rotation of the two ends of a uniform circular shaft under torque.",
    inputs=(
        VariableSpec(
            name="T",
            symbol="T",
            description="Applied torque",
            dimension="M L^2 T^-2",
            si_unit="N*m",
        ),
        VariableSpec(
            name="L",
            symbol="L",
            description="Shaft length",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="G",
            symbol="G",
            description="Shear modulus of the material",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="J",
            symbol="J",
            description="Polar second moment of area",
            dimension="L^4",
            si_unit="m^4",
        ),
    ),
    output=VariableSpec(
        name="phi",
        symbol=r"\phi",
        description="Angle of twist",
        dimension="1",
        si_unit="rad",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes the twist angle as theta.
        roylance("Shear and Torsion", "mit3_11f99_torsion", 2000, "eq. (13)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"T": 500.0, "L": 1.5, "G": 80000000000.0, "J": 2.5e-07},
            expected=0.0375,
            rel_tol=1e-12,
            note="Hand calculation: 500 * 1.5 / (80e9 * 2.5e-7) = 0.0375 rad.",
        ),
    ),
    assumptions=(
        "Linear elastic, homogeneous, isotropic material; small strains and displacements.",
        "Circular section; torque, J and G constant along the length (otherwise sum or "
        "integrate over segments).",
    ),
    tags=("torsion", "angle of twist", "shaft", "torsional stiffness"),
)
