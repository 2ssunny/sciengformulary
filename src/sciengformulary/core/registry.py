"""In-memory registry for looking up formulas by id or keyword."""

from __future__ import annotations

import difflib
from collections.abc import Iterable

from sciengformulary.core.spec import FormulaSpec

SUGGESTION_COUNT = 3


class FormulaRegistry:
    """A lookup table of formulas keyed by id."""

    def __init__(self, formulas: Iterable[FormulaSpec] = ()) -> None:
        """Create a registry, optionally pre-filled with formulas.

        Args:
            formulas: Formulas to register immediately.
        """
        self._formulas: dict[str, FormulaSpec] = {}
        for formula in formulas:
            self.register(formula)

    def register(self, formula: FormulaSpec) -> None:
        """Add a formula.

        Args:
            formula: The formula to add.

        Raises:
            ValueError: If a formula with the same id is already registered.
        """
        if formula.id in self._formulas:
            raise ValueError(f"Formula id {formula.id!r} is already registered.")
        self._formulas[formula.id] = formula

    def get(self, formula_id: str) -> FormulaSpec:
        """Return the formula with the given id.

        Args:
            formula_id: Dotted id, e.g. ``"aerodynamics.dynamic_pressure"``.

        Raises:
            KeyError: If no formula has that id. The message lists close matches.
        """
        try:
            return self._formulas[formula_id]
        except KeyError:
            suggestions = difflib.get_close_matches(formula_id, self._formulas, SUGGESTION_COUNT)
            raise KeyError(
                f"Unknown formula id {formula_id!r}. Close matches: {suggestions}."
            ) from None

    def list(self) -> list[FormulaSpec]:
        """Return all formulas, sorted by id."""
        return [self._formulas[formula_id] for formula_id in sorted(self._formulas)]

    def search(self, query: str) -> list[FormulaSpec]:
        """Find formulas whose text contains every word of the query.

        Matching is case-insensitive substring matching over the id, name,
        description and tags. Results are sorted by id, so output is deterministic.

        Args:
            query: Space-separated keywords, e.g. ``"dynamic pressure"``.
        """
        words = query.lower().split()
        matches = []
        for formula in self.list():
            text = _search_text(formula)
            if all(word in text for word in words):
                matches.append(formula)
        return matches

    def __contains__(self, formula_id: object) -> bool:
        return formula_id in self._formulas

    def __len__(self) -> int:
        return len(self._formulas)


def _search_text(formula: FormulaSpec) -> str:
    """Build the lowercase text a query is matched against."""
    readable_id = formula.id.replace(".", " ").replace("_", " ")
    parts = [formula.id, readable_id, formula.name, formula.description, *formula.tags]
    return " ".join(parts).lower()
