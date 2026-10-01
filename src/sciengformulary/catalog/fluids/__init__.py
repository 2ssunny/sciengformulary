"""Fluids formulas."""

from sciengformulary.catalog.fluids.hydrostatic_pressure_difference import (
    hydrostatic_pressure_difference,
)
from sciengformulary.catalog.fluids.kinematic_viscosity import kinematic_viscosity
from sciengformulary.catalog.fluids.mass_flow_rate import mass_flow_rate
from sciengformulary.catalog.fluids.newtonian_shear_stress import newtonian_shear_stress
from sciengformulary.catalog.fluids.pitot_static_airspeed import pitot_static_airspeed
from sciengformulary.catalog.fluids.poiseuille_volume_flow_rate import poiseuille_volume_flow_rate
from sciengformulary.catalog.fluids.reynolds_number import reynolds_number
from sciengformulary.catalog.fluids.stokes_drag_force import stokes_drag_force
from sciengformulary.core import FormulaSpec

FORMULAS: tuple[FormulaSpec, ...] = (
    hydrostatic_pressure_difference,
    mass_flow_rate,
    newtonian_shear_stress,
    kinematic_viscosity,
    reynolds_number,
    pitot_static_airspeed,
    poiseuille_volume_flow_rate,
    stokes_drag_force,
)
