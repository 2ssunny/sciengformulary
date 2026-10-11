"""Signed mass measurement error in parts per million."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.core import (
    FormulaSpec,
    ReferenceSpec,
    VariableSpec,
    VerificationCase,
)


def _evaluate(m_measured: float, m_reference: float) -> float:
    positive("m_measured", m_measured)
    positive("m_reference", m_reference)
    return finite_result(1e6 * ((m_measured - m_reference) / m_reference))


mass_error_ppm = FormulaSpec(
    id="spectroscopy.mass_error_ppm",
    name="Mass Error Ppm",
    equation="error_ppm = 1e6*(m_measured-m_reference)/m_reference",
    description="Signed mass measurement error in parts per million.",
    inputs=(
        VariableSpec(
            name="m_measured",
            symbol="m_measured",
            description="Measured mass or consistently scaled mass-to-charge value",
            dimension="M",
            si_unit="kg",
        ),
        VariableSpec(
            name="m_reference",
            symbol="m_reference",
            description="Reference mass on the same scale",
            dimension="M",
            si_unit="kg",
        ),
    ),
    output=VariableSpec(
        name="error_ppm",
        symbol="error_ppm",
        description="Signed numerical mass error in ppm",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        ReferenceSpec(
            source_type="official_web",
            title="A Framework for Utilizing High Resolution Mass Spectrometry and Non-Targeted Analysis (NTA) in Rapid Response and Emergency Situations",
            organization="U.S. Environmental Protection Agency",
            url="https://pmc.ncbi.nlm.nih.gov/articles/PMC9280853/",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"m_measured": 1001, "m_reference": 1000},
            expected=1000,
            note="A relative excess of 1/1000 equals 1000 ppm.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"m_measured": 999, "m_reference": 1000},
            expected=-1000,
            note="A relative deficit of 1/1000 equals -1000 ppm.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Derived result: Express relative mass difference as parts per million, using the source definition of ppm mass error.",
        "Measured and reference values refer to the same ion, isotope composition, adduct and charge state.",
        "Signed relative error; this does not predict instrument calibration performance.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "spectroscopy", "mass error ppm"),
)
