"""Materials formulas."""

from sciengformulary.catalog.materials.bulk_modulus_from_youngs_modulus import (
    bulk_modulus_from_youngs_modulus,
)
from sciengformulary.catalog.materials.composite_longitudinal_modulus import (
    composite_longitudinal_modulus,
)
from sciengformulary.catalog.materials.composite_transverse_modulus import (
    composite_transverse_modulus,
)
from sciengformulary.catalog.materials.critical_energy_release_rate import (
    critical_energy_release_rate,
)
from sciengformulary.catalog.materials.elastic_strain_energy_density import (
    elastic_strain_energy_density,
)
from sciengformulary.catalog.materials.engineering_strain import engineering_strain
from sciengformulary.catalog.materials.engineering_stress import engineering_stress
from sciengformulary.catalog.materials.mode_i_stress_intensity_factor import (
    mode_i_stress_intensity_factor,
)
from sciengformulary.catalog.materials.shear_modulus_from_youngs_modulus import (
    shear_modulus_from_youngs_modulus,
)
from sciengformulary.catalog.materials.thermal_strain import thermal_strain
from sciengformulary.catalog.materials.true_strain import true_strain
from sciengformulary.catalog.materials.true_stress import true_stress
from sciengformulary.catalog.materials.uniaxial_hookes_law import uniaxial_hookes_law
from sciengformulary.catalog.materials.von_mises_stress_principal import von_mises_stress_principal
from sciengformulary.catalog.materials.weibull_survival_probability import (
    weibull_survival_probability,
)
from sciengformulary.core import FormulaSpec

FORMULAS: tuple[FormulaSpec, ...] = (
    engineering_stress,
    engineering_strain,
    true_stress,
    true_strain,
    uniaxial_hookes_law,
    shear_modulus_from_youngs_modulus,
    bulk_modulus_from_youngs_modulus,
    thermal_strain,
    elastic_strain_energy_density,
    von_mises_stress_principal,
    mode_i_stress_intensity_factor,
    critical_energy_release_rate,
    weibull_survival_probability,
    composite_longitudinal_modulus,
    composite_transverse_modulus,
)
