"""Formula specification: metadata plus a numerical evaluator."""

from __future__ import annotations

import inspect
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from sciengformulary.core.reference import ReferenceSpec
from sciengformulary.core.variable import VariableSpec
from sciengformulary.core.verification import VerificationCase

FORMULA_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+$")


@dataclass(frozen=True)
class FormulaSpec:
    """One scientific or engineering formula: what it computes, when it applies, and how.

    The evaluator is plain arithmetic and does no unit conversion. Inputs must be given
    in one consistent unit system, and the result is in the matching unit of that same
    system. Each variable's ``si_unit`` shows one such consistent choice.

    Attributes:
        id: Unique dotted identifier, ``<domain>.<snake_case_name>``.
        name: Human-readable name.
        equation: Symbolic equation as plain text, e.g. ``"q = 0.5 * rho * V^2"``.
        inputs: Input variables. Each ``name`` must be a parameter of ``evaluator``.
        output: The variable the formula computes.
        evaluator: Function taking the inputs as keyword arguments and returning the output.
        references: At least one verified source for the equation and its applicability.
            A formula without one cannot be constructed, so it cannot enter the catalog.
        verification_cases: At least one known input/output case the evaluator must
            reproduce. These check the implementation, not the science: see
            :class:`VerificationCase`.
        description: What the formula represents.
        assumptions: Conditions under which the formula is valid.
        tags: Extra search keywords and aliases.
    """

    id: str
    name: str
    equation: str
    inputs: tuple[VariableSpec, ...]
    output: VariableSpec
    evaluator: Callable[..., float] = field(repr=False)
    references: tuple[ReferenceSpec, ...]
    verification_cases: tuple[VerificationCase, ...]
    description: str = ""
    assumptions: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        # Fail at import time so a malformed or miscomputing formula never reaches a caller.
        self.validate()
        self.verify()

    def validate(self) -> None:
        """Check the id, inputs, evaluator signature, references, and verification cases.

        This is structural: it does not run the evaluator. :meth:`verify` does.

        Raises:
            ValueError: If the formula breaks a catalog rule.
            TypeError: If a reference or case has the wrong type.
        """
        if not FORMULA_ID_PATTERN.match(self.id):
            raise ValueError(
                f"Formula id {self.id!r} must look like '<domain>.<snake_case_name>'."
            )
        names = self.input_names
        if len(set(names)) != len(names):
            raise ValueError(f"Formula {self.id!r} has duplicate input names: {names}.")
        parameters = set(inspect.signature(self.evaluator).parameters)
        if parameters != set(names):
            raise ValueError(
                f"Formula {self.id!r}: evaluator parameters {sorted(parameters)} "
                f"do not match input names {sorted(names)}."
            )
        if not isinstance(self.references, tuple) or not self.references:
            raise ValueError(
                f"Formula {self.id!r} needs a tuple of at least one ReferenceSpec. "
                "Formulas without a verified reference stay out of the catalog."
            )
        for reference in self.references:
            if not isinstance(reference, ReferenceSpec):
                raise TypeError(
                    f"Formula {self.id!r}: references must be ReferenceSpec objects, "
                    f"got {type(reference).__name__}."
                )
            reference.validate()
        if not isinstance(self.verification_cases, tuple) or not self.verification_cases:
            raise ValueError(
                f"Formula {self.id!r} needs a tuple of at least one VerificationCase. "
                "Formulas whose evaluator is not checked numerically stay out of the catalog."
            )
        for number, case in enumerate(self.verification_cases, start=1):
            if not isinstance(case, VerificationCase):
                raise TypeError(
                    f"Formula {self.id!r}: verification_cases must be VerificationCase "
                    f"objects, got {type(case).__name__}."
                )
            case.validate()
            missing = sorted(set(names) - set(case.inputs))
            unknown = sorted(set(case.inputs) - set(names))
            if missing or unknown:
                raise ValueError(
                    f"Formula {self.id!r} verification case {number}: inputs must be exactly "
                    f"{sorted(names)}; missing {missing}, unknown {unknown}."
                )

    def verify(self) -> None:
        """Run every verification case through the evaluator and compare the results.

        A pass shows the evaluator implements the declared equation for these cases.
        It does not show the equation is scientifically correct or applicable.

        Raises:
            ValueError: If the evaluator raises, returns a non-number, or returns a
                value outside a case's tolerances. The message names the formula, the
                case, the expected and actual values, and the tolerances.
        """
        total = len(self.verification_cases)
        for number, case in enumerate(self.verification_cases, start=1):
            label = f"Formula {self.id!r} verification case {number}/{total} ({case.note})"
            try:
                actual = self.evaluate(**case.inputs)
            except Exception as error:
                raise ValueError(
                    f"{label}: evaluator raised {type(error).__name__}: {error} "
                    f"for inputs {dict(case.inputs)}."
                ) from error
            if not case.matches(actual):
                raise ValueError(
                    f"{label}: inputs {dict(case.inputs)} expected {case.expected!r}, "
                    f"got {actual!r} (rel_tol={case.rel_tol!r}, abs_tol={case.abs_tol!r})."
                )

    @property
    def input_names(self) -> tuple[str, ...]:
        """Keyword argument names accepted by :meth:`evaluate`."""
        return tuple(variable.name for variable in self.inputs)

    def evaluate(self, **values: float) -> float:
        """Evaluate the formula numerically.

        Args:
            **values: One keyword argument per input variable, in consistent units.

        Returns:
            The output value, in the unit consistent with the inputs.

        Raises:
            TypeError: If an input is missing or an unknown input is given.
        """
        expected = set(self.input_names)
        missing = sorted(expected - set(values))
        unexpected = sorted(set(values) - expected)
        if missing or unexpected:
            raise TypeError(
                f"{self.id} expects inputs {list(self.input_names)}; "
                f"missing {missing}, unexpected {unexpected}."
            )
        return self.evaluator(**values)

    def to_dict(self) -> dict[str, Any]:
        """Return the metadata as JSON-serializable data (the evaluator is omitted)."""
        return {
            "id": self.id,
            "name": self.name,
            "equation": self.equation,
            "description": self.description,
            "inputs": [variable.to_dict() for variable in self.inputs],
            "output": self.output.to_dict(),
            "assumptions": list(self.assumptions),
            "references": [reference.to_dict() for reference in self.references],
            "references_ieee": [reference.format_ieee() for reference in self.references],
            "verification_cases": [case.to_dict() for case in self.verification_cases],
            "tags": list(self.tags),
        }
