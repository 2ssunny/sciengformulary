"""Aerodynamics formulas."""

from auto_3dx_formulas.catalog.aerodynamics.dynamic_pressure import dynamic_pressure
from auto_3dx_formulas.core import FormulaSpec

FORMULAS: tuple[FormulaSpec, ...] = (
    dynamic_pressure,
)
