"""Shear Modulus from Young's Modulus: G = E / (2 * (1 + nu))."""

from sciengformulary.catalog._sources import roylance
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(E: float, nu: float) -> float:  # noqa: N803 - symbols as written in the source
    return E / (2.0 * (1.0 + nu))


shear_modulus_from_youngs_modulus = FormulaSpec(
    id="materials.shear_modulus_from_youngs_modulus",
    name="Shear Modulus from Young's Modulus",
    equation="G = E / (2 * (1 + nu))",
    description="Shear modulus of an isotropic linear elastic material from E and nu.",
    inputs=(
        VariableSpec(
            name="E",
            symbol="E",
            description="Young's modulus of the material",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="nu",
            symbol=r"\nu",
            description="Poisson's ratio",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="G",
        symbol="G",
        description="Shear modulus of the material",
        dimension="M L^-1 T^-2",
        si_unit="Pa",
    ),
    evaluator=_evaluate,
    references=(
        roylance("Constitutive Equations", "mit3_11f99_const", 2000, "text following eq. (2)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"E": 200000000000.0, "nu": 0.25},
            expected=80000000000.0,
            rel_tol=1e-12,
            note="Hand calculation: 200e9 / 2.5 = 80e9 Pa.",
        ),
    ),
    assumptions=(
        "Isotropic material only; composites, single crystals and textured metals need their "
        "full anisotropic constants.",
        "-1 < nu < 0.5 for a stable isotropic solid.",
    ),
    tags=("shear modulus", "elastic constants", "Poisson's ratio", "isotropic"),
)
