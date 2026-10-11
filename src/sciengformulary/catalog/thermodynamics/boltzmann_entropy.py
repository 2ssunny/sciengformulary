"""Entropy from an equiprobable microstate count."""

import math

from sciengformulary.catalog._constants import (
    BOLTZMANN_CONSTANT,
)
from sciengformulary.catalog._domain import finite_result, integer
from sciengformulary.catalog._sources import bipm_si_defining_constants
from sciengformulary.core import (
    FormulaSpec,
    ReferenceSpec,
    VariableSpec,
    VerificationCase,
)


def _evaluate(W: float) -> float:
    W = integer("W", W, minimum=1)
    return finite_result(BOLTZMANN_CONSTANT * math.log(W))


boltzmann_entropy = FormulaSpec(
    id="thermodynamics.boltzmann_entropy",
    name="Boltzmann Entropy",
    equation="S = k_B * ln(W)",
    description="Entropy from an equiprobable microstate count.",
    inputs=(
        VariableSpec(
            name="W",
            symbol="W",
            description="Number of equally probable accessible microstates",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="S",
        symbol="S",
        description="Boltzmann entropy",
        dimension="M L^2 T^-2 Theta^-1",
        si_unit="J/K",
    ),
    evaluator=_evaluate,
    references=(
        ReferenceSpec(
            source_type="official_web",
            title="16.2 Entropy",
            organization="OpenStax",
            url="https://openstax.org/books/chemistry-2e/pages/16-2-entropy",
            accessed="2026-10-10",
        ),
        bipm_si_defining_constants(),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"W": 1},
            expected=0,
            note="One accessible microstate has ln(1)=0.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
        VerificationCase(
            inputs={"W": 2},
            expected=9.569929616929079e-24,
            note="Independent Decimal evaluation of k_B ln(2).",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Accessible microstates are equally probable.",
        "W is a positive integer; this is the entropy of the system, not per mole.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "thermodynamics", "boltzmann entropy"),
)
