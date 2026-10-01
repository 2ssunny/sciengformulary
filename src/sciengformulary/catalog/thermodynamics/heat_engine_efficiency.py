"""Heat Engine Thermal Efficiency: eta = 1 - Q_C / Q_H."""

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(Q_H: float, Q_C: float) -> float:  # noqa: N803 - symbols as written in the source
    return 1.0 - Q_C / Q_H


heat_engine_efficiency = FormulaSpec(
    id="thermodynamics.heat_engine_efficiency",
    name="Heat Engine Thermal Efficiency",
    equation="eta = 1 - Q_C / Q_H",
    description="Fraction of the heat input that a cyclic heat engine converts to net work.",
    inputs=(
        VariableSpec(
            name="Q_H",
            symbol="Q_H",
            description="Heat absorbed from the hot reservoir per cycle (magnitude)",
            dimension="M L^2 T^-2",
            si_unit="J",
        ),
        VariableSpec(
            name="Q_C",
            symbol="Q_C",
            description="Heat rejected to the cold reservoir per cycle (magnitude)",
            dimension="M L^2 T^-2",
            si_unit="J",
        ),
    ),
    output=VariableSpec(
        name="eta",
        symbol=r"\eta",
        description="Thermal efficiency",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        openstax_university_physics(2, "4-2-heat-engines", "sec. 4.2, eq. (4.2)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"Q_H": 1000.0, "Q_C": 600.0},
            expected=0.4,
            rel_tol=1e-12,
            note="Hand calculation: 1 - 600/1000 = 0.4.",
        ),
    ),
    assumptions=(
        "Complete cycles, so the working substance returns to its initial state.",
        "Heats are positive magnitudes; rates (W) may be used instead of per-cycle energies.",
    ),
    tags=("thermal efficiency", "heat engine", "first law", "cycle"),
)
