"""Rigid diatomic moment of inertia."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import (
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(mu: float, r: float) -> float:
    positive("mu", mu)
    positive("r", r)
    return finite_result(mu * r**2)


diatomic_moment_of_inertia = FormulaSpec(
    id="spectroscopy.diatomic_moment_of_inertia",
    name="Diatomic Moment Of Inertia",
    equation="I = mu*r^2",
    description="Rigid diatomic moment of inertia.",
    inputs=(
        VariableSpec(
            name="mu", symbol="mu", description="Two-body reduced mass", dimension="M", si_unit="kg"
        ),
        VariableSpec(
            name="r", symbol="r", description="Internuclear separation", dimension="L", si_unit="m"
        ),
    ),
    output=VariableSpec(
        name="I",
        symbol="I",
        description="Moment of inertia about an axis through the center of mass perpendicular to the bond",
        dimension="M L^2",
        si_unit="kg*m^2",
    ),
    evaluator=_evaluate,
    references=(
        openstax_section(
            "university-physics-volume-3",
            "9-2-molecular-spectra",
            "9.2 Molecular Spectra",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"mu": 1, "r": 2},
            expected=4,
            note="Reduced mass one and separation two give inertia four.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"mu": 2, "r": 2},
            expected=8,
            note="Doubling reduced mass doubles moment of inertia.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Rigid diatomic molecule modeled as two point masses.",
        "The rotational axis is perpendicular to the bond and passes through the center of mass.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "spectroscopy", "diatomic moment of inertia"),
)
