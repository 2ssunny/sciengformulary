"""de Broglie matter-wave wavelength."""

from sciengformulary.catalog._constants import (
    PLANCK_CONSTANT,
)
from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import bipm_si_defining_constants
from sciengformulary.core import (
    FormulaSpec,
    ReferenceSpec,
    VariableSpec,
    VerificationCase,
)


def _evaluate(p: float) -> float:
    positive("p", p)
    return finite_result(PLANCK_CONSTANT / p)


de_broglie_wavelength = FormulaSpec(
    id="spectroscopy.de_broglie_wavelength",
    name="De Broglie Wavelength",
    equation="lambda = h/p",
    description="de Broglie matter-wave wavelength.",
    inputs=(
        VariableSpec(
            name="p",
            symbol="p",
            description="Magnitude of particle momentum",
            dimension="M L T^-1",
            si_unit="kg*m/s",
        ),
    ),
    output=VariableSpec(
        name="lambda",
        symbol="lambda",
        description="Matter-wave wavelength",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        ReferenceSpec(
            source_type="official_web",
            title="6.5 De Broglie’s Matter Waves",
            organization="OpenStax",
            url="https://openstax.org/books/university-physics-volume-3/pages/6-5-de-broglies-matter-waves",
            accessed="2026-10-10",
        ),
        bipm_si_defining_constants(),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"p": 1},
            expected=6.62607015e-34,
            note="One kg m/s gives numerical wavelength h in metres.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"p": 2},
            expected=3.313035075e-34,
            note="Doubling momentum halves wavelength.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "p is momentum, not kinetic energy; for relativistic particles use relativistic momentum.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "spectroscopy", "de broglie wavelength"),
)
