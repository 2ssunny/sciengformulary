"""Reaction Gibbs energy from a reversible cell potential."""

from sciengformulary.catalog._constants import (
    FARADAY_CONSTANT,
)
from sciengformulary.catalog._domain import finite, finite_result, integer
from sciengformulary.catalog._sources import (
    bipm_si_defining_constants,
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(z: float, E: float) -> float:
    z = integer("z", z, minimum=1)
    finite("E", E)
    return finite_result(-z * FARADAY_CONSTANT * E)


reaction_gibbs_from_potential = FormulaSpec(
    id="electrochemistry.reaction_gibbs_from_potential",
    name="Reaction Gibbs From Potential",
    equation="delta_G = -z*F*E",
    description="Reaction Gibbs energy from a reversible cell potential.",
    inputs=(
        VariableSpec(
            name="z",
            symbol="z",
            description="Electrons transferred per balanced reaction",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="E",
            symbol="E",
            description="Reversible cell potential",
            dimension="M L^2 T^-3 I^-1",
            si_unit="V",
        ),
    ),
    output=VariableSpec(
        name="delta_G",
        symbol="delta_G",
        description="Molar reaction Gibbs energy",
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
            inputs={"z": 1, "E": 1},
            expected=-96485.33212331001,
            note="One electron and one volt gives -F J/mol.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"z": 2, "E": 0},
            expected=0,
            note="Zero potential gives zero Gibbs energy.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "E is the reversible potential for the specified reaction.",
        "Using E_standard yields delta_G_standard; reaction direction and electron count must match.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "electrochemistry", "reaction gibbs from potential"),
)
