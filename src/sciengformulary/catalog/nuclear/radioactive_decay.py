"""Radioactive Decay Law: N = N0 * exp(-lambda * t)."""

import math

from sciengformulary.catalog._sources import (
    doe_fundamentals_handbook,
    openstax_university_physics,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    N0: float,  # noqa: N803
    decay_constant: float,
    t: float,
) -> float:
    return N0 * math.exp(-decay_constant * t)


radioactive_decay = FormulaSpec(
    id="nuclear.radioactive_decay",
    name="Radioactive Decay Law",
    equation="N = N0 * exp(-lambda * t)",
    description="Number of undecayed nuclei remaining after time t.",
    inputs=(
        VariableSpec(
            name="N0",
            symbol="N_0",
            description="Number of nuclei at t = 0",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="decay_constant",
            symbol=r"\lambda",
            description="Decay constant",
            dimension="T^-1",
            si_unit="1/s",
        ),
        VariableSpec(
            name="t",
            symbol="t",
            description="Elapsed time",
            dimension="T",
            si_unit="s",
        ),
    ),
    output=VariableSpec(
        name="N",
        symbol="N",
        description="Number of undecayed nuclei at time t",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        openstax_university_physics(3, "10-3-radioactive-decay", "sec. 10.3, eq. (10.11)"),
        doe_fundamentals_handbook(
            "DOE-HDBK-1019/1-93",
            "Module 1 Radioactivity, eq. (1-4), p. 31 (also (1-5), p. 32)",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"N0": 1000.0, "decay_constant": 0.1, "t": 10.0},
            expected=367.8794411714423,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation: 1000 / e.",
        ),
    ),
    assumptions=(
        "Single radionuclide with no production (no parent feeding it).",
        "Statistical law: accurate for large N; individual decays are random.",
        "decay_constant and t in reciprocal units (1/s with s, 1/yr with yr).",
    ),
    tags=("radioactive decay", "exponential decay", "half-life", "nuclear"),
)
