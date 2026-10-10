"""Eckert Number: Ec = u_inf^2 / (c_p * (T_w - T_inf))."""

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    u_inf: float,
    c_p: float,
    T_w: float,  # noqa: N803
    T_inf: float,  # noqa: N803
) -> float:
    finite("u_inf", u_inf)
    positive("c_p", c_p)
    finite("T_w", T_w)
    finite("T_inf", T_inf)
    delta_t = T_w - T_inf
    if delta_t == 0:
        raise ValueError("T_w and T_inf must differ: the Eckert number divides by T_w - T_inf.")
    return finite_result(u_inf * u_inf / (c_p * delta_t))


eckert_number = FormulaSpec(
    id="heat_transfer.eckert_number",
    name="Eckert Number",
    equation="Ec = u_inf^2 / (c_p * (T_w - T_inf))",
    description=(
        "Ratio of the flow's kinetic energy to the enthalpy difference that drives the heat "
        "transfer; small values mean viscous heating of the fluid can be neglected."
    ),
    inputs=(
        VariableSpec(
            name="u_inf",
            symbol=r"u_\infty",
            description="Free-stream speed",
            dimension="L T^-1",
            si_unit="m/s",
        ),
        VariableSpec(
            name="c_p",
            symbol="c_p",
            description="Specific heat at constant pressure",
            dimension="L^2 T^-2 Theta^-1",
            si_unit="J/(kg*K)",
        ),
        VariableSpec(
            name="T_w",
            symbol="T_w",
            description="Wall temperature",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="T_inf",
            symbol=r"T_\infty",
            description="Free-stream temperature",
            dimension="Theta",
            si_unit="K",
        ),
    ),
    output=VariableSpec(
        name="Ec",
        symbol="Ec",
        description="Eckert number (takes the sign of T_w - T_inf)",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        lienhard_heat_transfer(
            "sec. 6.5, p. 310 (list of conditions for the laminar flat-plate results)",
            accessed=ENGINEERING_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"u_inf": 10.0, "c_p": 2000.0, "T_w": 325.0, "T_inf": 300.0},
            expected=0.002,
            rel_tol=1e-12,
            note="Hand calculation: 10^2 / (2000 * 25) = 0.002; 50-digit mpmath agrees.",
        ),
        VerificationCase(
            inputs={"u_inf": 15.0, "c_p": 1007.0, "T_w": 200.0, "T_inf": 290.0},
            expected=-0.0024826216484607746,
            rel_tol=1e-12,
            note="Cooled wall gives a negative value; 50-digit mpmath: 225 / (1007 * -90).",
        ),
    ),
    assumptions=(
        "The temperature difference is signed, T_w - T_inf, exactly as the source writes it, so "
        "a cooled wall gives a negative Eckert number.",
        "c_p must be positive and T_w must differ from T_inf; otherwise ValueError is raised.",
        "Viscous heating is negligible when the Eckert number is much smaller than one.",
        "Dimensionally homogeneous: any consistent units (J/kg equals m^2/s^2); only the "
        "temperature difference enters, so Celsius and kelvin give the same value.",
    ),
    tags=("Eckert number", "dimensionless group", "viscous dissipation", "convection"),
)
