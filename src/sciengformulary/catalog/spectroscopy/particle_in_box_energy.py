"""One-dimensional infinite-well energy levels."""

from sciengformulary.catalog._constants import (
    PLANCK_CONSTANT,
)
from sciengformulary.catalog._domain import finite_result, integer, positive
from sciengformulary.catalog._sources import bipm_si_defining_constants
from sciengformulary.core import (
    FormulaSpec,
    ReferenceSpec,
    VariableSpec,
    VerificationCase,
)


def _evaluate(n: float, m: float, L: float) -> float:
    n = integer("n", n, minimum=1)
    positive("m", m)
    positive("L", L)
    return finite_result(n**2 * PLANCK_CONSTANT**2 / (8 * m * L**2))


particle_in_box_energy = FormulaSpec(
    id="spectroscopy.particle_in_box_energy",
    name="Particle In Box Energy",
    equation="E_n = n^2*h^2/(8*m*L^2)",
    description="One-dimensional infinite-well energy levels.",
    inputs=(
        VariableSpec(
            name="n",
            symbol="n",
            description="Positive integer quantum number",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="m", symbol="m", description="Particle mass", dimension="M", si_unit="kg"
        ),
        VariableSpec(name="L", symbol="L", description="Box length", dimension="L", si_unit="m"),
    ),
    output=VariableSpec(
        name="E_n",
        symbol="E_n",
        description="Energy of the box eigenstate",
        dimension="M L^2 T^-2",
        si_unit="J",
    ),
    evaluator=_evaluate,
    references=(
        ReferenceSpec(
            source_type="official_web",
            title="7.4 The Quantum Particle in a Box",
            organization="OpenStax",
            url="https://openstax.org/books/university-physics-volume-3/pages/7-4-the-quantum-particle-in-a-box",
            accessed="2026-10-10",
        ),
        bipm_si_defining_constants(),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"n": 1, "m": 1, "L": 1},
            expected=5.488100704090128e-68,
            note="Independent Decimal h squared divided by eight.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"n": 2, "m": 1, "L": 1},
            expected=2.1952402816360512e-67,
            note="n=2 energy is four times the n=1 energy.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Nonrelativistic particle in a one-dimensional infinite square well.",
        "Potential is zero inside the box; n starts at one.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "spectroscopy", "particle in box energy"),
)
