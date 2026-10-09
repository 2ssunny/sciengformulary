"""Thermodynamics formulas."""

from sciengformulary.catalog.thermodynamics.carnot_efficiency import carnot_efficiency
from sciengformulary.catalog.thermodynamics.carnot_refrigerator_cop import carnot_refrigerator_cop
from sciengformulary.catalog.thermodynamics.heat_engine_efficiency import heat_engine_efficiency
from sciengformulary.catalog.thermodynamics.ideal_gas_entropy_change import ideal_gas_entropy_change
from sciengformulary.catalog.thermodynamics.ideal_gas_pressure import ideal_gas_pressure
from sciengformulary.catalog.thermodynamics.isentropic_temperature_ratio import (
    isentropic_temperature_ratio,
)
from sciengformulary.catalog.thermodynamics.isothermal_entropy_change import (
    isothermal_entropy_change,
)
from sciengformulary.catalog.thermodynamics.isothermal_work import isothermal_work
from sciengformulary.catalog.thermodynamics.maxwell_speed_distribution import (
    maxwell_speed_distribution,
)
from sciengformulary.catalog.thermodynamics.mean_free_path import mean_free_path
from sciengformulary.catalog.thermodynamics.mean_molecular_speed import mean_molecular_speed
from sciengformulary.catalog.thermodynamics.mean_molecular_translational_kinetic_energy import (
    mean_molecular_translational_kinetic_energy,
)
from sciengformulary.catalog.thermodynamics.monatomic_ideal_gas_internal_energy import (
    monatomic_ideal_gas_internal_energy,
)
from sciengformulary.catalog.thermodynamics.rms_molecular_speed import rms_molecular_speed
from sciengformulary.catalog.thermodynamics.sensible_heat import sensible_heat
from sciengformulary.catalog.thermodynamics.specific_heat_at_constant_pressure import (
    specific_heat_at_constant_pressure,
)
from sciengformulary.catalog.thermodynamics.specific_heat_at_constant_volume_from_gamma import (
    specific_heat_at_constant_volume_from_gamma,
)
from sciengformulary.catalog.thermodynamics.stagnation_temperature import stagnation_temperature
from sciengformulary.catalog.thermodynamics.van_der_waals_pressure import van_der_waals_pressure
from sciengformulary.catalog.thermodynamics.antoine_vapor_pressure import antoine_vapor_pressure
from sciengformulary.core import FormulaSpec

FORMULAS: tuple[FormulaSpec, ...] = (
    ideal_gas_pressure,
    van_der_waals_pressure,
    mean_molecular_translational_kinetic_energy,
    monatomic_ideal_gas_internal_energy,
    maxwell_speed_distribution,
    mean_molecular_speed,
    rms_molecular_speed,
    mean_free_path,
    specific_heat_at_constant_pressure,
    specific_heat_at_constant_volume_from_gamma,
    stagnation_temperature,
    isothermal_work,
    isothermal_entropy_change,
    ideal_gas_entropy_change,
    isentropic_temperature_ratio,
    heat_engine_efficiency,
    carnot_efficiency,
    carnot_refrigerator_cop,
    sensible_heat,
    antoine_vapor_pressure,
)
