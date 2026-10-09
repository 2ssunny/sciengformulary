"""Mechanics formulas."""

from sciengformulary.catalog.mechanics.angular_momentum_rigid_body import (
    angular_momentum_rigid_body,
)
from sciengformulary.catalog.mechanics.centripetal_acceleration import centripetal_acceleration
from sciengformulary.catalog.mechanics.circular_motion_period import circular_motion_period
from sciengformulary.catalog.mechanics.constant_acceleration_position import (
    constant_acceleration_position,
)
from sciengformulary.catalog.mechanics.constant_acceleration_speed_squared import (
    constant_acceleration_speed_squared,
)
from sciengformulary.catalog.mechanics.constant_acceleration_velocity import (
    constant_acceleration_velocity,
)
from sciengformulary.catalog.mechanics.critical_damping_coefficient import (
    critical_damping_coefficient,
)
from sciengformulary.catalog.mechanics.damped_angular_frequency import damped_angular_frequency
from sciengformulary.catalog.mechanics.forced_vibration_amplitude import forced_vibration_amplitude
from sciengformulary.catalog.mechanics.gravitational_force import gravitational_force
from sciengformulary.catalog.mechanics.gravitational_potential_energy import (
    gravitational_potential_energy,
)
from sciengformulary.catalog.mechanics.impulse_of_constant_force import impulse_of_constant_force
from sciengformulary.catalog.mechanics.kinetic_friction_force import kinetic_friction_force
from sciengformulary.catalog.mechanics.linear_drag_falling_speed import linear_drag_falling_speed
from sciengformulary.catalog.mechanics.natural_angular_frequency import natural_angular_frequency
from sciengformulary.catalog.mechanics.parallel_axis_moment_of_inertia import (
    parallel_axis_moment_of_inertia,
)
from sciengformulary.catalog.mechanics.rotational_kinetic_energy import rotational_kinetic_energy
from sciengformulary.catalog.mechanics.static_friction_limit import static_friction_limit
from sciengformulary.catalog.mechanics.tangential_speed import tangential_speed
from sciengformulary.catalog.mechanics.translational_kinetic_energy import (
    translational_kinetic_energy,
)
from sciengformulary.catalog.mechanics.weight import weight
from sciengformulary.catalog.mechanics.linear_spring_force import linear_spring_force
from sciengformulary.catalog.mechanics.torque_from_tangential_force import (
    torque_from_tangential_force,
)
from sciengformulary.core import FormulaSpec

FORMULAS: tuple[FormulaSpec, ...] = (
    weight,
    static_friction_limit,
    kinetic_friction_force,
    constant_acceleration_velocity,
    constant_acceleration_position,
    constant_acceleration_speed_squared,
    tangential_speed,
    circular_motion_period,
    centripetal_acceleration,
    gravitational_force,
    parallel_axis_moment_of_inertia,
    translational_kinetic_energy,
    rotational_kinetic_energy,
    gravitational_potential_energy,
    impulse_of_constant_force,
    angular_momentum_rigid_body,
    linear_drag_falling_speed,
    natural_angular_frequency,
    critical_damping_coefficient,
    damped_angular_frequency,
    forced_vibration_amplitude,
    linear_spring_force,
    torque_from_tangential_force,
)
