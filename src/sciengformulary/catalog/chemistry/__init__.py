"""Chemistry formulas."""

from sciengformulary.catalog.chemistry.air_fuel_ratio_from_equivalence_ratio import (
    air_fuel_ratio_from_equivalence_ratio,
)
from sciengformulary.catalog.chemistry.amount_from_mass import (
    amount_from_mass,
)
from sciengformulary.catalog.chemistry.boiling_point_elevation import (
    boiling_point_elevation,
)
from sciengformulary.catalog.chemistry.dalton_partial_pressure import (
    dalton_partial_pressure,
)
from sciengformulary.catalog.chemistry.degree_of_unsaturation import (
    degree_of_unsaturation,
)
from sciengformulary.catalog.chemistry.dilution_concentration import (
    dilution_concentration,
)
from sciengformulary.catalog.chemistry.distribution_ratio import (
    distribution_ratio,
)
from sciengformulary.catalog.chemistry.entities_from_amount import (
    entities_from_amount,
)
from sciengformulary.catalog.chemistry.equivalence_ratio_from_mixture_fraction import (
    equivalence_ratio_from_mixture_fraction,
)
from sciengformulary.catalog.chemistry.freezing_point_depression import (
    freezing_point_depression,
)
from sciengformulary.catalog.chemistry.henry_law_concentration import (
    henry_law_concentration,
)
from sciengformulary.catalog.chemistry.mass_concentration import (
    mass_concentration,
)
from sciengformulary.catalog.chemistry.mass_fraction import (
    mass_fraction,
)
from sciengformulary.catalog.chemistry.molality import (
    molality,
)
from sciengformulary.catalog.chemistry.molar_concentration import (
    molar_concentration,
)
from sciengformulary.catalog.chemistry.mole_fraction import (
    mole_fraction,
)
from sciengformulary.catalog.chemistry.osmotic_pressure import (
    osmotic_pressure,
)
from sciengformulary.catalog.chemistry.percent_yield import (
    percent_yield,
)
from sciengformulary.catalog.chemistry.raoult_partial_pressure import (
    raoult_partial_pressure,
)
from sciengformulary.catalog.chemistry.repeated_extraction_remaining_fraction import (
    repeated_extraction_remaining_fraction,
)
from sciengformulary.catalog.chemistry.stoichiometric_product_amount import (
    stoichiometric_product_amount,
)
from sciengformulary.catalog.chemistry.titration_equivalence_volume import (
    titration_equivalence_volume,
)
from sciengformulary.catalog.chemistry.volume_fraction import (
    volume_fraction,
)
from sciengformulary.catalog.chemistry.weak_acid_distribution_ratio import (
    weak_acid_distribution_ratio,
)
from sciengformulary.core import (
    FormulaSpec,
)

FORMULAS: tuple[FormulaSpec, ...] = (
    air_fuel_ratio_from_equivalence_ratio,
    equivalence_ratio_from_mixture_fraction,
    amount_from_mass,
    entities_from_amount,
    molar_concentration,
    molality,
    mole_fraction,
    mass_fraction,
    volume_fraction,
    mass_concentration,
    dilution_concentration,
    percent_yield,
    stoichiometric_product_amount,
    degree_of_unsaturation,
    henry_law_concentration,
    raoult_partial_pressure,
    boiling_point_elevation,
    freezing_point_depression,
    osmotic_pressure,
    dalton_partial_pressure,
    distribution_ratio,
    repeated_extraction_remaining_fraction,
    weak_acid_distribution_ratio,
    titration_equivalence_volume,
)
