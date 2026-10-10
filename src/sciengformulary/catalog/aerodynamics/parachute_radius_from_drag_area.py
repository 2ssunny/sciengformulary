"""Parachute Canopy Radius from Drag Area: R = sqrt(CdS / (C_D * pi))."""

import math

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, mathlib, nasa_glenn
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(CdS: float, C_D: float) -> float:  # noqa: N803
    non_negative("CdS", CdS)
    positive("C_D", C_D)
    return finite_result(math.sqrt(CdS / (C_D * math.pi)))


parachute_radius_from_drag_area = FormulaSpec(
    id="aerodynamics.parachute_radius_from_drag_area",
    name="Parachute Canopy Radius from Drag Area",
    equation="R = sqrt(CdS / (C_D * pi))",
    description=(
        "Radius of a circular canopy whose projected area is the reference area of its drag "
        "coefficient, from the measured drag area C_D S and the drag coefficient C_D. It is "
        "mathematics.circle_area inverted for the area S = CdS / C_D; use "
        "aerodynamics.terminal_velocity_drag_area to obtain CdS from a descent."
    ),
    inputs=(
        VariableSpec(
            name="CdS",
            symbol="C_D S",
            description="Drag area of the canopy, drag coefficient times reference area",
            dimension="L^2",
            si_unit="m^2",
        ),
        VariableSpec(
            name="C_D",
            symbol="C_D",
            description="Drag coefficient referenced to the projected canopy area",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="R",
        symbol="R",
        description="Radius of the inflated, projected circular canopy",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # Derived: the page defines the drag through D = C_d rho V^2 A / 2 with A a reference
        # area, so the drag area is C_d A and A = CdS / C_D. Symbol: A -> S.
        nasa_glenn(
            "Terminal Velocity Interactive",
            "termvel",
            2024,
            "Terminal Velocity Interactive",
            accessed=ENGINEERING_ACCESSED,
        ),
        # The area of a disc of radius R is pi R^2 (the statement cited by
        # mathematics.circle_area), so S = pi R^2 and R = sqrt(S / pi).
        mathlib(
            "Mathlib/MeasureTheory/Measure/Lebesgue/VolumeOfBalls.lean#L395",
            "lemma EuclideanSpace.volume_ball_fin_two",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"CdS": 1.0, "C_D": 1.5},
            expected=0.46065886596178063,
            rel_tol=1e-11,
            note="Drag area 1.0 m^2 and C_D 1.5; mpmath root of pi R^2 = CdS / C_D.",
        ),
        VerificationCase(
            inputs={"CdS": 2.5, "C_D": 0.75},
            expected=1.0300645387285055,
            rel_tol=1e-11,
            note="Drag area 2.5 m^2 and C_D 0.75; mpmath root of pi R^2 = CdS / C_D.",
        ),
        VerificationCase(
            inputs={"CdS": 0.04, "C_D": 1.0},
            expected=0.11283791670955126,
            rel_tol=1e-11,
            note="Small drag area, C_D 1: R = sqrt(0.04 / pi); mpmath root of pi R^2 = S.",
        ),
    ),
    assumptions=(
        "Derived result: the reference area is S = CdS / C_D (definition of drag area in the "
        "drag equation) and a circle of radius R has area pi R^2, so R = sqrt(CdS / (C_D pi)).",
        "C_D must be referenced to the projected (inflated) circular canopy area pi R^2, not "
        "to the cloth area. A drag coefficient taken from a different reference area gives a "
        "wrong radius.",
        "CdS is not negative; a zero drag area gives a zero radius. Any consistent length "
        "unit works; SI is documented.",
    ),
    tags=("parachute", "drag area", "canopy", "geometry"),
)
