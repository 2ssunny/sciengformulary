"""Colburn Equation for Turbulent Pipe Flow: Nu_D = 0.023 * Re_D^0.8 * Pr^(1/3)."""

from sciengformulary.catalog._domain import finite, finite_result
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

_RE_MIN = 1.0e4
_PR_MIN = 0.67
_PR_MAX = 100.0


def _evaluate(Re_D: float, Pr: float) -> float:  # noqa: N803 - symbols as written in the source
    if finite("Re_D", Re_D) < _RE_MIN:
        raise ValueError(f"Re_D must be at least {_RE_MIN:g} for this correlation, got {Re_D!r}.")
    if not _PR_MIN <= finite("Pr", Pr) <= _PR_MAX:
        raise ValueError(f"Pr must lie in [{_PR_MIN}, {_PR_MAX:g}], got {Pr!r}.")
    # Library implementations (for example the Python "ht" package) restrict this equation
    # to narrower ranges, Re 1e4 to 1e5 and Pr 0.5 to 3; the textbook ranges are used here.
    return finite_result(0.023 * Re_D**0.8 * Pr ** (1.0 / 3.0))


colburn_pipe_nusselt = FormulaSpec(
    id="heat_transfer.colburn_pipe_nusselt",
    name="Colburn Equation for Turbulent Pipe Flow",
    equation="Nu_D = 0.023 * Re_D^0.8 * Pr^(1/3)",
    description=(
        "Early power-law estimate of the diameter-based Nusselt number for fully developed "
        "turbulent flow in a smooth round pipe. It is the Colburn analogy combined with a "
        "smooth-pipe friction fit; the Gnielinski correlations are the more accurate modern "
        "choice."
    ),
    inputs=(
        VariableSpec(
            name="Re_D",
            symbol="Re_D",
            description="Reynolds number based on the pipe diameter, at least 10^4",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="Pr",
            symbol="Pr",
            description="Prandtl number, from 0.67 to 100",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="Nu_D",
        symbol="Nu_D",
        description="Nusselt number h D / k based on the pipe diameter",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The source obtains the equation from Colburn's analogy and the smooth-pipe friction
        # fit f/4 = 0.046 Re_D^-0.2 (eq. 7.38), valid for Re_D >= 10 000.
        lienhard_heat_transfer("sec. 7.3, eq. (7.39a), p. 368", accessed=ENGINEERING_ACCESSED),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"Re_D": 100000.0, "Pr": 1.2},
            expected=244.41147091200054,
            rel_tol=1e-12,
            note="0.023 * 1e5^0.8 * 1.2^(1/3) evaluated with 50-digit arithmetic (mpmath).",
        ),
        VerificationCase(
            inputs={"Re_D": 10000.0, "Pr": 0.67},
            expected=31.89721533251494,
            rel_tol=1e-12,
            note="Lower edge of both ranges, Re_D = 1e4 and Pr = 0.67; 50-digit arithmetic.",
        ),
    ),
    assumptions=(
        "Fully developed turbulent flow in a smooth circular pipe with Re_D >= 10^4, the range "
        "of the friction fit the equation is built on.",
        "Intended for modest wall-to-fluid temperature differences, so that properties barely "
        "vary across the pipe; properties are taken at the local bulk temperature (the source "
        "states this for its Sieder-Tate form of the same equation).",
        "The source quotes errors of up to +25 % and -40 % over 0.67 <= Pr <= 100, usually much "
        "smaller; the evaluator raises ValueError outside that Prandtl range.",
        "Dimensionless; the coefficient 0.023 holds in any consistent unit system.",
    ),
    tags=("Nusselt number", "pipe flow", "turbulent", "Colburn", "forced convection"),
)
