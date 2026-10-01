"""Torsional Shear Stress in a Circular Shaft: tau = T * r / J."""

from sciengformulary.catalog._sources import roylance
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    T: float,  # noqa: N803
    r: float,
    J: float,  # noqa: N803
) -> float:
    return T * r / J


torsional_shear_stress = FormulaSpec(
    id="structures.torsional_shear_stress",
    name="Torsional Shear Stress in a Circular Shaft",
    equation="tau = T * r / J",
    description=(
        "Shear stress at radius r in a circular shaft carrying torque T; maximum at the outer "
        "surface."
    ),
    inputs=(
        VariableSpec(
            name="T",
            symbol="T",
            description="Applied torque",
            dimension="M L^2 T^-2",
            si_unit="N*m",
        ),
        VariableSpec(
            name="r",
            symbol="r",
            description="Radial position in the section",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="J",
            symbol="J",
            description="Polar second moment of area of the section",
            dimension="L^4",
            si_unit="m^4",
        ),
    ),
    output=VariableSpec(
        name="tau",
        symbol=r"\tau",
        description="Shear stress at radius r",
        dimension="M L^-1 T^-2",
        si_unit="Pa",
    ),
    evaluator=_evaluate,
    references=(
        roylance("Shear and Torsion", "mit3_11f99_torsion", 2000, "eq. (14)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"T": 500.0, "r": 0.02, "J": 2.5e-07},
            expected=40000000.0,
            rel_tol=1e-12,
            note="Hand calculation: 500 * 0.02 / 2.5e-7 = 4e7 Pa.",
        ),
    ),
    assumptions=(
        "Linear elastic, homogeneous, isotropic material; small strains and displacements.",
        "Solid or hollow circular shafts only; non-circular sections warp and need other results.",
    ),
    tags=("torsion", "shear stress", "shaft", "torque"),
)
