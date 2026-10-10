"""Burning-Surface to Throat-Area Ratio: K_n = A_b / A_t."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(A_b: float, A_t: float) -> float:  # noqa: N803 - symbols as in the source
    positive("A_b", A_b)
    positive("A_t", A_t)
    return finite_result(A_b / A_t)


burn_to_throat_area_ratio = FormulaSpec(
    id="propulsion.burn_to_throat_area_ratio",
    name="Burning-Surface to Throat-Area Ratio",
    equation="K_n = A_b / A_t",
    description=(
        "Ratio of the propellant burning-surface area to the nozzle throat area of a "
        "solid rocket motor, a basic internal-ballistics parameter. It is unrelated to "
        "propulsion.nozzle_expansion_ratio, which compares exit and throat areas."
    ),
    inputs=(
        VariableSpec(
            name="A_b",
            symbol="A_b",
            description="Propellant burning-surface area",
            dimension="L^2",
            si_unit="m^2",
        ),
        VariableSpec(
            name="A_t",
            symbol="A_t",
            description="Nozzle throat area",
            dimension="L^2",
            si_unit="m^2",
        ),
    ),
    output=VariableSpec(
        name="K_n",
        symbol="K_n",
        description="Ratio of burning-surface area to throat area",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Stated: K_n is defined in words as the ratio of the propellant burning-surface area
        # to the nozzle throat area; the equation restates that definition.
        nasa_technical_report(
            "Solid Rocket Motor Performance Analysis and Prediction",
            (),
            "NASA SP-8039",
            1971,
            "https://ntrs.nasa.gov/citations/19720011135",
            "sec. 2.1.2, text under eq. (15), p. 10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"A_b": 0.5, "A_t": 0.001},
            expected=500.0,
            rel_tol=1e-12,
            note="Hand calculation: 0.5 / 0.001 = 500.",
        ),
        VerificationCase(
            inputs={"A_b": 0.01, "A_t": 0.01},
            expected=1.0,
            rel_tol=1e-12,
            note="Edge case: equal areas give a ratio of exactly 1.",
        ),
        VerificationCase(
            inputs={"A_b": 0.123, "A_t": 0.00041},
            expected=300.0,
            rel_tol=1e-12,
            note="Hand calculation: 0.123 / 0.00041 = 300.",
        ),
    ),
    assumptions=(
        "Definition for solid-propellant motors; the burning-surface area changes as the grain "
        "regresses, so K_n is a function of time unless stated for a particular web position.",
        "Both areas must be positive and in the same unit.",
    ),
    tags=("solid rocket motor", "internal ballistics", "burning area", "propulsion"),
)
