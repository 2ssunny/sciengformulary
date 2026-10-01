"""Lumped-Capacity Time Constant: tau = rho * c * V / (h * A)."""

from sciengformulary.catalog._sources import lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    rho: float,
    c: float,
    V: float,  # noqa: N803
    h: float,
    A: float,  # noqa: N803
) -> float:
    return rho * c * V / (h * A)


lumped_capacity_time_constant = FormulaSpec(
    id="heat_transfer.lumped_capacity_time_constant",
    name="Lumped-Capacity Time Constant",
    equation="tau = rho * c * V / (h * A)",
    description=(
        "Time constant of a body cooling or heating by convection when its internal temperature "
        "stays nearly uniform."
    ),
    inputs=(
        VariableSpec(
            name="rho",
            symbol=r"\rho",
            description="Density of the body",
            dimension="M L^-3",
            si_unit="kg/m^3",
        ),
        VariableSpec(
            name="c",
            symbol="c",
            description="Specific heat capacity of the body",
            dimension="L^2 T^-2 Theta^-1",
            si_unit="J/(kg*K)",
        ),
        VariableSpec(
            name="V",
            symbol="V",
            description="Body volume",
            dimension="L^3",
            si_unit="m^3",
        ),
        VariableSpec(
            name="h",
            symbol="h",
            description="Convective heat transfer coefficient",
            dimension="M T^-3 Theta^-1",
            si_unit="W/(m^2*K)",
        ),
        VariableSpec(
            name="A",
            symbol="A",
            description="Surface area exchanging heat",
            dimension="L^2",
            si_unit="m^2",
        ),
    ),
    output=VariableSpec(
        name="tau",
        symbol=r"\tau",
        description="Time constant (time to cover 63 % of the change)",
        dimension="T",
        si_unit="s",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes the time constant as T.
        lienhard_heat_transfer("sec. 1.3, eqs. (1.21)-(1.22)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"rho": 7800.0, "c": 500.0, "V": 1e-06, "h": 100.0, "A": 0.0006},
            expected=65.0,
            rel_tol=1e-12,
            note="Hand calculation: 7800 * 500 * 1e-6 / (100 * 6e-4) = 65 s.",
        ),
    ),
    assumptions=(
        "Biot number h L / k_body much less than 1 so the body temperature is nearly uniform; "
        "the cited text uses Bi < 0.1 for about 3 % uniformity in a cylinder example.",
        "Constant h, properties and fluid temperature; no heat generation or radiation.",
    ),
    tags=("lumped capacitance", "time constant", "transient", "thermocouple response"),
)
