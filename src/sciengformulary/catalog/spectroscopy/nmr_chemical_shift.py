"""NMR chemical shift from a frequency offset."""

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.core import (
    FormulaSpec,
    ReferenceSpec,
    VariableSpec,
    VerificationCase,
)


def _evaluate(delta_nu: float, nu_reference: float) -> float:
    finite("delta_nu", delta_nu)
    positive("nu_reference", nu_reference)
    return finite_result(1e6 * (delta_nu / nu_reference))


nmr_chemical_shift = FormulaSpec(
    id="spectroscopy.nmr_chemical_shift",
    name="Nmr Chemical Shift",
    equation="delta_ppm = 1e6*delta_nu/nu_reference",
    description="NMR chemical shift from a frequency offset.",
    inputs=(
        VariableSpec(
            name="delta_nu",
            symbol="delta_nu",
            description="Sample frequency minus reference frequency",
            dimension="T^-1",
            si_unit="Hz",
        ),
        VariableSpec(
            name="nu_reference",
            symbol="nu_reference",
            description="Operating reference frequency in Hz",
            dimension="T^-1",
            si_unit="Hz",
        ),
    ),
    output=VariableSpec(
        name="delta_ppm",
        symbol="delta_ppm",
        description="Numerical chemical shift in ppm",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        ReferenceSpec(
            source_type="official_web",
            title="13.3 Chemical Shifts",
            organization="OpenStax",
            url="https://openstax.org/books/organic-chemistry/pages/13-3-chemical-shifts",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"delta_nu": 1000, "nu_reference": 500000000.0},
            expected=2,
            note="1000 Hz / 500 MHz = 2 ppm.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"delta_nu": -100, "nu_reference": 100000000.0},
            expected=-1,
            note="Upfield frequency offset gives -1 ppm.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Both frequency inputs are in Hz, not MHz.",
        "Return value is the numerical ppm value; a dimensionless relative shift is delta_ppm*1e-6.",
        "Reference and nucleus must match the chosen chemical-shift convention.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "spectroscopy", "nmr chemical shift"),
)
