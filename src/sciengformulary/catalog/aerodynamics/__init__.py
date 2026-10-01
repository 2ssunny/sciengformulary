"""Aerodynamics formulas."""

from sciengformulary.catalog.aerodynamics.dynamic_pressure import dynamic_pressure
from sciengformulary.core import FormulaSpec

FORMULAS: tuple[FormulaSpec, ...] = (
    dynamic_pressure,
)
