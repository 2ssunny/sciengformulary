"""Whole-catalog validation used by CI and available to users.

Run it with ``python -m sciengformulary.validation``. The exit status is non-zero if any
check fails. It never accesses the network: reference URLs are recorded, not fetched.

What it checks is the machine-checkable part of the catalog: structure, references,
registration, serialization, and the numerical verification cases. It cannot tell whether
a cited source really supports a formula; that is the job of human review.
"""

from __future__ import annotations

import importlib
import inspect
import json
import pkgutil
import sys

from sciengformulary import __version__, catalog, formulas
from sciengformulary.catalog import ALL_FORMULAS, DOMAINS
from sciengformulary.core import FormulaSpec, ReferenceSpec, VerificationCase


def validate_catalog() -> list[str]:
    """Check every formula in the catalog.

    Returns:
        One message per problem found; an empty list means the catalog is valid.
    """
    errors = _duplicate_and_registry_errors()
    for formula in ALL_FORMULAS:
        errors.extend(_formula_errors(formula))
    errors.extend(_domain_errors())
    errors.extend(_unregistered_errors())
    return errors


def _duplicate_and_registry_errors() -> list[str]:
    errors = []
    ids = [formula.id for formula in ALL_FORMULAS]
    duplicates = sorted({formula_id for formula_id in ids if ids.count(formula_id) > 1})
    if duplicates:
        errors.append(f"duplicate formula ids: {duplicates}")
    if len(formulas) != len(ALL_FORMULAS):
        errors.append(f"registry has {len(formulas)} formulas, catalog has {len(ALL_FORMULAS)}")
    return errors


def _formula_errors(formula: FormulaSpec) -> list[str]:
    try:
        # validate() repeats the construction-time structural rules; verify() runs the cases.
        formula.validate()
        inputs = set(formula.input_names)
        parameters = set(inspect.signature(formula.evaluator).parameters)
        if parameters != inputs:
            raise ValueError(f"evaluator parameters {sorted(parameters)} != inputs")
        if not formula.references:
            raise ValueError("no references")
        for reference in formula.references:
            if not isinstance(reference, ReferenceSpec):
                raise TypeError(f"not a ReferenceSpec: {reference!r}")
            reference.validate()
            if not reference.format_ieee().strip():
                raise ValueError("empty IEEE citation")
        if not formula.verification_cases:
            raise ValueError("no verification cases")
        for case in formula.verification_cases:
            if not isinstance(case, VerificationCase):
                raise TypeError(f"not a VerificationCase: {case!r}")
            if set(case.inputs) != inputs:
                raise ValueError(f"case inputs {sorted(case.inputs)} != inputs")
        formula.verify()
        json.dumps(formula.to_dict())
        if formulas.get(formula.id) is not formula:
            raise ValueError("registry returns a different object for this id")
    except Exception as error:  # report every failing formula, not only the first
        return [f"{formula.id}: {type(error).__name__}: {error}"]
    return []


def _domain_errors() -> list[str]:
    errors = []
    for domain in DOMAINS:
        name = domain.__name__.rsplit(".", 1)[-1]
        for formula in domain.FORMULAS:
            if formula.id.split(".", 1)[0] != name:
                errors.append(f"{formula.id} is registered in domain {name!r}")
    return errors


def _unregistered_errors() -> list[str]:
    """Every FormulaSpec defined anywhere in the catalog package must be registered."""
    errors = []
    registered = {id(formula) for formula in ALL_FORMULAS}
    for module_info in pkgutil.walk_packages(catalog.__path__, f"{catalog.__name__}."):
        module = importlib.import_module(module_info.name)
        for name, value in vars(module).items():
            if isinstance(value, FormulaSpec) and id(value) not in registered:
                errors.append(f"{module_info.name}.{name} ({value.id}) is not registered")
    return errors


def main() -> int:
    """Validate the catalog, print a summary, and return a process exit status."""
    errors = validate_catalog()
    if errors:
        print(f"Catalog validation failed ({len(errors)} problem(s)):")
        print("\n".join(f"  - {error}" for error in errors))
        return 1
    cases = sum(len(formula.verification_cases) for formula in ALL_FORMULAS)
    print(
        f"sciengformulary {__version__}: {len(ALL_FORMULAS)} formulas in {len(DOMAINS)} "
        f"domains valid; {cases} verification cases passed."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
