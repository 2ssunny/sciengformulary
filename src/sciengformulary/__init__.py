"""SciEng Formulary: verified scientific and engineering formulas.

Each formula carries its variables, units, assumptions, references, and an executable
evaluator that is checked against known numerical cases.

Example:
    >>> from sciengformulary import formulas
    >>> formulas.get("aerodynamics.dynamic_pressure").evaluate(rho=1.225, V=120.0)
    8820.0
"""

from sciengformulary.catalog import ALL_FORMULAS
from sciengformulary.core import (
    FormulaRegistry,
    FormulaSpec,
    ReferenceSpec,
    VariableSpec,
    VerificationCase,
)

__version__ = "1.0.0"

formulas = FormulaRegistry(ALL_FORMULAS)

__all__ = [
    "FormulaRegistry",
    "FormulaSpec",
    "ReferenceSpec",
    "VariableSpec",
    "VerificationCase",
    "formulas",
    "__version__",
]
