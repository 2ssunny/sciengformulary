"""Reaction Gibbs energy away from standard composition."""

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


def _evaluate(delta_G_standard: float, T: float, Q: float) -> float:
    finite("delta_G_standard", delta_G_standard)
    positive("T", T)
    positive("Q", Q)
    return finite_result(delta_G_standard + MOLAR_GAS_CONSTANT * T * math.log(Q))


reaction_gibbs_energy = FormulaSpec(
    id="thermodynamics.reaction_gibbs_energy",
    name="Reaction Gibbs Energy",
    equation="delta_G = delta_G_standard + R_u * T * ln(Q)",
    description="Reaction Gibbs energy away from standard composition.",
    inputs=(
        VariableSpec(
            name="delta_G_standard",
            symbol="delta_G_standard",
            description="Standard molar reaction Gibbs energy",
            dimension="M L^2 T^-2 N^-1",
            si_unit="J/mol",
        ),
        VariableSpec(
            name="T", symbol="T", description="Absolute temperature", dimension="Theta", si_unit="K"
        ),
        VariableSpec(
            name="Q",
            symbol="Q",
            description="Dimensionless reaction quotient",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="delta_G",
        symbol="delta_G",
        description="Molar reaction Gibbs energy at the given composition",
        dimension="M L^2 T^-2 N^-1",
        si_unit="J/mol",
    ),
    evaluator=_evaluate,
    references=(
        openstax_section(
            "chemistry-2e",
            "16-4-free-energy",
            "16.4 Free Energy",
            accessed="2026-10-10",
        ),
        bipm_si_defining_constants(),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"delta_G_standard": -10000, "T": 300, "Q": 1},
            expected=-10000,
            note="Q = 1 removes the composition correction.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"delta_G_standard": 0, "T": 300, "Q": 2.718281828459045},
            expected=2494.338785445972,
            note="ln(e)=1 gives 300 R in J/mol.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Q uses activities consistent with the standard states of delta_G_standard.",
        "Use SI temperature and the same balanced reaction normalization.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "thermodynamics", "reaction gibbs energy"),
)
