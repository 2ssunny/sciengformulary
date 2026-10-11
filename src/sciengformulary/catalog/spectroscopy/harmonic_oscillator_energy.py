"""Harmonic vibrational energy including zero-point energy."""

from sciengformulary.catalog._constants import (
    PLANCK_CONSTANT,
)
from sciengformulary.catalog._domain import finite_result, integer, positive
from sciengformulary.catalog._sources import (
    bipm_si_defining_constants,
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(v: float, nu: float) -> float:
    v = integer("v", v, minimum=0)
    positive("nu", nu)
    return finite_result((v + 0.5) * PLANCK_CONSTANT * nu)


harmonic_oscillator_energy = FormulaSpec(
    id="spectroscopy.harmonic_oscillator_energy",
    name="Harmonic Oscillator Energy",
    equation="E_v = (v+1/2)*h*nu",
    description="Harmonic vibrational energy including zero-point energy.",
    inputs=(
        VariableSpec(
            name="v",
            symbol="v",
            description="Vibrational quantum number",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="nu",
            symbol="nu",
            description="Harmonic oscillator frequency",
            dimension="T^-1",
            si_unit="Hz",
        ),
    ),
    output=VariableSpec(
        name="E_v",
        symbol="E_v",
        description="Energy relative to the potential minimum",
        dimension="M L^2 T^-2",
        si_unit="J",
    ),
    evaluator=_evaluate,
    references=(
        openstax_section(
            "university-physics-volume-3",
            "7-5-the-quantum-harmonic-oscillator",
            "7.5 The Quantum Harmonic Oscillator",
            accessed="2026-10-10",
        ),
        bipm_si_defining_constants(),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"v": 0, "nu": 1},
            expected=3.313035075e-34,
            note="Zero-point energy is h/2 at one Hz.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"v": 1, "nu": 1},
            expected=9.939105225e-34,
            note="First excited state is 3h/2 at one Hz.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Ideal quantum harmonic oscillator; anharmonic corrections excluded.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "spectroscopy", "harmonic oscillator energy"),
)
