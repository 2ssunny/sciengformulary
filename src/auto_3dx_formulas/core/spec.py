"""Formula specification: metadata plus a numerical evaluator."""

from __future__ import annotations

import inspect
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from auto_3dx_formulas.core.variable import VariableSpec

FORMULA_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+$")


@dataclass(frozen=True)
class FormulaSpec:
    """One engineering formula: what it computes, when it applies, and how to evaluate it.

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
        description: What the formula represents.
        assumptions: Conditions under which the formula is valid.
        references: Sources, as plain citation strings. Empty means none recorded yet.
        tags: Extra search keywords and aliases.
    """

    id: str
    name: str
    equation: str
    inputs: tuple[VariableSpec, ...]
    output: VariableSpec
    evaluator: Callable[..., float] = field(repr=False)
    description: str = ""
    assumptions: tuple[str, ...] = ()
    references: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        # Fail at import time so a malformed formula never reaches an agent.
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
            "references": list(self.references),
            "tags": list(self.tags),
        }
