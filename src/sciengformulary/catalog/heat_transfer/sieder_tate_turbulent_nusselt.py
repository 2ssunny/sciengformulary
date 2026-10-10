"""Sieder-Tate Correlation for Turbulent Pipe Flow.

Nu_D = 0.023 * Re_D^0.8 * Pr^(1/3) * (mu_b / mu_w)^0.14.
"""

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

_RE_MIN = 1.0e4
_PR_MIN = 0.67
_PR_MAX = 100.0


def _evaluate(
    Re_D: float,  # noqa: N803 - symbols as written in the source
    Pr: float,  # noqa: N803
    mu_b: float,
    mu_w: float,
) -> float:
    if finite("Re_D", Re_D) < _RE_MIN:
        raise ValueError(f"Re_D must be at least {_RE_MIN:g} for this correlation, got {Re_D!r}.")
    if not _PR_MIN <= finite("Pr", Pr) <= _PR_MAX:
        raise ValueError(f"Pr must lie in [{_PR_MIN}, {_PR_MAX:g}], got {Pr!r}.")
    positive("mu_b", mu_b)
    positive("mu_w", mu_w)
    # The textbook prints the coefficient 0.023, as used here. Some libraries (for example
    # the Python "ht" package) use 0.027 from the original 1936 paper and note the dispute.
    return finite_result(0.023 * Re_D**0.8 * Pr ** (1.0 / 3.0) * (mu_b / mu_w) ** 0.14)


sieder_tate_turbulent_nusselt = FormulaSpec(
    id="heat_transfer.sieder_tate_turbulent_nusselt",
    name="Sieder-Tate Correlation for Turbulent Pipe Flow",
    equation="Nu_D = 0.023 * Re_D^0.8 * Pr^(1/3) * (mu_b / mu_w)^0.14",
    description=(
        "Colburn-type diameter-based Nusselt number for turbulent flow of a liquid in a round "
        "pipe, with a viscosity-ratio factor for the case where the wall and bulk temperatures "
        "differ enough to change the viscosity. It reduces to the Colburn equation when the "
        "two viscosities are equal."
    ),
    inputs=(
        VariableSpec(
            name="Re_D",
            symbol="Re_D",
            description="Reynolds number based on the pipe diameter, bulk properties, >= 10^4",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="Pr",
            symbol="Pr",
            description="Prandtl number at the bulk temperature, from 0.67 to 100",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="mu_b",
            symbol=r"\mu_b",
            description="Dynamic viscosity at the bulk temperature, positive",
            dimension="M L^-1 T^-1",
            si_unit="Pa*s",
        ),
        VariableSpec(
            name="mu_w",
            symbol=r"\mu_w",
            description="Dynamic viscosity at the wall temperature, positive",
            dimension="M L^-1 T^-1",
            si_unit="Pa*s",
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
        lienhard_heat_transfer("sec. 7.3, eq. (7.40), pp. 368-369", accessed=ENGINEERING_ACCESSED),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"Re_D": 100000.0, "Pr": 5.0, "mu_b": 0.000554, "mu_w": 0.000316},
            expected=425.45439365112526,
            rel_tol=1e-12,
            note=(
                "Viscosities taken from the textbook's Example 7.3; value from 50-digit "
                "arithmetic (mpmath) of the printed equation."
            ),
        ),
        VerificationCase(
            inputs={"Re_D": 10000.0, "Pr": 0.67, "mu_b": 0.001, "mu_w": 0.001},
            expected=31.89721533251494,
            rel_tol=1e-12,
            note="Equal viscosities remove the correction, leaving the Colburn value; 50 digits.",
        ),
    ),
    assumptions=(
        "Liquids in fully developed turbulent flow in smooth pipes, Re_D >= 10^4 (the range of "
        "the Colburn equation it modifies).",
        "All properties, including those in Re_D and Pr, are evaluated at the local bulk "
        "temperature, except mu_w, the viscosity at the wall temperature.",
        "The source describes this as an early correlation with errors of up to +25 % and -40 % "
        "over 0.67 <= Pr <= 100 and prefers the Gnielinski equation with a property-variation "
        "correction; the evaluator raises ValueError outside that Prandtl range.",
        "Coefficient 0.023 as printed in the cited textbook. Dimensionless; the viscosity ratio "
        "is unit-free, so any consistent units work.",
    ),
    tags=("Nusselt number", "pipe flow", "turbulent", "Sieder-Tate", "variable properties"),
)
