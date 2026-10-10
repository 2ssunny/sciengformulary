"""Crossflow Effectiveness, C_max Stream Mixed:
eps = (1 / C_r) * (1 - exp(-C_r * (1 - exp(-NTU)))).
"""

import math

from sciengformulary.catalog._domain import finite, non_negative
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    NTU: float,  # noqa: N803
    C_r: float,  # noqa: N803
) -> float:
    non_negative("NTU", NTU)
    if not 0 < finite("C_r", C_r) <= 1:
        raise ValueError(f"C_r must lie in (0, 1], got {C_r!r}.")
    # With b = 1 - exp(-NTU) and y = C_r * b, the stated (1 - exp(-y)) / C_r equals
    # b * (1 - exp(-y)) / y. Both factors are computed with expm1, and the division by y
    # (which can be tiny or zero) is replaced by its limit 1.
    b = -math.expm1(-NTU)
    y = C_r * b
    if y == 0:
        return b
    return b * (-math.expm1(-y) / y)


crossflow_cmax_mixed_effectiveness = FormulaSpec(
    id="heat_transfer.crossflow_cmax_mixed_effectiveness",
    name="Crossflow Effectiveness, C_max Stream Mixed",
    equation="eps = (1 / C_r) * (1 - exp(-C_r * (1 - exp(-NTU))))",
    description=(
        "Effectiveness of a single-pass crossflow heat exchanger in which the stream with the "
        "larger capacity rate is mixed and the stream with the smaller one is unmixed."
    ),
    inputs=(
        VariableSpec(
            name="NTU",
            symbol="NTU",
            description="Number of transfer units, U A / C_min",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="C_r",
            symbol="C_r",
            description="Capacity-rate ratio C_min / C_max (above 0, up to 1)",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="eps",
        symbol=r"\varepsilon",
        description="Effectiveness, Q / (C_min * (T_h,in - T_c,in))",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes R = Cmin/Cmax and (1/R) * (1 - exp{-R [1 - exp(-NTU)]}).
        lienhard_heat_transfer(
            "sec. 3.3, Table 3.1 (crossflow, one stream mixed: Cmax mixed, Cmin unmixed), p. 125",
            accessed=ENGINEERING_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"NTU": 5.0, "C_r": 0.7},
            expected=0.7158099831204696,
            rel_tol=1e-12,
            note="50-digit mpmath evaluation of the equation.",
        ),
        VerificationCase(
            inputs={"NTU": 1.0, "C_r": 1.0},
            expected=0.4685363946133843,
            rel_tol=1e-12,
            note="Balanced flow, C_r = 1; 50-digit mpmath evaluation.",
        ),
    ),
    assumptions=(
        "Steady operation, no heat loss to the surroundings, negligible axial conduction.",
        "Constant overall coefficient U and constant specific heats of both streams.",
        "Single-pass crossflow; the C_max stream is mixed and the C_min stream is unmixed. The "
        "opposite assignment is the C_min-mixed formula.",
        "C_r = C_min / C_max with 0 < C_r <= 1, and NTU >= 0 with NTU = U A / C_min; "
        "otherwise ValueError is raised. C_r = 0 is outside the stated range.",
        "Dimensionless: no unit system enters.",
    ),
    tags=("heat exchanger", "effectiveness", "crossflow", "effectiveness-NTU"),
)
