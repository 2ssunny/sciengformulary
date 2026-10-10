"""Wien's Displacement Law: lambda_max = b / T."""

from sciengformulary.catalog._constants import (
    WIEN_CONSTANT_REFERENCE,
    WIEN_WAVELENGTH_DISPLACEMENT_CONSTANT,
)
from sciengformulary.catalog._sources import (
    lienhard_heat_transfer,
    openstax_university_physics,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(T: float) -> float:  # noqa: N803 - symbols as written in the source
    return WIEN_WAVELENGTH_DISPLACEMENT_CONSTANT / T


wien_peak_wavelength = FormulaSpec(
    id="heat_transfer.wien_peak_wavelength",
    name="Wien's Displacement Law",
    equation="lambda_max = b / T",
    description="Wavelength at which a blackbody's spectral emission per unit wavelength peaks.",
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
        name="lambda_max",
        symbol=r"\lambda_{max}",
        description="Peak wavelength",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes lambda_max T = 2.898e-3 m K; the constant here is the CODATA value.
        openstax_university_physics(3, "6-1-blackbody-radiation", "sec. 6.1, eq. (6.1)"),
        WIEN_CONSTANT_REFERENCE,
        # The book prints the constant to six digits (2897.77 um K).
        lienhard_heat_transfer("sec. 1.3, eq. (1.29), p. 30"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"T": 5778.0},
            expected=5.015181645898235e-07,
            rel_tol=1e-12,
            note=(
                "Independent 40-digit decimal evaluation of 2.897771955e-3 / 5778 (about 0.5 "
                "micrometre for the Sun's surface temperature)."
            ),
        ),
    ),
    assumptions=(
        "Blackbody (or grey body) emitter.",
        "Peak of the per-wavelength spectrum; the per-frequency spectrum peaks at a different "
        "wavelength.",
    ),
    tags=("Wien", "blackbody", "peak wavelength", "thermal radiation"),
)
