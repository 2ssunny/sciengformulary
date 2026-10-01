"""Formula catalog, grouped by engineering domain.

Each domain package lists its formulas in a ``FORMULAS`` tuple; this module joins them.
Every formula is validated when it is constructed, including its references, so a
formula without a verified reference cannot be imported into the catalog.
"""

from types import ModuleType

from auto_3dx_formulas.catalog import (
    aerodynamics,
    fluids,
    materials,
    orbital,
    structures,
    thermodynamics,
)
from auto_3dx_formulas.core import FormulaSpec

DOMAINS: tuple[ModuleType, ...] = (
    aerodynamics,
    fluids,
    materials,
    orbital,
    structures,
    thermodynamics,
)


def _collect(domains: tuple[ModuleType, ...]) -> tuple[FormulaSpec, ...]:
    """Join the domain ``FORMULAS`` tuples, checking each formula sits in its own domain."""
    collected = []
    for domain in domains:
        domain_name = domain.__name__.rsplit(".", 1)[-1]
        for formula in domain.FORMULAS:
            if not isinstance(formula, FormulaSpec):
                raise TypeError(
                    f"{domain.__name__}.FORMULAS contains a non-FormulaSpec: {formula!r}."
                )
            if formula.id.split(".", 1)[0] != domain_name:
                raise ValueError(
                    f"Formula {formula.id!r} is registered in domain {domain_name!r}; "
                    f"its id must start with '{domain_name}.'."
                )
            collected.append(formula)
    return tuple(collected)


ALL_FORMULAS: tuple[FormulaSpec, ...] = _collect(DOMAINS)
