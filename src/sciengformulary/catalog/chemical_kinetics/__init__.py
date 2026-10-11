"""Verified chemical kinetics formula catalog."""

from sciengformulary.catalog.chemical_kinetics.arrhenius_first_order_constant import (
    arrhenius_first_order_constant,
)
from sciengformulary.catalog.chemical_kinetics.arrhenius_rate_ratio import (
    arrhenius_rate_ratio,
)
from sciengformulary.catalog.chemical_kinetics.average_reaction_rate import (
    average_reaction_rate,
)
from sciengformulary.catalog.chemical_kinetics.bimolecular_rate import (
    bimolecular_rate,
)
from sciengformulary.catalog.chemical_kinetics.second_order_concentration import (
    second_order_concentration,
)
from sciengformulary.catalog.chemical_kinetics.second_order_half_life import (
    second_order_half_life,
)
from sciengformulary.catalog.chemical_kinetics.zero_order_concentration import (
    zero_order_concentration,
)
from sciengformulary.catalog.chemical_kinetics.zero_order_half_life import (
    zero_order_half_life,
)
from sciengformulary.core import (
    FormulaSpec,
)

FORMULAS: tuple[FormulaSpec, ...] = (
    average_reaction_rate,
    bimolecular_rate,
    zero_order_concentration,
    second_order_concentration,
    zero_order_half_life,
    second_order_half_life,
    arrhenius_first_order_constant,
    arrhenius_rate_ratio,
)
