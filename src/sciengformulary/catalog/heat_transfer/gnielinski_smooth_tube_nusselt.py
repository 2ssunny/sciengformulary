"""Gnielinski Smooth-Pipe Power Law for Gases: Nu_D = 0.0214 * (Re_D^0.8 - 100) * Pr^0.4."""

from sciengformulary.catalog._domain import finite, finite_result
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

_RE_RANGE = (2300.0, 5.0e6)
_PR_RANGE = (0.6, 1.5)


def _evaluate(Re_D: float, Pr: float) -> float:  # noqa: N803 - symbols as written in the source
    if not _RE_RANGE[0] <= finite("Re_D", Re_D) <= _RE_RANGE[1]:
        raise ValueError(f"Re_D must lie in [{_RE_RANGE[0]:g}, {_RE_RANGE[1]:g}], got {Re_D!r}.")
    if not _PR_RANGE[0] <= finite("Pr", Pr) <= _PR_RANGE[1]:
        raise ValueError(f"Pr must lie in [{_PR_RANGE[0]}, {_PR_RANGE[1]}], got {Pr!r}.")
    # Library implementations (for example the Python "ht" package) quote Re 1e4 to 5e6 and
    # Pr 0.5 to 1.5; the textbook ranges are used here.
    return finite_result(0.0214 * (Re_D**0.8 - 100.0) * Pr**0.4)


gnielinski_smooth_tube_nusselt = FormulaSpec(
    id="heat_transfer.gnielinski_smooth_tube_nusselt",
    name="Gnielinski Smooth-Pipe Power Law for Gases",
    equation="Nu_D = 0.0214 * (Re_D^0.8 - 100) * Pr^0.4",
    description=(
        "Power-law fit of the Gnielinski pipe correlation for smooth round pipes and fluids with "
        "Prandtl numbers near one, such as gases. It needs no friction factor, unlike the "
        "general Gnielinski form, and applies only for Prandtl numbers up to 1.5."
    ),
    inputs=(
        VariableSpec(
            name="Re_D",
            symbol="Re_D",
            description="Reynolds number based on the pipe diameter, 2300 to 5e6",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="Pr",
            symbol="Pr",
            description="Prandtl number, 0.6 to 1.5",
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
        # The source gives this fit as agreeing with its general Gnielinski equation (7.41)
        # over 2300 <= Re_D <= 5e6 for 0.6 <= Pr <= 1.5.
        lienhard_heat_transfer("sec. 7.3, eq. (7.43a), p. 371", accessed=ENGINEERING_ACCESSED),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"Re_D": 100000.0, "Pr": 1.2},
            expected=227.8880049437343,
            rel_tol=1e-12,
            note="0.0214 * (1e5^0.8 - 100) * 1.2^0.4 evaluated with 50-digit arithmetic.",
        ),
        VerificationCase(
            inputs={"Re_D": 2300.0, "Pr": 0.6},
            expected=6.787598638783551,
            rel_tol=1e-12,
            note="Lower edges of both ranges; 50-digit arithmetic (mpmath).",
        ),
        VerificationCase(
            inputs={"Re_D": 5000000.0, "Pr": 1.5},
            expected=5752.230790481048,
            rel_tol=1e-12,
            note="Upper edges of both ranges; 50-digit arithmetic (mpmath).",
        ),
    ),
    assumptions=(
        "Smooth round pipe, fully developed flow, for 2300 <= Re_D <= 5e6 and 0.6 <= Pr <= 1.5; "
        "the evaluator raises ValueError outside these ranges.",
        "Properties are evaluated at the bulk temperature. Corrections for strongly varying "
        "properties are separate and are not included.",
        "Dimensionless; the constants 0.0214 and 100 hold in any consistent unit system.",
    ),
    tags=("Nusselt number", "pipe flow", "turbulent", "Gnielinski", "gas", "smooth pipe"),
)
