"""Wing Aspect Ratio: AR = b^2 / S."""

from sciengformulary.catalog._sources import nasa_glenn
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(b: float, S: float) -> float:  # noqa: N803 - symbols as written in the source
    return b**2 / S


aspect_ratio = FormulaSpec(
    id="aerodynamics.aspect_ratio",
    name="Wing Aspect Ratio",
    equation="AR = b^2 / S",
    description=(
        "Slenderness of a wing: span squared divided by planform area. For a rectangular wing it "
        "reduces to span over chord."
    ),
    inputs=(
        VariableSpec(
            name="b",
            symbol="b",
            description="Wing span, tip to tip",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="S",
            symbol="S",
            description="Wing planform (projected) area, not the wetted area",
            dimension="L^2",
            si_unit="m^2",
        ),
    ),
    output=VariableSpec(
        name="AR",
        symbol="AR",
        description="Aspect ratio",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes the span as s and the wing area as A.
        nasa_glenn("Wing Geometry", "wing-geometry", 2025),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"b": 10.0, "S": 16.0},
            expected=6.25,
            rel_tol=1e-12,
            note="Hand calculation: 10^2 / 16 = 6.25.",
        ),
    ),
    assumptions=(
        "S is the projected planform area bounded by the leading and trailing edges and the "
        "tips; using total surface area gives about half the correct value.",
        "Pure geometry; valid for any planform.",
    ),
    tags=("aspect ratio", "AR", "span", "wing geometry", "planform"),
)
