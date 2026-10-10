"""Fixed-End Vertical Reaction, Point Load: R_A = P * (L - a)^2 * (L + 2 a) / L^3."""

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
    # Ratios keep intermediate products bounded; the result is at most |P| in size.
    u = a / L
    v = (L - a) / L
    return finite_result(P * v**2 * (1.0 + 2.0 * u))


fixed_end_reaction_point_load = FormulaSpec(
    id="structures.fixed_end_reaction_point_load",
    name="Fixed-End Vertical Reaction, Point Load",
    equation="R_A = P * (L - a)^2 * (L + 2*a) / L^3",
    description=(
        "Vertical reaction at the near clamp of a beam fixed at both ends under a transverse "
        "point load at distance a from that end."
    ),
    inputs=(
        VariableSpec(
            name="P",
            symbol="P",
            description="Transverse point load",
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
            description="Span between the two clamped ends",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="R_A",
        symbol="R_A",
        description="Vertical reaction at the near end, resisting the load P",
        dimension="M L T^-2",
        si_unit="N",
    ),
    evaluator=_evaluate,
    references=(
        # The notes give the integration procedure (eqs. (1)-(4)), the cantilever curve for a
        # point load (Fig. 6) and the superposition statement (p. 9); the reaction itself is not
        # printed. Derived two ways: (a) integrate E I v'' = M(x) piecewise with v = v' = 0 at
        # both ends and continuity at x = a, which gives R_A = P b^2 (L + 2a) / L^3 with
        # b = L - a; (b) superpose the Fig. 6 cantilever curve with a tip load and tip couple
        # that cancel the tip deflection and slope, which gives the far-end reaction
        # R_B = P a^2 (L + 2b) / L^3, and then R_A = P - R_B.
        roylance(
            "Beam Displacements",
            "mit3_11f99_bdisp",
            2000,
            "eqs. (1)-(4), pp. 1-2; Fig. 6 and the superposition paragraph, p. 9",
            accessed=ENGINEERING_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"P": 10000.0, "a": 2.0, "L": 6.0},
            expected=7407.407407407408,
            rel_tol=1e-12,
            note="Hand calculation with b = 4: 10000 * 16 * 10 / 216 = 7407.407 N.",
        ),
        VerificationCase(
            inputs={"P": 10000.0, "a": 0.0, "L": 6.0},
            expected=10000.0,
            rel_tol=1e-12,
            note="Load at the near clamp: the whole load goes to that support.",
        ),
        VerificationCase(
            inputs={"P": 10000.0, "a": 6.0, "L": 6.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-09,
            note="Load at the far clamp: the near support carries nothing.",
        ),
        VerificationCase(
            inputs={"P": 8000.0, "a": 2.0, "L": 4.0},
            expected=4000.0,
            rel_tol=1e-12,
            note="Midspan load: symmetry gives P / 2 = 4000 N.",
        ),
    ),
    assumptions=(
        "Prismatic, linear elastic Euler-Bernoulli beam fixed against translation and rotation "
        "at both ends; small deflections and slopes; E I is constant and cancels, so the "
        "result does not depend on E or I.",
        "The far-end reaction is P a^2 (L + 2 (L - a)) / L^3, and the two reactions sum to P.",
        "L must be finite and positive, P and a finite, and a between 0 and L inclusive; "
        "otherwise ValueError is raised.",
        "Derived result: obtained by integrating E I v'' = M with four end conditions plus "
        "continuity at the load, and independently by superposition of the printed cantilever "
        "curve; the source does not print this reaction.",
        "Homogeneous in any consistent unit set (the result has the unit of P).",
    ),
    tags=("fixed-end reaction", "point load", "beam", "statically indeterminate"),
)
