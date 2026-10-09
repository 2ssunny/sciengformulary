"""Angle Between Two Lines in 3-D: phi = arccos(|u . v| / (|u| |v|))."""

import math
from fractions import Fraction

from sciengformulary.catalog._sources import selinger_linear_algebra
from sciengformulary.catalog.mathematics._domain import finite
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _cross_norm_and_dot(
    first_name: str,
    first: tuple[float, float, float],
    second_name: str,
    second: tuple[float, float, float],
) -> tuple[float, float]:
    """Return (|first x second|, first . second) for two non-zero 3-D vectors.

    The angle does not depend on the lengths, so each vector is first scaled by an exact power
    of two that brings its largest component near 1; products of very small or very large
    components then cannot underflow or overflow. The dot product and the cross-product
    components are formed exactly with rational arithmetic and rounded once, so nearly parallel
    or nearly perpendicular vectors do not lose digits to cancellation. Shared by
    ``angle_between_lines_3d`` and ``angle_between_line_and_plane``.
    """
    scaled = []
    for name, vector in ((first_name, first), (second_name, second)):
        for axis, value in zip("xyz", vector):
            finite(f"{name}{axis}", value)
        if not any(vector):
            raise ValueError(
                f"{name} must be a non-zero vector; the angle is undefined for {name} = 0."
            )
        exact = [Fraction(value) for value in vector]
        largest = max(abs(component) for component in exact)
        shift = Fraction(2) ** (largest.denominator.bit_length() - largest.numerator.bit_length())
        scaled.append([component * shift for component in exact])
    (ax, ay, az), (bx, by, bz) = scaled
    cross = math.hypot(float(ay * bz - az * by), float(az * bx - ax * bz), float(ax * by - ay * bx))
    return cross, float(ax * bx + ay * by + az * bz)


def _evaluate(ux: float, uy: float, uz: float, vx: float, vy: float, vz: float) -> float:
    cross, dot = _cross_norm_and_dot("u", (ux, uy, uz), "v", (vx, vy, vz))
    # |u x v| = |u| |v| sin(theta) and u . v = |u| |v| cos(theta) for the angle theta in
    # [0, pi] between the vectors, so atan2(|u x v|, |u . v|) = arccos(|u . v| / (|u| |v|)).
    # Unlike arccos of a rounded cosine it stays accurate near 0 and pi/2.
    return math.atan2(cross, abs(dot))


