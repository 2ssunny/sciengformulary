"""Total entropy change for second-law analysis."""

from sciengformulary.catalog._domain import finite, finite_result
from sciengformulary.core import (
    FormulaSpec,
    ReferenceSpec,
    VariableSpec,
    VerificationCase,
)


def _evaluate(delta_S_system: float, delta_S_surroundings: float) -> float:
    finite("delta_S_system", delta_S_system)
    finite("delta_S_surroundings", delta_S_surroundings)
    return finite_result(delta_S_system + delta_S_surroundings)


total_entropy_change = FormulaSpec(
    id="thermodynamics.total_entropy_change",
    name="Total Entropy Change",
    equation="delta_S_total = delta_S_system + delta_S_surroundings",
    description="Total entropy change for second-law analysis.",
    inputs=(
        VariableSpec(
            name="delta_S_system",
            symbol="delta_S_system",
            description="Entropy change of the system",
            dimension="M L^2 T^-2 Theta^-1",
            si_unit="J/K",
        ),
        VariableSpec(
            name="delta_S_surroundings",
            symbol="delta_S_surroundings",
            description="Entropy change of its surroundings",
            dimension="M L^2 T^-2 Theta^-1",
            si_unit="J/K",
        ),
    ),
    output=VariableSpec(
        name="delta_S_total",
        symbol="delta_S_total",
        description="Combined entropy change",
        dimension="M L^2 T^-2 Theta^-1",
        si_unit="J/K",
    ),
    evaluator=_evaluate,
    references=(
        ReferenceSpec(
            source_type="official_web",
            title="16.3 The Second and Third Laws of Thermodynamics",
            organization="OpenStax",
            url="https://openstax.org/books/chemistry-2e/pages/16-3-the-second-and-third-laws-of-thermodynamics",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"delta_S_system": -1, "delta_S_surroundings": 2},
            expected=1,
            note="-1 + 2 = 1 J/K.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"delta_S_system": 1, "delta_S_surroundings": -1},
            expected=0,
            note="Equal opposite changes give zero combined entropy.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "System and surroundings together form the isolated total under consideration.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "thermodynamics", "total entropy change"),
)
