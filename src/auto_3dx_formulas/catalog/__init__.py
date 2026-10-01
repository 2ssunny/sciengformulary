"""Formula catalog, grouped by engineering domain.

Each domain package lists its formulas in a ``FORMULAS`` tuple; this module joins them.
"""

from auto_3dx_formulas.catalog import (
    aerodynamics,
    fluids,
    materials,
    orbital,
    structures,
    thermodynamics,
)
from auto_3dx_formulas.core import FormulaSpec

ALL_FORMULAS: tuple[FormulaSpec, ...] = (
    *aerodynamics.FORMULAS,
    *fluids.FORMULAS,
    *materials.FORMULAS,
    *orbital.FORMULAS,
    *structures.FORMULAS,
    *thermodynamics.FORMULAS,
)
