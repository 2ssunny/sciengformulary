"""Electric charge transferred by a constant current."""

from sciengformulary.catalog._domain import finite, finite_result, non_negative
from sciengformulary.catalog._sources import (
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(I: float, t: float) -> float:  # noqa: E741 - symbols as written in the source
    finite("I", I)
    non_negative("t", t)
    return finite_result(I * t)


constant_current_charge = FormulaSpec(
    id="electrochemistry.constant_current_charge",
    name="Constant Current Charge",
    equation="Q_electric = I*t",
    description="Electric charge transferred by a constant current.",
    inputs=(
        VariableSpec(
            name="I", symbol="I", description="Signed constant current", dimension="I", si_unit="A"
        ),
        VariableSpec(name="t", symbol="t", description="Duration", dimension="T", si_unit="s"),
    ),
    output=VariableSpec(
        name="Q_electric",
        symbol="Q_electric",
        description="Transferred electric charge",
        dimension="I T",
        si_unit="C",
    ),
    evaluator=_evaluate,
    references=(
        openstax_section(
            "chemistry-2e",
            "17-7-electrolysis",
            "17.7 Electrolysis",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"I": 2, "t": 30},
            expected=60,
            note="2 A for 30 s transfers 60 C.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"I": -2, "t": 30},
            expected=-60,
            note="Reversing current reverses signed transferred charge.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Derived result: Use the source current-times-time relation in the electrolysis charge calculation.",
        "Current is constant; variable current requires integration.",
        "Keep a consistent sign convention for current and transferred charge.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "electrochemistry", "constant current charge"),
)
