"""Propulsion formulas."""

from sciengformulary.catalog.propulsion.rocket_thrust import rocket_thrust
from sciengformulary.catalog.propulsion.specific_impulse import specific_impulse
from sciengformulary.catalog.propulsion.average_thrust import average_thrust
from sciengformulary.catalog.propulsion.burn_to_throat_area_ratio import burn_to_throat_area_ratio
from sciengformulary.catalog.propulsion.effective_exhaust_velocity import effective_exhaust_velocity
from sciengformulary.catalog.propulsion.effective_exhaust_velocity_from_impulse import (
    effective_exhaust_velocity_from_impulse,
)
from sciengformulary.catalog.propulsion.nozzle_expansion_ratio import nozzle_expansion_ratio
from sciengformulary.catalog.propulsion.regression_rate_from_mass_flow import (
    regression_rate_from_mass_flow,
)
from sciengformulary.catalog.propulsion.rocket_equation_final_mass import rocket_equation_final_mass
from sciengformulary.catalog.propulsion.thrust_coefficient import thrust_coefficient
from sciengformulary.catalog.propulsion.thrust_to_weight_ratio import thrust_to_weight_ratio
from sciengformulary.catalog.propulsion.tsiolkovsky_delta_v import tsiolkovsky_delta_v
from sciengformulary.core import FormulaSpec

FORMULAS: tuple[FormulaSpec, ...] = (
    rocket_thrust,
    specific_impulse,
    average_thrust,
    burn_to_throat_area_ratio,
    effective_exhaust_velocity,
    effective_exhaust_velocity_from_impulse,
    nozzle_expansion_ratio,
    regression_rate_from_mass_flow,
    rocket_equation_final_mass,
    thrust_coefficient,
    thrust_to_weight_ratio,
    tsiolkovsky_delta_v,
)
