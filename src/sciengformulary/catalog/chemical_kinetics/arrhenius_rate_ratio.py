"""Arrhenius rate change between two temperatures."""

import math

from sciengformulary.catalog._constants import (
    MOLAR_GAS_CONSTANT,
)
from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import (
    bipm_si_defining_constants,
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(Ea: float, T1: float, T2: float) -> float:
    finite("Ea", Ea)
    positive("T1", T1)
    positive("T2", T2)
    return finite_result(math.exp(-Ea / MOLAR_GAS_CONSTANT * (1 / T2 - 1 / T1)))


arrhenius_rate_ratio = FormulaSpec(
    id="chemical_kinetics.arrhenius_rate_ratio",
    name="Arrhenius Rate Ratio",
    equation="k2/k1 = exp[-Ea/R_u*(1/T2-1/T1)]",
    description="Arrhenius rate change between two temperatures.",
    inputs=(
        VariableSpec(
            name="Ea",
            symbol="Ea",
            description="Molar apparent activation energy",
            dimension="M L^2 T^-2 N^-1",
            si_unit="J/mol",
        ),
        VariableSpec(
            name="T1",
            symbol="T1",
            description="First absolute temperature",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="T2",
            symbol="T2",
            description="Second absolute temperature",
            dimension="Theta",
            si_unit="K",
        ),
    ),
    output=VariableSpec(
        name="rate_ratio",
        symbol="rate_ratio",
        description="Rate constant at T2 divided by that at T1",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        openstax_section(
            "chemistry-2e",
            "12-5-collision-theory",
            "12.5 Collision Theory",
            accessed="2026-10-10",
        ),
        bipm_si_defining_constants(),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"Ea": 10000, "T1": 300, "T2": 300},
            expected=1,
            note="Equal temperatures give rate ratio one.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"Ea": 4988.677570891944, "T1": 300, "T2": 600},
            expected=2.718281828459045,
            note="The exponent is one; Decimal exp(1) gives the ratio.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Derived result: Divide the two Arrhenius equations with the same pre-exponential factor.",
        "Same rate law and mechanism; A and Ea approximately constant over the interval.",
        "This ratio is dimensionless and is applicable to any reaction order with consistent k units.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemical kinetics", "arrhenius rate ratio"),
)
