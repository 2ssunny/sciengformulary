"""Reduced mass for two-body molecular models."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import (
    macmillan_reduced_mass,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(m1: float, m2: float) -> float:
    positive("m1", m1)
    positive("m2", m2)
    return finite_result(min(m1, m2) / (1 + min(m1, m2) / max(m1, m2)))


reduced_mass = FormulaSpec(
    id="spectroscopy.reduced_mass",
    name="Reduced Mass",
    equation="mu = m1*m2/(m1+m2)",
    description="Reduced mass for two-body molecular models.",
    inputs=(
        VariableSpec(
            name="m1", symbol="m1", description="Mass of particle 1", dimension="M", si_unit="kg"
        ),
        VariableSpec(
            name="m2", symbol="m2", description="Mass of particle 2", dimension="M", si_unit="kg"
        ),
    ),
    output=VariableSpec(
        name="mu", symbol="mu", description="Two-body reduced mass", dimension="M", si_unit="kg"
    ),
    evaluator=_evaluate,
    references=(
        macmillan_reduced_mass(
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"m1": 2, "m2": 2},
            expected=1,
            note="Equal masses have reduced mass equal to half either mass.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"m1": 2, "m2": 3},
            expected=1.2,
            note="1/mu=1/2+1/3, so mu=6/5.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Nonrelativistic two-body relative-motion reduction.",
        "For diatomic vibration use individual atomic masses, not molar masses.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "spectroscopy", "reduced mass"),
)
