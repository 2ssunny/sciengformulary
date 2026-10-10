"""Subsonic Center of Pressure of a Trapezoidal Fin, from Barrowman's method."""

from sciengformulary.catalog._domain import finite, finite_result, non_negative
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(x_t: float, c_r: float, c_t: float) -> float:
    finite("x_t", x_t)
    non_negative("c_r", c_r)
    non_negative("c_t", c_t)
    if c_r + c_t == 0:
        raise ValueError("c_r and c_t must not both be zero.")
    chord_sum = c_r + c_t
    # Ratios are formed before products (c_r * (c_t / chord_sum)) so that tiny or huge lengths
    # neither underflow nor overflow.
    position = (x_t / 3.0) * ((c_r + 2.0 * c_t) / chord_sum) + (
        chord_sum - c_r * (c_t / chord_sum)
    ) / 6.0
    return finite_result(position)


trapezoidal_fin_center_of_pressure = FormulaSpec(
    id="aerodynamics.trapezoidal_fin_center_of_pressure",
    name="Subsonic Center of Pressure of a Trapezoidal Fin",
    equation=(
        "x_f = (x_t / 3) * (c_r + 2 * c_t) / (c_r + c_t) "
        "+ (1 / 6) * (c_r + c_t - c_r * c_t / (c_r + c_t))"
    ),
    description=(
        "Distance, measured parallel to the root chord from the leading edge of the fin root, "
        "of the subsonic center of pressure of a trapezoidal fin, taken at the quarter-chord "
        "point of the mean aerodynamic chord. Part of Barrowman's method; add the distance "
        "from the nose tip to the root leading edge to get the position from the nose."
    ),
    inputs=(
        VariableSpec(
            name="x_t",
            symbol="x_t",
            description=(
                "Distance between the leading edge of the root chord and the leading edge of "
                "the tip chord, measured parallel to the root (positive when swept back)"
            ),
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="c_r",
            symbol="c_r",
            description="Root chord",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="c_t",
            symbol="c_t",
            description="Tip chord (zero for a delta-shaped fin)",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="x_f",
        symbol="x_f",
        description="Chordwise center-of-pressure position from the root leading edge",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # Stated, with one change: eq. (3-30) prints X_T = l_T + (x_t/3)(c_r + 2 c_t)/(c_r + c_t)
        # + (1/6)[c_r + c_t - c_r c_t/(c_r + c_t)], built from the mean aerodynamic chord
        # (3-24), its spanwise position (3-26) and the quarter-chord rule (3-28), (3-29).
        # Here the offset l_T of the root leading edge from the nose is dropped, so x_f is
        # X_T - l_T. Symbols: X_T - l_T -> x_f.
        nasa_technical_report(
            "The Practical Calculation of the Aerodynamic Characteristics of Slender Finned "
            "Vehicles",
            ("J. S. Barrowman",),
            "NASA/TM-2001-209983",
            1967,
            "https://ntrs.nasa.gov/citations/20010047838",
            "sec. 3.12, eqs. (3-13), (3-18), (3-24), (3-26), (3-28), (3-29), (3-30), pp. 7-10",
            organization=(
                "NASA Goddard Space Flight Center (reissue of a March 1967 Catholic "
                "University of America master's dissertation)"
            ),
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"c_r": 0.12, "c_t": 0.06, "x_t": 0.06},
            expected=0.049999999999999996,
            rel_tol=1e-11,
            note=(
                "Fin with root chord 0.12 m, tip chord 0.06 m, span 0.1 m and tip offset "
                "0.06 m; mpmath quadrature of the mean-chord definition (3-13)."
            ),
        ),
        VerificationCase(
            inputs={"c_r": 0.2, "c_t": 0.2, "x_t": 0.0},
            expected=0.05,
            rel_tol=1e-11,
            note="Boundary case: rectangular fin, center of pressure at a quarter chord.",
        ),
        VerificationCase(
            inputs={"c_r": 0.1, "c_t": 0.0, "x_t": 0.1},
            expected=0.05,
            rel_tol=1e-11,
            note="Boundary case: delta fin with zero tip chord; mpmath quadrature of (3-13).",
        ),
        VerificationCase(
            inputs={"c_r": 0.3, "c_t": 0.1, "x_t": 0.25},
            expected=0.15833333333333333,
            rel_tol=1e-11,
            note="Swept tapered fin; mpmath quadrature of the mean-chord definition (3-13).",
        ),
    ),
    assumptions=(
        "Derived result: the source prints X_T = l_T + (x_t/3)(c_r + 2 c_t)/(c_r + c_t) + "
        "(1/6)[c_r + c_t - c_r c_t/(c_r + c_t)] (eq. 3-30), with l_T the distance from the "
        "nose to the root leading edge; this formula returns X_T - l_T, measured from the "
        "root leading edge.",
        "Barrowman's method, subsonic flow: the section center of pressure is at a quarter "
        "chord and the fin center of pressure lies on the quarter-chord line at the mean "
        "aerodynamic chord, independent of Mach number in this treatment. Supersonic fins "
        "need the source's separate strip theory, which is not included.",
        "Straight-edged trapezoidal planform with arbitrary sweep. Lengths are measured "
        "parallel to the root chord from the leading edge of the root; c_r and c_t are not "
        "negative and not both zero, x_t may have either sign; any consistent length unit.",
    ),
    tags=("fin", "center of pressure", "mean aerodynamic chord", "Barrowman", "rocket"),
)
