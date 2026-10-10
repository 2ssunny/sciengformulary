"""Physical constants used inside catalog evaluators, with their NIST sources.

Values are the 2022 CODATA recommended values as published by NIST. Constants that the
SI defines exactly are exact here. The Stefan-Boltzmann and Wien constants are also exact,
because they follow from the exact h, k and c, but NIST prints them with "..."; they are
given here to full double precision, computed at 60 digits from those exact constants:
sigma = 2 pi^5 k^4 / (15 h^3 c^2) and b = h c / (k x), where x = 4.96511423174427630...
solves x = 5 (1 - exp(-x)). Versions up to 1.0.0 used the printed digits only
(5.670374419e-8 and 2.897771955e-3), which are low by 3.3e-11 and 6.4e-11 relative.
"""

from sciengformulary.catalog._sources import nist_codata

BOLTZMANN_CONSTANT = 1.380649e-23  # J/K, exact
PLANCK_CONSTANT = 6.62607015e-34  # J/Hz, exact
STEFAN_BOLTZMANN_CONSTANT = 5.6703744191844294e-8  # W m^-2 K^-4, exact (derived)
WIEN_WAVELENGTH_DISPLACEMENT_CONSTANT = 2.8977719551851727e-3  # m K, exact (derived)
NEWTONIAN_CONSTANT_OF_GRAVITATION = 6.67430e-11  # m^3 kg^-1 s^-2, uncertainty 1.5e-15
STANDARD_ACCELERATION_OF_GRAVITY = 9.80665  # m/s^2, exact by definition

BOLTZMANN_CONSTANT_REFERENCE = nist_codata("Boltzmann constant", "k")
PLANCK_CONSTANT_REFERENCE = nist_codata("Planck constant", "h")
STEFAN_BOLTZMANN_CONSTANT_REFERENCE = nist_codata("Stefan-Boltzmann constant", "sigma")
WIEN_CONSTANT_REFERENCE = nist_codata("Wien wavelength displacement law constant", "bwien")
GRAVITATIONAL_CONSTANT_REFERENCE = nist_codata("Newtonian constant of gravitation", "bg")
STANDARD_GRAVITY_REFERENCE = nist_codata("standard acceleration of gravity", "gn")
