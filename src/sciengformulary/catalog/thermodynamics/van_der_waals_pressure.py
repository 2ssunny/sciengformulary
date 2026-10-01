"""Van der Waals Equation of State: p = R * T / (v - b) - a / v^2."""

from sciengformulary.catalog._sources import naca_report_1135
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    R: float,  # noqa: N803
    T: float,  # noqa: N803
    v: float,
    a: float,
    b: float,
) -> float:
    return R * T / (v - b) - a / v**2


van_der_waals_pressure = FormulaSpec(
    id="thermodynamics.van_der_waals_pressure",
    name="Van der Waals Equation of State",
    equation="p = R * T / (v - b) - a / v^2",
    description=(
        "Pressure of a real gas corrected for molecular size (b) and intermolecular attraction "
        "(a), written per unit mass with specific volume."
    ),
    inputs=(
        VariableSpec(
            name="R",
            symbol="R",
            description="Specific gas constant (287 J/(kg K) for dry air)",
            dimension="L^2 T^-2 Theta^-1",
            si_unit="J/(kg*K)",
        ),
        VariableSpec(
            name="T",
            symbol="T",
            description="Absolute temperature",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="v",
            symbol="v",
            description="Specific volume (volume per unit mass)",
            dimension="L^3 M^-1",
            si_unit="m^3/kg",
        ),
        VariableSpec(
            name="a",
            symbol="a",
            description="Attraction constant for the gas, per-mass form",
            dimension="M^-1 L^5 T^-2",
            si_unit="Pa*m^6/kg^2",
        ),
        VariableSpec(
            name="b",
            symbol="b",
            description="Excluded-volume constant for the gas, per-mass form",
            dimension="L^3 M^-1",
            si_unit="m^3/kg",
        ),
    ),
    output=VariableSpec(
        name="p",
        symbol="p",
        description="Pressure",
        dimension="M L^-1 T^-2",
        si_unit="Pa",
    ),
    evaluator=_evaluate,
    references=(
        # Specific-volume form exactly as in the source; molar tables of a and b must be converted
        # to per-mass values first.
        naca_report_1135("eq. (4)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"R": 1.0, "T": 2.0, "v": 3.0, "a": 4.0, "b": 1.0},
            expected=0.5555555555555556,
            rel_tol=1e-12,
            note="Exact arithmetic: 1 * 2 / (3 - 1) - 4 / 9 = 5/9.",
        ),
    ),
    assumptions=(
        "a and b are empirical, gas-specific constants in units consistent with the per-mass "
        "form (they differ from the more common molar values).",
        "Semi-quantitative near the critical point and in the two-phase region; v must exceed b.",
    ),
    tags=("real gas", "van der Waals", "equation of state", "non-ideal gas"),
)
