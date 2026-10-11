"""Spectroscopic inverse wavelength."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import (
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(lambda_vac: float) -> float:
    positive("lambda_vac", lambda_vac)
    return finite_result(1 / lambda_vac)


vacuum_wavenumber = FormulaSpec(
    id="spectroscopy.vacuum_wavenumber",
    name="Vacuum Wavenumber",
    equation="wavenumber = 1/lambda_vac",
    description="Spectroscopic inverse wavelength.",
    inputs=(
        VariableSpec(
            name="lambda_vac",
            symbol="lambda_vac",
            description="Vacuum wavelength",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="wavenumber",
        symbol="wavenumber",
        description="Vacuum spectroscopic wavenumber",
        dimension="L^-1",
        si_unit="1/m",
    ),
    evaluator=_evaluate,
    references=(
        openstax_section(
            "chemistry-2e",
            "6-1-electromagnetic-energy",
            "6.1 Electromagnetic Energy",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"lambda_vac": 1e-06},
            expected=1000000.0,
            note="One micrometre gives 1e6 m^-1 = 10000 cm^-1.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"lambda_vac": 1},
            expected=1,
            note="One metre gives one inverse metre.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Spectroscopic wavenumber, not angular wavenumber 2*pi/lambda.",
        "Output is m^-1; divide by 100 to display cm^-1.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "spectroscopy", "vacuum wavenumber"),
)
