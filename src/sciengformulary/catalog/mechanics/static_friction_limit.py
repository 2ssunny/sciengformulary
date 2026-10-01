"""Limiting Static Friction: f_s_max = mu_s * N."""

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(mu_s: float, N: float) -> float:  # noqa: N803 - symbols as written in the source
    return mu_s * N


static_friction_limit = FormulaSpec(
    id="mechanics.static_friction_limit",
    name="Limiting Static Friction",
    equation="f_s_max = mu_s * N",
    description="Largest static friction force a dry contact can supply before sliding starts.",
    inputs=(
        VariableSpec(
            name="mu_s",
            symbol=r"\mu_s",
            description="Coefficient of static friction for the surface pair",
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
        name="f_s_max",
        symbol="f_{s,max}",
        description="Maximum static friction force",
        dimension="M L T^-2",
        si_unit="N",
    ),
    evaluator=_evaluate,
    references=(
        openstax_university_physics(1, "6-2-friction", "sec. 6.2, eq. (6.1)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"mu_s": 0.45, "N": 980.0},
            expected=441.0,
            rel_tol=1e-12,
            note="Hand calculation: 0.45 * 980 = 441 N.",
        ),
    ),
    assumptions=(
        "Dry (Coulomb) friction; lubricated or viscous contacts do not follow it.",
        "This is an upper bound: below impending motion the actual static friction equals "
        "whatever balances the applied force.",
        "mu_s is an empirical property of the particular surface pair and condition.",
    ),
    tags=("friction", "static friction", "Coulomb friction", "impending motion"),
)
