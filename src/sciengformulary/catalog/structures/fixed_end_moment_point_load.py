"""Fixed-End Moment, Point Load: M_A = P * a * (L - a)^2 / L^2."""

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
    v = (L - a) / L
    return finite_result(P * a * v**2)


fixed_end_moment_point_load = FormulaSpec(
    id="structures.fixed_end_moment_point_load",
    name="Fixed-End Moment, Point Load",
    equation="M_A = P * a * (L - a)^2 / L^2",
    description=(
        "Magnitude of the clamping moment at the near end of a beam fixed at both ends under a "
        "transverse point load at distance a from that end."
    ),
    inputs=(
        VariableSpec(
            name="P",
            symbol="P",
            description="Transverse point load (downward positive)",
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
        name="M_A",
        symbol="M_A",
        description=(
            "Magnitude of the fixed-end moment at the near end (hogging for a downward load); "
            "for the far end use L - a in place of a"
        ),
        dimension="M L^2 T^-2",
        si_unit="N*m",
    ),
    evaluator=_evaluate,
    references=(
        # The notes give the integration procedure (eqs. (1)-(4)), the cantilever curve for a
        # point load (Fig. 6) and the superposition statement (p. 9); the moment itself is not
        # printed. Derived two ways: (a) the clamped-clamped integration used for the reaction,
        # solved for the near-end moment with v = v' = 0 at both ends, gives a magnitude
        # P a b^2 / L^2 with b = L - a; (b) the far-end moment P a^2 b / L^2 follows by
        # mirror symmetry (a <-> b) and is reproduced by superposing the Fig. 6 cantilever
        # curve with a tip load and tip couple.
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
            expected=8888.888888888889,
            rel_tol=1e-12,
            note="Hand calculation with b = 4: 10000 * 2 * 16 / 36 = 8888.889 N*m.",
        ),
        VerificationCase(
            inputs={"P": 10000.0, "a": 0.0, "L": 6.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-09,
            note="Load at the near clamp (a = 0): no moment at that end.",
        ),
        VerificationCase(
            inputs={"P": 10000.0, "a": 6.0, "L": 6.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-09,
            note="Load at the far clamp (a = L): no moment at the near end.",
        ),
        VerificationCase(
            inputs={"P": 8000.0, "a": 2.0, "L": 4.0},
            expected=4000.0,
            rel_tol=1e-12,
            note="Midspan load: P L / 8 = 8000 * 4 / 8 = 4000 N*m.",
        ),
    ),
    assumptions=(
        "Prismatic, linear elastic Euler-Bernoulli beam fixed against translation and rotation "
        "at both ends; small deflections and slopes; E I does not appear.",
        "Magnitude only: for P >= 0 (downward) the value is the hogging moment at the near "
        "end, and the same load gives a hogging moment at the far end. The sign convention "
        "of any particular analysis program is not adopted; P < 0 gives a negative value.",
        "The far-end moment is obtained by calling the formula with a replaced by L - a.",
        "L must be finite and positive, P and a finite, and a between 0 and L inclusive; "
        "otherwise ValueError is raised.",
        "Derived result: obtained from E I v'' = M with the four end conditions and continuity "
        "at the load; the source does not print this moment.",
        "Homogeneous in any consistent unit set (force times length).",
    ),
    tags=("fixed-end moment", "point load", "beam", "moment distribution"),
)
