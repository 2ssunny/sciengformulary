"""Planar TLC migration relative to the solvent front."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.core import (
    FormulaSpec,
    ReferenceSpec,
    VariableSpec,
    VerificationCase,
)


def _evaluate(distance_spot: float, distance_front: float) -> float:
    non_negative("distance_spot", distance_spot)
    positive("distance_front", distance_front)
    if distance_spot > distance_front:
        raise ValueError("the spot cannot lie past the solvent front in this TLC model")
    return finite_result(distance_spot / distance_front)


tlc_retardation_factor = FormulaSpec(
    id="chromatography.tlc_retardation_factor",
    name="Tlc Retardation Factor",
    equation="Rf = distance_spot/distance_front",
    description="Planar TLC migration relative to the solvent front.",
    inputs=(
        VariableSpec(
            name="distance_spot",
            symbol="distance_spot",
            description="Distance from the origin to the center of the analyte spot",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="distance_front",
            symbol="distance_front",
            description="Distance from the same origin to the solvent front",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="Rf", symbol="Rf", description="TLC retardation factor", dimension="1", si_unit="-"
    ),
    evaluator=_evaluate,
    references=(
        ReferenceSpec(
            source_type="course_material",
            title="2.3C: The Retention Factor",
            organization="Butte College",
            url="https://chem.libretexts.org/Bookshelves/Organic_Chemistry/Organic_Chemistry_Lab_Techniques_(Nichols)/02%3A_Chromatography/2.03%3A_Thin_Layer_Chromatography_(TLC)/2.3C%3A_The_Retention_Factor",
            accessed="2026-10-10",
            authors=("L. Nichols",),
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"distance_spot": 0.02, "distance_front": 0.05},
            expected=0.4,
            note="Spot at 2 cm with solvent front at 5 cm gives Rf=0.4.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"distance_spot": 0, "distance_front": 0.05},
            expected=0,
            note="Spot remaining at the origin gives Rf=0.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "Measure both distances from the same spotting origin along the development direction.",
        "Rf depends on stationary phase, mobile phase and experimental conditions; it is not an invariant molecular constant.",
        "The spot center must lie between the origin and solvent front.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chromatography", "tlc retardation factor"),
)
