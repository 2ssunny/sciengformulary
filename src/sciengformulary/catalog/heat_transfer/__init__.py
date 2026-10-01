"""Heat transfer formulas."""

from sciengformulary.catalog.heat_transfer.biot_number import biot_number
from sciengformulary.catalog.heat_transfer.blackbody_emissive_power import blackbody_emissive_power
from sciengformulary.catalog.heat_transfer.colburn_analogy_stanton_number import (
    colburn_analogy_stanton_number,
)
from sciengformulary.catalog.heat_transfer.convective_heat_flux import convective_heat_flux
from sciengformulary.catalog.heat_transfer.fourier_conduction_heat_flux import (
    fourier_conduction_heat_flux,
)
from sciengformulary.catalog.heat_transfer.laminar_flat_plate_local_nusselt import (
    laminar_flat_plate_local_nusselt,
)
from sciengformulary.catalog.heat_transfer.laminar_flat_plate_skin_friction import (
    laminar_flat_plate_skin_friction,
)
from sciengformulary.catalog.heat_transfer.laminar_pipe_h_uniform_heat_flux import (
    laminar_pipe_h_uniform_heat_flux,
)
from sciengformulary.catalog.heat_transfer.laminar_pipe_h_uniform_wall_temperature import (
    laminar_pipe_h_uniform_wall_temperature,
)
from sciengformulary.catalog.heat_transfer.linearized_radiation_heat_transfer_coefficient import (
    linearized_radiation_heat_transfer_coefficient,
)
from sciengformulary.catalog.heat_transfer.log_mean_temperature_difference import (
    log_mean_temperature_difference,
)
from sciengformulary.catalog.heat_transfer.lumped_capacity_temperature_ratio import (
    lumped_capacity_temperature_ratio,
)
from sciengformulary.catalog.heat_transfer.lumped_capacity_time_constant import (
    lumped_capacity_time_constant,
)
from sciengformulary.catalog.heat_transfer.net_radiative_exchange import net_radiative_exchange
from sciengformulary.catalog.heat_transfer.nusselt_number import nusselt_number
from sciengformulary.catalog.heat_transfer.photon_energy import photon_energy
from sciengformulary.catalog.heat_transfer.plane_wall_conduction_rate import (
    plane_wall_conduction_rate,
)
from sciengformulary.catalog.heat_transfer.plane_wall_thermal_resistance import (
    plane_wall_thermal_resistance,
)
from sciengformulary.catalog.heat_transfer.prandtl_number import prandtl_number
from sciengformulary.catalog.heat_transfer.radiation_heat_transfer_coefficient import (
    radiation_heat_transfer_coefficient,
)
from sciengformulary.catalog.heat_transfer.semi_infinite_solid_step_response import (
    semi_infinite_solid_step_response,
)
from sciengformulary.catalog.heat_transfer.stanton_number import stanton_number
from sciengformulary.catalog.heat_transfer.thermal_diffusivity import thermal_diffusivity
from sciengformulary.catalog.heat_transfer.wien_peak_wavelength import wien_peak_wavelength
from sciengformulary.core import FormulaSpec

FORMULAS: tuple[FormulaSpec, ...] = (
    thermal_diffusivity,
    fourier_conduction_heat_flux,
    plane_wall_conduction_rate,
    plane_wall_thermal_resistance,
    semi_infinite_solid_step_response,
    convective_heat_flux,
    nusselt_number,
    prandtl_number,
    stanton_number,
    laminar_pipe_h_uniform_heat_flux,
    laminar_pipe_h_uniform_wall_temperature,
    colburn_analogy_stanton_number,
    laminar_flat_plate_skin_friction,
    laminar_flat_plate_local_nusselt,
    lumped_capacity_time_constant,
    lumped_capacity_temperature_ratio,
    biot_number,
    radiation_heat_transfer_coefficient,
    linearized_radiation_heat_transfer_coefficient,
    log_mean_temperature_difference,
    photon_energy,
    blackbody_emissive_power,
    net_radiative_exchange,
    wien_peak_wavelength,
)
