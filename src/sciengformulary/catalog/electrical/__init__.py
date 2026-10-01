"""Electrical formulas."""

from sciengformulary.catalog.electrical.conductor_resistance import conductor_resistance
from sciengformulary.catalog.electrical.ohms_law_voltage import ohms_law_voltage
from sciengformulary.core import FormulaSpec

FORMULAS: tuple[FormulaSpec, ...] = (
    ohms_law_voltage,
    conductor_resistance,
)
