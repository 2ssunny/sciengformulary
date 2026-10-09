"""Fixed Bar Axial Reaction, Linearly Varying Load: far-end reaction of a trapezoidal load."""

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, roylance
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    p1: float,
    p2: float,
    x1: float,
    x2: float,
    L: float,  # noqa: N803
) -> float:
    finite("p1", p1)
    finite("p2", p2)
    finite("x1", x1)
    finite("x2", x2)
    positive("L", L)
    if not 0 <= x1 <= x2 <= L:
        raise ValueError(f"The load must satisfy 0 <= x1 <= x2 <= L, got x1={x1!r}, x2={x2!r}.")
    return finite_result(
        (x2 - x1) * (2.0 * p1 * x1 + p1 * x2 + p2 * x1 + 2.0 * p2 * x2) / (6.0 * L)
    )


fixed_bar_axial_reaction_linear_load = FormulaSpec(
    id="structures.fixed_bar_axial_reaction_linear_load",
    name="Fixed Bar Axial Reaction, Linearly Varying Load",
    equation="R_B = (x2 - x1) * (2*p1*x1 + p1*x2 + p2*x1 + 2*p2*x2) / (6 * L)",
    description=(
        "Axial reaction at the far end of a uniform bar fixed at both ends under an axial load "
        "that varies linearly between x1 and x2 and is zero elsewhere."
    ),
    inputs=(
        VariableSpec(
            name="p1",
            symbol="p_1",
            description="Axial load intensity per unit length at x1",
            dimension="M T^-2",
            si_unit="N/m",
        ),
        VariableSpec(
            name="p2",
            symbol="p_2",
            description="Axial load intensity per unit length at x2",
            dimension="M T^-2",
            si_unit="N/m",
        ),
        VariableSpec(
            name="x1",
            symbol="x_1",
            description="Start of the loaded segment, measured from the near end",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="x2",
            symbol="x_2",
            description="End of the loaded segment, measured from the near end (x1 <= x2 <= L)",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="L",
            symbol="L",
            description="Bar length",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="R_B",
        symbol="R_B",
        description=(
            "Axial reaction at the far end (x = L); the near-end reaction is the total load "
            "minus R_B"
        ),
        dimension="M L T^-2",
        si_unit="N",
    ),
    evaluator=_evaluate,
    references=(
        # The notes solve statically indeterminate bar assemblies with three relations
        # (p. 11): constitutive delta = P L / (A E), compatibility and equilibrium; the point
        # load result R_B = P a / L follows from them (see fixed_bar_axial_reaction_point_load,
        # also derived). Because the response is linear, a distributed load p(s) gives
        # R_B = (1 / L) * integral of p(s) s ds on [x1, x2]; with p linear from p1 at x1 to p2
        # at x2, exact integration gives the closed form above. The notes state superposition
        # only for beams (p. 9 of the beam module); here it is applied to a linear bar.
        roylance(
            "Trusses",
            "mit3_11f99_truss",
            2000,
            "p. 11 (constitutive delta = P L / (A E), compatibility, equilibrium)",
            accessed=ENGINEERING_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"p1": 1000.0, "p2": 1000.0, "x1": 0.0, "x2": 6.0, "L": 6.0},
            expected=3000.0,
            rel_tol=1e-12,
            note="Uniform full-span load: p L / 2 = 1000 * 6 / 2 = 3000 N.",
        ),
        VerificationCase(
            inputs={"p1": 0.0, "p2": 900.0, "x1": 0.0, "x2": 6.0, "L": 6.0},
            expected=1800.0,
            rel_tol=1e-12,
            note="Triangle that is zero at the near end: resultant 2700 N acts at 2L/3 -> 1800 N.",
        ),
        VerificationCase(
            inputs={"p1": 400.0, "p2": 1200.0, "x1": 2.0, "x2": 4.0, "L": 6.0},
            expected=844.4444444444445,
            rel_tol=1e-12,
            note="Partial segment on [2, 4]; exact rational integral of p(s) s / L.",
        ),
        VerificationCase(
            inputs={"p1": 400.0, "p2": 400.0, "x1": 3.0, "x2": 3.0, "L": 6.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-09,
            note="Zero-length load (x1 = x2) carries no load, so the reaction is zero.",
        ),
    ),
    assumptions=(
        "Prismatic linear elastic bar with uniform A E, fixed against axial displacement at "
        "both ends; small displacements; the load is zero outside [x1, x2].",
        "A E cancels, so the result does not depend on the material or the cross-section.",
        "L must be finite and positive, the loads finite, and 0 <= x1 <= x2 <= L; otherwise "
        "ValueError is raised.",
        "Derived result: superposition (linear response) of the point-load reaction "
        "R_B = P a / L integrated over the load distribution, with the integral checked "
        "against the closed form; the source does not print it.",
        "Homogeneous in any consistent unit set (force per length times length).",
    ),
    tags=("axial", "fixed bar", "distributed load", "reaction"),
)
