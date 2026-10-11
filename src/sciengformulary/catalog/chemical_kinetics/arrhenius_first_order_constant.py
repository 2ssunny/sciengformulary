"""Arrhenius temperature law for first-order kinetics."""

import math

from sciengformulary.catalog._constants import (
    MOLAR_GAS_CONSTANT,
)
from sciengformulary.catalog._domain import (
    finite,
    finite_result,
    non_negative,
    positive,
)
from sciengformulary.catalog._sources import (
    bipm_si_defining_constants,
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(A: float, Ea: float, T: float) -> float:
    non_negative("A", A)
    finite("Ea", Ea)
    positive("T", T)
    return finite_result(A * math.exp(-Ea / (MOLAR_GAS_CONSTANT * T)))


arrhenius_first_order_constant = FormulaSpec(
    id="chemical_kinetics.arrhenius_first_order_constant",
    name="Arrhenius First Order Constant",
    equation="k = A * exp(-Ea/(R_u*T))",
    description="Arrhenius temperature law for first-order kinetics.",
    inputs=(
        VariableSpec(
            name="A",
            symbol="A",
            description="First-order pre-exponential factor",
            dimension="T^-1",
            si_unit="1/s",
        ),
        VariableSpec(
            name="Ea",
            symbol="Ea",
            description="Apparent molar activation energy",
            dimension="M L^2 T^-2 N^-1",
            si_unit="J/mol",
        ),
        VariableSpec(
            name="T", symbol="T", description="Absolute temperature", dimension="Theta", si_unit="K"
        ),
    ),
    output=VariableSpec(
        name="k",
        symbol="k",
        description="First-order rate constant",
        dimension="T^-1",
        si_unit="1/s",
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
            inputs={"A": 2, "Ea": 0, "T": 300},
            expected=2,
            note="Zero activation energy gives k=A.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"A": 2, "Ea": 2494.338785445972, "T": 300},
            expected=0.7357588823428847,
            note="Ea/(RT)=1; independent Decimal 2 exp(-1).",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "First-order rate constant; A has units s^-1.",
        "Arrhenius parameters describe the same mechanism over the selected temperature range.",
        "Apparent negative activation energies are permitted, not assumed impossible.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemical kinetics", "arrhenius first order constant"),
)
