"""Spanwise Location of the Mean Aerodynamic Chord of a Trapezoid (Barrowman)."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(s: float, c_r: float, c_t: float) -> float:
    positive("s", s)
    non_negative("c_r", c_r)
    non_negative("c_t", c_t)
    if c_r + c_t == 0:
        raise ValueError("c_r and c_t must not both be zero.")
    # Divide before multiplying so that tiny or huge lengths do not underflow or overflow.
    return finite_result((s / 3.0) * ((c_r + 2.0 * c_t) / (c_r + c_t)))


trapezoid_mac_spanwise_location = FormulaSpec(
    id="aerodynamics.trapezoid_mac_spanwise_location",
    name="Spanwise Location of the Mean Aerodynamic Chord of a Trapezoid",
    equation="Y_mac = (s / 3) * (c_r + 2 * c_t) / (c_r + c_t)",
    description=(
        "Distance from the root chord, along the span, at which the chord of a "
        "straight-tapered (trapezoidal) panel equals its mean aerodynamic chord. It locates "
        "the chord on which Barrowman's method places the fin center of pressure."
    ),
    inputs=(
        VariableSpec(
            name="s",
            symbol="s",
            description="Span of the panel, root to tip, measured perpendicular to the root",
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
            description="Tip chord (zero for a delta-shaped panel)",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="Y_mac",
        symbol="Y_MA",
        description="Spanwise location of the mean aerodynamic chord, measured from the root",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # Stated: eq. (3-26) prints Y_MA = (s/3)(c_r + 2 c_t)/(c_r + c_t), the solution of
        # c(Y_MA) = c_MA (3-25) for the mean aerodynamic chord of (3-13), (3-18) and (3-24).
        # Symbols: Y_MA -> Y_mac.
        nasa_technical_report(
            "The Practical Calculation of the Aerodynamic Characteristics of Slender Finned "
            "Vehicles",
            ("J. S. Barrowman",),
            "NASA/TM-2001-209983",
            1967,
            "https://ntrs.nasa.gov/citations/20010047838",
            "sec. 3.12, eq. (3-26), p. 10 (with (3-13), (3-18), (3-24), (3-25))",
            organization=(
                "NASA Goddard Space Flight Center (reissue of a March 1967 Catholic "
                "University of America master's dissertation)"
            ),
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"c_r": 0.12, "c_t": 0.06, "s": 0.1},
            expected=0.044444444444444446,
            rel_tol=1e-11,
            note=(
                "Fin with root chord 0.12 m, tip chord 0.06 m and span 0.1 m; mpmath "
                "quadrature of the mean-chord definition (3-13) and solution of c(y) = c_MA."
            ),
        ),
        VerificationCase(
            inputs={"c_r": 0.2, "c_t": 0.2, "s": 0.15},
            expected=0.075,
            rel_tol=1e-11,
            note="Boundary case: rectangular panel, mean chord at mid-span.",
        ),
        VerificationCase(
            inputs={"c_r": 0.1, "c_t": 0.0, "s": 0.05},
            expected=0.016666666666666666,
            rel_tol=1e-11,
            note="Boundary case: delta panel with zero tip chord, one third of the span.",
        ),
        VerificationCase(
            inputs={"c_r": 0.3, "c_t": 0.1, "s": 0.12},
            expected=0.049999999999999996,
            rel_tol=1e-11,
            note="Swept tapered panel; mpmath quadrature of (3-13) and solution of c(y) = c_MA.",
        ),
    ),
    assumptions=(
        "Trapezoidal planform with straight leading and trailing edges; the mean "
        "aerodynamic chord is the integral of the squared chord over the span divided by the "
        "planform area (eq. 3-13). Sweep does not enter, because only the chord distribution "
        "along the span matters.",
        "The span is measured from the root chord to the tip chord; c_r and c_t are not "
        "negative and not both zero; any consistent length unit.",
        "This is geometry used by Barrowman's subsonic fin method (sec. 3.12) and carries no "
        "flow assumption of its own.",
    ),
    tags=("mean aerodynamic chord", "trapezoid", "wing geometry", "fin", "Barrowman"),
)
