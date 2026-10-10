"""Semi-Major Axis from Apsis Radii: a = (r_p + r_a) / 2."""

from sciengformulary.catalog._sources import (
    nasa_cr_2005_213034,
    openstax_university_physics,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(r_p: float, r_a: float) -> float:
    return 0.5 * (r_p + r_a)


semi_major_axis_from_apsides = FormulaSpec(
    id="orbital.semi_major_axis_from_apsides",
    name="Semi-Major Axis from Apsis Radii",
    equation="a = (r_p + r_a) / 2",
    description=(
        "Semi-major axis of an elliptical orbit from its closest and farthest distances to the "
        "central body's centre."
    ),
    inputs=(
        VariableSpec(
            name="r_p",
            symbol="r_p",
            description="Periapsis radius (closest distance, measured from the centre)",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="r_a",
            symbol="r_a",
            description="Apoapsis radius (farthest distance, measured from the centre)",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="a",
        symbol="a",
        description="Semi-major axis",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # Stated in the section text: the semi-major axis is one-half the sum of the perihelion and
        # aphelion.
        openstax_university_physics(1, "13-5-keplers-laws-of-planetary-motion", "sec. 13.5"),
        # The report prints a_trans = (r_initial + r_final) / 2 for a transfer ellipse whose perigee
        # and apogee are those two radii.
        nasa_cr_2005_213034("eq. (6), p. 16"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"r_p": 6678000.0, "r_a": 42164000.0},
            expected=24421000.0,
            rel_tol=1e-12,
            note="Hand calculation: (6.678e6 + 4.2164e7) / 2 = 2.4421e7 m.",
        ),
    ),
    assumptions=(
        "Radii from the centre of the central body, not altitudes above its surface.",
        "Closed (elliptical) orbit.",
    ),
    tags=("semi-major axis", "periapsis", "apoapsis", "ellipse", "transfer orbit"),
)
