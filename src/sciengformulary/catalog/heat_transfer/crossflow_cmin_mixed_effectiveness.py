"""Crossflow Effectiveness, C_min Stream Mixed:
eps = 1 - exp(-(1 - exp(-NTU * C_r)) / C_r).
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
    # The stated exponent is w = (1 - exp(-NTU * C_r)) / C_r = NTU * (1 - exp(-x)) / x with
    # x = NTU * C_r. Using expm1 and the limit 1 of (1 - exp(-x)) / x at x = 0 keeps w exact for
    # small x and gives w = NTU at C_r = 0.
    x = NTU * C_r
    w = NTU if x == 0 else NTU * (-math.expm1(-x) / x)
    return -math.expm1(-w)


crossflow_cmin_mixed_effectiveness = FormulaSpec(
    id="heat_transfer.crossflow_cmin_mixed_effectiveness",
    name="Crossflow Effectiveness, C_min Stream Mixed",
    equation="eps = 1 - exp(-(1 - exp(-NTU * C_r)) / C_r); eps = 1 - exp(-NTU) for C_r = 0",
    description=(
        "Effectiveness of a single-pass crossflow heat exchanger in which the stream with the "
        "smaller capacity rate is mixed and the stream with the larger one is unmixed."
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
        # The source writes R = Cmin/Cmax and 1 - exp{-[1 - exp(-NTU R)] / R} for R > 0. At
        # C_r = 0 that form is 0/0 in the exponent; the limit of (1 - exp(-NTU C_r)) / C_r as
        # C_r tends to 0 is NTU, so eps tends to 1 - exp(-NTU), the form for a stream at
        # constant temperature. That limit is the derived branch.
        lienhard_heat_transfer(
            "sec. 3.3, Table 3.1 (crossflow, one stream mixed: Cmin mixed, Cmax unmixed), p. 125",
            accessed=ENGINEERING_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"NTU": 5.0, "C_r": 0.7},
            expected=0.7497843941508544,
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
        "Derived result: at C_r = 0 the stated form has a 0/0 exponent. Its limit as C_r tends "
        "to 0 is 1 - exp(-NTU), and the evaluator uses it at exactly C_r = 0. Values at small "
        "C_r agree with it.",
        "Steady operation, no heat loss to the surroundings, negligible axial conduction.",
        "Constant overall coefficient U and constant specific heats of both streams.",
        "Single-pass crossflow; the C_min stream is mixed and the C_max stream is unmixed. The "
        "opposite assignment is the C_max-mixed formula.",
        "C_r = C_min / C_max, so 0 <= C_r <= 1, and NTU >= 0 with NTU = U A / C_min; "
        "otherwise ValueError is raised.",
        "Dimensionless: no unit system enters.",
    ),
    tags=("heat exchanger", "effectiveness", "crossflow", "effectiveness-NTU"),
)
