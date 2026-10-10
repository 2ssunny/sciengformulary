"""Fixed Bar Axial Reaction, Point Load: R_A = P * (L - a) / L."""

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, roylance
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    P: float,  # noqa: N803
    a: float,
    L: float,  # noqa: N803
) -> float:
    finite("P", P)
    finite("a", a)
    positive("L", L)
    if not 0 <= a <= L:
        raise ValueError(f"a must lie between 0 and L, got a={a!r} and L={L!r}.")
    return finite_result(P * ((L - a) / L))


fixed_bar_axial_reaction_point_load = FormulaSpec(
    id="structures.fixed_bar_axial_reaction_point_load",
    name="Fixed Bar Axial Reaction, Point Load",
    equation="R_A = P * (L - a) / L",
    description=(
        "Axial reaction at the near end of a uniform bar fixed at both ends under an axial "
        "point load at distance a from that end."
    ),
    inputs=(
        VariableSpec(
            name="P",
            symbol="P",
            description="Axial point load",
            dimension="M L T^-2",
            si_unit="N",
        ),
        VariableSpec(
            name="a",
            symbol="a",
            description="Distance of the load from the near end, between 0 and L",
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
        name="R_A",
        symbol="R_A",
        description="Axial reaction at the near end (the share of P carried by that support)",
        dimension="M L T^-2",
        si_unit="N",
    ),
    evaluator=_evaluate,
    references=(
        # The notes solve statically indeterminate bar assemblies with three relations
        # (p. 11): the constitutive law delta = P L / (A E), compatibility of the joint
        # displacements, and equilibrium. Applying them here: the bar is two segments of
        # lengths a and L - a with the same A E, joined at the load point; compatibility
        # R_A a / (A E) = R_B (L - a) / (A E) and equilibrium R_A + R_B = P give
        # R_A = P (L - a) / L and R_B = P a / L. The notes do not print this result.
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
            inputs={"P": 9000.0, "a": 2.0, "L": 6.0},
            expected=6000.0,
            rel_tol=1e-12,
            note="Hand calculation: 9000 * (6 - 2) / 6 = 6000 N.",
        ),
        VerificationCase(
            inputs={"P": 9000.0, "a": 0.0, "L": 6.0},
            expected=9000.0,
            rel_tol=1e-12,
            note="Load at the near end (a = 0): that support carries all of P.",
        ),
        VerificationCase(
            inputs={"P": 9000.0, "a": 6.0, "L": 6.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-09,
            note="Load at the far end (a = L): the near support carries nothing.",
        ),
    ),
    assumptions=(
        "Prismatic linear elastic bar with uniform A E, fixed against axial displacement at "
        "both ends; small displacements.",
        "A E cancels, so the result does not depend on the material or the cross-section.",
        "The far-end reaction is P a / L, and the two reactions sum to P.",
        "L must be finite and positive, P and a finite, and a between 0 and L inclusive; "
        "otherwise ValueError is raised.",
        "Derived result: from the three relations of the source (constitutive, compatibility, "
        "equilibrium) applied to the two bar segments on either side of the load.",
        "Homogeneous in any consistent unit set (the result has the unit of P).",
    ),
    tags=("axial", "fixed bar", "reaction", "statically indeterminate"),
)
