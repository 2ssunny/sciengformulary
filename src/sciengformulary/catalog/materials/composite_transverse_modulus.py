"""Composite Transverse Modulus (Series Model): 1 / E2 = V_f / E_f + (1 - V_f) / E_m."""

from sciengformulary.catalog._sources import roylance
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    V_f: float,  # noqa: N803
    E_f: float,  # noqa: N803
    E_m: float,  # noqa: N803
) -> float:
    return 1.0 / (V_f / E_f + (1.0 - V_f) / E_m)


composite_transverse_modulus = FormulaSpec(
    id="materials.composite_transverse_modulus",
    name="Composite Transverse Modulus (Series Model)",
    equation="1 / E2 = V_f / E_f + (1 - V_f) / E_m",
    description=(
        "Estimate of the modulus of a unidirectional composite across the fibres, with fibre and "
        "matrix carrying equal stress (series model)."
    ),
    inputs=(
        VariableSpec(
            name="V_f",
            symbol="V_f",
            description="Fibre volume fraction",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="E_f",
            symbol="E_f",
            description="Fibre Young's modulus (transverse)",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="E_m",
            symbol="E_m",
            description="Matrix Young's modulus",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
    ),
    output=VariableSpec(
        name="E2",
        symbol="E_2",
        description="Composite modulus across the fibres",
        dimension="M L^-1 T^-2",
        si_unit="Pa",
    ),
    evaluator=_evaluate,
    references=(
        roylance("Introduction to Composite Materials", "mit3_11f99_composites", 2000, "eq. (2)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"V_f": 0.6, "E_f": 230000000000.0, "E_m": 3500000000.0},
            expected=8554729011.689692,
            rel_tol=1e-12,
            note="Exact rational arithmetic: 1 / (0.6/230e9 + 0.4/3.5e9).",
        ),
    ),
    assumptions=(
        "The cited module calls this series estimate unreliable; treat it as a rough estimate "
        "and prefer measured values or a better micromechanics model.",
        "Continuous aligned fibres; load perpendicular to them.",
    ),
    tags=("composites", "transverse modulus", "series model", "inverse rule of mixtures"),
)
