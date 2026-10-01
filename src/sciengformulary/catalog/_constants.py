"""Physical constants used inside catalog evaluators, with their NIST sources.

Values are the 2022 CODATA recommended values as published by NIST. Constants that the
SI defines exactly are exact here; the Stefan-Boltzmann and Wien constants are the
published values truncated where NIST prints "...".
"""

from sciengformulary.catalog._sources import nist_codata

BOLTZMANN_CONSTANT = 1.380649e-23  # J/K, exact
PLANCK_CONSTANT = 6.62607015e-34  # J/Hz, exact
STEFAN_BOLTZMANN_CONSTANT = 5.670374419e-8  # W m^-2 K^-4
WIEN_WAVELENGTH_DISPLACEMENT_CONSTANT = 2.897771955e-3  # m K
NEWTONIAN_CONSTANT_OF_GRAVITATION = 6.67430e-11  # m^3 kg^-1 s^-2, uncertainty 1.5e-15
STANDARD_ACCELERATION_OF_GRAVITY = 9.80665  # m/s^2, exact by definition

BOLTZMANN_CONSTANT_REFERENCE = nist_codata("Boltzmann constant", "k")
PLANCK_CONSTANT_REFERENCE = nist_codata("Planck constant", "h")
STEFAN_BOLTZMANN_CONSTANT_REFERENCE = nist_codata("Stefan-Boltzmann constant", "sigma")
WIEN_CONSTANT_REFERENCE = nist_codata("Wien wavelength displacement law constant", "bwien")
GRAVITATIONAL_CONSTANT_REFERENCE = nist_codata("Newtonian constant of gravitation", "bg")
STANDARD_GRAVITY_REFERENCE = nist_codata("standard acceleration of gravity", "gn")
