"""Faraday law product mass with current efficiency."""

from sciengformulary.catalog._constants import (
    FARADAY_CONSTANT,
)
from sciengformulary.catalog._domain import (
    finite,
    finite_result,
    integer,
    non_negative,
    positive,
)
from sciengformulary.catalog._sources import (
    bipm_si_defining_constants,
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(efficiency: float, I: float, t: float, M: float, z: float) -> float:  # noqa: E741 - symbols as written in the source
    finite("efficiency", efficiency)
    if not 0 <= efficiency <= 1:
        raise ValueError("efficiency must be between zero and one")
    non_negative("I", I)
    non_negative("t", t)
    positive("M", M)
    z = integer("z", z, minimum=1)
    return finite_result(efficiency * I * t * M / (z * FARADAY_CONSTANT))


electrolysis_product_mass = FormulaSpec(
    id="electrochemistry.electrolysis_product_mass",
    name="Electrolysis Product Mass",
    equation="m = efficiency*I*t*M/(z*F)",
    description="Faraday law product mass with current efficiency.",
    inputs=(
        VariableSpec(
            name="efficiency",
            symbol="efficiency",
            description="Faradaic current efficiency",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="I",
            symbol="I",
            description="Magnitude of constant current",
            dimension="I",
            si_unit="A",
        ),
        VariableSpec(
            name="t", symbol="t", description="Electrolysis duration", dimension="T", si_unit="s"
        ),
        VariableSpec(
            name="M",
            symbol="M",
            description="Molar mass of deposited or generated product",
            dimension="M N^-1",
            si_unit="kg/mol",
        ),
        VariableSpec(
            name="z",
            symbol="z",
            description="Electrons needed per product formula unit",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="m", symbol="m", description="Generated product mass", dimension="M", si_unit="kg"
    ),
    evaluator=_evaluate,
    references=(
        openstax_section(
            "chemistry-2e",
            "17-7-electrolysis",
            "17.7 Electrolysis",
            accessed="2026-10-10",
        ),
        bipm_si_defining_constants(),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"efficiency": 1, "I": 96485.33212331001, "t": 1, "M": 0.1, "z": 1},
            expected=0.1,
            note="One Faraday gives one mole and 0.1 kg for this molar mass.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"efficiency": 0.5, "I": 96485.33212331001, "t": 1, "M": 0.1, "z": 2},
            expected=0.025,
            note="Half efficiency and two electrons gives one quarter mole.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Constant current and a defined electron-to-product stoichiometry.",
        "Efficiency accounts for competing Faradaic processes, not product purity or collection losses.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "electrochemistry", "electrolysis product mass"),
)
