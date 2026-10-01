"""Mean Free Path of a Gas Molecule: l = 1 / (sqrt(2) * pi * d^2 * n)."""

import math

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(d: float, n: float) -> float:
    return 1.0 / (math.sqrt(2.0) * math.pi * d**2 * n)


mean_free_path = FormulaSpec(
    id="thermodynamics.mean_free_path",
    name="Mean Free Path of a Gas Molecule",
    equation="l = 1 / (sqrt(2) * pi * d^2 * n)",
    description="Average distance a molecule travels between collisions in a dilute gas.",
    inputs=(
        VariableSpec(
            name="d",
            symbol="d",
            description="Effective molecular (collision) diameter",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="n",
            symbol="n",
            description="Number density of molecules (molecules per unit volume)",
            dimension="L^-3",
            si_unit="1/m^3",
        ),
    ),
    output=VariableSpec(
        name="l",
        symbol=r"\ell",
        description="Mean free path",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes V / (4 sqrt(2) pi r^2 N) with molecular radius r = d / 2 and N / V = n.
        openstax_university_physics(
            2,
            "2-2-pressure-temperature-and-rms-speed",
            "sec. 2.2, eq. (2.10)",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"d": 3.7e-10, "n": 2.5e+25},
            expected=6.576452272878788e-08,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation (air-like values near sea level).",
        ),
    ),
    assumptions=(
        "Dilute ideal gas in thermal equilibrium (kinetic theory); T must be absolute.",
        "Hard-sphere molecules of a single species with the stated effective diameter.",
    ),
    tags=("mean free path", "kinetic theory", "Knudsen", "rarefied gas"),
)
