"""Nuclear formulas."""

from sciengformulary.catalog.nuclear.activity import activity
from sciengformulary.catalog.nuclear.half_life import half_life
from sciengformulary.catalog.nuclear.radioactive_decay import radioactive_decay
from sciengformulary.core import FormulaSpec

FORMULAS: tuple[FormulaSpec, ...] = (
    radioactive_decay,
    half_life,
    activity,
)
