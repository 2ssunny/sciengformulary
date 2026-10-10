"""Peclet Number: Pe = u * L / alpha."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    u: float,
    L: float,  # noqa: N803
    alpha: float,
) -> float:
    non_negative("u", u)
    positive("L", L)
    positive("alpha", alpha)
    return finite_result(u * L / alpha)


peclet_number = FormulaSpec(
    id="heat_transfer.peclet_number",
    name="Peclet Number",
    equation="Pe = u * L / alpha",
    description=(
        "Ratio of heat carried along by the flow to heat conducted through the fluid; it equals "
        "the product of the Reynolds and Prandtl numbers."
    ),
    inputs=(
        VariableSpec(
            name="u",
            symbol="u",
            description="Flow speed",
            dimension="L T^-1",
            si_unit="m/s",
        ),
        VariableSpec(
            name="L",
            symbol="L",
            description="Characteristic length",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="alpha",
            symbol=r"\alpha",
            description="Thermal diffusivity of the fluid",
            dimension="L^2 T^-1",
            si_unit="m^2/s",
        ),
    ),
    output=VariableSpec(
        name="Pe",
        symbol="Pe",
        description="Peclet number",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes the plate form u_inf x / alpha and states it equals Re_x Pr.
        lienhard_heat_transfer("sec. 6.5, eq. (6.61), p. 307", accessed=ENGINEERING_ACCESSED),
        # The cylinder-in-crossflow section uses the same product with the diameter, Re_D Pr.
        lienhard_heat_transfer("sec. 7.6, p. 391", accessed=ENGINEERING_ACCESSED),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"u": 1.5, "L": 2.0, "alpha": 1e-07},
            expected=30000000.0,
            rel_tol=1e-12,
            note="Hand calculation: 1.5 * 2.0 / 1e-7 = 3e7; 50-digit mpmath agrees.",
        ),
        VerificationCase(
            inputs={"u": 0.0, "L": 2.0, "alpha": 1e-07},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Fluid at rest: no convective transport, so the group is zero.",
        ),
    ),
    assumptions=(
        "The length and velocity scales must be those of the correlation in use (plate "
        "distance x, diameter D, ...).",
        "u must be finite and not negative (it is a speed); L and alpha must be finite and "
        "positive; otherwise ValueError is raised.",
        "Equals Re * Pr when Re and Pr use the same u and L.",
        "Dimensionally homogeneous: any consistent units.",
    ),
    tags=("Peclet number", "dimensionless group", "convection", "thermal diffusivity"),
)
