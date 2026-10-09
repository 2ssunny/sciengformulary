"""Fixed-End Moment, Partial Linearly Varying Load: near-end moment of a trapezoidal load.

M_A = (1 / L^2) * integral from x1 to x2 of w(s) * s * (L - s)^2 ds, with w varying linearly
from w1 at x1 to w2 at x2; the closed form is given in the equation field.
"""

import math

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, roylance
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


# Three-point Gauss-Legendre rule on [-1, 1]: nodes -sqrt(3/5), 0, +sqrt(3/5) with weights
# 5/9, 8/9, 5/9. It integrates polynomials up to degree 5 exactly, and the integrand
# w(s) s (L - s)^2 below has degree 4. Each node is stored as the fraction _NODE_FRACTION of
# the way from x1 to x2, paired with its complement, so no cancelling difference is formed.
_SQRT_3_5 = math.sqrt(0.6)
_NODE_FRACTION = ((1.0 - _SQRT_3_5) / 2.0, 0.5, (1.0 + _SQRT_3_5) / 2.0)
_NODE_COMPLEMENT = _NODE_FRACTION[::-1]
_WEIGHT = (5.0 / 9.0, 8.0 / 9.0, 5.0 / 9.0)


def _evaluate(
    w1: float,
    w2: float,
    x1: float,
    x2: float,
    L: float,  # noqa: N803
) -> float:
    finite("w1", w1)
    finite("w2", w2)
    finite("x1", x1)
    finite("x2", x2)
    positive("L", L)
    if not 0 <= x1 <= x2 <= L:
        raise ValueError(f"The load must satisfy 0 <= x1 <= x2 <= L, got x1={x1!r}, x2={x2!r}.")
    # M_A = (1 / L^2) * (x2 - x1) / 2 * sum_i W_i g(s_i), g(s) = w(s) s (L - s)^2, evaluated as
    # (x2 - x1) / 2 * sum_i W_i w_i s_i ((L - s_i) / L)^2 with s_i = x1 (1 - u_i) + x2 u_i.
    # w, s and L - s are each a convex combination of their end values, so for loads of one
    # sign every term is non-negative and nothing cancels; L - s is built from L - x1 and
    # L - x2, which stays accurate for loads next to the far clamp.
    far_1 = L - x1
    far_2 = L - x2
    total = 0.0
    for u, v, weight in zip(_NODE_FRACTION, _NODE_COMPLEMENT, _WEIGHT):
        load = w1 * v + w2 * u
        position = x1 * v + x2 * u
        lever = (far_1 * v + far_2 * u) / L
        total += weight * load * position * lever * lever
    return finite_result(0.5 * (x2 - x1) * total)


