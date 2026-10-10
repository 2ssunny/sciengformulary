"""Angle Between a Line and a Plane: theta = pi/2 - arccos(|n . d| / (|n| |d|))."""

import math

from sciengformulary.catalog._sources import selinger_linear_algebra
from sciengformulary.catalog.mathematics.angle_between_lines_3d import _cross_norm_and_dot
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(dx: float, dy: float, dz: float, nx: float, ny: float, nz: float) -> float:
    cross, dot = _cross_norm_and_dot("n", (nx, ny, nz), "d", (dx, dy, dz))
    # With phi the angle between n and d folded into [0, pi/2] (a line has no sense), the
    # line-plane angle is pi/2 - phi, and sin(pi/2 - phi) = |n . d|/(|n||d|),
    # cos(pi/2 - phi) = |n x d|/(|n||d|). atan2 of these stays accurate near 0 and pi/2.
    return math.atan2(abs(dot), cross)


angle_between_line_and_plane = FormulaSpec(
    id="mathematics.angle_between_line_and_plane",
    name="Angle Between a Line and a Plane",
    equation=(
        "theta = pi/2 - arccos(|nx*dx + ny*dy + nz*dz| / (sqrt(nx^2 + ny^2 + nz^2) * sqrt(dx^2 + "
        "dy^2 + dz^2)))"
    ),
    description=(
        "Angle between a line with direction vector d and a plane with normal vector n: the "
        "complement of the angle between the line and the normal. The result lies between 0 (line "
        "parallel to the plane or inside it) and pi/2 (line perpendicular to the plane)."
    ),
    inputs=(
        VariableSpec(
            name="dx",
            symbol="d_x",
            description="x component of the line direction vector d",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="dy",
            symbol="d_y",
            description="y component of the line direction vector d",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="dz",
            symbol="d_z",
            description="z component of the line direction vector d",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="nx",
            symbol="n_x",
            description="x component of the plane normal vector n",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="ny",
            symbol="n_y",
            description="y component of the plane normal vector n",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="nz",
            symbol="n_z",
            description="z component of the plane normal vector n",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="theta",
        symbol=r"\theta",
        description="Angle between the line and the plane, in radians",
        dimension="1",
        si_unit="rad",
    ),
    evaluator=_evaluate,
    references=(
        # Source statement (sec. 3.2 example): the angle between a line and a plane is
        # pi/2 - phi, with phi the angle between the line's direction vector d and the plane's
        # normal n; the worked case has n.d > 0. Step: sec. 3.1 allows replacing d by -d (the
        # same line), so phi is folded to arccos(|n.d| / (|n||d|)) in [0, pi/2]; then
        # pi/2 - arccos(y) = arcsin(y) gives theta = arcsin(|n.d| / (|n||d|)) in [0, pi/2].
        selinger_linear_algebra("sec. 3.2, exa:angle-line-plane"),
        # A direction vector may be reversed, and angles involving a line take the smaller of
        # theta and pi - theta: this is what the absolute value of n.d implements.
        selinger_linear_algebra("sec. 3.1, exa:angle-between-two-lines"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"dx": 2, "dy": -1, "dz": -2, "nx": 2, "ny": 2, "nz": -1},
            expected=0.4605539916813224,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Worked example of the source (about 0.46 rad): pi / 2 - arccos(4 / 9), 50-digit "
                "mpmath."
            ),
        ),
        VerificationCase(
            inputs={"dx": -2, "dy": 1, "dz": 2, "nx": 2, "ny": 2, "nz": -1},
            expected=0.4605539916813224,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "The same line with reversed direction (n . d = -4) gives the same angle by the "
                "absolute-value rule (mpmath, 50 digits)."
            ),
        ),
        VerificationCase(
            inputs={"dx": 1, "dy": 2, "dz": 3, "nx": 4, "ny": -5, "nz": 6},
            expected=0.3741558840072683,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="pi / 2 - arccos(12 / sqrt(14 * 77)), 50-digit mpmath.",
        ),
        VerificationCase(
            inputs={"dx": 0, "dy": 0, "dz": -3, "nx": 0, "ny": 0, "nz": 1},
            expected=1.5707963267948966,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Line along the normal, opposite sense: upper end of the range, pi / 2.",
        ),
        VerificationCase(
            inputs={"dx": 1, "dy": 0, "dz": 0, "nx": 0, "ny": 0, "nz": 1},
            expected=0.0,
            rel_tol=0.0,
            abs_tol=1e-12,
            note=(
                "Direction perpendicular to the normal, so the line is parallel to the plane: "
                "lower end of the range, 0."
            ),
        ),
    ),
    assumptions=(
        "d is the direction vector of the line and n a normal vector of the plane; both must be "
        "non-zero, otherwise ValueError is raised. Their lengths and senses do not matter.",
        "Result in radians in [0, pi/2], the acute (or right) angle between the line and the "
        "plane: 0 when the line is parallel to the plane or lies in it (the formula does not tell "
        "these apart) and pi/2 when the line is perpendicular to the plane.",
        "Derived result: the source gives theta = pi/2 - arccos(n.d/(|n||d|)) in a worked example "
        "with n.d > 0; that literal form is negative when n.d < 0. Combining it with the source's "
        "rule from sec. 3.1 that -d is an equally valid direction vector gives the absolute value "
        "of n.d, and pi/2 - arccos(y) = arcsin(y) turns it into arcsin(|n.d|/(|n||d|)). The "
        "evaluator returns atan2(|n.d|, |n x d|), the same angle. The identities were checked "
        "with 50-digit mpmath, and the tests compare the evaluator with the pi/2 - arccos(...) "
        "form evaluated in mpmath, including reversed directions.",
        "The dot and cross products are formed exactly from the given floating-point components "
        "(after an exact power-of-two scaling of each vector) and rounded once, so lines that are "
        "nearly parallel to the plane or nearly perpendicular to it keep full relative accuracy. "
        "Measured: relative error below 3e-16 against 60+ digit mpmath on 2700 direction/normal "
        "pairs (component magnitudes 1e-300 to 1e300 with each vector scaled independently, "
        "directions within 1e-15 (relative) of parallel or of perpendicular). Outside that range "
        "accuracy is not characterised.",
    ),
    tags=(
        "angle between line and plane",
        "normal vector",
        "direction vector",
        "geometry",
        "linear algebra",
    ),
)
