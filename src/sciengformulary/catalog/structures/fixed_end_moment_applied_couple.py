"""Fixed-End Moment, Applied Couple: M_A = M0 * (L - a) * (3 a - L) / L^2 (signed)."""

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, roylance
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    M0: float,  # noqa: N803
    a: float,
    L: float,  # noqa: N803
) -> float:
    finite("M0", M0)
    finite("a", a)
    positive("L", L)
    if not 0 <= a <= L:
        raise ValueError(f"a must lie between 0 and L, got a={a!r} and L={L!r}.")
    u = a / L
    v = (L - a) / L
    # The result is signed: do not take an absolute value.
    return finite_result(M0 * v * (3.0 * u - 1.0))


fixed_end_moment_applied_couple = FormulaSpec(
    id="structures.fixed_end_moment_applied_couple",
    name="Fixed-End Moment, Applied Couple",
    equation="M_A = M0 * (L - a) * (3*a - L) / L^2",
    description=(
        "Signed clamping moment at the near end of a beam fixed at both ends when a "
        "concentrated couple is applied at distance a from that end."
    ),
    inputs=(
        VariableSpec(
            name="M0",
            symbol="M_0",
            description="Applied concentrated couple, counterclockwise positive",
            dimension="M L^2 T^-2",
            si_unit="N*m",
        ),
        VariableSpec(
            name="a",
            symbol="a",
            description="Position of the couple measured from the near end, between 0 and L",
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
        name="M_A",
        symbol="M_A",
        description=(
            "Moment exerted on the beam by the near clamp, counterclockwise positive, with the "
            "x axis running from the near end towards the far end (signed result)"
        ),
        dimension="M L^2 T^-2",
        si_unit="N*m",
    ),
    evaluator=_evaluate,
    references=(
        # The notes give the integration procedure (eqs. (1)-(4)), the cantilever curve for a
        # point load (Fig. 6) and the superposition statement (p. 9); the couple solution is
        # not printed. Derived two ways. (a) Clamped-clamped integration with a concentrated
        # couple M0 at x = a, taking M(x) = R_A x - M_A - M0 <x - a>^0 (counterclockwise M0
        # and M_A on the beam), gives M_A = M0 b (2a - b) / L^2 with b = L - a, which is the
        # form above because 2a - b = 3a - L. (b) A couple is the limit of two opposite point
        # loads a small distance apart, so M_A(couple) = -M0 * d/da [M_A(point load) / P] with
        # M_A(point load) the counterclockwise near-end moment P a b^2 / L^2; this reproduces
        # the same expression (checked symbolically).
        # Sign convention (fixed here, not taken from any program or text): x from the near end
        # to the far end, and both the couple and the clamp moment counterclockwise positive.
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
            inputs={"M0": 5000.0, "a": 1.5, "L": 6.0},
            expected=-937.5,
            rel_tol=1e-12,
            note="Hand calculation with b = 4.5: 5000 * 4.5 * (4.5 - 6) / 36 = -937.5 N*m.",
        ),
        VerificationCase(
            inputs={"M0": 5000.0, "a": 2.0, "L": 6.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-09,
            note="Couple at one third of the span (a = L / 3): 3a - L = 0, so M_A = 0.",
        ),
        VerificationCase(
            inputs={"M0": 5000.0, "a": 0.0, "L": 6.0},
            expected=-5000.0,
            rel_tol=1e-12,
            note="Couple at the near clamp (a = 0): the clamp resists it fully, M_A = -M0.",
        ),
        VerificationCase(
            inputs={"M0": 5000.0, "a": 6.0, "L": 6.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-09,
            note="Couple at the far clamp (a = L): b = 0, so the near end carries nothing.",
        ),
    ),
    assumptions=(
        "Prismatic, linear elastic Euler-Bernoulli beam fixed against translation and rotation "
        "at both ends; small deflections and slopes; E I does not appear.",
        "Sign convention, fixed explicitly: x runs from the near end to the far end; the "
        "applied couple M0 and the result M_A (the moment the near clamp exerts on the beam) "
        "are both counterclockwise positive. M_A is negative for a < L / 3, zero at a = L / 3 "
        "and a = L, and positive between L / 3 and L (opposite signs are used in other texts "
        "and programs).",
        "The vertical reaction at the near end for the same loading is 6 M0 a b / L^3 with "
        "b = L - a, not computed by this item.",
        "L must be finite and positive, M0 and a finite, and a between 0 and L inclusive; "
        "otherwise ValueError is raised.",
        "Derived result: obtained from E I v'' = M with the convention above and, "
        "independently, as the limit of two opposite point loads; the source does not print "
        "this moment.",
        "Homogeneous in any consistent unit set (force times length).",
    ),
    tags=("fixed-end moment", "applied couple", "beam", "moment distribution"),
)
