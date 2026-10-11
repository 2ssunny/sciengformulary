"""Van Deemter plate-height model."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import (
    harvey_analytical_chemistry,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(A: float, B: float, C: float, u: float) -> float:
    non_negative("A", A)
    non_negative("B", B)
    non_negative("C", C)
    positive("u", u)
    return finite_result(A + B / u + C * u)


van_deemter_plate_height = FormulaSpec(
    id="chromatography.van_deemter_plate_height",
    name="Van Deemter Plate Height",
    equation="H = A + B/u + C*u",
    description="Van Deemter plate-height model.",
    inputs=(
        VariableSpec(
            name="A",
            symbol="A",
            description="Eddy-diffusion coefficient",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="B",
            symbol="B",
            description="Longitudinal-diffusion coefficient",
            dimension="L^2 T^-1",
            si_unit="m^2/s",
        ),
        VariableSpec(
            name="C",
            symbol="C",
            description="Combined mass-transfer coefficient",
            dimension="T",
            si_unit="s",
        ),
        VariableSpec(
            name="u",
            symbol="u",
            description="Mobile-phase linear velocity",
            dimension="L T^-1",
            si_unit="m/s",
        ),
    ),
    output=VariableSpec(
        name="H", symbol="H", description="Model plate height", dimension="L", si_unit="m"
    ),
    evaluator=_evaluate,
    references=(
        harvey_analytical_chemistry(
            (
                "12%3A_Chromatographic_and_Electrophoretic_Methods/12.03%3A_Optimizing_Chromatogr"
                "aphic_Separations"
            ),
            "12.3: Optimizing Chromatographic Separations",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"A": 1, "B": 4, "C": 1, "u": 2},
            expected=5,
            note="1+4/2+1*2=5.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"A": 0, "B": 0, "C": 1, "u": 2},
            expected=2,
            note="Only mass transfer remains, giving H=2.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Empirical van Deemter model with coefficients valid for the specified column, analyte and conditions.",
        "u is linear velocity, not volumetric flow rate; coefficients must use that same velocity convention.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chromatography", "van deemter plate height"),
)
