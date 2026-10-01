"""Bulk Modulus from Young's Modulus: K = E / (3 * (1 - 2 * nu))."""

from sciengformulary.catalog._sources import roylance
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(E: float, nu: float) -> float:  # noqa: N803 - symbols as written in the source
    return E / (3.0 * (1.0 - 2.0 * nu))


bulk_modulus_from_youngs_modulus = FormulaSpec(
    id="materials.bulk_modulus_from_youngs_modulus",
    name="Bulk Modulus from Young's Modulus",
    equation="K = E / (3 * (1 - 2 * nu))",
    description="Bulk modulus of an isotropic linear elastic material from E and nu.",
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
        name="K",
        symbol="K",
        description="Bulk modulus",
        dimension="M L^-1 T^-2",
        si_unit="Pa",
    ),
    evaluator=_evaluate,
    references=(
        roylance("Constitutive Equations", "mit3_11f99_const", 2000, "Example 2"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"E": 207000000000.0, "nu": 0.3},
            expected=172500000000.0,
            rel_tol=1e-12,
            note=(
                "Worked example in the cited module: steel with E = 207 GPa and nu = 0.3 gives K = "
                "173 GPa (172.5 GPa before rounding)."
            ),
        ),
    ),
    assumptions=(
        "Isotropic material only.",
        "nu must be below 0.5; K grows without bound as nu approaches 0.5 (incompressible).",
    ),
    tags=("bulk modulus", "elastic constants", "compressibility", "isotropic"),
)
