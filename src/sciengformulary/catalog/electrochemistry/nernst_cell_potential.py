"""Temperature-dependent Nernst equation."""

import math

from sciengformulary.catalog._constants import (
    FARADAY_CONSTANT,
    MOLAR_GAS_CONSTANT,
)
from sciengformulary.catalog._domain import finite, finite_result, integer, positive
from sciengformulary.catalog._sources import bipm_si_defining_constants
from sciengformulary.core import (
    FormulaSpec,
    ReferenceSpec,
    VariableSpec,
    VerificationCase,
)


def _evaluate(E_standard: float, T: float, z: float, Q: float) -> float:
    finite("E_standard", E_standard)
    positive("T", T)
    z = integer("z", z, minimum=1)
    positive("Q", Q)
    return finite_result(E_standard - MOLAR_GAS_CONSTANT * T / (z * FARADAY_CONSTANT) * math.log(Q))


nernst_cell_potential = FormulaSpec(
    id="electrochemistry.nernst_cell_potential",
    name="Nernst Cell Potential",
    equation="E = E_standard - (R_u*T/(z*F))*ln(Q)",
    description="Temperature-dependent Nernst equation.",
    inputs=(
        VariableSpec(
            name="E_standard",
            symbol="E_standard",
            description="Standard cell potential",
            dimension="M L^2 T^-3 I^-1",
            si_unit="V",
        ),
        VariableSpec(
            name="T", symbol="T", description="Absolute temperature", dimension="Theta", si_unit="K"
        ),
        VariableSpec(
            name="z",
            symbol="z",
            description="Number of electrons transferred in the balanced reaction",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="Q",
            symbol="Q",
            description="Dimensionless activity reaction quotient",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="E",
        symbol="E",
        description="Equilibrium cell potential",
        dimension="M L^2 T^-3 I^-1",
        si_unit="V",
    ),
    evaluator=_evaluate,
    references=(
        ReferenceSpec(
            source_type="official_web",
            title="17.4 Potential, Free Energy, and Equilibrium",
            organization="OpenStax",
            url="https://openstax.org/books/chemistry-2e/pages/17-4-potential-free-energy-and-equilibrium",
            accessed="2026-10-10",
        ),
        bipm_si_defining_constants(),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"E_standard": 1, "T": 300, "z": 2, "Q": 1},
            expected=1,
            note="Q=1 gives the standard potential.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"E_standard": 0, "T": 300, "z": 1, "Q": 2.718281828459045},
            expected=-0.025851999786435532,
            note="ln(e)=1; independent Decimal -300R/F.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Reversible equilibrium potential with Q for the same balanced redox reaction.",
        "Activity-based quotient; natural logarithm; SI constants and temperature.",
        "Does not include overpotential, ohmic drop or kinetic polarization under load.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "electrochemistry", "nernst cell potential"),
)
