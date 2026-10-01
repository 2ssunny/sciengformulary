"""Second Moment of Area of a Rectangle: I = b * h^3 / 12."""

from sciengformulary.catalog._sources import roylance
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(b: float, h: float) -> float:
    return b * h**3 / 12.0


rectangle_second_moment_of_area = FormulaSpec(
    id="structures.rectangle_second_moment_of_area",
    name="Second Moment of Area of a Rectangle",
    equation="I = b * h^3 / 12",
    description=(
        "Second moment of area of a solid rectangular section about its centroidal axis parallel "
        "to the side b."
    ),
    inputs=(
        VariableSpec(
            name="b",
            symbol="b",
            description="Section width, parallel to the bending axis",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="h",
            symbol="h",
            description="Section depth, perpendicular to the bending axis",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="I",
        symbol="I",
        description="Second moment of area about the centroidal axis",
        dimension="L^4",
        si_unit="m^4",
    ),
    evaluator=_evaluate,
    references=(
        roylance("Stresses in Beams", "mit3_11f99_bstress", 2000, "eq. (5)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"b": 0.05, "h": 0.1},
            expected=4.166666666666667e-06,
            rel_tol=1e-12,
            note="Hand calculation: 0.05 * 0.1^3 / 12 = 4.1667e-6 m^4.",
        ),
    ),
    assumptions=(
        "About the centroidal axis parallel to b; use the parallel-axis theorem for other axes.",
        "Area property, not the mass moment of inertia.",
    ),
    tags=("second moment of area", "area moment of inertia", "rectangle", "beam section"),
)
