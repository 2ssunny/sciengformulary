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
from sciengformulary.catalog.aerodynamics.barometric_pressure_gradient_layer import (
    barometric_pressure_gradient_layer,
)
from sciengformulary.catalog.aerodynamics.barometric_pressure_isothermal_layer import (
    barometric_pressure_isothermal_layer,
)
from sciengformulary.catalog.aerodynamics.climb_gradient import climb_gradient
from sciengformulary.catalog.aerodynamics.conical_transition_center_of_pressure import (
    conical_transition_center_of_pressure,
)
from sciengformulary.catalog.aerodynamics.conical_transition_normal_force_slope import (
    conical_transition_normal_force_slope,
)
from sciengformulary.catalog.aerodynamics.density_altitude import density_altitude
from sciengformulary.catalog.aerodynamics.energy_height import energy_height
from sciengformulary.catalog.aerodynamics.geopotential_height import geopotential_height
from sciengformulary.catalog.aerodynamics.induced_drag_force import induced_drag_force
from sciengformulary.catalog.aerodynamics.isentropic_area_mach_ratio import (
    isentropic_area_mach_ratio,
)
from sciengformulary.catalog.aerodynamics.isentropic_mass_flow_rate import isentropic_mass_flow_rate
from sciengformulary.catalog.aerodynamics.nose_normal_force_slope import nose_normal_force_slope
from sciengformulary.catalog.aerodynamics.parachute_radius_from_drag_area import (
    parachute_radius_from_drag_area,
)
from sciengformulary.catalog.aerodynamics.power_series_nose_center_of_pressure import (
    power_series_nose_center_of_pressure,
)
from sciengformulary.catalog.aerodynamics.sears_haack_wave_drag_area import (
    sears_haack_wave_drag_area,
)
from sciengformulary.catalog.aerodynamics.single_fin_normal_force_slope import (
    single_fin_normal_force_slope,
)
from sciengformulary.catalog.aerodynamics.slender_body_center_of_pressure_from_volume import (
    slender_body_center_of_pressure_from_volume,
)
from sciengformulary.catalog.aerodynamics.stall_speed import stall_speed
from sciengformulary.catalog.aerodynamics.terminal_velocity_drag_area import (
    terminal_velocity_drag_area,
)
from sciengformulary.catalog.aerodynamics.trapezoid_mac_spanwise_location import (
    trapezoid_mac_spanwise_location,
)
from sciengformulary.catalog.aerodynamics.trapezoidal_fin_center_of_pressure import (
    trapezoidal_fin_center_of_pressure,
)
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
    barometric_pressure_gradient_layer,
    barometric_pressure_isothermal_layer,
    climb_gradient,
    conical_transition_center_of_pressure,
    conical_transition_normal_force_slope,
    density_altitude,
    energy_height,
    geopotential_height,
    induced_drag_force,
    isentropic_area_mach_ratio,
    isentropic_mass_flow_rate,
    nose_normal_force_slope,
    parachute_radius_from_drag_area,
    power_series_nose_center_of_pressure,
    sears_haack_wave_drag_area,
    single_fin_normal_force_slope,
    slender_body_center_of_pressure_from_volume,
    stall_speed,
    terminal_velocity_drag_area,
    trapezoid_mac_spanwise_location,
    trapezoidal_fin_center_of_pressure,
)
