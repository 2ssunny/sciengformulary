"""Volume of a d-Dimensional Ball: V = pi^(d/2) * r^d / Gamma(d/2 + 1)."""

import math

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog.mathematics._domain import integer, non_negative
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

# math.gamma(d/2 + 1) stays finite up to d = 340 (Gamma(171) = 170!); beyond that, or when an
# intermediate power overflows or underflows, the evaluator works in log space.
_DIRECT_MAX_DIMENSION = 340


def _evaluate(d: int, r: float) -> float:
    dimension = integer("d", d, minimum=1)
    non_negative("r", r)
    if r == 0:
        return 0.0
    half = dimension / 2.0
    if dimension <= _DIRECT_MAX_DIMENSION:
        try:
            volume = math.pi**half * r**dimension / math.gamma(half + 1.0)
        except OverflowError:
            volume = math.inf
        if 0 < volume < math.inf:
            return volume
    log_volume = half * math.log(math.pi) + dimension * math.log(r) - math.lgamma(half + 1.0)
    return math.exp(log_volume)


n_ball_volume = FormulaSpec(
    id="mathematics.n_ball_volume",
    name="Volume of a d-Dimensional Ball",
    equation="V = pi^(d/2) * r^d / Gamma(d/2 + 1)",
    description=(
        "Lebesgue volume (d-dimensional content) of a ball of radius r in d-dimensional "
        "Euclidean space. d = 1 gives the segment length 2r, d = 2 the disc area pi r^2 and "
        "d = 3 the solid sphere volume (see mathematics.sphere_volume)."
    ),
    inputs=(
        VariableSpec(
            name="d",
            symbol="d",
            description="Dimension of the space (positive integer)",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="r",
            symbol="r",
            description="Radius of the ball",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="V",
        symbol="V",
        description="d-dimensional volume of the ball (units of r^d)",
        dimension="L^d",
        si_unit="m^d",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib (EuclideanSpace R iota, d = card iota >= 1): volume(ball x r)
        #   = r^d * sqrt(pi)^d / Gamma(d/2 + 1) for r >= 0; sqrt(pi)^d = pi^(d/2).
        mathlib(
            "Mathlib/MeasureTheory/Measure/Lebesgue/VolumeOfBalls.lean#L308",
            "theorem EuclideanSpace.volume_ball",
        ),
        # Same Gamma form in any nontrivial (d >= 1) finite-dimensional real inner product space.
        mathlib(
            "Mathlib/MeasureTheory/Measure/Lebesgue/VolumeOfBalls.lean#L344",
            "theorem InnerProductSpace.volume_ball",
        ),
        # Closed forms for even d (pi^k / k! * r^d with d = 2k), used as a cross-check.
        mathlib(
            "Mathlib/MeasureTheory/Measure/Lebesgue/VolumeOfBalls.lean#L360",
            "lemma InnerProductSpace.volume_ball_of_dim_even",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"d": 1, "r": 1.0},
            expected=2.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "d = 1: segment of length 2r = 2; mpmath Gamma form, Mathlib odd-dimension "
                "closed form and slice integration agree."
            ),
        ),
        VerificationCase(
            inputs={"d": 2, "r": 1.0},
            expected=3.141592653589793,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "d = 2, unit disc: pi; mpmath Gamma form, even closed form pi^1/1! and slice "
                "integration agree."
            ),
        ),
        VerificationCase(
            inputs={"d": 3, "r": 2.0},
            expected=33.51032163829113,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "d = 3, r = 2: 32 pi / 3 = 33.5103216382911278...; mpmath Gamma form, odd closed "
                "form and slice integration agree."
            ),
        ),
        VerificationCase(
            inputs={"d": 4, "r": 1.0},
            expected=4.934802200544679,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "d = 4, r = 1: pi^2 / 2 = 4.9348022005446793...; mpmath Gamma form, even closed "
                "form and slice integration agree."
            ),
        ),
        VerificationCase(
            inputs={"d": 7, "r": 0.5},
            expected=0.036912234143214075,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "d = 7, r = 0.5: 16 pi^3 / 105 * 0.5^7 = 0.03691223414321407163...; mpmath Gamma "
                "form and odd closed form agree."
            ),
        ),
        VerificationCase(
            inputs={"d": 20, "r": 1.0},
            expected=0.02580689139001406,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "d = 20, r = 1: pi^10 / 10! = 0.02580689139001406001...; mpmath Gamma form and "
                "even closed form agree."
            ),
        ),
        VerificationCase(
            inputs={"d": 1, "r": 0.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-12,
            note="r = 0 gives volume 0 exactly.",
        ),
    ),
    assumptions=(
        "d is a whole number with d >= 1 (integral floats such as 3.0 are accepted); d = 0, "
        "fractional d and negative r raise ValueError.",
        "Euclidean (straight-line) distance in d dimensions; the open and closed balls have the "
        "same volume.",
        "The output dimension depends on the input d: V is in the radius unit raised to the "
        "power d, written L^d (m^d in SI). For d = 3 this is an ordinary volume, for d = 2 an "
        "area and for d = 1 a length.",
        "For d above 340, or when an intermediate power overflows or underflows, the value is "
        "computed in log space; its relative error then grows with the size of ln V (about "
        "1e-13 at d = 400). Results beyond the float range raise OverflowError or underflow "
        "to 0.",
    ),
    tags=("n-ball", "hypersphere", "volume", "Gamma function", "geometry"),
)
