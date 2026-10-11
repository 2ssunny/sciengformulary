"""Radiation wavelength in vacuum."""

from sciengformulary.catalog._constants import (
    SPEED_OF_LIGHT,
)
from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import (
    bipm_si_defining_constants,
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(nu: float) -> float:
    positive("nu", nu)
    return finite_result(SPEED_OF_LIGHT / nu)


vacuum_wavelength = FormulaSpec(
    id="spectroscopy.vacuum_wavelength",
    name="Vacuum Wavelength",
    equation="lambda_vac = c0 / nu",
    description="Radiation wavelength in vacuum.",
    inputs=(
        VariableSpec(
            name="nu",
            symbol="nu",
            description="Radiation frequency",
            dimension="T^-1",
            si_unit="Hz",
        ),
    ),
    output=VariableSpec(
        name="lambda_vac",
        symbol="lambda_vac",
        description="Vacuum wavelength",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        openstax_section(
            "chemistry-2e",
            "6-1-electromagnetic-energy",
            "6.1 Electromagnetic Energy",
            accessed="2026-10-10",
        ),
        bipm_si_defining_constants(),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"nu": 299792458},
            expected=1,
            note="At frequency c0 Hz, wavelength is exactly one metre.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"nu": 299792458000000},
            expected=1e-06,
            note="Frequency c0 times 1e6 corresponds to one micrometre.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Vacuum wavelength; in a material use the appropriate phase velocity rather than c0.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "spectroscopy", "vacuum wavelength"),
)
