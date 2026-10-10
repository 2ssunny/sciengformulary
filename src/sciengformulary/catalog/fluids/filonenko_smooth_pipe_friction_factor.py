"""Filonenko Smooth-Pipe Friction Factor: f_D = (1.82 * log10(Re) - 1.64)^-2."""

import math

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

_RE_MIN = 2300.0
_RE_MAX = 5.0e6


def _evaluate(Re: float) -> float:  # noqa: N803
    positive("Re", Re)
    if not _RE_MIN <= Re <= _RE_MAX:
        raise ValueError(f"Re must lie in [2300, 5e6] for the Filonenko correlation, got {Re!r}.")
    return finite_result(1.0 / (1.82 * math.log10(Re) - 1.64) ** 2)


filonenko_smooth_pipe_friction_factor = FormulaSpec(
    id="fluids.filonenko_smooth_pipe_friction_factor",
    name="Filonenko Smooth-Pipe Friction Factor",
    equation="f_D = (1.82 * log10(Re) - 1.64)^-2",
    description=(
        "Explicit Darcy friction factor for turbulent flow in a hydraulically smooth circular "
        "pipe, as a function of the diameter-based Reynolds number only."
    ),
    inputs=(
        VariableSpec(
            name="Re",
            symbol="Re_D",
            description="Reynolds number based on pipe diameter",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="f_D",
        symbol="f",
        description="Darcy-Weisbach friction factor",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The source prints the expression as its eq. (7.42) and works it at Re_D = 412,300
        # (f rounded to 0.0136); the symbols are the same up to renaming.
        lienhard_heat_transfer(
            "sec. 7.3, eq. (7.42), p. 369; worked value p. 372",
            accessed=ENGINEERING_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"Re": 412300.0},
            expected=0.013584916790961722,
            rel_tol=1e-12,
            note=(
                "Reynolds number of the worked pipe example on p. 372, where the textbook rounds "
                "f to 0.0136; the expected value is the 50-digit mpmath result."
            ),
        ),
        VerificationCase(
            inputs={"Re": 2300.0},
            expected=0.04986145767700318,
            rel_tol=1e-12,
            note="Lower end of the stated range; 50-digit mpmath value.",
        ),
        VerificationCase(
            inputs={"Re": 5000000.0},
            expected=0.008980905197987004,
            rel_tol=1e-12,
            note="Upper end of the stated range; 50-digit mpmath value.",
        ),
    ),
    assumptions=(
        "Hydraulically smooth wall (relative roughness zero); Darcy friction factor of the "
        "source's pipe-flow definition, not the Fanning factor.",
        "Re must lie in 2300 <= Re <= 5e6, otherwise ValueError is raised. The source attaches "
        "this range to the use of the relation together with its Gnielinski correlation; it "
        "does not give a separate range for the friction-factor relation itself.",
        "Re is based on pipe diameter and the cross-section-average speed.",
    ),
    tags=("friction factor", "Filonenko", "smooth pipe", "turbulent", "Darcy-Weisbach"),
)
