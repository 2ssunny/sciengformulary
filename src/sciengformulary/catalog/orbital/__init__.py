"""Orbital mechanics formulas."""

from sciengformulary.catalog.orbital.elliptical_orbit_specific_energy import (
    elliptical_orbit_specific_energy,
)
from sciengformulary.catalog.orbital.gravitational_parameter_from_surface_gravity import (
    gravitational_parameter_from_surface_gravity,
)
from sciengformulary.catalog.orbital.orbital_period import orbital_period
from sciengformulary.catalog.orbital.semi_major_axis_from_apsides import (
    semi_major_axis_from_apsides,
)
from sciengformulary.catalog.orbital.specific_orbital_energy import specific_orbital_energy
from sciengformulary.catalog.orbital.barker_parabolic_anomaly_from_mean_anomaly import (
    barker_parabolic_anomaly_from_mean_anomaly,
)
from sciengformulary.catalog.orbital.barker_parabolic_mean_anomaly import (
    barker_parabolic_mean_anomaly,
)
from sciengformulary.catalog.orbital.bielliptic_total_delta_v import bielliptic_total_delta_v
from sciengformulary.catalog.orbital.circular_orbit_speed import circular_orbit_speed
from sciengformulary.catalog.orbital.conic_orbit_radius import conic_orbit_radius
from sciengformulary.catalog.orbital.eccentric_anomaly_from_true_anomaly import (
    eccentric_anomaly_from_true_anomaly,
)
from sciengformulary.catalog.orbital.edelbaum_delta_v import edelbaum_delta_v
from sciengformulary.catalog.orbital.flight_path_angle import flight_path_angle
from sciengformulary.catalog.orbital.hohmann_first_impulse import hohmann_first_impulse
from sciengformulary.catalog.orbital.hohmann_second_impulse import hohmann_second_impulse
from sciengformulary.catalog.orbital.hohmann_transfer_time import hohmann_transfer_time
from sciengformulary.catalog.orbital.hyperbolic_asymptote_true_anomaly import (
    hyperbolic_asymptote_true_anomaly,
)
from sciengformulary.catalog.orbital.hyperbolic_eccentric_anomaly_from_true_anomaly import (
    hyperbolic_eccentric_anomaly_from_true_anomaly,
)
from sciengformulary.catalog.orbital.hyperbolic_kepler_mean_anomaly import (
    hyperbolic_kepler_mean_anomaly,
)
from sciengformulary.catalog.orbital.hyperbolic_true_anomaly_from_eccentric_anomaly import (
    hyperbolic_true_anomaly_from_eccentric_anomaly,
)
from sciengformulary.catalog.orbital.j2_nodal_precession_rate import j2_nodal_precession_rate
from sciengformulary.catalog.orbital.kepler_mean_anomaly_from_eccentric_anomaly import (
    kepler_mean_anomaly_from_eccentric_anomaly,
)
from sciengformulary.catalog.orbital.keplerian_mean_motion import keplerian_mean_motion
from sciengformulary.catalog.orbital.laplace_sphere_of_influence_radius import (
    laplace_sphere_of_influence_radius,
)
from sciengformulary.catalog.orbital.mean_motion_semi_major_axis_sensitivity import (
    mean_motion_semi_major_axis_sensitivity,
)
from sciengformulary.catalog.orbital.semi_latus_rectum import semi_latus_rectum
from sciengformulary.catalog.orbital.specific_angular_momentum import specific_angular_momentum
from sciengformulary.catalog.orbital.true_anomaly_from_eccentric_anomaly import (
    true_anomaly_from_eccentric_anomaly,
)
from sciengformulary.catalog.orbital.vis_viva_speed import vis_viva_speed
from sciengformulary.core import FormulaSpec

FORMULAS: tuple[FormulaSpec, ...] = (
    specific_orbital_energy,
    elliptical_orbit_specific_energy,
    semi_major_axis_from_apsides,
    orbital_period,
    gravitational_parameter_from_surface_gravity,
    barker_parabolic_anomaly_from_mean_anomaly,
    barker_parabolic_mean_anomaly,
    bielliptic_total_delta_v,
    circular_orbit_speed,
    conic_orbit_radius,
    eccentric_anomaly_from_true_anomaly,
    edelbaum_delta_v,
    flight_path_angle,
    hohmann_first_impulse,
    hohmann_second_impulse,
    hohmann_transfer_time,
    hyperbolic_asymptote_true_anomaly,
    hyperbolic_eccentric_anomaly_from_true_anomaly,
    hyperbolic_kepler_mean_anomaly,
    hyperbolic_true_anomaly_from_eccentric_anomaly,
    j2_nodal_precession_rate,
    kepler_mean_anomaly_from_eccentric_anomaly,
    keplerian_mean_motion,
    laplace_sphere_of_influence_radius,
    mean_motion_semi_major_axis_sensitivity,
    semi_latus_rectum,
    specific_angular_momentum,
    true_anomaly_from_eccentric_anomaly,
    vis_viva_speed,
)
