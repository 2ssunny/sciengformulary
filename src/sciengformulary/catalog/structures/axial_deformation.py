"""Axial Deformation of a Bar: delta = N * L / (E * A)."""

from sciengformulary.catalog._sources import roylance
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    N: float,  # noqa: N803
    L: float,  # noqa: N803
    E: float,  # noqa: N803
    A: float,  # noqa: N803
) -> float:
    return N * L / (E * A)


axial_deformation = FormulaSpec(
    id="structures.axial_deformation",
    name="Axial Deformation of a Bar",
    equation="delta = N * L / (E * A)",
    description="Change in length of a straight bar carrying a constant axial force.",
    inputs=(
        VariableSpec(
            name="N",
            symbol="N",
            description="Axial force, tension positive",
            dimension="M L T^-2",
            si_unit="N",
        ),
        VariableSpec(
            name="L",
            symbol="L",
            description="Bar length",
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
            name="A",
            symbol="A",
            description="Cross-sectional area",
            dimension="L^2",
            si_unit="m^2",
        ),
    ),
    output=VariableSpec(
        name="delta",
        symbol=r"\delta",
        description="Elongation (negative for shortening)",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes delta = PL/AE with P the axial member force.
        roylance("Trusses", "mit3_11f99_truss", 2000, "p. 6"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"N": 10000.0, "L": 2.0, "E": 200000000000.0, "A": 0.0001},
            expected=0.001,
            rel_tol=1e-12,
            note="Hand calculation: 1e4 * 2 / (200e9 * 1e-4) = 1e-3 m.",
        ),
    ),
    assumptions=(
        "Linear elastic, homogeneous, isotropic material; small strains and displacements.",
        "Constant force, area and modulus along the length; otherwise integrate N / (E A) over "
        "the length.",
        "Compressive members must also be checked for buckling.",
    ),
    tags=("axial load", "elongation", "bar", "truss member", "stiffness"),
)
