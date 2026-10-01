"""Engineering formulas with metadata, for AI agents working alongside auto-3dx.

Example:
    >>> from auto_3dx_formulas import formulas
    >>> formulas.get("aerodynamics.dynamic_pressure").evaluate(rho=1.225, V=120.0)
    8820.0
"""

from auto_3dx_formulas.catalog import ALL_FORMULAS
from auto_3dx_formulas.core import FormulaRegistry, FormulaSpec, ReferenceSpec, VariableSpec

__version__ = "0.1.0"

formulas = FormulaRegistry(ALL_FORMULAS)

__all__ = [
    "FormulaRegistry",
    "FormulaSpec",
    "ReferenceSpec",
    "VariableSpec",
    "formulas",
    "__version__",
]
