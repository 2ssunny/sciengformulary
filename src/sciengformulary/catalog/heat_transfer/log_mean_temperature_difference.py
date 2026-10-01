"""Log Mean Temperature Difference: LMTD = (dT_a - dT_b) / ln(dT_a / dT_b)."""

import math

from sciengformulary.catalog._sources import lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(dT_a: float, dT_b: float) -> float:  # noqa: N803 - symbols as written in the source
    return (dT_a - dT_b) / math.log(dT_a / dT_b)


log_mean_temperature_difference = FormulaSpec(
    id="heat_transfer.log_mean_temperature_difference",
    name="Log Mean Temperature Difference",
    equation="LMTD = (dT_a - dT_b) / ln(dT_a / dT_b)",
    description=(
        "Effective mean temperature difference between the streams of a two-stream heat exchanger; "
        "the heat duty is U A times this value."
    ),
    inputs=(
        VariableSpec(
            name="dT_a",
            symbol=r"\Delta T_a",
            description="Hot-minus-cold temperature difference at one end",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="dT_b",
            symbol=r"\Delta T_b",
            description="Hot-minus-cold temperature difference at the other end",
            dimension="Theta",
            si_unit="K",
        ),
    ),
    output=VariableSpec(
        name="LMTD",
        symbol=r"\Delta T_{lm}",
        description="Log mean temperature difference",
        dimension="Theta",
        si_unit="K",
    ),
    evaluator=_evaluate,
    references=(
        lienhard_heat_transfer("sec. 3.2, eq. (3.13)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"dT_a": 40.0, "dT_b": 20.0},
            expected=28.85390081777927,
            rel_tol=1e-12,
            note=(
                "Worked example in the cited section: condenser at 60 C heating water from 20 C to "
                "40 C gives LMTD = 28.85 K."
            ),
        ),
    ),
    assumptions=(
        "Parallel-flow or counterflow exchanger (or one stream at constant temperature); other "
        "arrangements need a correction factor.",
        "Constant overall coefficient U and constant specific heats.",
        "dT_a and dT_b must be positive and unequal; when they are equal the limit is that "
        "common value, which this evaluator does not handle.",
    ),
    tags=("heat exchanger", "LMTD", "log mean temperature difference", "counterflow"),
)
