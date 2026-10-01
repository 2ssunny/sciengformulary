"""Composite Longitudinal Modulus (Rule of Mixtures): E1 = V_f * E_f + (1 - V_f) * E_m."""

from sciengformulary.catalog._sources import roylance
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    V_f: float,  # noqa: N803
    E_f: float,  # noqa: N803
    E_m: float,  # noqa: N803
) -> float:
    return V_f * E_f + (1.0 - V_f) * E_m


composite_longitudinal_modulus = FormulaSpec(
    id="materials.composite_longitudinal_modulus",
    name="Composite Longitudinal Modulus (Rule of Mixtures)",
    equation="E1 = V_f * E_f + (1 - V_f) * E_m",
    description=(
        "Young's modulus of a unidirectional fibre composite along the fibres, with fibre and "
        "matrix strained equally (parallel model)."
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
            description="Fibre Young's modulus (axial)",
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
        name="E1",
        symbol="E_1",
        description="Composite modulus along the fibres",
        dimension="M L^-1 T^-2",
        si_unit="Pa",
    ),
    evaluator=_evaluate,
    references=(
        # The module writes V_m = 1 - V_f for the matrix fraction.
        roylance("Introduction to Composite Materials", "mit3_11f99_composites", 2000, "eq. (1)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"V_f": 0.6, "E_f": 230000000000.0, "E_m": 3500000000.0},
            expected=139400000000.0,
            rel_tol=1e-12,
            note="Hand calculation: 0.6 * 230e9 + 0.4 * 3.5e9 = 139.4e9 Pa.",
        ),
    ),
    assumptions=(
        "Continuous, aligned fibres perfectly bonded to the matrix; load along the fibres.",
        "No voids; V_f between 0 and 1.",
    ),
    tags=("composites", "rule of mixtures", "fibre", "longitudinal modulus"),
)
