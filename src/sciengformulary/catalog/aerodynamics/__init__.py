"""Aerodynamics formulas."""

from sciengformulary.catalog.aerodynamics.aspect_ratio import aspect_ratio
from sciengformulary.catalog.aerodynamics.drag_force import drag_force
from sciengformulary.catalog.aerodynamics.dynamic_pressure import dynamic_pressure
from sciengformulary.catalog.aerodynamics.induced_drag_coefficient import induced_drag_coefficient
from sciengformulary.catalog.aerodynamics.isentropic_density_ratio import isentropic_density_ratio
from sciengformulary.catalog.aerodynamics.isentropic_pressure_ratio import isentropic_pressure_ratio
from sciengformulary.catalog.aerodynamics.isentropic_temperature_ratio import (
    isentropic_temperature_ratio,
)
from sciengformulary.catalog.aerodynamics.lift_force import lift_force
from sciengformulary.catalog.aerodynamics.mach_number import mach_number
from sciengformulary.catalog.aerodynamics.normal_shock_density_ratio import (
    normal_shock_density_ratio,
)
from sciengformulary.catalog.aerodynamics.normal_shock_downstream_mach import (
    normal_shock_downstream_mach,
)
from sciengformulary.catalog.aerodynamics.normal_shock_pressure_ratio import (
    normal_shock_pressure_ratio,
)
from sciengformulary.catalog.aerodynamics.normal_shock_total_pressure_ratio import (
    normal_shock_total_pressure_ratio,
)
from sciengformulary.catalog.aerodynamics.speed_of_sound_ideal_gas import speed_of_sound_ideal_gas
from sciengformulary.core import FormulaSpec

FORMULAS: tuple[FormulaSpec, ...] = (
    dynamic_pressure,
    lift_force,
    drag_force,
    induced_drag_coefficient,
    aspect_ratio,
    speed_of_sound_ideal_gas,
    mach_number,
    isentropic_temperature_ratio,
    isentropic_pressure_ratio,
    isentropic_density_ratio,
    normal_shock_pressure_ratio,
    normal_shock_density_ratio,
    normal_shock_downstream_mach,
    normal_shock_total_pressure_ratio,
)
