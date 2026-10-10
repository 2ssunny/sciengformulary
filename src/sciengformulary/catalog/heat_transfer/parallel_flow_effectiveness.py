"""Parallel-Flow Effectiveness: eps = (1 - exp(-NTU * (1 + C_r))) / (1 + C_r)."""

import math

from sciengformulary.catalog._domain import finite, non_negative
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    NTU: float,  # noqa: N803
    C_r: float,  # noqa: N803
) -> float:
    non_negative("NTU", NTU)
    if not 0 <= finite("C_r", C_r) <= 1:
        raise ValueError(f"C_r must lie in [0, 1], got {C_r!r}.")
    # -expm1(-z) = 1 - exp(-z) without cancellation when NTU is small.
    return -math.expm1(-NTU * (1 + C_r)) / (1 + C_r)


parallel_flow_effectiveness = FormulaSpec(
    id="heat_transfer.parallel_flow_effectiveness",
    name="Parallel-Flow Heat Exchanger Effectiveness",
    equation="eps = (1 - exp(-NTU * (1 + C_r))) / (1 + C_r)",
    description=(
        "Effectiveness of a single-pass parallel-flow (co-current) heat exchanger as a function "
        "of the number of transfer units and the capacity-rate ratio."
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
            description="Capacity-rate ratio C_min / C_max (0 to 1)",
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
        # The source writes the ratio as Cmin/Cmax and the equation in the same form.
        lienhard_heat_transfer("sec. 3.3, eq. (3.20), p. 122", accessed=ENGINEERING_ACCESSED),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"NTU": 1.5, "C_r": 0.5},
            expected=0.5964005169587571,
            rel_tol=1e-12,
            note=(
                "Worked example in the cited section (Example 3.5, p. 123) prints 0.596; the "
                "value here is the 50-digit mpmath evaluation."
            ),
        ),
        VerificationCase(
            inputs={"NTU": 5.0, "C_r": 0.7},
            expected=0.5881156068417585,
            rel_tol=1e-12,
            note="50-digit mpmath evaluation of the equation.",
        ),
        VerificationCase(
            inputs={"NTU": 2.0, "C_r": 1.0},
            expected=0.4908421805556329,
            rel_tol=1e-12,
            note="Balanced flow, C_r = 1; 50-digit mpmath evaluation.",
        ),
        VerificationCase(
            inputs={"NTU": 0.0, "C_r": 0.5},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="No transfer area gives no heat transfer, so the effectiveness is zero.",
        ),
    ),
    assumptions=(
        "Steady operation, no heat loss to the surroundings, negligible axial conduction.",
        "Constant overall coefficient U and constant specific heats of both streams.",
        "Single-pass parallel (co-current) flow.",
        "C_r = C_min / C_max, so 0 <= C_r <= 1, and NTU >= 0 with NTU = U A / C_min; "
        "otherwise ValueError is raised. The source gives the equation for any ratio and plots "
        "it for 0 to 1; this evaluator accepts the plotted range only.",
        "Dimensionless: no unit system enters.",
    ),
    tags=("heat exchanger", "effectiveness", "parallel flow", "effectiveness-NTU"),
)
