"""Counterflow Effectiveness:
eps = (1 - exp(-NTU * (1 - C_r))) / (1 - C_r * exp(-NTU * (1 - C_r))) for C_r < 1;
eps = NTU / (1 + NTU) for C_r = 1.
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
    if not 0 <= finite("C_r", C_r) <= 1:
        raise ValueError(f"C_r must lie in [0, 1], got {C_r!r}.")
    if C_r == 1:
        return NTU / (1 + NTU)
    # With a = 1 - exp(-NTU * (1 - C_r)), computed as -expm1 to avoid cancellation, the
    # stated ratio a / (1 - C_r * (1 - a)) becomes a / ((1 - C_r) + C_r * a). This stays
    # accurate as C_r approaches 1, where both terms of the denominator shrink together.
    a = -math.expm1(-NTU * (1 - C_r))
    return a / ((1 - C_r) + C_r * a)


counterflow_effectiveness = FormulaSpec(
    id="heat_transfer.counterflow_effectiveness",
    name="Counterflow Heat Exchanger Effectiveness",
    equation=(
        "eps = (1 - exp(-NTU * (1 - C_r))) / (1 - C_r * exp(-NTU * (1 - C_r))) for C_r < 1; "
        "eps = NTU / (1 + NTU) for C_r = 1"
    ),
    description=(
        "Effectiveness of a single-pass counterflow heat exchanger as a function of the number "
        "of transfer units and the capacity-rate ratio, including the balanced-flow limit."
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
        # The source states the C_r < 1 form (with R = Cmin/Cmax) and plots the
        # Cmin/Cmax = 1 curve. At C_r = 1 the stated form is 0/0; applying L'Hopital's rule in
        # C_r (checked symbolically) gives NTU / (1 + NTU), which is the derived branch.
        lienhard_heat_transfer("sec. 3.3, eq. (3.21), p. 122", accessed=ENGINEERING_ACCESSED),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"NTU": 5.0, "C_r": 0.7},
            expected=0.9206703686051108,
            rel_tol=1e-12,
            note="50-digit mpmath evaluation of the stated form.",
        ),
        VerificationCase(
            inputs={"NTU": 5.0, "C_r": 1.0},
            expected=0.8333333333333334,
            rel_tol=1e-12,
            note="Balanced flow: limit NTU / (1 + NTU) = 5/6, exact fraction.",
        ),
        VerificationCase(
            inputs={"NTU": 1.5, "C_r": 0.0},
            expected=0.7768698398515702,
            rel_tol=1e-12,
            note="C_r = 0 reduces the stated form to 1 - exp(-NTU); 50-digit mpmath.",
        ),
    ),
    assumptions=(
        "Derived result: at C_r = 1 the stated form is 0/0. Its limit as C_r tends to 1 is "
        "NTU / (1 + NTU), found with L'Hopital's rule, and the evaluator uses it at exactly "
        "C_r = 1. The limit is continuous: values at C_r just below 1 agree with it.",
        "Steady operation, no heat loss to the surroundings, negligible axial conduction.",
        "Constant overall coefficient U and constant specific heats of both streams.",
        "Single-pass counterflow.",
        "C_r = C_min / C_max, so 0 <= C_r <= 1, and NTU >= 0 with NTU = U A / C_min; "
        "otherwise ValueError is raised.",
        "Dimensionless: no unit system enters.",
    ),
    tags=("heat exchanger", "effectiveness", "counterflow", "effectiveness-NTU"),
)
