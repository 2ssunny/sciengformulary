"""Variable specification used for formula inputs and outputs."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class VariableSpec:
    r"""One physical quantity that a formula consumes or produces.

    Units are documentation only: evaluators do no unit conversion. ``si_unit`` is a
    reference unit that shows what "consistent units" means for this quantity; it does
    not force callers to use SI.

    Attributes:
        name: Python identifier used as the keyword argument, e.g. ``"rho"``.
        symbol: LaTeX symbol as written in the source, e.g. ``r"\rho"`` or ``"C_L"``.
            Kept ASCII so it prints safely in any console.
        description: Plain-language meaning, e.g. ``"Fluid density"``.
        dimension: Dimensional formula in base dimensions M, L, T, Theta (temperature),
            N (amount), I (current), e.g. ``"M L^-3"``. Use ``"1"`` if dimensionless.
        si_unit: Matching SI unit for reference, e.g. ``"kg/m^3"``. Use ``"-"`` if
            dimensionless.
    """

    name: str
    symbol: str
    description: str
    dimension: str
    si_unit: str

    def to_dict(self) -> dict[str, Any]:
        """Return the variable as JSON-serializable data."""
        return asdict(self)
