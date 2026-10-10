"""Grashof Number: Gr_L = g * beta * |T_w - T_inf| * L^3 / nu^2."""

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    g: float,
    beta: float,
    T_w: float,  # noqa: N803
    T_inf: float,  # noqa: N803
    L: float,  # noqa: N803
    nu: float,
) -> float:
    positive("g", g)
    positive("beta", beta)
    finite("T_w", T_w)
    finite("T_inf", T_inf)
    positive("L", L)
    positive("nu", nu)
    # L^3 / nu^2 is grouped as L * (L / nu)^2 so that a very small nu does not underflow nu^2.
    return finite_result(g * beta * abs(T_w - T_inf) * L * (L / nu) ** 2)


grashof_number = FormulaSpec(
    id="heat_transfer.grashof_number",
    name="Grashof Number",
    equation="Gr_L = g * beta * |T_w - T_inf| * L^3 / nu^2",
    description=(
        "Ratio of buoyancy to viscous forces that governs natural convection from a surface."
    ),
    inputs=(
        VariableSpec(
            name="g",
            symbol="g",
            description="Gravitational acceleration",
            dimension="L T^-2",
            si_unit="m/s^2",
        ),
        VariableSpec(
            name="beta",
            symbol=r"\beta",
            description="Volumetric thermal expansion coefficient of the fluid",
            dimension="Theta^-1",
            si_unit="1/K",
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
            description="Ambient fluid temperature",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="L",
            symbol="L",
            description="Characteristic length",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="nu",
            symbol=r"\nu",
            description="Kinematic viscosity of the fluid",
            dimension="L^2 T^-1",
            si_unit="m^2/s",
        ),
    ),
    output=VariableSpec(
        name="Gr_L",
        symbol="Gr_L",
        description="Grashof number based on the length L",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The source defines the temperature difference as |T_w - T_inf|.
        lienhard_heat_transfer("sec. 8.3, eq. (8.9), p. 418", accessed=ENGINEERING_ACCESSED),
    ),
    verification_cases=(
        VerificationCase(
            inputs={
                "g": 9.80665,
                "beta": 0.000933,
                "T_w": 378.2,
                "T_inf": 200.0,
                "L": 0.9144,
                "nu": 1.636e-05,
            },
            expected=4657491516.530312,
            rel_tol=1e-12,
            note="50-digit mpmath evaluation of the equation.",
        ),
        VerificationCase(
            inputs={
                "g": 9.80665,
                "beta": 0.0033333333333333335,
                "T_w": 280.0,
                "T_inf": 300.0,
                "L": 0.1,
                "nu": 1.5e-05,
            },
            expected=2905674.074074074,
            rel_tol=1e-12,
            note="Cooled wall, so the absolute temperature difference of 20 K applies; mpmath.",
        ),
        VerificationCase(
            inputs={
                "g": 9.80665,
                "beta": 0.0033333333333333335,
                "T_w": 300.0,
                "T_inf": 300.0,
                "L": 0.1,
                "nu": 1.5e-05,
            },
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="No temperature difference gives no buoyancy: the product is zero.",
        ),
    ),
    assumptions=(
        "The temperature difference is taken as an absolute value, as the source defines it, so "
        "the sign of T_w - T_inf does not matter.",
        "g, beta, L and nu must be finite and positive; otherwise ValueError is raised. A "
        "result outside the float range raises OverflowError.",
        "beta and nu are evaluated at the fluid temperature the chosen correlation calls for; "
        "this evaluator does not choose it.",
        "Dimensionally homogeneous: any consistent units; only the temperature difference "
        "enters, and beta must be the inverse of the same temperature unit.",
    ),
    tags=("Grashof number", "dimensionless group", "natural convection", "buoyancy"),
)
