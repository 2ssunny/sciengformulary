"""Ideal two-species gas mixing entropy."""

import math

from sciengformulary.catalog._constants import (
    MOLAR_GAS_CONSTANT,
)
from sciengformulary.catalog._domain import finite_result, non_negative
from sciengformulary.catalog._sources import bipm_si_defining_constants
from sciengformulary.core import (
    FormulaSpec,
    ReferenceSpec,
    VariableSpec,
    VerificationCase,
)


def _evaluate(n1: float, n2: float) -> float:
    non_negative("n1", n1)
    non_negative("n2", n2)
    total = finite_result(n1 + n2)
    if total == 0:
        raise ValueError("at least one gas amount must be positive")
    terms = [(n, math.log(total) - math.log(n)) for n in (n1, n2) if n > 0]
    return finite_result(MOLAR_GAS_CONSTANT * math.fsum(n * log_ratio for n, log_ratio in terms))


ideal_binary_gas_mixing_entropy = FormulaSpec(
    id="thermodynamics.ideal_binary_gas_mixing_entropy",
    name="Ideal Binary Gas Mixing Entropy",
    equation="delta_S_mix = -R_u*(n1*ln(x1) + n2*ln(x2))",
    description="Ideal two-species gas mixing entropy.",
    inputs=(
        VariableSpec(
            name="n1",
            symbol="n1",
            description="Amount of ideal gas species 1",
            dimension="N",
            si_unit="mol",
        ),
        VariableSpec(
            name="n2",
            symbol="n2",
            description="Amount of a distinct ideal gas species 2",
            dimension="N",
            si_unit="mol",
        ),
    ),
    output=VariableSpec(
        name="delta_S_mix",
        symbol="delta_S_mix",
        description="Entropy of mixing",
        dimension="M L^2 T^-2 Theta^-1",
        si_unit="J/K",
    ),
    evaluator=_evaluate,
    references=(
        ReferenceSpec(
            source_type="official_web",
            title="4.6 Entropy",
            organization="OpenStax",
            url="https://openstax.org/books/university-physics-volume-2/pages/4-6-entropy",
            accessed="2026-10-10",
        ),
        bipm_si_defining_constants(),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"n1": 1, "n2": 1},
            expected=11.52629264328796,
            note="Two distinct gases each expand twofold; independent Decimal 2 R ln(2).",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"n1": 1, "n2": 0},
            expected=0,
            note="Only one species gives zero mixing entropy.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "Derived result: Apply the reversible ideal-gas expansion entropy n*R*ln(V_final/V_initial) separately to each gas; x_i=n_i/(n1+n2).",
        "Initially separate distinct ideal gases at the same temperature and pressure; final mixture at that temperature.",
        "Species must be distinguishable; do not label two portions of the same gas as distinct species.",
        "At least one gas amount must be positive.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "thermodynamics", "ideal binary gas mixing entropy"),
)
