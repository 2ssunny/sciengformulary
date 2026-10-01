"""Formula catalog, grouped by knowledge domain.

Each domain package lists its formulas in a ``FORMULAS`` tuple; this module joins them.
Every formula is validated when it is constructed, including its references and its
numerical verification cases, so a formula without a reference, or whose evaluator does
not reproduce its verification cases, cannot be imported into the catalog.
"""

from types import ModuleType

from sciengformulary.catalog import (
    aerodynamics,
    fluids,
    materials,
    orbital,
    propulsion,
    structures,
    thermodynamics,
)
from sciengformulary.core import FormulaSpec

DOMAINS: tuple[ModuleType, ...] = (
    aerodynamics,
    fluids,
    materials,
    orbital,
    propulsion,
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