fixed_end_moment_partial_linear_load = FormulaSpec(
    id="structures.fixed_end_moment_partial_linear_load",
    name="Fixed-End Moment, Partial Linearly Varying Load",
    equation=(
        "M_A = (x2 - x1) * (10*L^2*(2*w1*x1 + w1*x2 + w2*x1 + 2*w2*x2) "
        "- 10*L*(3*w1*x1^2 + 2*w1*x1*x2 + w1*x2^2 + w2*x1^2 + 2*w2*x1*x2 + 3*w2*x2^2) "
        "+ 3*(4*w1*x1^3 + 3*w1*x1^2*x2 + 2*w1*x1*x2^2 + w1*x2^3 + w2*x1^3 + 2*w2*x1^2*x2 "
        "+ 3*w2*x1*x2^2 + 4*w2*x2^3)) / (60 * L^2)"
    ),
    description=(
        "Magnitude of the near-end clamping moment of a beam fixed at both ends under a "
        "transverse load that varies linearly between x1 and x2 and is zero elsewhere."
    ),
    inputs=(
        VariableSpec(
            name="w1",
            symbol="w_1",
            description="Load intensity per unit length at x1 (downward positive)",
            dimension="M T^-2",
            si_unit="N/m",
        ),
        VariableSpec(
            name="w2",
            symbol="w_2",
            description="Load intensity per unit length at x2 (downward positive)",
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
            description="Span between the two clamped ends",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="M_A",
        symbol="M_A",
        description="Magnitude of the fixed-end moment at the near end (hogging for downward load)",
        dimension="M L^2 T^-2",
        si_unit="N*m",
    ),
    evaluator=_evaluate,
    references=(
        # The notes state (p. 9) that responses to separate loads superpose, so the near-end
        # moment of a distributed load is the integral of the point-load moment
        # P a b^2 / L^2 (itself derived, see fixed_end_moment_point_load) over the load:
        # M_A = (1 / L^2) * integral of w(s) s (L - s)^2 ds on [x1, x2], with w linear from w1
        # at x1 to w2 at x2. Exact integration gives the polynomial in the equation field; it
        # reduces to w L^2 / 12 for a uniform full-span load, w L^2 / 30 for a triangle that
        # is zero at the near end, and w L^2 / 20 for a triangle that is zero at the far end.
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
            inputs={"w1": 2000.0, "w2": 2000.0, "x1": 0.0, "x2": 6.0, "L": 6.0},
            expected=6000.0,
            rel_tol=1e-12,
            note="Uniform full-span load: w L^2 / 12 = 2000 * 36 / 12 = 6000 N*m.",
        ),
        VerificationCase(
            inputs={"w1": 0.0, "w2": 3000.0, "x1": 0.0, "x2": 5.0, "L": 5.0},
            expected=2500.0,
            rel_tol=1e-12,
            note="Triangle that is zero at the near end: w L^2 / 30 = 3000 * 25 / 30 = 2500.",
        ),
        VerificationCase(
            inputs={"w1": 3000.0, "w2": 0.0, "x1": 0.0, "x2": 5.0, "L": 5.0},
            expected=3750.0,
            rel_tol=1e-12,
            note="Triangle that is zero at the far end: w L^2 / 20 = 3000 * 25 / 20 = 3750.",
        ),
        VerificationCase(
            inputs={"w1": 1000.0, "w2": 2500.0, "x1": 1.0, "x2": 3.5, "L": 6.0},
            expected=3472.222222222222,
            rel_tol=1e-12,
            note="Partial trapezoid on [1, 3.5]; exact rational integral of the point-load moment.",
        ),
        VerificationCase(
            inputs={"w1": 1000.0, "w2": 1000.0, "x1": 2.0, "x2": 2.0, "L": 6.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-09,
            note="Zero-length load (x1 = x2) carries no load, so the moment is zero.",
        ),
    ),
    assumptions=(
        "Prismatic, linear elastic Euler-Bernoulli beam fixed against translation and rotation "
        "at both ends; small deflections and slopes; E I does not appear.",
        "The load varies linearly from w1 at x1 to w2 at x2 and is zero outside [x1, x2]; "
        "by superposition the moment is the integral of the point-load result.",
        "Magnitude only: for w1, w2 >= 0 (downward) the value is the hogging moment at the near "
        "end. The far-end moment follows by mirroring the load (x -> L - x).",
        "L must be finite and positive, the loads finite, and 0 <= x1 <= x2 <= L; otherwise "
        "ValueError is raised.",
        "Derived result: closed form from exact integration of the superposed point-load "
        "moment, checked against the uniform and triangular special cases; the source does "
        "not print it.",
        "The evaluator integrates the exact integrand by three-point Gauss-Legendre "
        "quadrature, which is exact for this degree-4 integrand and equals the closed form in "
        "the equation field; unlike the expanded polynomial it has no cancelling terms. "
        "Against 60-digit mpmath integration, 3000 random same-sign loads (including loads "
        "within 1e-12 L of the far clamp and ending at x2 = L) agreed to 7e-16 relative at "
        "worst. Loads of mixed sign partly cancel physically, and then the relative error "
        "grows with the cancellation (about 5e-14 when the result is above 1e-3 of the "
        "same-sign value).",
        "Homogeneous in any consistent unit set (force per length times length squared).",
    ),
    tags=("fixed-end moment", "distributed load", "trapezoidal load", "beam"),
)
