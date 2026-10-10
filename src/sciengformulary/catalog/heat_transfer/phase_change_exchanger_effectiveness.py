"""Effectiveness of a Heat Exchanger with One Stream Changing Phase: eps = 1 - exp(-NTU)."""

import math

from sciengformulary.catalog._domain import non_negative
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(NTU: float) -> float:  # noqa: N803 - symbol as written in the source
    non_negative("NTU", NTU)
    # expm1 keeps full precision for small NTU.
    return -math.expm1(-NTU)


phase_change_exchanger_effectiveness = FormulaSpec(
    id="heat_transfer.phase_change_exchanger_effectiveness",
    name="Effectiveness with One Stream Changing Phase",
    equation="eps = 1 - exp(-NTU)",
    description=(
        "Effectiveness of a heat exchanger in which one stream stays at a uniform temperature "
        "(a condensing or boiling stream), so the capacity-rate ratio is zero and the flow "
        "arrangement no longer matters. This is the zero-ratio special case of the general "
        "parallel-flow and counterflow effectiveness relations."
    ),
    inputs=(
        VariableSpec(
            name="NTU",
            symbol="NTU",
            description="Number of transfer units U A / C_min, not negative",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="eps",
        symbol=r"\varepsilon",
        description="Heat exchanger effectiveness Q / (C_min (T_h,in - T_c,in))",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The source prints this relation as eq. (3.22) for the single-stream limit
        # C_min/C_max -> 0, obtained there by letting the ratio go to zero in eq. (3.20) or
        # (3.21), and notes that it defines the C_min/C_max = 0 curve of Figs. 3.16 and 3.17.
        lienhard_heat_transfer(
            "sec. 3.3, eq. (3.22), p. 126; limit of eqs. (3.20)-(3.21), p. 122",
            accessed=ENGINEERING_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"NTU": 1.0},
            expected=0.6321205588285577,
            rel_tol=1e-12,
            note="1 - 1/e evaluated with 50-digit arithmetic (mpmath).",
        ),
        VerificationCase(
            inputs={"NTU": 5.0},
            expected=0.9932620530009145,
            rel_tol=1e-12,
            note="1 - exp(-5) evaluated with 50-digit arithmetic (mpmath).",
        ),
        VerificationCase(
            inputs={"NTU": 0.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="No transfer area gives no heat transfer: 1 - exp(0) = 0.",
        ),
    ),
    assumptions=(
        "Stated by the source as the single-stream limit, the relation reached when the "
        "capacity-rate ratio C_min/C_max goes to zero in the parallel-flow or counterflow "
        "effectiveness relation.",
        "One stream is at an effectively constant temperature (C_max tends to infinity), for "
        "example a condenser or evaporator. Then the flow arrangement does not change the "
        "result.",
        "Steady operation, no heat loss to the surroundings, negligible axial conduction, and "
        "constant overall coefficient and specific heats along the exchanger.",
        "NTU is based on C_min, the capacity rate of the stream that changes temperature; "
        "NTU must not be negative.",
    ),
    tags=("heat exchanger", "effectiveness", "NTU", "condenser", "evaporator"),
)
