"""Internal Energy of a Monatomic Ideal Gas: U = 3 * N * k_B * T / 2."""

from sciengformulary.catalog._constants import (
    BOLTZMANN_CONSTANT,
    BOLTZMANN_CONSTANT_REFERENCE,
)
from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(N: float, T: float) -> float:  # noqa: N803 - symbols as written in the source
    return 1.5 * N * BOLTZMANN_CONSTANT * T


monatomic_ideal_gas_internal_energy = FormulaSpec(
    id="thermodynamics.monatomic_ideal_gas_internal_energy",
    name="Internal Energy of a Monatomic Ideal Gas",
    equation="U = 3 * N * k_B * T / 2",
    description="Internal energy of N atoms of a monatomic ideal gas.",
    inputs=(
        VariableSpec(
            name="N",
            symbol="N",
            description="Number of atoms",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="T",
            symbol="T",
            description="Absolute temperature",
            dimension="Theta",
            si_unit="K",
        ),
    ),
    output=VariableSpec(
        name="U",
        symbol="U",
        description="Internal energy",
        dimension="M L^2 T^-2",
        si_unit="J",
    ),
    evaluator=_evaluate,
    references=(
        openstax_university_physics(
            2,
            "2-2-pressure-temperature-and-rms-speed",
            "sec. 2.2, eq. (2.7)",
        ),
        BOLTZMANN_CONSTANT_REFERENCE,
    ),
    verification_cases=(
        VerificationCase(
            inputs={"N": 6.02214076e+23, "T": 300.0},
            expected=3741.508178168958,
            rel_tol=1e-12,
            note="Exact arithmetic for one mole: 1.5 * N_A * k_B * 300.",
        ),
    ),
    assumptions=(
        "Dilute ideal gas in thermal equilibrium (kinetic theory); T must be absolute.",
        "Monatomic gases only (He, Ne, Ar, ...); diatomic and polyatomic gases store "
        "additional rotational and vibrational energy.",
    ),
    tags=("internal energy", "monatomic gas", "kinetic theory", "equipartition"),
)
