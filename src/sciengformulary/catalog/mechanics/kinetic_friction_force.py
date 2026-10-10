"""Kinetic Friction Force: f_k = mu_k * N."""

from sciengformulary.catalog._sources import (
    doe_fundamentals_handbook,
    openstax_university_physics,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(mu_k: float, N: float) -> float:  # noqa: N803 - symbols as written in the source
    return mu_k * N


kinetic_friction_force = FormulaSpec(
    id="mechanics.kinetic_friction_force",
    name="Kinetic Friction Force",
    equation="f_k = mu_k * N",
    description="Friction force opposing the relative sliding of two dry surfaces.",
    inputs=(
        VariableSpec(
            name="mu_k",
            symbol=r"\mu_k",
            description="Coefficient of kinetic friction for the surface pair",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="N",
            symbol="N",
            description="Normal contact force between the surfaces",
            dimension="M L T^-2",
            si_unit="N",
        ),
    ),
    output=VariableSpec(
        name="f_k",
        symbol="f_k",
        description="Kinetic friction force magnitude",
        dimension="M L T^-2",
        si_unit="N",
    ),
    evaluator=_evaluate,
    references=(
        openstax_university_physics(1, "6-2-friction", "sec. 6.2, eq. (6.2)"),
        doe_fundamentals_handbook(
            "DOE-HDBK-1010-92",
            "Module 4 'Application of Newton's Laws', Types of Force: Friction, eq. (4-6), p. 19 "
            "(CP-04)",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"mu_k": 0.3, "N": 980.0},
            expected=294.0,
            rel_tol=1e-12,
            note="Hand calculation: 0.30 * 980 = 294 N.",
        ),
    ),
    assumptions=(
        "Dry (Coulomb) friction with the surfaces already sliding.",
        "mu_k is empirical, usually smaller than mu_s, and roughly independent of sliding "
        "speed over moderate ranges.",
    ),
    tags=("friction", "kinetic friction", "sliding", "Coulomb friction"),
)
