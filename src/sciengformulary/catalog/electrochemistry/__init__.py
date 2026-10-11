"""Electrochemistry formulas."""

from sciengformulary.catalog.electrochemistry.cell_potential import cell_potential
from sciengformulary.catalog.electrochemistry.constant_current_charge import (
    constant_current_charge,
)
from sciengformulary.catalog.electrochemistry.electrolysis_product_mass import (
    electrolysis_product_mass,
)
from sciengformulary.catalog.electrochemistry.nernst_cell_potential import (
    nernst_cell_potential,
)
from sciengformulary.catalog.electrochemistry.reaction_gibbs_from_potential import (
    reaction_gibbs_from_potential,
)
from sciengformulary.catalog.electrochemistry.tafel_current_density import (
    tafel_current_density,
)
from sciengformulary.catalog.electrochemistry.thermal_voltage import thermal_voltage
from sciengformulary.core import FormulaSpec

FORMULAS: tuple[FormulaSpec, ...] = (
    tafel_current_density,
    thermal_voltage,
    cell_potential,
    nernst_cell_potential,
    reaction_gibbs_from_potential,
    electrolysis_product_mass,
    constant_current_charge,
)
