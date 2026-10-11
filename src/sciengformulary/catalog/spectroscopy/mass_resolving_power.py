"""Mass-spectrometric resolving power with an explicit width convention."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.core import (
    FormulaSpec,
    ReferenceSpec,
    VariableSpec,
    VerificationCase,
)


def _evaluate(m: float, delta_m: float) -> float:
    positive("m", m)
    positive("delta_m", delta_m)
    return finite_result(m / delta_m)


mass_resolving_power = FormulaSpec(
    id="spectroscopy.mass_resolving_power",
    name="Mass Resolving Power",
    equation="R_m = m/delta_m",
    description="Mass-spectrometric resolving power with an explicit width convention.",
    inputs=(
        VariableSpec(
            name="m",
            symbol="m",
            description="Mass at which resolving power is evaluated",
            dimension="M",
            si_unit="kg",
        ),
        VariableSpec(
            name="delta_m",
            symbol="delta_m",
            description="Peak mass width or separation measured with a declared criterion",
            dimension="M",
            si_unit="kg",
        ),
    ),
    output=VariableSpec(
        name="R_m", symbol="R_m", description="Mass resolving power", dimension="1", si_unit="-"
    ),
    evaluator=_evaluate,
    references=(
        ReferenceSpec(
            source_type="technical_report",
            title="Molecular Mass Distribution Measurement by Mass Spectrometry",
            organization="National Institute of Standards and Technology",
            url="https://www.govinfo.gov/content/pkg/GOVPUB-C13-82e3bd6da4b35d4156deae064324462c/pdf/GOVPUB-C13-82e3bd6da4b35d4156deae064324462c.pdf",
            accessed="2026-10-10",
            authors=("W. E. Wallace", "C. M. Guttman"),
            report_number="NIST SP 960-21",
            year=2010,
            locator="sec. 2.2",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"m": 100, "delta_m": 0.01},
            expected=10000,
            note="100/0.01=10000; any common mass unit gives the same ratio.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"m": 200, "delta_m": 0.01},
            expected=20000,
            note="At the same width, twice the mass gives twice the ratio.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Mass and delta_m use the same unit and compatible charge state; an m/z ratio can equivalently be used when its width uses the same scale.",
        "Declare the width criterion (for example FWHM or a specified valley criterion) when reporting the result.",
        "Peak separation and single-peak width conventions are not automatically interchangeable.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "spectroscopy", "mass resolving power"),
)
