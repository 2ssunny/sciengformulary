"""Haaland Friction Factor: f_D = (1.8 * log10(6.9 / Re + (eD / 3.7)^1.11))^-2."""

import math

from sciengformulary.catalog._domain import finite, finite_result
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

_RE_MIN = 4000.0
_RE_MAX = 1.0e8
_ED_MAX = 0.05


def _evaluate(
    Re: float,  # noqa: N803
    eD: float,  # noqa: N803
) -> float:
    finite("Re", Re)
    finite("eD", eD)
    if not _RE_MIN <= Re <= _RE_MAX:
        raise ValueError(f"Re must lie in [4000, 1e8] for the Haaland correlation, got {Re!r}.")
    if not 0.0 <= eD <= _ED_MAX:
        raise ValueError(f"eD must lie in [0, 0.05] for the Haaland correlation, got {eD!r}.")
    return finite_result(1.0 / (1.8 * math.log10(6.9 / Re + (eD / 3.7) ** 1.11)) ** 2)


haaland_friction_factor = FormulaSpec(
    id="fluids.haaland_friction_factor",
    name="Haaland Friction Factor",
    equation="f_D = (1.8 * log10(6.9 / Re + (eD / 3.7)^1.11))^-2",
    description=(
        "Explicit approximation of the Darcy friction factor for turbulent flow in a rough "
        "circular pipe, from the Reynolds number and the relative roughness."
    ),
    inputs=(
        VariableSpec(
            name="Re",
            symbol="Re_D",
            description="Reynolds number based on pipe diameter",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="eD",
            symbol=r"\varepsilon/D",
            description="Relative roughness (wall roughness height divided by inner diameter)",
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
        # The source prints f = 1 / {1.8 log10[6.9 / Re_D + ((eps / D) / 3.7)^1.11]}^2 as the
        # Darcy factor of its eq. (7.33), with the ranges used in the checks below. Some
        # software libraries label the same expression as the Fanning factor; the number is
        # the Darcy value either way.
        lienhard_heat_transfer("sec. 7.3, eq. (7.50), p. 373", accessed=ENGINEERING_ACCESSED),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"Re": 100000.0, "eD": 0.0001},
            expected=0.01826505301479386,
            rel_tol=1e-12,
            note="50-digit mpmath value; an independent library example agrees.",
        ),
        VerificationCase(
            inputs={"Re": 25000.0, "eD": 0.002},
            expected=0.028505893955530846,
            rel_tol=1e-12,
            note="Mid-range point; 50-digit mpmath value.",
        ),
        VerificationCase(
            inputs={"Re": 4000.0, "eD": 0.05},
            expected=0.07763488009595958,
            rel_tol=1e-12,
            note="Corner of the validity range, lowest Re with the roughest pipe; mpmath value.",
        ),
        VerificationCase(
            inputs={"Re": 100000000.0, "eD": 0.0},
            expected=0.006018514872911013,
            rel_tol=1e-12,
            note="Corner of the validity range, highest Re with a smooth wall; mpmath value.",
        ),
        VerificationCase(
            inputs={"Re": 4000.0, "eD": 0.0},
            expected=0.04042284932911364,
            rel_tol=1e-12,
            note="Corner of the validity range, lowest Re with a smooth wall; mpmath value.",
        ),
    ),
    assumptions=(
        "Turbulent flow in a full circular pipe with uniform wall roughness; Darcy friction "
        "factor of the source's eq. (7.33), not the Fanning factor.",
        "Valid only for 4000 <= Re <= 1e8 and 0 <= eD <= 0.05, as the source states; "
        "ValueError is raised outside these ranges. eD = 0 (smooth wall) is allowed.",
        "Re is based on pipe diameter; eD is the roughness height divided by the inner "
        "diameter. The source states these limits for its own use of the correlation; the "
        "original Haaland paper was not consulted.",
    ),
    tags=("friction factor", "Haaland", "turbulent", "rough pipe", "Moody", "Darcy-Weisbach"),
)
