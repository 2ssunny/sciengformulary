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
from sciengformulary.core import FormulaSpec

FORMULAS: tuple[FormulaSpec, ...] = (
    specific_orbital_energy,
    elliptical_orbit_specific_energy,
    semi_major_axis_from_apsides,
    orbital_period,
    gravitational_parameter_from_surface_gravity,
)
