"""Steady-State Forced Vibration Amplitude."""

import math

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    F0: float,  # noqa: N803
    m: float,
    k: float,
    b: float,
    omega: float,
) -> float:
    return F0 / math.sqrt(m**2 * (omega**2 - k / m) ** 2 + b**2 * omega**2)


forced_vibration_amplitude = FormulaSpec(
    id="mechanics.forced_vibration_amplitude",
    name="Steady-State Forced Vibration Amplitude",
    equation="A = F0 / sqrt(m^2 * (omega^2 - k / m)^2 + b^2 * omega^2)",
    description=(
        "Amplitude of the steady oscillation of a damped mass-spring system driven by a sinusoidal "
        "force of amplitude F0 and angular frequency omega."
    ),
    inputs=(
        VariableSpec(
            name="F0",
            symbol="F_0",
            description="Amplitude of the sinusoidal driving force",
            dimension="M L T^-2",
            si_unit="N",
        ),
        VariableSpec(
            name="m",
            symbol="m",
            description="Mass of the body",
            dimension="M",
            si_unit="kg",
        ),
        VariableSpec(
            name="k",
            symbol="k",
            description="Linear spring stiffness",
            dimension="M T^-2",
            si_unit="N/m",
        ),
        VariableSpec(
            name="b",
            symbol="b",
            description="Viscous damping coefficient (damping force = -b times velocity)",
            dimension="M T^-1",
            si_unit="kg/s",
        ),
        VariableSpec(
            name="omega",
            symbol=r"\omega",
            description="Angular frequency of the driving force",
            dimension="T^-1",
            si_unit="rad/s",
        ),
    ),
    output=VariableSpec(
        name="A",
        symbol="A",
        description="Steady-state displacement amplitude",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes omega_0^2 for k/m. The sheet's form F0 / sqrt((k - m nu^2)^2 + (c
        # nu)^2) is the same with nu = omega and c = b.
        openstax_university_physics(1, "15-6-forced-oscillations", "sec. 15.6, eq. (15.29)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"F0": 10.0, "m": 2.0, "k": 200.0, "b": 8.0, "omega": 8.0},
            expected=0.10380684981717496,
            rel_tol=1e-12,
            note=(
                "Independent 40-digit decimal evaluation: 10 / sqrt(4 * 36^2 + 64 * 64) = 10 / "
                "sqrt(9280)."
            ),
        ),
    ),
    assumptions=(
        "Single-degree-of-freedom mass-spring-damper with linear spring and viscous damping; "
        "the damping force is proportional to velocity.",
        "Steady state only, after the transient has decayed.",
        "With b = 0 the amplitude is unbounded at omega^2 = k/m (resonance).",
    ),
    tags=("forced vibration", "resonance", "frequency response", "driven oscillator"),
)
