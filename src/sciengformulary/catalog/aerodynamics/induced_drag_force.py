"""Induced Drag Force of a Finite Wing: D_i = L^2 / (q * pi * b^2 * e)."""

import math

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, nasa_glenn
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    L: float,  # noqa: N803
    q: float,
    b: float,
    e: float,
) -> float:
    finite("L", L)
    positive("q", q)
    positive("b", b)
    if not 0 < positive("e", e) <= 1:
        raise ValueError(f"e must satisfy 0 < e <= 1, got {e!r}.")
    return finite_result(L**2 / (q * math.pi * b**2 * e))


induced_drag_force = FormulaSpec(
    id="aerodynamics.induced_drag_force",
    name="Induced Drag Force of a Finite Wing",
    equation="D_i = L^2 / (q * pi * b^2 * e)",
    description=(
        "Induced drag, the drag due to lift, of a finite wing as a force, from the lift, the "
        "dynamic pressure, the span and the span efficiency factor. It is the dimensional form "
        "of aerodynamics.induced_drag_coefficient combined with aerodynamics.lift_force and "
        "aerodynamics.aspect_ratio: the wing area cancels, so it is not an input."
    ),
    inputs=(
        VariableSpec(
            name="L",
            symbol="L",
            description="Lift force (its sign does not matter)",
            dimension="M L T^-2",
            si_unit="N",
        ),
        VariableSpec(
            name="q",
            symbol="q",
            description="Dynamic pressure of the freestream",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="b",
            symbol="b",
            description="Wing span",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="e",
            symbol="e",
            description="Span efficiency factor (1 for an elliptic lift distribution)",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="D_i",
        symbol="D_i",
        description="Induced drag force",
        dimension="M L T^-2",
        si_unit="N",
    ),
    evaluator=_evaluate,
    references=(
        # Derived: C_di = C_l^2 / (pi AR e) with AR = s^2 / A (span s, wing area A) is printed on
        # the induced-drag-coefficient page; with C_l = L / (q A) (lift equation, L = C_l
        # (rho V^2 / 2) A) and D_i = C_di q A (drag equation of the terminal-velocity page, the
        # same dynamic-pressure form) the wing
        # area cancels and D_i = L^2 / (q pi b^2 e). Symbols: s -> b, A -> S (cancelled).
        nasa_glenn(
            "Induced Drag Coefficient",
            "induced-drag-coefficient",
            2023,
            "Induced Drag Coefficient",
            accessed=ENGINEERING_ACCESSED,
        ),
        nasa_glenn(
            "Lift Equation",
            "lift-equation",
            2024,
            "Lift Equation",
            accessed=ENGINEERING_ACCESSED,
        ),
        nasa_glenn(
            "Terminal Velocity Interactive",
            "termvel",
            2024,
            "Terminal Velocity Interactive",
            accessed=ENGINEERING_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"L": 20000.0, "q": 5000.0, "b": 10.0, "e": 1.0},
            expected=254.64790894703253,
            rel_tol=1e-12,
            note=(
                "Elliptic loading; mpmath evaluation of C_di * q * S with C_l = L / (q S) and "
                "AR = b^2 / S for an arbitrary S."
            ),
        ),
        VerificationCase(
            inputs={"L": 50000.0, "q": 2000.0, "b": 12.0, "e": 0.8},
            expected=3453.8833136262006,
            rel_tol=1e-12,
            note="e = 0.8; same mpmath construction through the coefficient form.",
        ),
        VerificationCase(
            inputs={"L": 0.0, "q": 2000.0, "b": 12.0, "e": 0.8},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Boundary case: zero lift gives zero induced drag.",
        ),
    ),
    assumptions=(
        "Derived result: C_di = C_l^2 / (pi AR e) with AR = b^2 / S, C_l = L / (q S) and "
        "D_i = C_di q S give D_i = L^2 / (q pi b^2 e); the wing area S cancels.",
        "Lifting-line theory for a planar wing in subsonic flow at small angle of attack; the "
        "source states the coefficient and e without derivation. e is 1 for an elliptic lift "
        "distribution and below 1 otherwise.",
        "L, q and b are in a consistent unit system, for example N, Pa and m.",
    ),
    tags=("induced drag", "drag due to lift", "finite wing", "lifting line"),
)
