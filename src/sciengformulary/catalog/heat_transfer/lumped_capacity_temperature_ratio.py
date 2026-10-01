"""Lumped-Capacity Temperature Response: (T - T_inf) / (T_i - T_inf) = exp(-t / tau)."""

import math

from sciengformulary.catalog._sources import lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(t: float, tau: float) -> float:
    return math.exp(-t / tau)


lumped_capacity_temperature_ratio = FormulaSpec(
    id="heat_transfer.lumped_capacity_temperature_ratio",
    name="Lumped-Capacity Temperature Response",
    equation="(T - T_inf) / (T_i - T_inf) = exp(-t / tau)",
    description=(
        "Fraction of the initial temperature difference remaining after time t for a lumped body "
        "in a fluid at fixed temperature."
    ),
    inputs=(
        VariableSpec(
            name="t",
            symbol="t",
            description="Elapsed time",
            dimension="T",
            si_unit="s",
        ),
        VariableSpec(
            name="tau",
            symbol=r"\tau",
            description="Lumped-capacity time constant rho c V / (h A)",
            dimension="T",
            si_unit="s",
        ),
    ),
    output=VariableSpec(
        name="theta",
        symbol=r"\Theta",
        description="Remaining fraction (T - T_inf) / (T_i - T_inf)",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The sheet's general form includes a heat-generation term; this is its no-generation case.
        lienhard_heat_transfer("sec. 1.3, eq. (1.22)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"t": 65.0, "tau": 65.0},
            expected=0.36787944117144233,
            rel_tol=1e-12,
            note="One time constant leaves 1/e of the initial difference.",
        ),
    ),
    assumptions=(
        "Same conditions as the lumped-capacity time constant: Bi much less than 1, constant h "
        "and fluid temperature.",
        "No internal heat generation and no radiation.",
    ),
    tags=("lumped capacitance", "Newtonian cooling", "transient", "exponential decay"),
)
