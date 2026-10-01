"""Mathematics formulas."""

from sciengformulary.catalog.mathematics.normal_probability_density import (
    normal_probability_density,
)
from sciengformulary.catalog.mathematics.stirling_factorial_approximation import (
    stirling_factorial_approximation,
)
from sciengformulary.core import FormulaSpec

FORMULAS: tuple[FormulaSpec, ...] = (
    normal_probability_density,
    stirling_factorial_approximation,
)
