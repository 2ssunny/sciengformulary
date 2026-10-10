"""Gnielinski Correlation for Pipe Flow.

Nu_D = (f/8) (Re_D - 1000) Pr / (1 + 12.7 sqrt(f/8) (Pr^(2/3) - 1)).
"""

import math

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

_RE_RANGE = (2300.0, 5.0e6)
_PR_RANGE = (0.6, 1.0e5)


def _evaluate(
    Re_D: float,  # noqa: N803 - symbols as written in the source
    Pr: float,  # noqa: N803
    f: float,
) -> float:
    if not _RE_RANGE[0] <= finite("Re_D", Re_D) <= _RE_RANGE[1]:
        raise ValueError(f"Re_D must lie in [{_RE_RANGE[0]:g}, {_RE_RANGE[1]:g}], got {Re_D!r}.")
    if not _PR_RANGE[0] <= finite("Pr", Pr) <= _PR_RANGE[1]:
        raise ValueError(f"Pr must lie in [{_PR_RANGE[0]}, {_PR_RANGE[1]:g}], got {Pr!r}.")
    positive("f", f)
    # Library implementations (for example the Python "ht" package) quote Pr 0.5 to 2000;
    # the textbook range is used here.
    half_f = f / 8.0
    denominator = 1.0 + 12.7 * math.sqrt(half_f) * (Pr ** (2.0 / 3.0) - 1.0)
    if denominator <= 0.0:
        # Reachable for Pr < 1 with a very large f (about f >= 0.6 at Pr = 0.6).
        raise ValueError(
            "1 + 12.7 sqrt(f/8) (Pr^(2/3) - 1) must be positive; the friction factor "
            f"f={f!r} is too large for Pr={Pr!r}."
        )
    return finite_result(half_f * (Re_D - 1000.0) * Pr / denominator)


gnielinski_nusselt = FormulaSpec(
    id="heat_transfer.gnielinski_nusselt",
    name="Gnielinski Correlation for Pipe Flow",
    equation="Nu_D = (f / 8) * (Re_D - 1000) * Pr / (1 + 12.7 * sqrt(f / 8) * (Pr^(2/3) - 1))",
    description=(
        "Diameter-based Nusselt number for fully developed transitional and turbulent flow in a "
        "round pipe, written in terms of the Darcy friction factor so that rough as well as "
        "smooth pipes can be treated. Unlike the Colburn power law, it covers the transition "
        "range and a very wide Prandtl range."
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
            description="Prandtl number, 0.6 to 1e5",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="f",
            symbol="f",
            description="Darcy-Weisbach friction factor of the pipe, positive",
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
        lienhard_heat_transfer("sec. 7.3, eq. (7.41), p. 369", accessed=ENGINEERING_ACCESSED),
        # The text evaluates properties at the bulk temperature and gives Example 7.3 with
        # Re_D = 4.12e5, Pr = 3.61 and f = 0.0136.
        lienhard_heat_transfer(
            "sec. 7.3, p. 371 and Example 7.3, p. 372", accessed=ENGINEERING_ACCESSED
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"Re_D": 412000.0, "Pr": 3.61, "f": 0.0136},
            expected=1476.2264696347459,
            rel_tol=1e-12,
            note=(
                "Inputs of the textbook's Example 7.3; value from 50-digit arithmetic (mpmath). "
                "The textbook's printed 1570 includes a later property-variation correction "
                "(a factor of about 1.06) that this formula does not apply."
            ),
        ),
        VerificationCase(
            inputs={"Re_D": 100000.0, "Pr": 1.2, "f": 0.0185},
            expected=254.62682749359632,
            rel_tol=1e-12,
            note="Evaluated with 50-digit arithmetic (mpmath).",
        ),
        VerificationCase(
            inputs={"Re_D": 2300.0, "Pr": 0.6, "f": 0.05},
            expected=6.864094528152871,
            rel_tol=1e-12,
            note="Lower edges of both ranges, Re_D = 2300 and Pr = 0.6; 50-digit arithmetic.",
        ),
    ),
    assumptions=(
        "Fully developed flow in a round pipe with either uniform wall temperature or uniform "
        "wall heat flux, for 2300 <= Re_D <= 5e6 and 0.6 <= Pr <= 1e5; the evaluator raises "
        "ValueError outside these ranges.",
        "All properties, including those in Re_D and Pr, are evaluated at the bulk temperature. "
        "Corrections for strongly varying properties are separate and are not included.",
        "f is the Darcy friction factor of the actual pipe (for a smooth pipe, for example from "
        "Filonenko's equation); it is an input and is not checked against Re_D.",
        "For Pr < 1 the denominator 1 + 12.7 sqrt(f/8) (Pr^(2/3) - 1) falls to zero and below "
        "when f is very large (f of about 0.6 at Pr = 0.6, far above any pipe friction factor); "
        "ValueError is raised whenever it is not positive.",
        "Dimensionless; valid in any consistent unit system.",
    ),
    tags=("Nusselt number", "pipe flow", "turbulent", "Gnielinski", "forced convection"),
)
