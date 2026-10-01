"""Entropy Change for Reversible Isothermal Heat: delta_S = Q / T."""

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(Q: float, T: float) -> float:  # noqa: N803 - symbols as written in the source
    return Q / T


isothermal_entropy_change = FormulaSpec(
    id="thermodynamics.isothermal_entropy_change",
    name="Entropy Change for Reversible Isothermal Heat",
    equation="delta_S = Q / T",
    description=(
        "Entropy change of a system that absorbs heat Q reversibly at constant absolute "
        "temperature T."
    ),
    inputs=(
        VariableSpec(
            name="Q",
            symbol="Q",
            description="Heat absorbed by the system (negative if released)",
            dimension="M L^2 T^-2",
            si_unit="J",
        ),
        VariableSpec(
            name="T",
            symbol="T",
            description="Absolute temperature",
            dimension="Theta",
            si_unit="K",
        ),
    ),
    output=VariableSpec(
        name="delta_S",
        symbol=r"\Delta S",
        description="Entropy change",
        dimension="M L^2 T^-2 Theta^-1",
        si_unit="J/K",
    ),
    evaluator=_evaluate,
    references=(
        openstax_university_physics(2, "4-6-entropy", "sec. 4.6, eq. (4.8)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"Q": 1000.0, "T": 250.0},
            expected=4.0,
            rel_tol=1e-12,
            note="Hand calculation: 1000 / 250 = 4 J/K.",
        ),
    ),
    assumptions=(
        "Reversible heat transfer at constant T (for example a large reservoir or a phase "
        "change); for varying T integrate dQ/T.",
    ),
    tags=("entropy", "second law", "reservoir", "phase change"),
)
