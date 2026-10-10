"""Newton's Law of Universal Gravitation: F = G * m1 * m2 / r^2."""

from sciengformulary.catalog._constants import (
    GRAVITATIONAL_CONSTANT_REFERENCE,
    NEWTONIAN_CONSTANT_OF_GRAVITATION,
)
from sciengformulary.catalog._sources import (
    doe_fundamentals_handbook,
    openstax_university_physics,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(m1: float, m2: float, r: float) -> float:
    return NEWTONIAN_CONSTANT_OF_GRAVITATION * m1 * m2 / r**2


gravitational_force = FormulaSpec(
    id="mechanics.gravitational_force",
    name="Newton's Law of Universal Gravitation",
    equation="F = G * m1 * m2 / r^2",
    description="Attractive gravitational force between two point masses.",
    inputs=(
        VariableSpec(
            name="m1",
            symbol="m_1",
            description="Mass of the first body",
            dimension="M",
            si_unit="kg",
        ),
        VariableSpec(
            name="m2",
            symbol="m_2",
            description="Mass of the second body",
            dimension="M",
            si_unit="kg",
        ),
        VariableSpec(
            name="r",
            symbol="r",
            description="Distance between the centres of mass",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="F",
        symbol="F",
        description="Magnitude of the attractive force on each body",
        dimension="M L T^-2",
        si_unit="N",
    ),
    evaluator=_evaluate,
    references=(
        openstax_university_physics(
            1,
            "13-1-newtons-law-of-universal-gravitation",
            "sec. 13.1, eq. (13.1)",
        ),
        GRAVITATIONAL_CONSTANT_REFERENCE,
        # The handbook's G is an older value; the evaluator uses the CODATA constant cited above.
        doe_fundamentals_handbook(
            "DOE-HDBK-1010-92",
            "Module 3 'Force and Motion', Newton's Laws of Motion, eq. (3-2), p. 2 (CP-03)",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"m1": 5.972e+24, "m2": 7.348e+22, "r": 384400000.0},
            expected=1.9821107290792523e+20,
            rel_tol=1e-12,
            note=(
                "Independent 40-digit decimal evaluation with G = 6.67430e-11 (Earth and Moon "
                "masses and mean distance as illustrative inputs)."
            ),
        ),
    ),
    assumptions=(
        "Point masses, or spherically symmetric bodies with r measured between centres.",
        "Newtonian gravity; relativistic corrections are negligible except near very massive "
        "or compact bodies.",
        "G carries a relative standard uncertainty of about 2e-5.",
    ),
    tags=("gravitation", "gravity", "Newton", "inverse square"),
)
