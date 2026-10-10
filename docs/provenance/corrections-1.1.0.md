# Corrections to formulas released in 1.0.0

## Radiation constants (Stefan-Boltzmann sigma, Wien b)

NIST lists both 2022 CODATA values as exact, because they follow from the SI's exact
Planck constant h, Boltzmann constant k and speed of light c, but prints them with "...".
Version 1.0.0 used only the printed digits.

| Constant | 1.0.0 value | Corrected value | Relative change |
|---|---|---|---|
| sigma (W m^-2 K^-4) | 5.670374419e-8 | 5.6703744191844294e-8 | +3.25e-11 |
| b (m K) | 2.897771955e-3 | 2.8977719551851727e-3 | +6.39e-11 |

Corrected values are computed at 60 digits: sigma = 2 pi^5 k^4 / (15 h^3 c^2) and
b = h c / (k x), where x = 4.96511423174427630... solves x = 5 (1 - exp(-x)). Sources: the NIST
CODATA pages for sigma and b (already cited by the formulas) and the exact defining constants.

Numerical effect: every result of the formulas below increases by the same relative amount
(3.25e-11 for sigma, 6.39e-11 for b), far below any physical uncertainty but above the 1e-12
tolerance of the verification cases, whose expected values were recomputed at 60 digits:

- `heat_transfer.blackbody_emissive_power`, `net_radiative_exchange`,
  `radiation_heat_transfer_coefficient`, `linearized_radiation_heat_transfer_coefficient`,
  `wien_peak_wavelength` (released in 1.0.0)
- `heat_transfer.parallel_plate_radiation_exchange`, `concentric_cylinder_radiation_exchange`
  (new in this release)

Regression tests: `tests/test_catalog_corrections.py`.

## Reference year of `aerodynamics.lift_force`

The NASA Glenn "Lift Equation" page shows "Page Last Updated: July 10, 2024", before the
2026-10-01 access date of 1.0.0, so the cited year 2023 was wrong; it is now 2024. Only the
reference metadata changes; the formula and its results do not.
