"""Lift Force: L = C_L * (rho * V^2 / 2) * S."""

from sciengformulary.catalog._sources import nasa_glenn
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    C_L: float,  # noqa: N803
    rho: float,
    V: float,  # noqa: N803
    S: float,  # noqa: N803
) -> float:
    return C_L * 0.5 * rho * V**2 * S


lift_force = FormulaSpec(
    id="aerodynamics.lift_force",
    name="Lift Force",
    equation="L = C_L * (rho * V^2 / 2) * S",
    description=(
        "Aerodynamic force perpendicular to the oncoming flow, written as a lift coefficient times "
        "dynamic pressure times a reference area. The coefficient carries all the dependence on "
        "shape, attitude, viscosity and compressibility."
    ),
    inputs=(
        VariableSpec(
            name="C_L",
            symbol="C_L",
            description="Lift coefficient, based on the same reference area S",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="rho",
            symbol=r"\rho",
            description="Freestream air density",
            dimension="M L^-3",
            si_unit="kg/m^3",
        ),
        VariableSpec(
            name="V",
            symbol="V",
            description="Freestream speed relative to the body",
            dimension="L T^-1",
            si_unit="m/s",
        ),
        VariableSpec(
            name="S",
            symbol="S",
            description="Reference area the coefficient is based on (usually wing planform area)",
            dimension="L^2",
            si_unit="m^2",
        ),
    ),
    output=VariableSpec(
        name="L",
        symbol="L",
        description="Lift force",
        dimension="M L T^-2",
        si_unit="N",
    ),
    evaluator=_evaluate,
    references=(
        # The source names the area A; it is the wing area used to define C_L.
        nasa_glenn("Lift Equation", "lift-equation", 2024),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"C_L": 0.5, "rho": 1.225, "V": 50.0, "S": 16.0},
            expected=12250.0,
            rel_tol=1e-12,
            note="Hand calculation: 0.5 * (1.225 * 50^2 / 2) * 16 = 0.5 * 1531.25 * 16 = 12250 N.",
        ),
    ),
    assumptions=(
        "C_L must be known for the actual geometry, attitude, Reynolds number and Mach number, "
        "and must be based on the same reference area S used here.",
        "rho and V are freestream values.",
        "This is a definition of how lift scales, not a prediction of C_L; it gives no "
        "information about stall or separation.",
    ),
    tags=("lift equation", "lift coefficient", "C_L", "wing", "aerodynamic force"),
)
