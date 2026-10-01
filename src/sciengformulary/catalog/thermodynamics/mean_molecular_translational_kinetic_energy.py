"""Mean Translational Kinetic Energy of a Gas Molecule: KE_avg = 3 * k_B * T / 2."""

from sciengformulary.catalog._constants import (
    BOLTZMANN_CONSTANT,
    BOLTZMANN_CONSTANT_REFERENCE,
)
from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(T: float) -> float:  # noqa: N803 - symbols as written in the source
    return 1.5 * BOLTZMANN_CONSTANT * T


mean_molecular_translational_kinetic_energy = FormulaSpec(
    id="thermodynamics.mean_molecular_translational_kinetic_energy",
    name="Mean Translational Kinetic Energy of a Gas Molecule",
    equation="KE_avg = 3 * k_B * T / 2",
    description="Average translational kinetic energy per molecule of an ideal gas.",
    inputs=(
        VariableSpec(
            name="T",
            symbol="T",
            description="Absolute temperature",
            dimension="Theta",
            si_unit="K",
        ),
    ),
    output=VariableSpec(
        name="KE_avg",
        symbol=r"\overline{K}",
        description="Mean translational kinetic energy per molecule",
        dimension="M L^2 T^-2",
        si_unit="J",
    ),
    evaluator=_evaluate,
    references=(
        openstax_university_physics(
            2,
            "2-2-pressure-temperature-and-rms-speed",
            "sec. 2.2, eq. (2.6)",
        ),
        BOLTZMANN_CONSTANT_REFERENCE,
    ),
    verification_cases=(
        VerificationCase(
            inputs={"T": 300.0},
            expected=6.2129205e-21,
            rel_tol=1e-12,
            note="Exact arithmetic: 1.5 * 1.380649e-23 * 300.",
        ),
    ),
    assumptions=(
        "Dilute ideal gas in thermal equilibrium (kinetic theory); T must be absolute.",
        "Translational energy only; rotation and vibration add energy for polyatomic molecules.",
    ),
    tags=("kinetic theory", "molecular energy", "Boltzmann constant", "temperature"),
)
