"""Fundamental chromatography resolution approximation."""

import math

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import (
    harvey_analytical_chemistry,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(N: float, alpha: float, k_later: float) -> float:
    positive("N", N)
    positive("alpha", alpha)
    positive("k_later", k_later)
    if alpha < 1:
        raise ValueError("alpha must be at least one")
    return finite_result(math.sqrt(N) / 4 * ((alpha - 1) / alpha) * (k_later / (1 + k_later)))


fundamental_resolution_estimate = FormulaSpec(
    id="chromatography.fundamental_resolution_estimate",
    name="Fundamental Resolution Estimate",
    equation="Rs = sqrt(N)/4 * (alpha-1)/alpha * k_later/(1+k_later)",
    description="Fundamental chromatography resolution approximation.",
    inputs=(
        VariableSpec(
            name="N",
            symbol="N",
            description="Theoretical plate number for the later peak",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="alpha",
            symbol="alpha",
            description="Later/earlier retention-factor ratio",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="k_later",
            symbol="k_later",
            description="Retention factor of later peak",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="Rs",
        symbol="Rs",
        description="Estimated chromatographic resolution",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        harvey_analytical_chemistry(
            (
                "12%3A_Chromatographic_and_Electrophoretic_Methods/12.03%3A_Optimizing_Chromatogr"
                "aphic_Separations"
            ),
            "12.3: Optimizing Chromatographic Separations",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"N": 1600, "alpha": 2, "k_later": 1},
            expected=2.5,
            note="40/4 times 1/2 times 1/2 = 2.5.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"N": 1600, "alpha": 1, "k_later": 1},
            expected=0,
            note="Unit selectivity gives zero separation.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "Gaussian peaks with similar baseline widths; use compatible plate number and retention factors.",
        "alpha >= 1; alpha=1 is the coincident-peak limit.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chromatography", "fundamental resolution estimate"),
)
