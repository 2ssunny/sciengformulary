"""Harmonic diatomic stretching wavenumber."""

import math

from sciengformulary.catalog._constants import (
    SPEED_OF_LIGHT,
)
from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import (
    bipm_si_defining_constants,
    macmillan_reduced_mass,
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(k: float, mu: float) -> float:
    positive("k", k)
    positive("mu", mu)
    return finite_result(math.sqrt(k / mu) / (2 * math.pi * SPEED_OF_LIGHT))


diatomic_vibrational_wavenumber = FormulaSpec(
    id="spectroscopy.diatomic_vibrational_wavenumber",
    name="Diatomic Vibrational Wavenumber",
    equation="wavenumber = sqrt(k/mu)/(2*pi*c0)",
    description="Harmonic diatomic stretching wavenumber.",
    inputs=(
        VariableSpec(
            name="k",
            symbol="k",
            description="Harmonic bond force constant",
            dimension="M T^-2",
            si_unit="N/m",
        ),
        VariableSpec(
            name="mu", symbol="mu", description="Two-body reduced mass", dimension="M", si_unit="kg"
        ),
    ),
    output=VariableSpec(
        name="wavenumber",
        symbol="wavenumber",
        description="Harmonic vibrational wavenumber",
        dimension="L^-1",
        si_unit="1/m",
    ),
    evaluator=_evaluate,
    references=(
        openstax_section(
            "university-physics-volume-3",
            "7-5-the-quantum-harmonic-oscillator",
            "7.5 The Quantum Harmonic Oscillator",
            accessed="2026-10-10",
        ),
        macmillan_reduced_mass(
            accessed="2026-10-10",
        ),
        bipm_si_defining_constants(),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"k": 39.47841760435743, "mu": 1},
            expected=3.3356409519815204e-09,
            note="Chosen k gives frequency one Hz, hence wavenumber 1/c0.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"k": 157.91367041742973, "mu": 1},
            expected=6.671281903963041e-09,
            note="Fourfold k doubles frequency and wavenumber.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Derived result: Use omega=sqrt(k/mu), nu=omega/(2*pi) and spectroscopic wavenumber=nu/c0.",
        "Isolated diatomic harmonic stretching model; small displacements near equilibrium.",
        "Actual polyatomic normal modes and anharmonic transitions require additional treatment.",
        "Output m^-1; divide by 100 for cm^-1.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "spectroscopy", "diatomic vibrational wavenumber"),
)