angle_between_lines_3d = FormulaSpec(
    id="mathematics.angle_between_lines_3d",
    name="Angle Between Two Lines in 3-D",
    equation=(
        "phi = arccos(|ux*vx + uy*vy + uz*vz| / (sqrt(ux^2 + uy^2 + uz^2) * sqrt(vx^2 + vy^2 + "
        "vz^2)))"
    ),
    description=(
        "Angle between two lines in space given by direction vectors u and v. A line has no "
        "preferred direction, so the angle between the direction vectors is folded to the smaller "
        "of theta and pi - theta; the result lies between 0 and pi/2."
    ),
    inputs=(
        VariableSpec(
            name="ux",
            symbol="u_x",
            description="x component of the direction vector u of line 1",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="uy",
            symbol="u_y",
            description="y component of the direction vector u of line 1",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="uz",
            symbol="u_z",
            description="z component of the direction vector u of line 1",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="vx",
            symbol="v_x",
            description="x component of the direction vector v of line 2",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="vy",
            symbol="v_y",
            description="y component of the direction vector v of line 2",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="vz",
            symbol="v_z",
            description="z component of the direction vector v of line 2",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="phi",
        symbol=r"\varphi",
        description="Angle between the two lines, in radians",
        dimension="1",
        si_unit="rad",
    ),
    evaluator=_evaluate,
    references=(
        # Source statement (sec. 3.1): the angle between two lines is found from the dot product
        # of direction vectors; since -u is also a direction vector, the result is the smaller
        # of theta and pi - theta. Step: min(theta, pi - theta) = arccos(|u.v| / (|u| |v|))
        # because arccos is decreasing and arccos(-x) = pi - arccos(x).
        selinger_linear_algebra("sec. 3.1, exa:angle-between-two-lines"),
        # u . v = |u| |v| cos(theta) with theta in [0, pi]: supplies theta for the folding step.
        selinger_linear_algebra("sec. 2.6, prop:dot-product-angle"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"ux": -1, "uy": 1, "uz": 2, "vx": 2, "vy": 1, "vz": -1},
            expected=1.0471975511965979,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Direction vectors of the source's worked example: the vector angle 2 pi / 3 folds "
                "to pi / 3; 50-digit mpmath arccos with the min(theta, pi - theta) rule."
            ),
        ),
        VerificationCase(
            inputs={"ux": 1, "uy": 2, "uz": 3, "vx": 4, "vy": -5, "vz": 6},
            expected=1.1966404427876283,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Acute vector angle arccos(12 / sqrt(14 * 77)) is kept as it is (mpmath, 50 "
                "digits)."
            ),
        ),
        VerificationCase(
            inputs={"ux": 1, "uy": 0, "uz": 0, "vx": -1, "vy": 1, "vz": 0},
            expected=0.7853981633974483,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Vector angle 3 pi / 4 folds to pi / 4 (mpmath, 50 digits).",
        ),
        VerificationCase(
            inputs={"ux": 1, "uy": 0, "uz": 0, "vx": 0, "vy": 1, "vz": 0},
            expected=1.5707963267948966,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Perpendicular lines: upper end of the range, pi / 2.",
        ),
        VerificationCase(
            inputs={"ux": 1, "uy": 2, "uz": 3, "vx": -2, "vy": -4, "vz": -6},
            expected=0.0,
            rel_tol=0.0,
            abs_tol=1e-12,
            note=(
                "Antiparallel direction vectors describe parallel lines: lower end of the range, 0."
            ),
        ),
    ),
    assumptions=(
        "Each line is given by a non-zero direction vector; both vectors must be non-zero, "
        "otherwise ValueError is raised. The sign and the length of a direction vector do not "
        "matter.",
        "Result in radians in [0, pi/2]: 0 for parallel (or identical) lines and pi/2 for "
        "perpendicular lines. It differs from angle_between_vectors_3d, which returns the angle "
        "in [0, pi] and distinguishes the sense of the vectors, whenever the vectors make an "
        "obtuse angle.",
        "The value depends only on the directions, so skew lines get the angle between their "
        "directions; the source works the example for intersecting lines.",
        "Derived result: the source takes the smaller of theta and pi - theta, where theta is the "
        "angle between the direction vectors; that equals arccos(|u.v|/(|u||v|)) because arccos "
        "is decreasing and arccos(-x) = pi - arccos(x). The evaluator returns atan2(|u x v|, |u . "
        "v|), which is the same angle for non-zero vectors. The equality was checked with "
        "50-digit mpmath at several points, and the tests compare the evaluator with the source's "
        "min(theta, pi - theta) form evaluated in mpmath, including angles within 1e-9 of 0 and "
        "of pi/2.",
        "The dot and cross products are formed exactly from the given floating-point components "
        "(after an exact power-of-two scaling of each vector) and rounded once, so nearly "
        "parallel and nearly perpendicular directions keep full relative accuracy. Measured: "
        "relative error below 3e-16 against 60+ digit mpmath arccos on 2700 direction pairs "
        "(component magnitudes 1e-300 to 1e300 with each vector scaled independently, directions "
        "within 1e-15 (relative) of parallel or of perpendicular). Outside that range accuracy is "
        "not characterised.",
    ),
    tags=(
        "angle between lines",
        "direction vector",
        "lines in space",
        "geometry",
        "linear algebra",
    ),
)
