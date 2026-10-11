"""Rigid-rotor energy levels."""

import math

from sciengformulary.catalog._constants import (
    PLANCK_CONSTANT,
)
from sciengformulary.catalog._domain import finite_result, integer, positive
from sciengformulary.catalog._sources import (
    bipm_si_defining_constants,
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(J: float, I: float) -> float:  # noqa: E741 - symbols as written in the source
    J = integer("J", J, minimum=0)
    positive("I", I)
    return finite_result(J * (J + 1) * PLANCK_CONSTANT**2 / (8 * math.pi**2 * I))


rigid_rotor_energy = FormulaSpec(
    id="spectroscopy.rigid_rotor_energy",
    name="Rigid Rotor Energy",
    equation="E_J = J*(J+1)*h^2/(8*pi^2*I)",
    description="Rigid-rotor energy levels.",
    inputs=(
        VariableSpec(
            name="J",
            symbol="J",
            description="Rotational quantum number",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="I",
            symbol="I",
            description="Rigid-rotor moment of inertia",
            dimension="M L^2",
            si_unit="kg*m^2",
        ),
    ),
    output=VariableSpec(
        name="E_J",
        symbol="E_J",
        description="Rigid-rotor rotational energy",
        dimension="M L^2 T^-2",
        si_unit="J",
    ),
    evaluator=_evaluate,
    references=(
        openstax_section(
            "university-physics-volume-3",
            "9-2-molecular-spectra",
            "9.2 Molecular Spectra",
            accessed="2026-10-10",
        ),
        bipm_si_defining_constants(),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"J": 0, "I": 1},
            expected=0,
            note="Rotational ground state J=0 has zero energy in this model.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
        VerificationCase(
            inputs={"J": 1, "I": 1},
            expected=1.1121217185735183e-68,
            note="For J=1, E=h^2/(4*pi^2*I); Decimal arithmetic determines the h^2 numerator.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Rigid diatomic rotor; centrifugal distortion and fine structure excluded.",
        "Energy levels alone do not ensure dipole-allowed transitions.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "spectroscopy", "rigid rotor energy"),
)
