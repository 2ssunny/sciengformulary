"""Drag Force: D = C_D * (rho * V^2 / 2) * S."""

from sciengformulary.catalog._sources import nasa_glenn
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    C_D: float,  # noqa: N803
    rho: float,
    V: float,  # noqa: N803
    S: float,  # noqa: N803
) -> float:
    return C_D * 0.5 * rho * V**2 * S


drag_force = FormulaSpec(
    id="aerodynamics.drag_force",
    name="Drag Force",
    equation="D = C_D * (rho * V^2 / 2) * S",
    description=(
        "Aerodynamic force parallel to the oncoming flow, written as a drag coefficient times "
        "dynamic pressure times a reference area."
    ),
    inputs=(
        VariableSpec(
            name="C_D",
            symbol="C_D",
            description="Drag coefficient, based on the same reference area S",
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
        name="D",
        symbol="D",
        description="Drag force",
        dimension="M L T^-2",
        si_unit="N",
    ),
    evaluator=_evaluate,
    references=(
        # The source names the reference area A.
        nasa_glenn("Drag Equation", "drag-equation", 2025),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"C_D": 0.03, "rho": 1.225, "V": 50.0, "S": 16.0},
            expected=735.0,
            rel_tol=1e-12,
            note="Hand calculation: 0.03 * (1.225 * 50^2 / 2) * 16 = 0.03 * 1531.25 * 16 = 735 N.",
        ),
    ),
    assumptions=(
        "C_D must be based on the same reference area S (wing area, frontal area or wetted "
        "area); coefficients based on different areas are not interchangeable.",
        "C_D lumps together form, skin-friction, wave and induced drag for the stated flow "
        "conditions; it is normally measured, not derived.",
        "rho and V are freestream values.",
    ),
    tags=("drag equation", "drag coefficient", "C_D", "aerodynamic force"),
)
