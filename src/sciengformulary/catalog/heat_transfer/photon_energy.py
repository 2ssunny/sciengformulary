"""Photon Energy: E = h * nu."""

from sciengformulary.catalog._constants import (
    PLANCK_CONSTANT,
    PLANCK_CONSTANT_REFERENCE,
)
from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(nu: float) -> float:
    return PLANCK_CONSTANT * nu


photon_energy = FormulaSpec(
    id="heat_transfer.photon_energy",
    name="Photon Energy",
    equation="E = h * nu",
    description="Energy of one photon of a given frequency.",
    inputs=(
        VariableSpec(
            name="nu",
            symbol=r"\nu",
            description="Photon frequency",
            dimension="T^-1",
            si_unit="Hz",
        ),
    ),
    output=VariableSpec(
        name="E",
        symbol="E",
        description="Photon energy",
        dimension="M L^2 T^-2",
        si_unit="J",
    ),
    evaluator=_evaluate,
    references=(
        openstax_university_physics(3, "6-2-photoelectric-effect", "sec. 6.2, eq. (6.13)"),
        PLANCK_CONSTANT_REFERENCE,
    ),
    verification_cases=(
        VerificationCase(
            inputs={"nu": 500000000000000.0},
            expected=3.313035075e-19,
            rel_tol=1e-12,
            note="Exact arithmetic: 6.62607015e-34 * 5e14.",
        ),
    ),
    assumptions=(
        "nu is a frequency in hertz, not a wavelength or an angular frequency.",
    ),
    tags=("photon", "Planck", "quantum", "radiation", "frequency"),
)
