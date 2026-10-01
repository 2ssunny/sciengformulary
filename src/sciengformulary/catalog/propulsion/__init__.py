"""Propulsion formulas."""

from sciengformulary.catalog.propulsion.rocket_thrust import rocket_thrust
from sciengformulary.catalog.propulsion.specific_impulse import specific_impulse
from sciengformulary.core import FormulaSpec

FORMULAS: tuple[FormulaSpec, ...] = (
    rocket_thrust,
    specific_impulse,
)
