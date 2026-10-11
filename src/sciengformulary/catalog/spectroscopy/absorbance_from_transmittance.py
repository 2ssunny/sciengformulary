"""Absorbance from fractional transmittance."""

import math

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import (
    harvey_analytical_chemistry,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(T_fraction: float) -> float:
    positive("T_fraction", T_fraction)
    if T_fraction > 1:
        raise ValueError("ideal transmittance must not exceed one")
    return finite_result(-math.log10(T_fraction))


absorbance_from_transmittance = FormulaSpec(
    id="spectroscopy.absorbance_from_transmittance",
    name="Absorbance From Transmittance",
    equation="A = -log10(T_fraction)",
    description="Absorbance from fractional transmittance.",
    inputs=(
        VariableSpec(
            name="T_fraction",
            symbol="T_fraction",
            description="Fractional transmitted radiant power, not percent",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="A", symbol="A", description="Decadic absorbance", dimension="1", si_unit="-"
    ),
    evaluator=_evaluate,
    references=(
        harvey_analytical_chemistry(
            "10%3A_Spectroscopic_Methods/10.02%3A_Spectroscopy_Based_on_Absorption",
            "10.2: Spectroscopy Based on Absorption",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"T_fraction": 0.1},
            expected=1,
            note="Ten percent transmittance gives absorbance one.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"T_fraction": 1},
            expected=0,
            note="Full transmission gives zero absorbance.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "Ideal attenuation measurement with 0 < T_fraction <= 1.",
        "Convert percent transmittance to a fraction before evaluation.",
        "This ideal-model evaluator rejects apparent transmittance above one from baseline or instrumental artifacts.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "spectroscopy", "absorbance from transmittance"),
)
