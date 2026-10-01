"""Known input/output cases that check a formula's evaluator numerically."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any

# math.isclose defaults: agreement to about nine significant digits, no absolute floor.
DEFAULT_REL_TOL = 1e-9
DEFAULT_ABS_TOL = 0.0


@dataclass(frozen=True, kw_only=True)
class VerificationCase:
    """One known result that a formula's evaluator must reproduce.

    A case checks that the Python evaluator implements the declared equation. It does
    not show that the equation is scientifically correct or applicable; that rests on
    the formula's references and on human review.

    ``expected`` must be determined independently of the evaluator under test, e.g. from
    a worked example in a cited source or a hand calculation from the published
    equation. Never produce it by running the evaluator.

    Attributes:
        inputs: Input values keyed by the formula's input names, in consistent units.
        expected: The independently determined output for ``inputs``.
        rel_tol: Relative tolerance passed to :func:`math.isclose`.
        abs_tol: Absolute tolerance passed to :func:`math.isclose`.
        note: Where ``expected`` comes from and what the case checks.
    """

    # Stored read-only; excluded from the hash because a mapping is not hashable.
    inputs: Mapping[str, float] = field(hash=False)
    expected: float
    rel_tol: float = DEFAULT_REL_TOL
    abs_tol: float = DEFAULT_ABS_TOL
    note: str

    def __post_init__(self) -> None:
        if isinstance(self.inputs, Mapping):
            object.__setattr__(self, "inputs", MappingProxyType(dict(self.inputs)))
        self.validate()

    def validate(self) -> None:
        """Check that inputs, expected value, tolerances and note are well formed.

        Raises:
            ValueError: If a field is malformed.
        """
        problems = []
        if not isinstance(self.inputs, Mapping):
            problems.append("inputs must be a mapping of input name to number")
        else:
            for name, value in self.inputs.items():
                if not isinstance(name, str) or not name.isidentifier():
                    problems.append(f"input name {name!r} must be a Python identifier")
                elif not _is_finite_number(value):
                    problems.append(f"input {name!r} must be a finite int or float, got {value!r}")
        if not _is_finite_number(self.expected):
            problems.append(f"expected must be a finite int or float, got {self.expected!r}")
        for name in ("rel_tol", "abs_tol"):
            value = getattr(self, name)
            if not _is_finite_number(value) or value < 0:
                problems.append(f"{name} must be a finite, non-negative number, got {value!r}")
        if not isinstance(self.note, str) or not self.note.strip():
            problems.append("note must be a non-empty string explaining where expected comes from")
        if problems:
            raise ValueError(f"Invalid VerificationCase: {'; '.join(problems)}.")

    def matches(self, actual: float) -> bool:
        """Return whether ``actual`` equals ``expected`` within this case's tolerances."""
        return _is_finite_number(actual) and math.isclose(
            actual, self.expected, rel_tol=self.rel_tol, abs_tol=self.abs_tol
        )

    def to_dict(self) -> dict[str, Any]:
        """Return the case as JSON-serializable data."""
        return {
            "inputs": dict(self.inputs),
            "expected": self.expected,
            "rel_tol": self.rel_tol,
            "abs_tol": self.abs_tol,
            "note": self.note,
        }


def _is_finite_number(value: object) -> bool:
    """Accept int and float (not bool, which is an int subclass) that are finite."""
    if isinstance(value, bool):
        return False
    # Ints are always finite; math.isfinite would overflow on very large ones.
    return isinstance(value, int) or (isinstance(value, float) and math.isfinite(value))
