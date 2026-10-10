"""Wave Drag Area of a Sears-Haack Body: D_w / q = 128 * V^2 / (pi * L^4)."""

import math

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(V: float, L: float) -> float:  # noqa: N803
    non_negative("V", V)
    positive("L", L)
    return finite_result(128.0 * V**2 / (math.pi * L**4))


sears_haack_wave_drag_area = FormulaSpec(
    id="aerodynamics.sears_haack_wave_drag_area",
    name="Wave Drag Area of a Sears-Haack Body",
    equation="D_over_q = 128 * V^2 / (pi * L^4)",
    description=(
        "Supersonic wave drag divided by dynamic pressure, an area, of the closed slender "
        "body of minimum wave drag for a given volume and length (the Sears-Haack body). "
        "Multiply by the dynamic pressure from aerodynamics.dynamic_pressure to get the wave "
        "drag force; skin friction is not included."
    ),
    inputs=(
        VariableSpec(
            name="V",
            symbol="V",
            description="Body volume",
            dimension="L^3",
            si_unit="m^3",
        ),
        VariableSpec(
            name="L",
            symbol="L",
            description="Body length",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="D_over_q",
        symbol="D_w/q",
        description="Wave drag divided by dynamic pressure (drag area)",
        dimension="L^2",
        si_unit="m^2",
    ),
    evaluator=_evaluate,
    references=(
        # Stated: eq. (15) gives D_w/q = 128 V_b^2 / (pi l^4) for a Sears-Haack body from
        # slender-body theory; eq. (16) gives C_Dw = 24 V_b / l^3 on the maximum cross-section,
        # which agrees with it for A_max = 16 V / (3 pi l) (see the tests). Symbols: V_b -> V,
        # l -> L. The report takes the slender-body result from a reference that was not opened.
        nasa_technical_report(
            "An Experimental and Analytical Study of the Aerodynamic Interference Effects "
            "Between Two Sears-Haack Bodies at Mach 2.7",
            ("J. W. Bantle",),
            "NASA TM-85729",
            1985,
            "https://ntrs.nasa.gov/citations/19850018362",
            "sec. 'Bodies Alone', eq. (15), p. 33 (eq. (14) p. 32; eq. (16) p. 33)",
            organization="NASA Langley Research Center",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"V": 0.0002, "L": 1.0},
            expected=1.6297466172610084e-06,
            rel_tol=1e-12,
            note="V = 2e-4 m^3, L = 1 m; 50-digit mpmath evaluation of eq. (15).",
        ),
        VerificationCase(
            inputs={"V": 0.05, "L": 3.0},
            expected=0.0012575205380100374,
            rel_tol=1e-12,
            note="V = 0.05 m^3, L = 3 m; 50-digit mpmath evaluation of eq. (15).",
        ),
        VerificationCase(
            inputs={"V": 0.0, "L": 2.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Boundary case: zero volume gives zero wave drag.",
        ),
    ),
    assumptions=(
        "Linearised supersonic slender-body theory; the body has the Sears-Haack area "
        "distribution S(x) = A_max (4 x (L - x) / L^2)^(3/2). It does not apply to other "
        "shapes.",
        "Wave drag only: skin-friction and base drag are not included.",
        "V is not negative and L is positive; any consistent unit system works.",
    ),
    tags=("wave drag", "Sears-Haack", "supersonic", "slender body"),
)
