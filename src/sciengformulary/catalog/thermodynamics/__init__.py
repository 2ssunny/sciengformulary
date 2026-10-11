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
from sciengformulary.catalog.thermodynamics.boltzmann_entropy import (
    boltzmann_entropy,
)
from sciengformulary.catalog.thermodynamics.bond_enthalpy_reaction_estimate import (
    bond_enthalpy_reaction_estimate,
)
from sciengformulary.catalog.thermodynamics.clausius_clapeyron_pressure import (
    clausius_clapeyron_pressure,
)
from sciengformulary.catalog.thermodynamics.constant_external_pressure_work import (
    constant_external_pressure_work,
)
from sciengformulary.catalog.thermodynamics.enthalpy_change import (
    enthalpy_change,
)
from sciengformulary.catalog.thermodynamics.first_law_internal_energy import (
    first_law_internal_energy,
)
from sciengformulary.catalog.thermodynamics.gibbs_energy_change import (
    gibbs_energy_change,
)
from sciengformulary.catalog.thermodynamics.ideal_binary_gas_mixing_entropy import (
    ideal_binary_gas_mixing_entropy,
)
from sciengformulary.catalog.thermodynamics.ideal_gas_mixture_chemical_potential import (
    ideal_gas_mixture_chemical_potential,
)
from sciengformulary.catalog.thermodynamics.kp_kc_conversion import (
    kp_kc_conversion,
)
from sciengformulary.catalog.thermodynamics.nasa7_enthalpy import (
    nasa7_enthalpy,
)
from sciengformulary.catalog.thermodynamics.nasa7_entropy import (
    nasa7_entropy,
)
from sciengformulary.catalog.thermodynamics.nasa7_heat_capacity import (
    nasa7_heat_capacity,
)
from sciengformulary.catalog.thermodynamics.nasa9_heat_capacity import (
    nasa9_heat_capacity,
)
from sciengformulary.catalog.thermodynamics.pressure_equilibrium_constant import (
    pressure_equilibrium_constant,
)
from sciengformulary.catalog.thermodynamics.reaction_enthalpy_from_formation import (
    reaction_enthalpy_from_formation,
)
from sciengformulary.catalog.thermodynamics.reaction_gibbs_energy import (
    reaction_gibbs_energy,
)
from sciengformulary.catalog.thermodynamics.standard_reaction_gibbs_energy import (
    standard_reaction_gibbs_energy,
)
from sciengformulary.catalog.thermodynamics.total_entropy_change import (
    total_entropy_change,
)
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
    boltzmann_entropy,
    bond_enthalpy_reaction_estimate,
    clausius_clapeyron_pressure,
    constant_external_pressure_work,
    enthalpy_change,
    first_law_internal_energy,
    gibbs_energy_change,
    ideal_binary_gas_mixing_entropy,
    ideal_gas_mixture_chemical_potential,
    kp_kc_conversion,
    nasa7_enthalpy,
    nasa7_entropy,
    nasa7_heat_capacity,
    nasa9_heat_capacity,
    pressure_equilibrium_constant,
    reaction_enthalpy_from_formation,
    reaction_gibbs_energy,
    standard_reaction_gibbs_energy,
    total_entropy_change,
)
