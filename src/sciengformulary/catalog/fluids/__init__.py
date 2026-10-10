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
from sciengformulary.catalog.fluids.bond_number import bond_number
from sciengformulary.catalog.fluids.chezy_coefficient_from_manning import (
    chezy_coefficient_from_manning,
)
from sciengformulary.catalog.fluids.chezy_velocity import chezy_velocity
from sciengformulary.catalog.fluids.darcy_weisbach_pressure_drop import darcy_weisbach_pressure_drop
from sciengformulary.catalog.fluids.filonenko_smooth_pipe_friction_factor import (
    filonenko_smooth_pipe_friction_factor,
)
from sciengformulary.catalog.fluids.haaland_friction_factor import haaland_friction_factor
from sciengformulary.catalog.fluids.laminar_darcy_friction_factor import (
    laminar_darcy_friction_factor,
)
from sciengformulary.catalog.fluids.manning_velocity import manning_velocity
from sciengformulary.catalog.fluids.smooth_pipe_friction_factor_power_law import (
    smooth_pipe_friction_factor_power_law,
)
from sciengformulary.catalog.fluids.strouhal_number import strouhal_number
from sciengformulary.catalog.fluids.weber_number import weber_number
from sciengformulary.catalog.fluids.laminar_flat_plate_mean_skin_friction import (
    laminar_flat_plate_mean_skin_friction,
)
from sciengformulary.catalog.fluids.sutherland_viscosity_air import sutherland_viscosity_air
from sciengformulary.catalog.fluids.wind_shear_power_law import wind_shear_power_law
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
    bond_number,
    chezy_coefficient_from_manning,
    chezy_velocity,
    darcy_weisbach_pressure_drop,
    filonenko_smooth_pipe_friction_factor,
    haaland_friction_factor,
    laminar_darcy_friction_factor,
    manning_velocity,
    smooth_pipe_friction_factor_power_law,
    strouhal_number,
    weber_number,
    laminar_flat_plate_mean_skin_friction,
    sutherland_viscosity_air,
    wind_shear_power_law,
)
