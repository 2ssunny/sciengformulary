"""Linear Spring Force: F = k * (s_rel - s_0)."""

from sciengformulary.catalog._domain import finite, finite_result, non_negative
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, roylance
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(k: float, s_rel: float, s_0: float) -> float:
    non_negative("k", k)
    finite("s_rel", s_rel)
    finite("s_0", s_0)
    return finite_result(k * (s_rel - s_0))


linear_spring_force = FormulaSpec(
    id="mechanics.linear_spring_force",
    name="Linear Spring Force",
    equation="F = k * (s_rel - s_0)",
    description=(
        "Force carried by a linear spring whose current length differs from its unstretched "
        "length; positive when the spring is stretched."
    ),
    inputs=(
        VariableSpec(
            name="k",
            symbol="k",
            description="Spring stiffness (force per unit change in length), not negative",
            dimension="M T^-2",
            si_unit="N/m",
        ),
        VariableSpec(
            name="s_rel",
            symbol="s",
            description="Current length of the spring",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="s_0",
            symbol="s_0",
            description="Unstretched (unloaded) length of the spring",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="F",
        symbol="F",
        description="Spring force, tension positive",
        dimension="M L T^-2",
        si_unit="N",
    ),
    evaluator=_evaluate,
    references=(
        # The notes state the load-displacement form P = k * delta, with k the stiffness and
        # delta the resulting change in length (eq. (3)); eq. (7) gives k = A E / L for a bar.
        # Writing delta as the current length minus the unstretched length (s_rel - s_0) and P
        # as the tensile force F is the step that makes this a derived result.
        roylance(
            "Introduction to Elasticity",
            "mit3_11f99_elas_1",
            2000,
            "section 'Stiffness', eq. (3), p. 5; eq. (7), p. 6",
            accessed=ENGINEERING_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"k": 1000.0, "s_rel": 0.12, "s_0": 0.1},
            expected=20.0,
            rel_tol=1e-12,
            note="Hand calculation: 1000 N/m * (0.12 - 0.10) m = 20 N, a stretched spring.",
        ),
        VerificationCase(
            inputs={"k": 250.0, "s_rel": 0.08, "s_0": 0.08},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-09,
            note="Unstretched spring: s_rel = s_0 gives zero force.",
        ),
        VerificationCase(
            inputs={"k": 250.0, "s_rel": 0.05, "s_0": 0.08},
            expected=-7.5,
            rel_tol=1e-12,
            note="Hand calculation: 250 * (0.05 - 0.08) = -7.5 N, a compressed spring.",
        ),
    ),
    assumptions=(
        "Linear elastic spring in one dimension: the force is proportional to the change in "
        "length (Hooke's law), tension positive, so a compressed spring gives a negative force.",
        "Valid only while the response stays linear; the source gives no numerical limit on "
        "the extension.",
        "k must not be negative, and k, s_rel and s_0 must be finite; otherwise ValueError is "
        "raised. s_rel and s_0 are lengths and should not be negative, but only finiteness is "
        "checked, so keeping them physical is the caller's responsibility.",
        "Derived result: the deformation delta of the source's load-displacement law is the "
        "change in length, so delta = s_rel - s_0; the source does not print this form.",
        "Homogeneous in any consistent unit set (k in force per length).",
    ),
    tags=("spring", "Hooke's law", "stiffness", "force"),
)
