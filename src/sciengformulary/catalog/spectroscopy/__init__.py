"""Verified spectroscopy formula catalog."""

from sciengformulary.catalog.spectroscopy.absorbance_from_transmittance import (
    absorbance_from_transmittance,
)
from sciengformulary.catalog.spectroscopy.beer_lambert_absorbance import (
    beer_lambert_absorbance,
)
from sciengformulary.catalog.spectroscopy.de_broglie_wavelength import (
    de_broglie_wavelength,
)
from sciengformulary.catalog.spectroscopy.diatomic_moment_of_inertia import (
    diatomic_moment_of_inertia,
)
from sciengformulary.catalog.spectroscopy.diatomic_vibrational_wavenumber import (
    diatomic_vibrational_wavenumber,
)
from sciengformulary.catalog.spectroscopy.harmonic_oscillator_energy import (
    harmonic_oscillator_energy,
)
from sciengformulary.catalog.spectroscopy.hydrogenic_bohr_energy import (
    hydrogenic_bohr_energy,
)
from sciengformulary.catalog.spectroscopy.mass_error_ppm import (
    mass_error_ppm,
)
from sciengformulary.catalog.spectroscopy.mass_resolving_power import (
    mass_resolving_power,
)
from sciengformulary.catalog.spectroscopy.nmr_chemical_shift import (
    nmr_chemical_shift,
)
from sciengformulary.catalog.spectroscopy.particle_in_box_energy import (
    particle_in_box_energy,
)
from sciengformulary.catalog.spectroscopy.reduced_mass import (
    reduced_mass,
)
from sciengformulary.catalog.spectroscopy.rigid_rotor_energy import (
    rigid_rotor_energy,
)
from sciengformulary.catalog.spectroscopy.two_component_absorbance import (
    two_component_absorbance,
)
from sciengformulary.catalog.spectroscopy.vacuum_wavelength import (
    vacuum_wavelength,
)
from sciengformulary.catalog.spectroscopy.vacuum_wavenumber import (
    vacuum_wavenumber,
)
from sciengformulary.core import (
    FormulaSpec,
)

FORMULAS: tuple[FormulaSpec, ...] = (
    vacuum_wavelength,
    vacuum_wavenumber,
    beer_lambert_absorbance,
    absorbance_from_transmittance,
    two_component_absorbance,
    nmr_chemical_shift,
    reduced_mass,
    diatomic_vibrational_wavenumber,
    particle_in_box_energy,
    harmonic_oscillator_energy,
    de_broglie_wavelength,
    diatomic_moment_of_inertia,
    rigid_rotor_energy,
    hydrogenic_bohr_energy,
    mass_resolving_power,
    mass_error_ppm,
)
