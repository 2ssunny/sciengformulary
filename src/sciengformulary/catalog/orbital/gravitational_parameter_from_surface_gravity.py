"""Gravitational Parameter from Surface Gravity: mu = g * R^2."""

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(g: float, R: float) -> float:  # noqa: N803 - symbols as written in the source
    return g * R**2


gravitational_parameter_from_surface_gravity = FormulaSpec(
    id="orbital.gravitational_parameter_from_surface_gravity",
    name="Gravitational Parameter from Surface Gravity",
    equation="mu = g * R^2",
    description=(
        "Gravitational parameter G M of a body from its surface gravitational acceleration and "
        "radius."
    ),
    inputs=(
        VariableSpec(
            name="g",
            symbol="g",
            description="Gravitational acceleration at the surface",
            dimension="L T^-2",
            si_unit="m/s^2",
        ),
        VariableSpec(
            name="R",
            symbol="R",
            description="Radius of the body",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="mu",
        symbol=r"\mu",
        description="Gravitational parameter G M",
        dimension="L^3 T^-2",
        si_unit="m^3/s^2",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes g = G M / r^2; evaluated at r = R it gives G M = g R^2.
        openstax_university_physics(
            1,
            "13-2-gravitation-near-earths-surface",
            "sec. 13.2, eq. (13.2)",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"g": 9.81, "R": 6371000.0},
            expected=398184378210000.0,
            rel_tol=1e-12,
            note="Hand calculation: 9.81 * 6.371e6^2.",
        ),
    ),
    assumptions=(
        "Spherically symmetric, non-rotating body: measured surface gravity on a rotating "
        "planet includes a small centrifugal reduction and varies with latitude.",
    ),
    tags=("gravitational parameter", "GM", "surface gravity", "planet"),
)
