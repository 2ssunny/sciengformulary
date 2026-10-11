"""Standard reaction Gibbs energy from equilibrium."""

import math

from sciengformulary.catalog._constants import (
    MOLAR_GAS_CONSTANT,
)
from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import (
    bipm_si_defining_constants,
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(T: float, K: float) -> float:
    positive("T", T)
    positive("K", K)
    return finite_result(-MOLAR_GAS_CONSTANT * T * math.log(K))


standard_reaction_gibbs_energy = FormulaSpec(
    id="thermodynamics.standard_reaction_gibbs_energy",
    name="Standard Reaction Gibbs Energy",
    equation="delta_G_standard = -R_u * T * ln(K)",
    description="Standard reaction Gibbs energy from equilibrium.",
    inputs=(
        VariableSpec(
            name="T", symbol="T", description="Absolute temperature", dimension="Theta", si_unit="K"
        ),
        VariableSpec(
            name="K",
            symbol="K",
            description="Dimensionless thermodynamic equilibrium constant",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="delta_G_standard",
        symbol="delta_G_standard",
        description="Standard molar reaction Gibbs energy",
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
            inputs={"T": 300, "K": 1},
            expected=0,
            note="ln(1) = 0 gives zero standard Gibbs energy.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
        VerificationCase(
            inputs={"T": 300, "K": 2.718281828459045},
            expected=-2494.338785445972,
            note="ln(e) = 1; independent Decimal product -300 R.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "K is based on dimensionless activities and the chosen standard states.",
        "SI temperature; natural logarithm; molar reaction basis.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "thermodynamics", "standard reaction gibbs energy"),
)
