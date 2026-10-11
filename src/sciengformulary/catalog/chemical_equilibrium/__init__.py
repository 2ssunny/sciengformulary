"""Verified chemical equilibrium formula catalog."""

from sciengformulary.catalog.chemical_equilibrium.acid_dissociation_pka import (
    acid_dissociation_pka,
)
from sciengformulary.catalog.chemical_equilibrium.conjugate_base_constant import (
    conjugate_base_constant,
)
from sciengformulary.catalog.chemical_equilibrium.extended_debye_huckel_log_gamma import (
    extended_debye_huckel_log_gamma,
)
from sciengformulary.catalog.chemical_equilibrium.henderson_hasselbalch_ph import (
    henderson_hasselbalch_ph,
)
from sciengformulary.catalog.chemical_equilibrium.ionic_strength_two_species import (
    ionic_strength_two_species,
)
from sciengformulary.catalog.chemical_equilibrium.monoprotic_neutral_acid_fraction import (
    monoprotic_neutral_acid_fraction,
)
from sciengformulary.catalog.chemical_equilibrium.ph_from_activity import (
    ph_from_activity,
)
from sciengformulary.catalog.chemical_equilibrium.reaction_quotient import (
    reaction_quotient,
)
from sciengformulary.catalog.chemical_equilibrium.salt_molar_solubility import (
    salt_molar_solubility,
)
from sciengformulary.catalog.chemical_equilibrium.van_t_hoff_equilibrium_constant import (
    van_t_hoff_equilibrium_constant,
)
from sciengformulary.catalog.chemical_equilibrium.water_ion_product import (
    water_ion_product,
)
from sciengformulary.catalog.chemical_equilibrium.weak_electrolyte_ion_concentration import (
    weak_electrolyte_ion_concentration,
)
from sciengformulary.core import (
    FormulaSpec,
)

FORMULAS: tuple[FormulaSpec, ...] = (
    reaction_quotient,
    van_t_hoff_equilibrium_constant,
    ph_from_activity,
    acid_dissociation_pka,
    water_ion_product,
    conjugate_base_constant,
    henderson_hasselbalch_ph,
    weak_electrolyte_ion_concentration,
    salt_molar_solubility,
    ionic_strength_two_species,
    extended_debye_huckel_log_gamma,
    monoprotic_neutral_acid_fraction,
)
