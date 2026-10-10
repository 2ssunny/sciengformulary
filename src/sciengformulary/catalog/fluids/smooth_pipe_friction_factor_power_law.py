"""Smooth-Pipe Friction Factor Power Law: f_D = 0.184 * Re^-0.2."""

from sciengformulary.catalog._domain import finite, finite_result
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

_RE_MIN = 10000.0


def _evaluate(Re: float) -> float:  # noqa: N803
    finite("Re", Re)
    if Re < _RE_MIN:
        raise ValueError(f"Re must be at least 10000 for this power law, got {Re!r}.")
    return finite_result(0.184 * Re**-0.2)


smooth_pipe_friction_factor_power_law = FormulaSpec(
    id="fluids.smooth_pipe_friction_factor_power_law",
    name="Smooth-Pipe Friction Factor Power Law",
    equation="f_D = 0.184 * Re^-0.2",
    description=(
        "Approximate Darcy friction factor of a hydraulically smooth pipe in turbulent flow, "
        "from a power law in the diameter-based Reynolds number."
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
        # The source prints the smooth-pipe curve as C_f = f/4 = 0.046 / Re_D^0.2 (eq. 7.38).
        # Derived result: with the Darcy factor f = 4 C_f (eq. 7.34), f = 4 * 0.046 Re^-0.2
        # = 0.184 Re^-0.2.
        lienhard_heat_transfer("sec. 7.3, eq. (7.38), p. 368", accessed=ENGINEERING_ACCESSED),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"Re": 10000.0},
            expected=0.02916203474128449,
            rel_tol=1e-12,
            note="Lower limit of the stated range; 50-digit mpmath value of 0.184 * 1e4^-0.2.",
        ),
        VerificationCase(
            inputs={"Re": 100000.0},
            expected=0.0184,
            rel_tol=1e-12,
            note="Exact by hand: (1e5)^-0.2 = 0.1, so f = 0.0184.",
        ),
        VerificationCase(
            inputs={"Re": 1000000.0},
            expected=0.011609615138435557,
            rel_tol=1e-12,
            note="High Reynolds number; 50-digit mpmath value.",
        ),
    ),
    assumptions=(
        "Derived result: the coefficient 0.184 is 4 x 0.046, the source's skin-friction "
        "coefficient 0.046 multiplied by 4 through f = 4 C_f.",
        "Hydraulically smooth wall; an approximation of the smooth-pipe curve, not an exact law.",
        "Valid for Re >= 10000, the source's lower limit; ValueError is raised below it. The "
        "source states no upper limit.",
        "The exponent 0.2 and coefficient 0.046 differ from the Blasius form (0.25 power); do "
        "not mix the two.",
    ),
    tags=("friction factor", "power law", "smooth pipe", "turbulent", "Darcy-Weisbach"),
)
